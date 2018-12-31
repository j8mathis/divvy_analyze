import utils
from botocore.exceptions import EndpointConnectionError


def main():
    print_header()
    try:
        utils.create_tables()
        run_event()
    except EndpointConnectionError as e:
        print('ERROR:', e)
        print('Check your connections and try again')

def print_header():
    print('-----------------------------')
    print(' Divvy Analyze AWS Demo      ')
    print('-----------------------------')


def run_event():
    print('What do you want to do?')
    cmd = 'EMPTY'

    while cmd != 'x' and cmd:
        cmd = input('[S]tatic data load (takes a looong time), [L]ive data load, [R]un report, E[x]it: ')
        cmd = cmd.lower().strip()

        if cmd == 's':
            # this loads the static trip data from a zipped csv
            # after the initial load there is no need to reload this
            # mainly here for either new trip data or moving data into another location, table, etc
            trip_data = utils.files_from_zip("../data/Divvy_Trips_2016_Q3Q4.zip", "Divvy_Trips_.*Divvy_Trips.*csv$")
            utils.load_data('TripData', trip_data)
        elif cmd == 'l':
            # this loads current data about the stations pull from an http end point
            live_data = utils.get_live_data('https://feeds.divvybikes.com/stations/stations.json')
            utils.load_data('StationData', live_data)
        elif cmd == 'r':
            print('report coming right up')
        elif cmd != 'x' and cmd:
            print("Sorry, we don't understand '{}'.".format(cmd))

    print('C ya')


if __name__ == '__main__':
    main()
