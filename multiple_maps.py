from PIL import Image
import dash
from dash import Input, Output, State, dcc, html
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from colorcet import rainbow4, CET_D8, CET_CBTL2, CET_L19, CET_CBL4, CET_CBL1

df = pd.read_csv(r"https://raw.githubusercontent.com/FranciscoGBianco/Reconquista_Map/main/data/sitios.csv")

CET_CBTL2.reverse()

im_T = Image.open(r"images/T .tif")
im_pH = Image.open(r"images/pH.tif")
im_EC = Image.open(r"images/EC.tif")
im_TDS = Image.open(r"images/TD.tif")
im_OD = Image.open(r"images/OD.tif")

mapbox_layer_T = [{'below': 'traces', 'sourcetype': 'image', 'source': im_T, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_pH = [{'below': 'traces', 'sourcetype': 'image', 'source': im_pH, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_EC = [{'below': 'traces', 'sourcetype': 'image', 'source': im_EC, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_TDS = [{'below': 'traces', 'sourcetype': 'image', 'source': im_TDS, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_OD = [{'below': 'traces', 'sourcetype': 'image', 'source': im_OD, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]

# Create the Dash app
# app = dash.Dash(__name__)
app = dash.Dash(
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0'}]
                )

# Create the server
server = app.server

token = "pk.eyJ1IjoicGFjb2diIiwiYSI6ImNsZjhoNGRiejBiY3Mzb212Nzltc25wMngifQ.RgGO-dUtLQc7yOpz2lvZDQ"

map_figure = go.Figure(go.Scattermapbox())
map_figure.update_layout(
  margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
  mapbox_accesstoken=token,
  mapbox_style="light",
  mapbox_zoom=10,
  modebar={'add': "togglehover"},
  showlegend=False,
  autosize=True,
  mapbox_center=go.layout.mapbox.Center(lat=-34.568168, lon=-58.654091)
)
cbar = go.Scattermapbox(
            lat=[-34.568168],
            lon=[-58.654091],
            mode='markers',
            hoverinfo='none',
            marker=dict(
                size=0,
                showscale=True,
                colorscale=rainbow4,
                colorbar={'title':'OD (%)','orientation':'h', 'bgcolor': 'rgba(255,255,255,0.5)', 'bordercolor':'rgba(0,0,0,0)', 'len':0.6, 'lenmode':'fraction','x':0.5, 'y':0.01},
                cmin=0,
                cmax=100
            )
)

for i in range(len(df['lat'])):
    label = f"Sitio: {df['sitio'][i]}"
    map_figure.add_trace(go.Scattermapbox(
        mode="markers+text",
        lon=[df['long'][i]],
        lat=[df['lat'][i]],
        marker=dict(size=10,
                    symbol="marker",
                    allowoverlap=True,
                    ),
        text=df['Nombre'][i],
        name="",
        textposition="bottom right",
        hoverlabel={'bgcolor':'dimgray'},
        hovertemplate=label,
    )
    )
  
# Define the layout
app.layout = html.Div([
    dcc.Dropdown(id='parametro',
        # options=['pH', 'Oxígeno Disuelto', 'Conductividad', 'Solidos Disueltos Totales', 'Temperatura']
        options=[
            {'label': 'pH', 'value': 'pH'},
            {'label': 'Oxígeno Disuelto', 'value': 'OD'},
            {'label': 'Conductividad', 'value': 'EC'},
            {'label': 'Solidos Disueltos Totales', 'value': 'TDS'},
            {'label': 'Temperatura', 'value': 'T'}
        ],
        style={'height':"5vh"}
    ),
    dcc.Graph(
        id='mapa',
        figure=map_figure,
        style={"height": "92.5vh"},
    ),
])


@app.callback(Output('mapa', "figure"),
              Input('parametro', 'value'), suppress_callback_exceptions=True)
def update_param(param):
    params = {'pH': mapbox_layer_pH, 'OD': mapbox_layer_OD, 'EC': mapbox_layer_EC, 'TDS': mapbox_layer_TDS, 'T': mapbox_layer_T, None: []}
    units = {'pH': 'UpH', 'OD': '%', 'EC': 'µS/cm', 'TDS': 'mg/L', 'T': '°C', None: ''}
    limits_down = {'pH': 0, 'OD': 0, 'EC': 0, 'TDS': 0, 'T': 10, None: 0}
    limits_up = {'pH': 14, 'OD': 100, 'EC': 3000, 'TDS': 2000, 'T': 40, None: 0}
    cbars = {'pH': rainbow4, 'OD': CET_CBL4, 'EC': rainbow4, 'TDS': CET_CBL1, 'T': CET_CBTL2, None: rainbow4}
    fig = go.Figure(go.Scattermapbox())
    fig.update_layout(
        margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
        mapbox_accesstoken=token,
        mapbox_style="light",
        mapbox_zoom=10,
        mapbox_layers=params[param],
        modebar={'add': "togglehover"},
        showlegend=False,
        autosize=True,
        mapbox_center=go.layout.mapbox.Center(lat=-34.568168, lon=-58.654091)
    )

    cbar = go.Scattermapbox(
        lat=[-34.568168],
        lon=[-58.654091],
        mode='markers',
        hoverinfo='none',
        marker=dict(
            size=0,
            showscale=True,
            colorscale=cbars[param],
            colorbar={'title': f'{param} ({units[param]})', 'orientation': 'h', 'bgcolor': 'rgba(255,255,255,0.5)',
                      'bordercolor': 'rgba(0,0,0,0)', 'len': 0.6, 'lenmode': 'fraction', 'x': 0.5, 'y': 0.01},
            cmin=limits_down[param],
            cmax=limits_up[param]
        )
    )
  
    if param is not None:
        fig.add_trace(cbar)

    for i in range(len(df['lat'])):
        try:
            label = f"Sitio {df['sitio'][i]}, {param}: {df[param][i]} {units[param]}"
        except KeyError:
            label = f"Sitio {df['sitio'][i]}"
        fig.add_trace(go.Scattermapbox(
            mode="markers+text+lines",
            lon=[df['long'][i]],
            lat=[df['lat'][i]],
            marker=dict(size=10,
                        symbol="marker",
                        allowoverlap=True,
                        ),
            text=df['Nombre'][i],
            name="",
            textposition="bottom right",
            hoverlabel={'bgcolor': 'dimgray'},
            hovertemplate=label,
        )
        )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
    
