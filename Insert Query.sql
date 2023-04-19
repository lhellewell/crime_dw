BULK INSERT [dbo].[FactCrimes] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\FactCrimes.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);

BULK INSERT [dbo].[DimLocation] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\DimLocation.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);

BULK INSERT [dbo].[DimCrimeType] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\DimCrimeType.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);


BULK INSERT [dbo].[DimDate] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\DimDate.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);

BULK INSERT [dbo].[DimDate] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\DimCity.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);

BULK INSERT [dbo].[DimPatrolBeat] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\DimPatrolBeat.csv'
WITH (
    CHECK_CONSTRAINTS,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);