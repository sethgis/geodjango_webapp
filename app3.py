import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import dash_leaflet as dl
from dash import Input, Output
import folium


import ee
import os
import geemap


# <html>

# <head>

#   <title>Django and GEE</title>

#   {{ map.header.render|safe }}

# </head>

# <body>

#   <div class="row">
#     <div class="col-lg-12">
#       {{map.html.render|safe}}
#     </div>
#   </div>

#   <script>

#   {{ map.script.render|safe}}
    
#   </script>

# </body>


dir = os.path.dirname(__file__) or "."
ppk_file = os.path.join(dir, "ppk.json")
service_account = 'seth-311@seth-1568964691342.iam.gserviceaccount.com'
# service_account_privatekey = 'seth-1568964691342-85f5ab32f561.json'
# print(service_account_privatekey)
credentials = ee.ServiceAccountCredentials(service_account, ppk_file)
ee.Initialize(credentials)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date('2020-07-01', '2020-11-30')).first()
table = ee.FeatureCollection('users/snyawacha/LASWE_BOUNDARY_SYMMETRICAL_DIFFERENCE')
table = ee.FeatureCollection("users/snyawacha/LASWE_BOUNDARY_SYMMETRICAL_DIFFERENCE").geometry()
modisndvi = dataset.select('NDVI').clip(table)
visParams = {'min':0, 'max':3000, 'palette':['225ea8','41b6c4','a1dab4','034B48']}
vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}
# print(table)
# Image.getThumbURL(params, callback)
image_url = modisndvi.getThumbURL({
    'min': 0, 'max': 9000, 'dimensions': 512, 'region': table,
    'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]})
print(image_url)
type(modisndvi)
# print(modisndvi).getInfo()
# type(image_url)
m = folium.Map(location=[60.25, 24.8], zoom_start=10, control_scale=True)
from geo.Geoserver import Geoserver
geo = Geoserver('http://45.76.249.64:8085/geoserver', username='admin', password='geoserver')