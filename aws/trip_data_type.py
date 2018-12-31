class Trip:
    '''
    Neat way to build an object with data and then convert to a dict. Very nice to be able to control the data types
    '''
    def __init__(
            self, trip_id, starttime, stoptime, bikeid,
            tripduration, from_station_id, from_station_name, to_station_id, to_station_name,
            usertype, gender, birthyear):
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

    @staticmethod
    def create_from_dict(lookup):
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
            int(lookup['birthyear']) if lookup['birthyear'] else ''
        )