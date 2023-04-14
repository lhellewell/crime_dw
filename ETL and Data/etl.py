import pandas as pd
from datetime import datetime

FILENAME = '.\crime.csv'

# Helper functions

def zone_helper(x):
	if str(x)[0] == '7':
		return 'Airport'
	elif len(str(x)) == 3:
		return str(x)[0]
	else:
		return None

def zip_helper(x):
	if len(x) >= 2 and x[-2:] == '.0':
		return x[:-2]
	else: 
		return x

def dayofweek_helper(x):
	return datetime.strptime(x, '%Y-%m-%d').strftime('%A')

def month_helper(x):
	return datetime.strptime(x, '%Y-%m-%d').strftime('%B')

def quarter_helper(x):
	return (datetime.strptime(x, '%Y-%m-%d').month -1) // 3 + 1

def year_helper(x):
	return datetime.strptime(x, '%Y-%m-%d').year

def datekey_helper(x):
	return x.replace('-', '')

def indextype_helper(x):
	if x.startswith('ROBBERY'):
		return 'ROBBERY'
	elif x.startswith('BURGLARY'):
		return 'BURGLARY'
	elif x.startswith('LARCENY'):
		return 'LARCENY'
	return x

def indexcategory_helper(x):
	if x.startswith('BURGLARY') or x.startswith('LARCENY') or x == 'AUTO THEFT':
		return 'PROPERTY'
	return 'VIOLENT'


df = pd.read_csv(FILENAME, nrows=225000, parse_dates=['date'])

# Drops all duplicate crime numbers
df = df.drop_duplicates(subset=['number'])

# Add the appropriate dimensions missing from the dataset
df['zone'] = df['beat'].apply(zone_helper)

# Merging two neighbourhood columns, lookup takes priority as it is more accurate
df['neighborhood'] = df['neighbourhood_lookup'].combine_first(df['neighborhood'])

# Drop redundant column
df = df.drop('neighbourhood_lookup', axis=1)
df = df.drop('Unnamed: 0', axis=1)

# Drop Redundant Rows
df = df.dropna()

# Setting the types of each column
df = df.astype({'crime': str, 'number': int, 'date': 'str',\
'location': str, 'beat': str, 'zone': str, 'neighborhood': str, 'npu': str, 'lat': str, \
'long': str, 'type': str, 'road': str, 'city': str, 'county': str, 'state': str, 'postcode': str, 'country': str})

# rename columns to dimension names
df = df.rename(columns={'type': 'locationtype', 'postcode': 'zipcode', 'zone': 'policezone', 'beat': 'patrolbeat', 'crime': 'crimetype'})

# Remove the .0 at the end of zip code col after str conversion
df['zipcode'] = df['zipcode'].apply(zip_helper)

# Set the display option to show all columns
#pd.set_option('display.max_columns', None)

# Create a dictionary of dataframes for each dimension table
dim_tables = {}
dim_tables['DimCrimeType'] = df[['crimetype']].drop_duplicates()
dim_tables['DimLocation'] = df[['lat', 'long', 'location', 'locationtype', 'road', 'neighborhood', 'zipcode', 'npu', 'patrolbeat', 'policezone', 'city', 'county', 'state', 'country']].drop_duplicates()
dim_tables['DimDate'] = df[['date']].drop_duplicates()
dim_tables['DimPatrolBeat'] = df[['patrolbeat', 'policezone']].drop_duplicates()
dim_tables['DimCity'] = df[['city', 'county', 'state', 'country']].drop_duplicates()



# Adding dimensions for the date dimension table
dim_tables['DimDate']['DayOfWeek'] = dim_tables['DimDate']['date'].apply(dayofweek_helper)
dim_tables['DimDate']['Month'] = dim_tables['DimDate']['date'].apply(month_helper)
dim_tables['DimDate']['Quarter'] = dim_tables['DimDate']['date'].apply(quarter_helper)
dim_tables['DimDate']['Year'] = dim_tables['DimDate']['date'].apply(year_helper)

# Adding dimensions for the crime type dimension table
dim_tables['DimCrimeType']['IndexCrimeType'] = dim_tables['DimCrimeType']['crimetype'].apply(indextype_helper)
dim_tables['DimCrimeType']['IndexCrimeCategory'] = dim_tables['DimCrimeType']['crimetype'].apply(indexcategory_helper)


# Create the keys for each dimension table to be referenced as foreign keys
dim_tables['DimDate']['DateKey'] = dim_tables['DimDate']['date'].apply(datekey_helper)
dim_tables['DimLocation']['LocationKey'] = range(len(dim_tables['DimLocation']))
dim_tables['DimCrimeType']['CrimeTypeKey'] = range(len(dim_tables['DimCrimeType']))
dim_tables['DimPatrolBeat']['PatrolBeatKey'] = range(len(dim_tables['DimPatrolBeat']))
dim_tables['DimCity']['CityKey'] = range(len(dim_tables['DimCity']))

# Write each dimension table to a separate CSV file
for name, table in dim_tables.items():
    table.to_csv(f'{name}.csv', index=False)

# Linking the relationships between each table
dim_tables['DimLocation'] = pd.merge(dim_tables['DimLocation'], dim_tables['DimPatrolBeat'], on=['patrolbeat', 'policezone'])
dim_tables['DimLocation'] = pd.merge(dim_tables['DimLocation'], dim_tables['DimCity'], on=['city', 'county', 'state', 'country'])
fact_table = pd.merge(df, dim_tables['DimDate'], on='date')
fact_table = pd.merge(fact_table, dim_tables['DimCrimeType'], on='crimetype')
fact_table = pd.merge(fact_table, dim_tables['DimLocation'], on=['lat', 'long', 'location', 'locationtype', 'road', 'neighborhood', 'zipcode', 'patrolbeat', 'npu', 'policezone', 'city', 'county', 'state', 'country'])

# Sort the crimes by date 
fact_table = fact_table.sort_values(by='date')

# Dropping dimensions that were products of merges
fact_table = fact_table[['number', 'DateKey', 'CrimeTypeKey', 'LocationKey']]
dim_tables['DimLocation'] = dim_tables['DimLocation'].drop(['patrolbeat', 'policezone', 'city', 'county', 'state', 'country'], axis=1)

# Write the fact table to a CSV file
fact_table.to_csv('FactCrimes.csv', index=False)

print(dim_tables['DimCrimeType'].columns)
print(dim_tables['DimDate'].columns)
print(dim_tables['DimLocation'].columns)
print(dim_tables['DimPatrolBeat'].columns)
print(dim_tables['DimCity'].columns)
print(fact_table.columns)

