USE master;
GO


PRINT '';
PRINT '*** Dropping Database';
GO

IF EXISTS (SELECT [name] FROM [master].[sys].[databases] WHERE [name] = N'Crime')
DROP DATABASE Crime;
GO

PRINT '';
PRINT '*** Creating Database Crimes';
GO

Create database Crime
Go

Use Crime
Go

PRINT '';
PRINT '*** Creating Table DimDate';
GO

Create table DimDate
(
DateKey int primary key,
Date varchar(20) not null,
DayOfWeek varchar(50) not null,
Month varchar(20) not null,
Quarter int not null,
Year int not null
)
Go

PRINT '';
PRINT '*** Creating Table DimCrimeType';
GO

Create table DimCrimeType
(
CrimeTypeKey int primary key,
CrimeType varchar(50) not null,
IndexCrimeType varchar(50) not null,
IndexCrimeCategory varchar(20) not null,
)
Go

PRINT '';
PRINT '*** Creating Table DimLocation';
GO

Create table DimLocation
(
LocationKey int primary key,
Lat varchar(20) not null,
Long varchar(20) not null,
Location varchar(MAX) not null,
LocationType varchar(20) not null,
Road varchar(50) not null,
Neighborhood varchar(50) not null,
ZipCode varchar(50) not null,
NPU varchar(5) not null,
PatrolBeatKey int not null,
CityKey int not null,
)
Go

PRINT '';
PRINT '*** Creating Table DimPatrolBeat';
GO

Create table DimPatrolBeat
(
PatrolBeatKey int primary key,
PatrolBeat int not null,
PoliceZone varchar(20) not null,
)
Go

PRINT '';
PRINT '*** Creating Table DimCity';
GO

Create table DimCity
(
CityKey int primary key,
City varchar(50) not null,
County varchar(50) not null,
State varchar(50) not null,
Country varchar(50) not null,
)
Go

PRINT '';
PRINT '*** Creating Table FactCrimes';
GO

Create Table FactCrimes
(
CrimeNumber bigint primary key identity,
DateKey int not null,
CrimeTypeKey int not null,
LocationKey int not null,
)
Go

PRINT '';
PRINT '*** Add relation between fact table foreign keys to Primary keys of Dimensions';
GO

AlTER TABLE FactCrimes ADD CONSTRAINT 
FK_DateKey FOREIGN KEY (DateKey)REFERENCES DimDate(DateKey);
AlTER TABLE FactCrimes ADD CONSTRAINT 
FK_LocationKey FOREIGN KEY (LocationKey)REFERENCES DimLocation(LocationKey);
AlTER TABLE FactCrimes ADD CONSTRAINT 
FK_CrimeTypeKey FOREIGN KEY (CrimeTypeKey)REFERENCES DimCrimeType(CrimeTypeKey);
AlTER TABLE DimLocation ADD CONSTRAINT 
FK_PatrolBeatKey FOREIGN KEY (PatrolBeatKey)REFERENCES DimPatrolBeat(PatrolBeatKey);
AlTER TABLE DimLocation ADD CONSTRAINT 
FK_CityKey FOREIGN KEY (CityKey)REFERENCES DimCity(CityKey);
Go
