Select 
    min(stoptime - starttime) as min_duration,
    max(stoptime - starttime) as max_duration,
    avg(stoptime - starttime) as avg_duration
from 
	trip_data;
