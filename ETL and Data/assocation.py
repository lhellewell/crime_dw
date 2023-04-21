import pandas as pd


# Reading CSV's
df = pd.read_csv("./FactCrimes.csv")
DimDate = pd.read_csv("./DimDate.csv")
DimLocation = pd.read_csv("./DimLocation.csv")
DimCrimeType = pd.read_csv("./DimCrimeType.csv")
df = pd.merge(df, DimDate, on="DateKey")
df = pd.merge(df, DimLocation, on="LocationKey")
df = pd.merge(df, DimCrimeType, on="CrimeTypeKey")

# Drop unnecessary columns
df = df[['Neighborhood', 'Date', 'CrimeType']]

df = df.sort_values(by=['Date', 'Neighborhood'])

# Creation of case key essentially "transaction id"
case_key = df[['Neighborhood', 'Date']].drop_duplicates()
case_key.insert(0, 'CaseKey', range(len(case_key)))

# Merging to main df gain case key
df = pd.merge(df, case_key, on=['Neighborhood', 'Date'])

# Re-order columns
df = df[['CaseKey', 'Date', 'Neighborhood', 'CrimeType']]

# Creating the tables
nested_table = df[['CaseKey', 'CrimeType']].drop_duplicates()
case_table = df[['CaseKey', 'Date', 'Neighborhood']].drop_duplicates()

#print(nested_table)
#print(case_table)

# Write the views to a CSV file
case_table.to_csv('CaseTable.csv', index=False)
nested_table.to_csv('NestedTable.csv', index=False)