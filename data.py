# /usr/bin/env python3
# vim:fenc=utf-8
#
# Copyright © 2023 Kajetan Knopp <kajetan@knopp.com.pl>
#
# Distributed under terms of the MIT license.

"""
This file contains all data used in the project.
"""


from os import walk
import pandas as pd
from tqdm import tqdm
import plotly.express as px
import matplotlib.pyplot as plt

def get_all_files(dir):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir):
        f.extend([dir + '/' + file for file in filenames])
    return f

def concat_csv(l):
    return pd.concat([pd.read_csv(file) for file in tqdm(l)])

def clean_df(df):
    df = df[df['LSOA name'].str.contains('Barnet') & df['Crime type'].str.contains('Burglary')]
    df = df.dropna(subset=['Latitude', 'Longitude'])
    df = df.drop_duplicates()
    return df

def generate_data():
    all_street = get_all_files('data/metropolitan/street')
    all_outcomes = get_all_files('data/metropolitan/outcomes')
    lsoa_data = pd.read_csv('data/lsoa-data.csv', encoding= 'unicode_escape')
    earnings_data = pd.read_csv('data/modelled-household-income-estimates-lsoa.csv', encoding= 'unicode_escape')

    df_street = concat_csv(all_street)
    df_outcomes = concat_csv(all_outcomes)
    
    df_street = clean_df(df_street)
    full_df = pd.merge(df_street, df_outcomes, on='Crime ID', how='left')
    full_df = pd.merge(full_df, lsoa_data, on='LSOA code_x', how='left')
    full_df = pd.merge(full_df, earnings_data, on='LSOA code_x', how='left')

    full_df.to_csv('data/full_data.csv')
    return full_df

def read_data():
    return pd.read_csv('data/full_data.csv')

full_df = read_data()


fig = px.density_mapbox(full_df, lat = 'Latitude_x', lon = 'Longitude_x',                        radius = 8,
                        center = dict(lat = 51.59, lon = -0.1),
                        zoom = 10,
                        mapbox_style = 'open-street-map')

fig.show()

full_df['Outcome type'].value_counts().plot(kind='bar')

full_df['crime_count'] = full_df.groupby('LSOA code_x')['LSOA code_x'].transform('count')

for el in full_df['LSOA code_x'].unique():
    name = full_df[full_df['LSOA code_x'] == el]['LSOA name_x'].iloc[0]
    print(el, name,
          full_df[full_df['LSOA code_x'] == el]['crime_count'].iloc[0]) 

ser = pd.Series(full_df['Month_x'], name = 'value')
df = pd.DataFrame(ser)

stats_df = df \
.groupby('value') \
['value'] \
.agg('count') \
.pipe(pd.DataFrame) \
.rename(columns = {'value': 'frequency'})

# PDF
stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])

# CDF
stats_df['cdf'] = stats_df['pdf'].cumsum()
stats_df = stats_df.reset_index()

stats_df.plot(x = 'value', y = ['pdf', 'cdf'], grid = True)

plt.show()
