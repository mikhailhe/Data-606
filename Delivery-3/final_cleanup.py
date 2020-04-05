# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 21:55:08 2020

@author: Mikhail
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta

def data_clean():
    #Data reading and cleaning
    df = pd.read_csv(r'C:\Users\Mikhail\Documents\Data 606\US_Accidents_Dec19_stage1.csv', parse_dates = ['Start_Time', 'End_Time', 'Time_Elapsed'], infer_datetime_format = True)
    df = df.sort_values(by = ['Start_Time']).reset_index()
    df.drop(['index', 'Precipitation(in)'], axis = 1, inplace = True)
    df['Description'] = df['Description'].str.lower()
    df['Highway'] = 0
    df['Time_Elapsed'] = df['End_Time'] - df['Start_Time']
    #Encodes accidents that happened on an interstate highway
    df.loc[df['Description'].str.contains(r'accident on i-\d'), 'Highway'] = 1
    df['Day_of_Week'] = df['Start_Time'].dt.weekday
    df['Hour'] = df['Start_Time'].dt.hour
    df['Month'] = df['Start_Time'].dt.month
    df['Year'] = df['Start_Time'].dt.year
    
    i_cols = ['Temperature(F)', 'Humidity(%)','Pressure(in)','Wind_Speed(mph)', 'Visibility(mi)']
    
    #Interpolates missing values
    for i in i_cols:
        df[i] = df.groupby(['State', 'City', 'Year', 'Month', 'Day_of_Week'])[i].apply(lambda x: x.interpolate(limit = 4, limit_direction = 'both'))
        
    df.dropna(inplace = True)
        
    #Makes time elapsed into minutes
    df['Time_Elapsed'] = df['Time_Elapsed'].apply(lambda x: timedelta.total_seconds(x) / 60)
    
    #Only keeping values with a positive time elapsed
    df = df[df['Time_Elapsed'] >= 0]
    
    return df

if __name__ == '__main__':
    data_clean()
    