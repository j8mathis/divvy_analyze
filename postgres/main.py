import utils


def main():
    print_header()
    run_event()


def print_header():
    print('-----------------------------')
    print(' Divvy Analyze postgres Demo ')
    print('-----------------------------')


def run_event():
    print('What do you want to do?')
    cmd = 'EMPTY'
    d = utils.pgConnection()

    while cmd != 'x' and cmd:
        cmd = input('[L]ive data reload, [R]un report, E[x]it: ')
        cmd = cmd.lower().strip()

        if cmd == 'l':
            live_data = utils.get_live_data('https://feeds.divvybikes.com/stations/stations.json')
            d.execute("truncate station_data;")
            for i in live_data:
                d.execute("""
                        INSERT INTO station_data (station_id, latitude, longitude, status, station_name, 
                        available_docks, total_docks, available_bikes, load_datetime)
                        VALUES (%(station_id)s, %(latitude)s, %(longitude)s, %(status)s, %(station_name)s, 
                        %(available_docks)s, %(total_docks)s, %(available_bikes)s, %(load_datetime)s );
                        """, i)
        elif cmd == 'r':
            print('report coming right up')
        elif cmd != 'x' and cmd:
            print(f"Sorry, we don't understand '{cmd}'.")

    d.conn.close()
    print('C ya')


if __name__ == '__main__':
    main()
