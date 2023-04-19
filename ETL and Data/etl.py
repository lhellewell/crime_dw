import pandas as pd
from datetime import datetime

# Driver function
def main():
	FILENAME = '.\crime.csv'
	df = extract(FILENAME)
	dim_tables, fact_table = transform(df)
	load(dim_tables, fact_table)

if __name__ == "__main__":
    main()


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

def Datekey_helper(x):
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

# Initial extraction of csv dataset using filename into a dataframe
def extract(file):
	# Reading csv
	df = pd.read_csv(file, nrows=225000, parse_dates=['date'])

	# Drops all duplicate crime numbers
	df = df.drop_duplicates(subset=['number'])

	# Merging two neighbourhood columns, lookup takes priority as it is more accurate
	df['neighborhood'] = df['neighbourhood_lookup'].combine_first(df['neighborhood'])

	# Drop redundant column
	df = df.drop('neighbourhood_lookup', axis=1)
	df = df.drop('Unnamed: 0', axis=1)

	# Drop Redundant Rows
	df = df.dropna()

	# Removing any outliers
	df = df.drop(df.index[df['city'] != 'Atlanta'])
	return df

# Transformation stage
def transform(df):
	# Setting the types of each column
	df = df.astype({'crime': str, 'number': 'int64', 'date': 'str',\
	'location': str, 'beat': str, 'neighborhood': str, 'npu': str, 'lat': str, \
	'long': str, 'type': str, 'road': str, 'city': str, 'county': str, 'state': str, 'postcode': str, 'country': str})

	# rename columns to dimension names
	df = df.rename(columns={'type': 'LocationType', 'postcode': 'ZipCode', 'beat': 'PatrolBeat', 'crime': 'CrimeType', \
		'number': 'CrimeNumber', 'npu': 'NPU'})

	# Capitalise columns
	rename_object = {}
	for i in df.columns:
		rename_object[str(i)] = str(i)[0].upper() + str(i)[1:]
	df = df.rename(columns=rename_object)

	# Remove the .0 at the end of zip code col after str conversion
	df['ZipCode'] = df['ZipCode'].apply(zip_helper)

	# Create a dictionary of dataframes for each dimension table
	dim_tables = {}
	dim_tables['DimCrimeType'] = df[['CrimeType']].drop_duplicates()
	dim_tables['DimLocation'] = df[['Lat', 'Long', 'Location', 'LocationType', 'Road', 'Neighborhood', 'ZipCode', 'NPU', 'PatrolBeat', 'City', 'County', 'State', 'Country']].drop_duplicates()
	dim_tables['DimDate'] = df[['Date']].drop_duplicates()
	dim_tables['DimPatrolBeat'] = df[['PatrolBeat']].drop_duplicates()
	dim_tables['DimCity'] = df[['City', 'County', 'State', 'Country']].drop_duplicates()

	# Adding fields for the Date dimension table
	dim_tables['DimDate']['DayOfWeek'] = dim_tables['DimDate']['Date'].apply(dayofweek_helper)
	dim_tables['DimDate']['Month'] = dim_tables['DimDate']['Date'].apply(month_helper)
	dim_tables['DimDate']['Quarter'] = dim_tables['DimDate']['Date'].apply(quarter_helper)
	dim_tables['DimDate']['Year'] = dim_tables['DimDate']['Date'].apply(year_helper)

	# Adding fields for the PatrolBeat dimension table
	dim_tables['DimPatrolBeat']['PoliceZone'] = dim_tables['DimPatrolBeat']['PatrolBeat'].apply(zone_helper)


	# Adding fields for the crime type dimension table
	dim_tables['DimCrimeType']['IndexCrimeType'] = dim_tables['DimCrimeType']['CrimeType'].apply(indextype_helper)
	dim_tables['DimCrimeType']['IndexCrimeCategory'] = dim_tables['DimCrimeType']['CrimeType'].apply(indexcategory_helper)

	# Create the keys for each dimension table to be referenced as foreign keys
	dim_tables['DimDate'].insert(0, 'DateKey', dim_tables['DimDate']['Date'].apply(Datekey_helper))
	dim_tables['DimLocation'].insert(0, 'LocationKey', range(len(dim_tables['DimLocation'])))
	dim_tables['DimCrimeType'].insert(0, 'CrimeTypeKey', range(len(dim_tables['DimCrimeType'])))
	dim_tables['DimPatrolBeat'].insert(0, 'PatrolBeatKey', range(len(dim_tables['DimPatrolBeat'])))
	dim_tables['DimCity'].insert(0, 'CityKey', range(len(dim_tables['DimCity'])))

	# Linking the relationships between each table
	dim_tables['DimLocation'] = pd.merge(dim_tables['DimLocation'], dim_tables['DimPatrolBeat'], on=['PatrolBeat'])
	dim_tables['DimLocation'] = pd.merge(dim_tables['DimLocation'], dim_tables['DimCity'], on=['City', 'County', 'State', 'Country'])
	fact_table = pd.merge(df, dim_tables['DimDate'], on='Date')
	fact_table = pd.merge(fact_table, dim_tables['DimCrimeType'], on='CrimeType')
	fact_table = pd.merge(fact_table, dim_tables['DimLocation'], on=['Lat', 'Long', 'Location'])

	# Sort the crimes by Date 
	fact_table = fact_table.sort_values(by='Date')

	# Dropping dimensions that were products of merges
	fact_table = fact_table[['CrimeNumber', 'DateKey', 'CrimeTypeKey', 'LocationKey']]
	dim_tables['DimLocation'] = dim_tables['DimLocation'].drop(['PatrolBeat', 'PoliceZone', 'City', 'County', 'State', 'Country'], axis=1)
	return dim_tables, fact_table

def load(dim_tables, fact_table):
	# Write each dimension table to a separate CSV file
	for name, table in dim_tables.items():
		table.to_csv(f'{name}.csv', index=False)

	# Write the fact table to a CSV file
	fact_table.to_csv('FactCrimes.csv', index=False)

