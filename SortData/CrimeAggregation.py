import pandas as pd
import numpy as np

# Read in the data
df = pd.read_csv('../DC2Data/crimes.csv')
#['Crime ID', 'Month', 'Reported by', 'Falls within', 'Longitude',
       # 'Latitude', 'Location', 'LSOA code', 'LSOA name', 'Crime type',
       # 'Last outcome category', 'Context']

df_burglary = df[df['Crime type'] == 'Burglary']
print(df_burglary.describe())
df_burglary.to_csv('../DC2Data/burglary.csv')