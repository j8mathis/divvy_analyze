from zipfile import ZipFile
import re


def files_from_zip(base_zipfile,reg_exp=None):
    '''
    this function takes a zip file and optional reg_exp to produce a list of files
    '''

    with ZipFile(base_zipfile, 'r') as zip: 
        files = zip.namelist()
        if reg_exp:
            r = re.compile(reg_exp)
            csvlist = list(filter(r.match, files))
        else:
            csvlist = files


    return csvlist

files = files_from_zip("../../pentaho/divvy/divvy_data/Divvy_Trips_2016_Q3Q4.zip","Divvy_Trips_.*Divvy_Trips.*csv$")
print(files)

