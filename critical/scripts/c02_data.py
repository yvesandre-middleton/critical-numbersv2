#!/usr/bin/env python
import csv
import requests
from addict import Dict
import json
from datetime import date

# This script is set to run weekly on a cronjob on a local server to download the files and update data entries

c02_mean_url = "https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2/co2_annmean_mlo.csv"
c02_mean_url_global = "https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2/co2_annmean_gl.csv"
c02_ann_global_increase_url = "https://www.esrl.noaa.gov/gmd/webdata/ccgg/trends/co2/co2_gr_gl.csv"

with requests.Session() as s:
    mean_ma_download = s.get(c02_mean_url)
    mean_glbl_download = s.get(c02_mean_url_global)
    ann_inc_glbl_download = s.get(c02_ann_global_increase_url)

    mean_ma_decoded = mean_ma_download.content.decode('utf-8')
    mean_glbl_decoded = mean_glbl_download.content.decode('utf-8')
    ann_inc_glbl_decoded = ann_inc_glbl_download.content.decode('utf-8')

    mean_mauna_loa_cr = csv.reader(mean_ma_decoded.splitlines(), delimiter=',')
    mean_global_cr = csv.reader(mean_glbl_decoded.splitlines(), delimiter=',')
    ann_inc_global_cr = csv.reader(ann_inc_glbl_decoded.splitlines(), delimiter=',')

    mean_mauna_loa = list(mean_mauna_loa_cr)
    mean_global = list(mean_global_cr)
    ann_inc_global = list(ann_inc_global_cr)

    c02_data = Dict()

    if mean_mauna_loa and mean_global and ann_inc_global:
        for item in mean_mauna_loa:
            if item[0] == '1959':
                c02_data.mean_mauna_1959 = item[1]
        c02_data.mean_mauna_current = mean_mauna_loa[-1][1]
        for item in mean_global:
            if item[0] == '1980':
                c02_data.mean_global_1980 = item[1]
        c02_data.mean_global_current = mean_global[-1][1]

        c02_recent_avg_ann_inc = [float(ann_inc_global[-1][1]), float(ann_inc_global[-2][1]),
                                  float(ann_inc_global[-3][1]), float(ann_inc_global[-4][1]),
                                  float(ann_inc_global[-5][1]), float(ann_inc_global[-6][1]),
                                  float(ann_inc_global[-7][1]), float(ann_inc_global[-8][1]),
                                  float(ann_inc_global[-9][1]), float(ann_inc_global[-10][1])]

        c02_recent_avg_ann_increase = float(sum(c02_recent_avg_ann_inc)) / len(c02_recent_avg_ann_inc)

        c02_data.recent_avg_global_ann_increase = "{:.2f}".format(round(c02_recent_avg_ann_increase, 2))
        

        try:
            with open('/home/y_middleton/creations/critical_numbers_v2/critical/_data/climate_data/c02Data.json', 'w') as outfile:
                json.dump(c02_data, outfile)
            # create log file
            with open(f'/home/y_middleton/creations/critical_numbers_v2/critical/log/c02Data_'
                      f'{date.today()}.json', 'w') as outfile:
                json.dump(c02_data, outfile)
        except ValueError:
            print('JSON Creation FAILED')

        print("C02 data inserted: \n"
              "-------------------")
        print(c02_data)
