
with startts as(
select 
    extract(hour from starttime) as hour,
    count(extract(hour from starttime)) as starttime_count
from 
    trip_data
group by
    extract(hour from starttime)
),

endts as(
select
    extract(hour from stoptime) as hour,
    count(extract(hour from stoptime)) as stoptime_count
from 
    trip_data
group by
    extract(hour from stoptime)
)

select
    *
from 
    startts
join 
    endts using(hour)
order by
    hour