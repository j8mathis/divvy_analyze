#!/bin/bash

git_repo="/Users/jason/git/divvy_analyze"
psql="/usr/local/opt/libpq/bin/psql"
unzip="/usr/bin/unzip"

zip_file=$git_repo/data/Divvy_Trips_2016_Q3Q4.zip
unzip_loc=$git_repo/postgres

echo "git repo = $git_repo"

clean_up () {
  rm -rf $unzip_loc/Divvy_Trips_*.csv
}

$psql -h localhost -U postgres -c "drop database if exists divvy_analyze;"

clean_up

$psql -h localhost -U postgres -c "create database divvy_analyze;"

cat $git_repo/postgres/ddl/tables.sql | $psql -h localhost -U postgres -d divvy_analyze

echo "unzipping files" 
$unzip -j $zip_file Divvy_Trips*/Divvy_Trips_*.csv -d $unzip_loc

echo "loading data into stage table..."
for i in $( ls $unzip_loc/Divvy_Trips_*.csv); do
  echo "\copy stage_trip_data from '$i' with (format CSV, header, force_null(birthyear));" | $psql -h localhost -U postgres -d divvy_analyze
done

echo "removing duplicate rows and load into main table..."
$psql -h localhost -U postgres -d divvy_analyze -c "insert into trip_data select * from stage_trip_data group by 1,2,3,4,5,6,7,8,9,10,11,12;"

echo "cleaning up" 
clean_up
