import utils


def main():
    print_header()
    run_event()


def print_header():
    print('-----------------------------')
    print(' Divvy Analyze postgres Demo ')
    print('-----------------------------')


def run_report(conn_obj, name, url):
    url = \
        'https://raw.githubusercontent.com/j8mathis/divvy_analyze/master/postgres/queries/busiest_hours.sql'
    query = conn_obj.get_text_link(url)
    cur = conn_obj.execute(query)
    results = cur.fetchall()
    print("--------------")
    print(f"{name} Report")
    print("--------------")
    for i in results:
        print(i)
    cur.close()


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
            hour_url = \
                'https://raw.githubusercontent.com/j8mathis/divvy_analyze/master/postgres/queries/busiest_hours.sql'
            run_report(d, "Busiest Hour", hour_url)
            st_url = \
                'https://github.com/j8mathis/divvy_analyze/blob/master/postgres/queries/busiest_stations.sql'
            run_report(d, "Busiest Station", st_url)
            dur_url = \
                'https://github.com/j8mathis/divvy_analyze/blob/master/postgres/queries/duration.sql'
            run_report(d, "Duration", dur_url)

        elif cmd != 'x' and cmd:
            print(f"Sorry, we don't understand '{cmd}'.")

    d.conn.close()
    print('C ya')


if __name__ == '__main__':
    main()
