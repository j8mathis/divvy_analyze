import requests
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from zipfile import ZipFile
import re
from trip_data_type import Trip
import csv
import io
from datetime import datetime


def get_live_data(url):
    """
    This function pulls data from a http endpoint and loads each row into a dict and adds it to a list.
    :param (string) url: http endpoint containing the data
    :return: a list of dictionaries
    """

    resp = requests.get(url)
    resp.raise_for_status()

    live_data_raw = resp.json()
    live_data_list = live_data_raw.get('stationBeanList')
    now = str(datetime.now().isoformat())

    station_data = []
    for station in live_data_list:
        station_dict = {}
        station_dict['station_id'] = station.get('id')
        # dynamodb throws some weird error about floats, hence the casting below
        station_dict['latitude'] = Decimal(str(station.get('latitude')))
        station_dict['longitude'] = Decimal(str(station.get('longitude')))
        station_dict['status'] = station.get('status')
        station_dict['stationName'] = station.get('stationName')
        station_dict['availableDocks'] = station.get('availableDocks', 0)
        station_dict['totalDocks'] = station.get('totalDocks', 0)
        station_dict['availableBikes'] = station.get('availableBikes', 0)
        station_dict['load_datetime'] = now

        station_data.append(station_dict)

    return station_data


def chunks(l, n):
    """
    This function takes a list and creates lists the length of n. Wrap the call in a list to get a list of lists.
    Credit to Chris Albon who gives credit to someone else, ah community.
    ref: https://chrisalbon.com/python/data_wrangling/break_list_into_chunks_of_equal_size/
    :param (list) l: list you want to split
    :param (int) n: length of list returned
    :return: a series of lists the length of n
    """
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i + n]


def load_data(table, list_dict):
    """
    This function loads a list of dicts into dynamodb db.
    :param (string) table: Name of table to load data
    :param (dict) list_dict: A list of dicts
    :return: response from service
    """
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(table)

    with table.batch_writer() as batch:
        for i in list_dict:
            batch.put_item(Item=i)


def files_from_zip(base_zipfile, reg_exp=None):
    """
    This function unzip an archive and create a dict for each row and adds it to a list
    :param (string) base_zipfile: a zipfile containing csv files
    :param (string) reg_exp: optional regex expression
    :return: A list of dictionaries
    """

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


def create_table(**kwargs):
    """
    This is a simple function that creates a table in dynamodb.
    :param kwargs: table_name (string), partition_key (string)
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
    print(f"Creating {kwargs['table_name']}...")
    try:
        table = dynamodb.create_table(
            TableName=kwargs['table_name'],
            KeySchema=[
                {
                    'AttributeName': kwargs['partition_key'],
                    'KeyType': 'HASH'  # Partition key
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': kwargs['partition_key'],
                    'AttributeType': 'N'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

        table.wait_until_exists()
        print(f"{kwargs['table_name']} table status:", table.table_status)

    except ClientError as e:
        if e.response['Error']['Code'] == "ResourceInUseException":
            print(f"{kwargs['table_name']} table exists moving on...")
        else:
            raise e.response['Error']['Code']
