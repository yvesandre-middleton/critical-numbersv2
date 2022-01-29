#!/usr/bin/env python
import csv
import requests
from addict import Dict
import json
from datetime import date

# This script is set to run weekly on a cronjob on a local server to download the files and update data entries

temp_data_url = "https://www.ncdc.noaa.gov/cag/time-series/global/globe/land_ocean/ann/12/1880-2021.csv"

with requests.Session() as s:
    temp_download = s.get(temp_data_url)

    temp_decoded = temp_download.content.decode('utf-8')

    read_csv = csv.reader(temp_decoded.splitlines(), delimiter=',')

    temp_data = list(read_csv)

    temp_dict = Dict()

    if temp_data:
        for item in temp_data:    
            if item[0] == '1880':
                temp_dict.temp_1880 = item[1]
            elif item[0] == '1980':
                temp_dict.temp_1980 = item[1]
        temp_dict.temp_current = temp_data[-1][1]
        try:
            with open('/home/y_middleton/creations/critical_numbers_v2/critical/_data/climate_data/tempData.json', 'w') as outfile:
                json.dump(temp_dict, outfile)
            # create log file
            with open(f'/home/y_middleton/creations/critical_numbers_v2/critical/log/tempData_'
                      f'{date.today()}.json', 'w') as outfile:
                json.dump(temp_dict, outfile)
        except ValueError:
            print('JSON Creation FAILED')

        print("Temperature data inserted: \n"
              "-------------------")