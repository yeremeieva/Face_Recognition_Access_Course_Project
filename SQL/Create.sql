DROP DATABASE IF EXISTS AccessControlSystem;
CREATE DATABASE AccessControlSystem;

\c accesscontrolsystem

CREATE TYPE GenderType AS ENUM ('Male', 'Female');
CREATE TYPE PositionType AS ENUM ('Admin', 'Worker');
CREATE TYPE DoorDirection AS ENUM ('In', 'Out');

CREATE TABLE Person
(
    PersonID    integer         PRIMARY KEY,
    Name        varchar(50)     NOT NULL,
    Gender      GenderType      NOT NULL,
    Age         integer         NOT NULL CHECK (Age >= 0),
    PhoneNumber varchar(20)     NOT NULL,
    Position    PositionType    NOT NULL,
    FeatureVector bytea         NOT NULL,
    ImageData   bytea           NOT NULL
);


CREATE TABLE Door
(
    DoorID      integer         PRIMARY KEY,
    Location    varchar(50)     NOT NULL
);

CREATE TABLE Record
(
    RecordID    integer         PRIMARY KEY,
    RecordTime  TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::timestamp with time zone,
    Access      boolean         NOT NULL,
    ImageData   bytea           NOT NULL,
    DoorID      integer         NOT NULL references Door (DoorID),
    PersonID    integer         NULL references Person (PersonID),
    Direction   DoorDirection   NOT NULL
);


CREATE INDEX PersonID ON Person (PersonID);


CREATE VIEW DoorRecordView AS
SELECT *
FROM Record NATURAL JOIN Door;
