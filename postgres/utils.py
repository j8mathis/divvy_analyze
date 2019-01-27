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
    This class creates a connection to a postgres database. The credentials should be stored in a secured location,
    such as a secret vault. For example they are not.
    """

    def __init__(self):
        self.cstring = "host=localhost dbname=divvy_analyze user=postgres"

        self.conn = psycopg2.connect(self.cstring)

        # for my needs now setting autocommit to true
        self.conn.set_session(autocommit=True)

        return

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.conn!r}')

    @staticmethod
    def get_text_link(link):
        """
        This function takes an url and returns the text
        :param (string) link: a github "raw" link
        :return text:
        """
        query = requests.get(link)
        sql = query.text
        return sql

    def execute(self, sql, parameters=None):
        """
        :param (string) sql: text from the get_text_link method
        :param parameters: dict values for placeholders
        :return cursor: open cursor, fetch and close
        """
        cur = self.conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(sql, parameters)

        return cur
