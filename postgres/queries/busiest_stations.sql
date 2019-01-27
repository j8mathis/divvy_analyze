with from_count as (
select
    from_station_id,
    count(to_station_id) as from_count
from
    trip_data
group by
    from_station_id
),

to_count as (
select
    to_station_id,
    count(to_station_id) as to_count
from
    trip_data
group by
    to_station_id
)

select
    s.station_name,
    s.latitude,
    s.longitude,
    s.available_docks,
    s.total_docks,
    s.available_bikes,
    f.from_count,
    --to_range,
    t.to_count
    --from_range
from 
    station_data s
 join
     from_count f on f.from_station_id = s.station_id
 join
     to_count t on t.to_station_id = s.station_id
 group by
    s.station_name,
    s.latitude,
    s.longitude,
    s.available_docks,
    s.total_docks,
    s.available_bikes,
    f.from_count,
    t.to_count
 order by 
     from_count desc,
     to_count desc
limit 10; 