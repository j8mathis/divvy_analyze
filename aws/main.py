import utils
from botocore.exceptions import EndpointConnectionError
from datetime import datetime


def main():
    print_header()
    try:
        # not sure these need to be here but leaving for now
        utils.create_table(table_name='TripData', partition_key='trip_id')
        utils.create_table(table_name='StationData', partition_key='station_id')
        run_event()
    except EndpointConnectionError as e:
        print('ERROR:', e)
        print('Check your connections and try again')


def print_header():
    print('-----------------------------')
    print(' Divvy Analyze AWS Demo      ')
    print('-----------------------------')


def bulk_loader(table, list_dict):
    '''
    This function is a wrapper for the put item function.
    :param (string) table:
    :param (list) list_dict:
    '''
    for counter, i in enumerate(list_dict, 1):
        r = utils.put_item(table, i)
        if counter % 100 == 0:
            now = str(datetime.now().isoformat())
            print(f"{now} - Items Loaded: {counter} Last StatusCode: {r['ResponseMetadata']['HTTPStatusCode']}")

    print(f'bulk load complete')


def run_event():
    print('What do you want to do?')
    cmd = 'EMPTY'

    while cmd != 'x' and cmd:
        cmd = input('[S]tatic data load (takes a looong time), [L]ive data load, [R]un report, E[x]it: ')
        cmd = cmd.lower().strip()

        if cmd == 's':
            '''
            this loads the static trip data from a zipped csv
            after the initial load there is no need to reload this
            mainly here for either new trip data or moving data into another location, table, etc
            '''
            trip_data = utils.files_from_zip("../data/Divvy_Trips_2016_Q3Q4.zip", "Divvy_Trips_.*Divvy_Trips.*csv$")
            bulk_loader('TripData', trip_data)
        elif cmd == 'l':
            # this loads current data about the stations pulls from an http end point
            live_data = utils.get_live_data('https://feeds.divvybikes.com/stations/stations.json')
            bulk_loader('StationData', live_data)
        elif cmd == 'r':
            print('report coming right up')
        elif cmd != 'x' and cmd:
            print(f"Sorry, we don't understand '{cmd}'.")

    print('C ya')


if __name__ == '__main__':
    main()
