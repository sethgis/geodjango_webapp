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
dir = os.path.dirname(__file__) or "."
ppk_file = os.path.join(dir, "ppk.json")
service_account = ''
# service_account_privatekey = 'seth-1568964691342-85f5ab32f561.json'
# print(service_account_privatekey)
credentials = ee.ServiceAccountCredentials(service_account, ppk_file)
ee.Initialize(credentials)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

dataset = ee.ImageCollection('MODIS/006/MOD13Q1').filter(ee.Filter.date('2020-07-01', '2020-11-30')).first()
table = ee.FeatureCollection('users/snyawacha/LASWE_BOUNDARY_SYMMETRICAL_DIFFERENCE')
table = ee.FeatureCollection("users/snyawacha/LASWE_BOUNDARY_SYMMETRICAL_DIFFERENCE").geometry()
modisndvi = dataset.select('NDVI').clip(table)
# print(modisndvi)
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
# print(image_url)
# type(image_url)
src = modisndvi.getMapId(vis_paramsNDVI)["tile_fetcher"].url_format
print(src)




m = folium.Map(location=[60.25, 24.8],style={"top":1500,
        "bottom":0,
        "right":0,
        "left":0,
        "height": "95vh",
        "order":1,
        "z-index":"500",}, zoom_start=10, control_scale=True)
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

basemap = folium.Map(TileLayer="Mapbox Bright", style={'width': '1000px', 'height': '500px'})
map = folium.Map(location=[1.9577, 37.2972], zoom_start=5, TileLayer="Mapbox Bright", style={"top":1500,
        "bottom":0,
        "right":0,
        "left":0,
        "height": "95vh",
        "order":1,
        "z-index":"500",})
far = folium.Figure(width=1000, height=1000)
m=folium.Map(location=[1.9577, 37.2972], zoom_start=4).add_to(far)
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="primary", className="ms-2", n_clicks=0,
            ),
            width="auto",
        ),
    ],)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("Wind Erosion Factors", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                href="https://locateit.co.ke/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                # search_bar,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
    ),
    color="#032b0d",
    dark=True,)


access_token ="pk.eyJ1Ijoic2V0aG55YXdhY2hhIiwiYSI6ImNrdmk5NXJscTQzengycW9rdWN6azdpcjQifQ._AnDc8NPaSs5WMPhh9nvGA"  # settings.MAPBOX_TOKEN
id = "mapbox://styles/mapbox/satellite-v9"
mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/mapbox://styles/mapbox/satellite-v9/tiles/{{z}}/{{x}}/{{y}}{{r}}?access_token=pk.eyJ1Ijoic2V0aG55YXdhY2hhIiwiYSI6ImNrdmk5NXJscTQzengycW9rdWN6azdpcjQifQ._AnDc8NPaSs5WMPhh9nvGA"



base = html.Div(
    dl.Map(
        [dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}),

        dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"),dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?/",
                                            layers="VC", format="image/png", transparent=True),
            dl.LayersControl(
                [
                    dl.BaseLayer(
                        dl.TileLayer(), 
                        name="OpenStreetMaps",
                        checked=True,
                    ),
                      
                    
                    dl.BaseLayer(
                        dl.TileLayer(url = mapbox_url,
                        attribution="Mapbox",), 
                        id=id,
                        name="Mapbox",

            ), 
                    
                     dl.BaseLayer(
                        dl.TileLayer(
                            url="https://www.ign.es/wmts/mapa-raster?request=getTile&layer=MTN&TileMatrixSet=GoogleMapsCompatible&TileMatrix={z}&TileCol={x}&TileRow={y}&format=image/jpeg",
                            attribution="IGN",
                        ),
                        name="IGN",
                        # layers='0',
                        checked=False,
                           
                    ),
                ],
            ),
            html.Div(id='base'),
            # get_data(),
        ],
        zoom=4,
        center=(0.0236, 37.9062),
             
    ),
    style={
        "top":1500,
        "bottom":0,
        "right":0,
        "left":0,
        "height": "95vh",
        "order":1,
        "z-index":"500",
    },
)

style= { "top":0,
        "bottom":500,
        "right":0,
        "left":0,
        "height": "100vh",
        "order":1,}
        
map =  html.Div(dl.Map(
    [dl.TileLayer(), dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
     
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"), dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms/",
                                            layers="VC", format="image/png", transparent=False,)],
           center=[0.0236, 37.9062], zoom=4,
           ),
)


Map = geemap.Map()

# Center the map and display the image.
Map.centerObject(table)

Map





SIDEBAR_STYLE = {

    "position": "absolute",
    "top": 350,
    "left": 20,
    "bottom":350,
    "height":200,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#6d9460",
    "order":1,
    "z-index": "1000",
    "round":"80",
    "border-radius":"10px",
    "draggable":'True',
}
SIDEBAR_STYLE2 = {

    "position": "absolute",
    "top": 650,
    "left": 1350,
    "bottom":50,
    "height":200,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#6d9460",
    "order":1,
    "z-index": "1500",
    "round":"80",
    "border-radius":"10px",
    "draggable":'True',
}

sidebar = html.Div(
      [
        html.P("Factors", className="display-6", draggable= 'True'),
        dcc.Dropdown(
            [
                {"label": "Climate Erosivity", "value": "CE",},
                {"label": "Erodible Fraction", "value": "EF"},
                {"label": "Soil Crust", "value": "SC",},
                {"label": "Vegetation Sensitivity", "value": "VC"},
                {"label": "Surface Roughness", "value": "SR"},
                {"label": "ILSWE", "value": "ILSWE"},
            ],id='dropdown'),
   html.Div(id='out'),
    ],
    style=SIDEBAR_STYLE,
)




spinners = html.Div(
    [
        dbc.Spinner(color="primary"),
        dbc.Spinner(color="secondary"), 
    ]
)
output = {
        "top":0,
        "bottom":0,
        "right":0,
        "left":0,
        "height": "92vh",
        "order":1,
        "z-index":"500",
    },

SIDEBAR_STYLE2 = {

        "top":0,
        "bottom":0,
        "right":0,
        "left":0,
        "height": "92vh",
        "order":1,
        "z-index":"500",
    
}



app.layout = html.Div([
navbar,
sidebar,
base,
# m,

],)

@app.callback(
    Output('base','children'),
    Input('dropdown', 'value'))
def update_value(value):
    if value=="CE":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
     
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"), 
                              
     dl.BaseLayer(
                        dl.TileLayer(
                            url=src,
                            attribution="Google Earth Engine",
                        ),
                        name="NDVI",
                        # layers='0',
                        checked=False,
                           
                    ),
                                            ],
           center=[0.0236, 37.9062], zoom=4,
           style= SIDEBAR_STYLE2,
           ), 
    ), 
    elif value=="EF":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?",
                                            layers="CE", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
    elif value=="SC":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8080/geoserver/ADS/wms?/",
                                            layers="SC", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
    elif value=="VC":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?/",
                                            layers="VC", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
    elif value=="SR":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/raster/wms?/",
                                            layers="SR", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
    elif value=="ILSWE":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/raster/wms?/",
                                            layers="VC", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
    else:
        return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?/",
                                            layers="ILSWE", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
        



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True)

