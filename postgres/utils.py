import requests
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor


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
        station_dict = {'station_id': station.get('id'), 'latitude': station.get('latitude'),
                        'longitude': station.get('longitude'), 'status': station.get('status'),
                        'station_name': station.get('stationName'), 'available_docks': station.get('availableDocks', 0),
                        'total_docks': station.get('totalDocks', 0),
                        'available_bikes': station.get('availableBikes', 0), 'load_datetime': now}

        station_data.append(station_dict)

    return station_data


class pgConnection(object):
    """
    something here
    """

    def __init__(self):
        """
        database connection
        """

        self.cstring = "host=localhost dbname=divvy_analyze user=postgres"

        self.conn = psycopg2.connect(self.cstring)

        # for my needs now setting autocommit to true
        self.conn.set_session(autocommit=True)

        return

    def get_text_link(self, link):
        # git query text from github raw link
        query = requests.get(link)
        sql = query.text
        return sql

    def execute(self, sql, parameters=None):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(sql, parameters)

        return cur

    def cleanup(self):
        # don't think I will use this
        self.cur.close()
        self.conn.close()

        return
