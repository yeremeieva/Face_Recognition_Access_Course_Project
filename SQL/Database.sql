DROP DATABASE IF EXISTS AccessControlSystem;
CREATE DATABASE AccessControlSystem;


CREATE TYPE GenderType AS ENUM ('Male', 'Female');
CREATE TYPE PositionType AS ENUM ('Admin', 'Worker');
CREATE TYPE DoorDirection AS ENUM ('In', 'Out');

CREATE TABLE Person
(
    PersonID    integer         PRIMARY KEY,
    Name        varchar(50)     NOT NULL,
    Surname     varchar(50)     NOT NULL,
    Gender      GenderType      NOT NULL,
    Age         integer         NOT NULL CHECK (Age >= 0),
    PhoneNumber varchar(20)     NOT NULL,
    Position    PositionType    NOT NULL,
    FeatureVector bytea         NOT NULL,
    ImageData   bytea           NOT NULL
);


CREATE TABLE Door
(
    DoorID      integer         NOT NULL,
    AccessType  PositionType    NOT NULL,
    Direction   DoorDirection   NOT NULL,
    Location    varchar(50)     NOT NULL,
    PRIMARY KEY (DoorID, Direction)
);

CREATE TABLE Record
(
    RecordID    integer         PRIMARY KEY,
    RecordTime  TIMESTAMP WITH TIME ZONE DEFAULT ('now'::text)::timestamp with time zone,
    Access      boolean         NOT NULL,
    DoorID      integer         NOT NULL,
    Direction   DoorDirection   NOT NULL,
    PersonID    integer         NULL references Person (PersonID),
	FOREIGN KEY (DoorID, Direction) REFERENCES Door (DoorID, Direction)
);

CREATE INDEX PersonID ON Person (PersonID);


CREATE VIEW DoorRecordView AS
SELECT *
FROM Record NATURAL JOIN Door;



INSERT INTO Person (PersonID, Name, Surname, Gender, Age, PhoneNumber, Position, FeatureVector, ImageData)
VALUES
(1, 'John', 'Doe', 'Male', 30, '123-456-7890', 'Worker', ' ', ' '),
(2, 'Jane', 'Smith', 'Female', 25, '234-567-8901', 'Worker', ' ', ' '),
(3, 'Alice', 'Johnson', 'Female', 28, '345-678-9012', 'Worker', ' ', ' ');


INSERT INTO Door (DoorID, AccessType, Direction, Location)
VALUES
(1, 'Worker', 'In', 'Main Entrance'),
(1, 'Worker', 'Out', 'Main Entrance'),
(2, 'Worker', 'In', 'Office Entry'),
(2, 'Worker', 'Out', 'Office Entry');


INSERT INTO Record (RecordID, RecordTime, Access, DoorID, Direction, PersonID)
VALUES
(1, '2024-04-21 08:00:00+00', TRUE, 1, 'In', 1),
(2, '2024-04-21 12:00:00+00', TRUE, 1, 'Out', 1),
(3, '2024-04-21 09:00:00+00', FALSE, 2, 'In', 2),
(4, '2024-04-21 17:00:00+00', TRUE, 2, 'Out', 3);
