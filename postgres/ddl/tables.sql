create table if not exists trip_data(
trip_id int primary key not null,
starttime timestamp,
stoptime timestamp,
bikeid int,
tripduration int,
from_station_id int,
from_station_name text,
to_station_id int,
to_station_name text,
usertype text,
gender text,
birthyear int
);

create table if not exists stage_trip_data(
trip_id int,
starttime timestamp,
stoptime timestamp,
bikeid int,
tripduration int,
from_station_id int,
from_station_name text,
to_station_id int,
to_station_name text,
usertype text,
gender text,
birthyear int
);

create table if not exists station_data(
station_id int primary key not null,
latitude float,
longitude float,
status text,
station_name text,
available_docks int,
total_docks int,
available_bikes int,
load_datetime timestamptz
);