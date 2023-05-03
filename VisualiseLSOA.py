import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly
import pyproj

shape = gpd.read_file(r"DC2Data/LSOAShapes/")
shape.crs = {'init': 'epsg:27700'}

# print(shape.columns)

burglaries = pd.read_csv(r"DC2Data/burglary.csv")
counts = burglaries.groupby('LSOA code').size()
counts = counts.to_frame()
counts.columns = ['count']
counts = counts.reset_index()
counts = counts.rename(columns={'LSOA code': 'LSOA11CD'})
shape = shape.merge(counts, on='LSOA11CD')
shape.set_index('LSOA11NM', inplace=True)

shape.to_crs(epsg=4326, inplace=True)
fig = px.choropleth(shape, geojson=shape.geometry, locations=shape.index, color='count')
fig.update_geos(fitbounds="locations", visible=False)
fig.to_html('DC2Data/LSOAmap.html')
fig.show()
