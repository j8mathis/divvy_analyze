from datetime import datetime


class Trip:
    """
    Trip data object used for creating dictionaries from CSV files. This is maybe overkill here. .
    I learned this in Michael Kennedy's awesome jumpstart course.
    ref: https://github.com/mikeckennedy/python-jumpstart-course-demos
    *update 3.7 has data classes now and its less typing...I am in
    """

    def __init__(
            self, trip_id, starttime, stoptime, bikeid,
            tripduration, from_station_id, from_station_name, to_station_id, to_station_name,
            usertype, gender, birthyear, load_datetime):
        self.trip_id = trip_id
        self.starttime = starttime
        self.stoptime = stoptime
        self.bikeid = bikeid
        self.tripduration = tripduration
        self.from_station_id = from_station_id
        self.from_station_name = from_station_name
        self.to_station_id = to_station_id
        self.to_station_name = to_station_name
        self.usertype = usertype
        self.gender = gender
        self.birthyear = birthyear
        self.load_datetime = load_datetime

    @staticmethod
    def create_from_dict(lookup):
        """
        This function creates an object with data attributes below.
        :param (dict) lookup:
        :return: object with data attributes
        """
        now = str(datetime.now().isoformat())
        return Trip(
            int(lookup['trip_id']),
            lookup['starttime'],
            lookup['stoptime'],
            int(lookup['bikeid']),
            int(lookup['tripduration']),
            int(lookup['from_station_id']),
            lookup['from_station_name'],
            int(lookup['to_station_id']),
            lookup['to_station_name'],
            lookup['usertype'],
            lookup['gender'],
            # leave the empty string I am stripping them out before the load
            int(lookup['birthyear']) if lookup['birthyear'] else '',
            now

        )
