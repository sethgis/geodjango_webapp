from logging import PlaceHolder
import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import dash_leaflet as dl
from dash import Input, Output
from numpy import true_divide
from sympy import false, true
import pandas as pd
import matplotlib.pyplot as plt
import plotly 
import plotly.express as px
import seaborn as sns
import plotly.graph_objs as go


# ee.Initialize()
# PANDAS DATAFRAME

ILSWE = [['Very High',7665],['High',10912],['Moderate',8389],['Low',8722],['Very Low',17336]]
ilswe_df = pd.DataFrame(ILSWE, columns = ['Class', 'Area SQKM'])
CE = [['Very High',10475],['High',10629],['Moderate',10622],['Low',10829],['Very Low',10616]]
ce_df = pd.DataFrame(CE, columns = ['Class', 'Area SQKM'])
EF = [['Very High',10718],['High',10526],['Moderate',10867],['Low',10528],['Very Low',10397]]
ef_df = pd.DataFrame(EF, columns = ['Class', 'Area SQKM'])
SC = [['Very High',7665],['High',10912],['Moderate',8389],['Low',8722],['Very Low',17336]]
sc_df = pd.DataFrame(SC, columns = ['Class', 'Area SQKM'])
VC = [['Very High',10514],['High',10548],['Moderate',10894],['Low',10560],['Very Low',10594]]
vc_df = pd.DataFrame(VC, columns = ['Class', 'Area SQKM'])
SR = [['Very High',0],['High',30980],['Moderate',6244],['Low',15715],['Very Low',277]]
sr_df = pd.DataFrame(SR, columns = ['Class', 'Area SQKM'])


# fig = px.bar(ilswe_df, x='Class', y='Area SQKM')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

basemap = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'})


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


# url = 'https://services.nationalmap.gov/arcgis/services/USGSNAIPImagery/ImageServer/WMSServer?'
# Map.add_wms_layer(url=url, layers='0', name='NAIP Imagery', format='image/png')
# dl.WMSTileLayer(url = "https://services.nationalmap.gov/arcgis/services/USGSNAIPImagery/ImageServer/WMSServer?",
#             layers="NLCD_Canopy",format="imgae/png",transparent=true,),

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

# layers: "ldms:KEN_ADM10",
#             "layer-type": "overlay",
#             CQL_FILTER: "shapename = "+"'"+county+"'",
#             format: "image/png",
#             transparent: "true",
#             opacity: 1,


#####SIDEBAR BOOTSTRAP

SIDEBAR_STYLE = {

    "position": "absolute",
    "top": 650,
    "left": 20,
    "bottom":50,
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
            ],
            multi=False,
            id="dropdown",
            
            
        ),
   html.Div(id='out'),
    ],
    style=SIDEBAR_STYLE,
)

sidebar2 = html.Div(
      fig.show(),
        # dcc.Graph (figure = {'data': }),
    style=SIDEBAR_STYLE2,
)
# sidebar3 = html.Div(
#     fig = go.Figure(data=[go.Scatter(x=[1,2,3], y=[4,1,2])])
#     dcc.Graph(figure=fig),],
#     # html.Div(id='output')
# ], style = SIDEBAR_STYLE2]))




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
# map,
base,

sidebar,
# sidebar2,
],)



@app.callback(
    Output('base','children'),
    Input('dropdown', 'value'))
def update_value(value):
    if value=="CE":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
     
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                              activeColor="#214097", completedColor="#972158"), 
                              
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?/",
                                            layers="CE", format="image/png", transparent=True)],
           center=[0.0236, 37.9062], zoom=4,
           style= SIDEBAR_STYLE2,
           ), 
    ), 
    elif value=="EF":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?/",
                                            layers="EF", format="image/png", transparent=True)],
        center=[0.0236, 37.9062], zoom=4,
        style= SIDEBAR_STYLE2,
    ),)
    elif value=="SC":
     return html.Div(dl.Map([dl.TileLayer(),dl.LocateControl(options={'locateOptions': {'enableHighAccuracy': True}}), 
    
     dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                            activeColor="#214097", completedColor="#972158"),
                            
     dl.WMSTileLayer(url="http://45.76.249.64:8085/geoserver/ADS/wms?/",
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
    app.run_server(debug=True)