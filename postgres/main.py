import utils
import yaml


def main():
    print_header()
    run_event()


def print_header():
    print('-----------------------------')
    print(' Divvy Analyze postgres Demo ')
    print('-----------------------------')


def run_report(conn_obj, name, url):
    query = conn_obj.get_text_link(url)
    cur = conn_obj.execute(query)
    results = cur.fetchall()
    print("--------------")
    print(f"{name} Report")
    print("--------------")
    for i in results:
        print(i)
    print()
    cur.close()


def run_event():
    print('What do you want to do?')
    cmd = 'EMPTY'
    d = utils.pgConnection()

    while cmd != 'x' and cmd:
        cmd = input('[L]ive data reload, [R]un report, E[x]it: ')
        cmd = cmd.lower().strip()

        if cmd == 'l':
            """ This is a complete dump and reload of live station data """
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
            with open('queries.yaml', 'rb') as ymlfile:
                cfg = yaml.load(ymlfile)
            queries = list(cfg.keys())

            for q in queries:
                url = cfg[q]["query"]
                name = cfg[q]["name"]
                run_report(d, name, url)

        elif cmd != 'x' and cmd:
            print(f"Sorry, we don't understand '{cmd}'.")

    d.conn.close()
    print('C ya')


if __name__ == '__main__':
    main()
