USE master;
GO

Use Crime
Go

PRINT '';
PRINT '*** Dropping Association Tables if they already exist';
GO

IF OBJECT_ID('CaseTable', 'U') IS NOT NULL
DROP TABLE CaseTable;

IF OBJECT_ID('NestedTable', 'U') IS NOT NULL
DROP TABLE NestedTable;
GO

PRINT '';
PRINT '*** Creating Table CaseTable';
GO

Create table CaseTable
(
CaseKey int primary key,
Date varchar(20) not null,
Neighborhood varchar(50) not null,
)
Go

PRINT '';
PRINT '*** Creating Table NestedTable';
GO

Create table NestedTable
(
CaseKey int,
CrimeType varchar(50) not null,
)
Go

PRINT '';
PRINT '*** Inserting CaseTable.csv';
GO

BULK INSERT [dbo].[CaseTable] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\CaseTable.csv'
WITH (
	FIRSTROW=2,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);

PRINT '';
PRINT '*** Inserting NestedTable.csv';
GO

BULK INSERT [dbo].[NestedTable] FROM 'D:\UNI2023\Data Warehousing\Project 1\ETL and Data\NestedTable.csv'
WITH (
	FIRSTROW=2,
    DATAFILETYPE='char',
    FIELDTERMINATOR=',',
    ROWTERMINATOR='\n',
    --KEEPIDENTITY,
    TABLOCK
);