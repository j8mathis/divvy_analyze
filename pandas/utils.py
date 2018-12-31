from zipfile import ZipFile 
import pandas as pd
import requests
import json
import re

def df_from_zip_csv(base_zipfile,reg_exp=None):
    '''
    this function takes a zip file and optional reg_exp to produce
    a dataframe from csv files in a zipped archive
    ''' 

    with ZipFile(base_zipfile, 'r') as zip: 
        files = zip.namelist()
        if reg_exp:
            r = re.compile(reg_exp)
            csvlist = list(filter(r.match, files))
        else:
            csvlist = files

        df = pd.concat([pd.read_csv(zip.open(f)) for f in csvlist])
    return df

def get_request(link):
    '''
    this function gets json data from an http endpoint
    and loads it into a json structure. It also raises an error
    if need be. 
    '''
    try: 
        r = requests.get(link)
        r.raise_for_status()
        data = json.loads(r.text)
        return data
    except requests.exceptions.HTTPError as err:
        print("http request not successful", err)
        return False

def make_ranges(dframe,agg_column,output_column):
    '''
    this function makes ranges from the count columns
    '''
    dframe.loc[dframe[agg_column] < 10, output_column] = 'XS'
    dframe.loc[(dframe[agg_column] >= 10) & (dframe[agg_column] < 100), output_column] = 'S'
    dframe.loc[(dframe[agg_column] >= 100) & (dframe[agg_column] < 1500), output_column] = 'M'
    dframe.loc[(dframe[agg_column] >= 1500) & (dframe[agg_column] < 5000), output_column] = 'L'
    dframe.loc[dframe[agg_column] > 5000, output_column] = 'XL'
    return