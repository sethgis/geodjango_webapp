import dash 
import plotly.graph_objects as go # or plotly.express as px
import folium
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import dash_leaflet as dl
from dash import Input, Output
import folium
# import dash_core_components as dcc
# import dash_bootstrap_components as dbc
import dash_html_components as html
from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
import numpy as np 
from dash.dependencies import Input, Output
import plotly.graph_objs as go

data = pd.read_csv("D:\LOCATEIT projects\WIND_IGAD REGION\Correct statistics\SC_STATS.csv") # load data
dropdown_list = data["TYPE"].unique()

app = dash.Dash()


app.layout = html.Div([
    html.H1('My first app with folium map'),
    html.Iframe(id='map', srcDoc=open('Map10.html', 'r').read(), width='100%', height='600'),
    html.Button(id='map-submit-button', n_clicks=0, children='Submit'),
    dcc.Dropdown(id='selector', options=[{'label' : p, 'value' : p} for p in dropdown_list],
                                                      multi=False, value=dropdown_list[0],
                                                      style={'backgroundColor': '#1E1E1E'}
                                                      ),
    
])

# NOT NEEDED AT ALL!!!!!!!!!!!!!!!!!!!!!!!
# @app.callback(
#     dash.dependencies.Output('map', 'srcDoc'),
#     [dash.dependencies.Input('map-submit-button', 'n_clicks')])
# def update_map(n_clicks):
#     if n_clicks is None:
#         return dash.no_update
#     else:
#         return open('Map10.html', 'r').read()

@app.callback(
    dash.dependencies.Output('map', 'srcDoc'),
    [dash.dependencies.Input('selector', 'value')])

def update_graph(selector):
    global data 
    data2 = data
    data2 = data2[data2["TYPE"] == selector] 

    lat = list(data2["LAT"])
    lon = list(data2["LON"])
    elev = list(data2["ELEV"])
 
    html = """<h4>Volcano information:</h4>
Height: %s m
"""
    map = folium.Map(location=[38.58, -99.09], zoom_start=5, TileLayer="Mapbox Bright")
    fg = folium.FeatureGroup(name = "My Map")
 
    for lt, ln, el in zip(lat, lon, elev):
        iframe = folium.IFrame(html=html % str(el), width=200, height=100)
        fg.add_child(folium.Marker(location=[lt, ln], popup=folium.Popup(iframe), icon = folium.Icon(color = "green")))
 
 
    map.add_child(fg)
    map.save("mymapnew.html")

    return open('mymapnew.html', 'r').read()


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True,port='8000')