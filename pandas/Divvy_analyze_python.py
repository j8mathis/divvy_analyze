
# importing required modules 
import pandas as pd
from pandas.io.json import json_normalize
import utils as u
from datetime import datetime
import sys

#try to get live station from http request
station_data = u.get_request('https://feeds.divvybikes.com/stations/stations.json')

if not station_data:
    print("Cannot proceed without live data")
    sys.exit()

#take json and pull out what info you want
station_data_raw  = json_normalize(station_data['stationBeanList'])
station_data = station_data_raw[['id','latitude','longitude','status','stationName','availableDocks','totalDocks','availableBikes']]

# get dataframe from zipped csvs
df = u.df_from_zip_csv("../../pentaho/divvy/divvy_data/Divvy_Trips_2016_Q3Q4.zip","Divvy_Trips_.*Divvy_Trips.*csv$")

#create two df for "to" and "from" 
from_trips = pd.merge(df, station_data, left_on='from_station_id', right_on='id')
to_trips = pd.merge(df, station_data, left_on='to_station_id', right_on='id')

#count and group by station for each
from_count_total = from_trips.groupby(['from_station_id'])['from_station_id'].count().reset_index(name='from_count')
to_count_total = to_trips.groupby(['to_station_id'])['to_station_id'].count().reset_index(name='to_count')

#verifying counts above
#print(from_trips[from_trips['from_station_id']==582])
#print(to_trips[to_trips['to_station_id']==562])

#merge counts back onto dfs
from_trips_counts = pd.merge(from_trips, from_count_total, on='from_station_id')
to_trips_counts = pd.merge(to_trips, to_count_total, on='to_station_id')

#sort and select 
df_to_counts = to_trips_counts[['to_station_name','latitude','longitude','availableDocks','totalDocks','availableBikes','to_count']].sort_values(by='to_count', ascending=False)
df_from_counts = from_trips_counts[['from_station_name','from_count']].sort_values(by='from_count', ascending=False)

#drop dups after join 
df_from_final = df_from_counts.drop_duplicates().copy()
df_to_final = df_to_counts.drop_duplicates().copy()

#make xs,s,m,l labels 
u.make_ranges(df_from_final,'from_count','from_range')
u.make_ranges(df_to_final,'to_count','to_range')

#join from and to data for viewing and select columns
df_display = pd.merge(df_to_final, df_from_final, left_on='to_station_name', right_on='from_station_name')
df_display_final = df_display[['to_station_name','latitude','longitude','availableDocks','totalDocks','availableBikes','to_count','to_range','from_count','from_range']].copy()

#rename column for view
df_display_final.rename(columns={'to_station_name': 'stationName'}, inplace=True)
print(df_display_final.head(),"\n")

#gender analysis simple group by gender
df_display_gender = df.groupby(['gender'])['gender'].count().reset_index(name='count')      
print(df_display_gender.head(),"\n")

#age based analysis, find age of riders
df_age = df.dropna(subset=['birthyear']).copy()

now = datetime.now()
df_age['age'] = now.year - df_age['birthyear']
df_age_final = df_age.groupby(['age','birthyear'])['age'].count().reset_index(name='count')
df_display_age = df_age_final[['birthyear','age','count']].sort_values(by='count',ascending=False).reset_index(drop=True)
print(df_display_age.head(),"\n")
