import sys
from zipfile import ZipFile

import pandas as pd
import numpy
import os

import pandas.errors


# Source: https://www.nomisweb.co.uk/census/2021/bulk
path = r'A:\CensusData21'
output_folder = r'A:\ExtractedFiles'
codes = ["E01000248","E01000249","E01000250","E01000254","E01000292","E01000293","E01000167","E01000246","E01000247","E01000251","E01000252","E01000166","E01000168","E01000169","E01000172","E01000285","E01000287","E01000288","E01000289","E01000291","E01000294","E01000267","E01000268","E01000269","E01000270","E01000170","E01000171","E01000173","E01000174","E01000175","E01000228","E01000253","E01000279","E01000280","E01000286","E01000290","E01000271","E01000272","E01000273","E01000281","E01000282","E01000115","E01000116","E01000119","E01000120","E01000122","E01000117","E01000118","E01000121","E01000123","E01000124","E01000265","E01000266","E01000274","E01000320","E01000322","E01000275","E01000277","E01000283","E01000284","E01000321","E01000195","E01000229","E01000230","E01000231","E01000232","E01000233","E01000186","E01000187","E01000188","E01000189","E01000190","E01000191","E01000158","E01000159","E01000160","E01000161","E01000162","E01000324","E01000256","E01000258","E01000263","E01000264","E01000255","E01000257","E01000261","E01000262","E01000192","E01000193","E01000194","E01000226","E01000227","E01000299","E01000300","E01000302","E01000317","E01000318","E01000323","E01000276","E01000278","E01000301","E01000303","E01000304","E01000130","E01000132","E01000133","E01000234","E01000235","E01000156","E01000157","E01000163","E01000164","E01000165","E01000315","E01000197","E01000295","E01000296","E01000298","E01000125","E01000127","E01000128","E01000129","E01000131","E01000134","E01000198","E01000199","E01000204","E01000259","E01000260","E01000126","E01000151","E01000152","E01000153","E01000154","E01000176","E01000178","E01000184","E01000297","E01000316","E01000319","E01000196","E01000200","E01000201","E01000202","E01000203","E01000177","E01000179","E01000180","E01000181","E01000182","E01000185","E01000147","E01000148","E01000155","E01033572","E01033573","E01000239","E01000240","E01000241","E01000309","E01000237","E01000242","E01000243","E01000244","E01000245","E01000314","E01000183","E01000206","E01000207","E01000208","E01000210","E01000213","E01000236","E01000238","E01000310","E01000311","E01000205","E01000209","E01000211","E01000212","E01000216","E01000217","E01000150","E01000305","E01000306","E01000308","E01000312","E01000313","E01000145","E01000215","E01000218","E01000219","E01000220","E01000225","E01000135","E01000136","E01000144","E01000146","E01000214","E01000141","E01000221","E01000223","E01000307","E01000138","E01000142","E01000222","E01000224","E01000137","E01000139"]

# for file_name in os.listdir(path):
#     if file_name.endswith('.zip'):
#         zip_file_path = os.path.join(path, file_name)
#         with ZipFile(zip_file_path, 'r') as zip_file:
#             for member_name in zip_file.namelist():
#                 if member_name.endswith('lsoa.csv'):
#                     zip_file.extract(member_name, output_folder)

df = pd.DataFrame()  # Create an empty DataFrame

for file_name in os.listdir(output_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(output_folder, file_name)
        try:
            current_df = pd.read_csv(file_path, header=0)
            # Split the file name using the '-' delimiter
            parts = file_name.split('-')

            # Get the second part (index 1) from the split
            ts_part = parts[1]
            current_df[ts_part] = ts_part  # Add a new column with the ts_part value

            # Filter rows based on "geography code" column
            current_df = current_df[current_df['geography code'].isin(codes)]

            if df.empty:
                df = current_df
            else:
                df = pd.concat([df, current_df], axis=1)

        except pd.errors.EmptyDataError:
            print(file_path)
            continue

# Get the duplicated column names
duplicated_columns = df.columns[df.columns.duplicated()]

# Drop the duplicated columns, preserving the first occurrence
df = df.loc[:, ~df.columns.duplicated()]


df.to_csv(r'A:\CensusData21\merged.csv', index=False)


