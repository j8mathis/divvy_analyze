import requests
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from zipfile import ZipFile
import re
from trip_data_type import Trip
import csv
import io


def get_live_data(url):
    resp = requests.get(url)
    resp.raise_for_status()

    live_data_raw = resp.json()
    live_data_list = live_data_raw.get('stationBeanList')

    station_data = []
    for station in live_data_list:
        station_dict = {}
        station_dict['station_id'] = station.get('id')
        # dynamodb throw some weird error about floats, hence the casting below
        station_dict['latitude'] = Decimal(str(station.get('latitude')))
        station_dict['longitude'] = Decimal(str(station.get('longitude')))
        station_dict['status'] = station.get('status')
        station_dict['stationName'] = station.get('stationName')
        station_dict['availableDocks'] = station.get('availableDocks', 0)
        station_dict['totalDocks'] = station.get('totalDocks', 0)
        station_dict['availableBikes'] = station.get('availableBikes', 0)

        station_data.append(station_dict)

    return station_data


def load_data(table, data):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table)

    with table.batch_writer() as batch:
        for i in data:
            batch.put_item(i)


def files_from_zip(base_zipfile, reg_exp=None):
    '''
    this function takes a zip file and optional reg_exp to produce a list of files which then get extracted in into
    a list of dicts, ready to be loaded into the db
    '''

    with ZipFile(base_zipfile, 'r') as zip:
        files = zip.namelist()
        if reg_exp:
            r = re.compile(reg_exp)
            csvlist = list(filter(r.match, files))
        else:
            csvlist = files

        trips = []

        for i in csvlist:
            with zip.open(i, 'r') as fin:
                fin = io.TextIOWrapper(fin)
                reader = csv.DictReader(fin)
                for row in reader:
                    dict_row = Trip.create_from_dict(row)
                    # dynamodb throws a "AttributeValue may not contain an empty string"
                    # error when a value is '' #wtf number 2
                    stripped_row = {dict_key: dict_value for dict_key, dict_value in dict_row.__dict__.items()
                                    if dict_value != ''}
                    trips.append(stripped_row)

    return trips


def create_tables():
    # This doesn't have to live here or in the main but leaving it for now
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')

    try:
        tbl_station_data = dynamodb.create_table(
            TableName='StationData',
            KeySchema=[
                {
                    'AttributeName': 'station_id',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'station_id',
                    'AttributeType': 'N'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        tbl_station_data.meta.client.get_waiter('table_exists').wait(TableName='StationData')
        print("StationData table status:", tbl_station_data.table_status)

    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceInUseException":
            print('StationData table exists moving on...')
        else:
            raise e.response['Error']['Code']

    try:
        tbl_trip_data = dynamodb.create_table(
            TableName='TripData',
            KeySchema=[
                {
                    'AttributeName': 'trip_id',
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'trip_id',
                    'AttributeType': 'N'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        tbl_trip_data.meta.client.get_waiter('table_exists').wait(TableName='TripData')
        print("TripData table status:", tbl_trip_data.table_status)

    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceInUseException":
            print('TripData table exists moving on...')
        else:
            raise e.response['Error']['Code']
