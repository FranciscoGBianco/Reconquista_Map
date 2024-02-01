from PIL import Image
import dash
from dash import Input, Output, State, dcc, html
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
from colorcet import rainbow4, CET_D8, CET_CBTL2, CET_L19, CET_CBL4, CET_CBL1
from Mapa_reconquista.rastim import process_raster, get_mapbox_layer
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

df = pd.read_csv(r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Reconquista\Puntos\sitios.csv")

# Usage example
# raster_file_T = r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Pythonproject\outputs\FinalT.tif"
# raster_file_pH = r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Pythonproject\outputs\FinalpH.tif"
# raster_file_EC = r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Pythonproject\outputs\FinalEC.tif"
# raster_file_TDS = r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Pythonproject\outputs\FinalTDS.tif"
# raster_file_OD = r"C:\Users\paco_\OneDrive\Escritorio\SIG 2023\Pythonproject\outputs\FinalOD.tif"
# df_processed_T = process_raster(raster_file_T, "T (°C)")
# df_processed_pH = process_raster(raster_file_pH, "pH (UpH)")
# df_processed_EC = process_raster(raster_file_EC, "EC (µS/cm)")
# df_processed_TDS = process_raster(raster_file_TDS, "TDS (mg/L)")
# df_processed_OD = process_raster(raster_file_OD, "OD (%)")
# # df_processed_OD.head().to_excel('df_processed_OD.xlsx')
#
CET_CBTL2.reverse()
# # Usage example
# mapbox_layer_T = get_mapbox_layer(df_processed_T, cmap_col=CET_CBTL2, name="T (°C)", span_range=[10, 40], save=True)
# mapbox_layer_pH = get_mapbox_layer(df_processed_pH, cmap_col=rainbow4, name="pH (UpH)", span_range=[0, 14], save=True)
# mapbox_layer_EC = get_mapbox_layer(df_processed_EC, cmap_col=rainbow4, name="EC (µS/cm)", span_range=[0, 3000], save=True)
# mapbox_layer_TDS = get_mapbox_layer(df_processed_TDS, cmap_col=CET_CBL1, name="TDS (mg/L)", span_range=[0, 2000], save=True)
# mapbox_layer_OD = get_mapbox_layer(df_processed_OD, cmap_col=CET_CBL4, name="OD (%)", span_range=[0, 100], save=True)
# layers = [mapbox_layer_pH, mapbox_layer_OD, mapbox_layer_EC, mapbox_layer_TDS, mapbox_layer_T]
# print(mapbox_layer_OD)

im_T = Image.open(r"C:\Users\paco_\OneDrive\Escritorio\Reconquista dashboard\T .tif")
im_pH = Image.open(r"C:\Users\paco_\OneDrive\Escritorio\Reconquista dashboard\pH.tif")
im_EC = Image.open(r"C:\Users\paco_\OneDrive\Escritorio\Reconquista dashboard\EC.tif")
im_TDS = Image.open(r"C:\Users\paco_\OneDrive\Escritorio\Reconquista dashboard\TD.tif")
im_OD = Image.open(r"C:\Users\paco_\OneDrive\Escritorio\Reconquista dashboard\OD.tif")

mapbox_layer_T = [{'below': 'traces', 'sourcetype': 'image', 'source': im_T, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_pH = [{'below': 'traces', 'sourcetype': 'image', 'source': im_pH, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_EC = [{'below': 'traces', 'sourcetype': 'image', 'source': im_EC, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_TDS = [{'below': 'traces', 'sourcetype': 'image', 'source': im_TDS, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
mapbox_layer_OD = [{'below': 'traces', 'sourcetype': 'image', 'source': im_OD, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]
# [{'below': 'traces', 'sourcetype': 'image', 'source': <PIL.Image.Image image mode=RGBA size=3200x2000 at 0x1F281CF88E0>, 'coordinates': [[-58.89950688274488, -34.38955324120631], [-58.57809083223908, -34.38955324120631], [-58.57809083223908, -34.70780133291272], [-58.89950688274488, -34.70780133291272]], 'opacity': 0.85}]

# Create the Dash app
# app = dash.Dash(__name__)
app = dash.Dash(
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0'}]
                )
# load_figure_template('SOLAR')

token = "pk.eyJ1IjoicGFjb2diIiwiYSI6ImNsZjhoNGRiejBiY3Mzb212Nzltc25wMngifQ.RgGO-dUtLQc7yOpz2lvZDQ"

map_figure = go.Figure(go.Scattermapbox())
map_figure.update_layout(
  margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
  mapbox_accesstoken=token,
  mapbox_style="light",
  mapbox_zoom=10,
  # mapbox_layers=mapbox_layer_OD,
  modebar={'add': "togglehover"},
  showlegend=False,
  autosize=True,
  # showscale=True,
  mapbox_center=go.layout.mapbox.Center(lat=-34.568168, lon=-58.654091)
  # taken from previous step
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
                # colorbar={'title':'T (°C)', 'bgcolor': 'rgba(255,255,255,0.5)', 'bordercolor':'rgba(0,0,0,0)', 'len':0.6, 'lenmode':'fraction','x':0.95, 'y':0.6},
                colorbar={'title':'OD (%)','orientation':'h', 'bgcolor': 'rgba(255,255,255,0.5)', 'bordercolor':'rgba(0,0,0,0)', 'len':0.6, 'lenmode':'fraction','x':0.5, 'y':0.01},
                cmin=0,
                cmax=100
            )
)
# map_figure.add_trace(cbar)

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
        # mapbox_style='carto-positron'
    )
    )
# Define the layout
app.layout = html.Div([
    # html.P('Ultima actualización: 17/12'),
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
        style={"height": "95vh"},
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
        # showscale=True,
        mapbox_center=go.layout.mapbox.Center(lat=-34.568168, lon=-58.654091)
        # taken from previous step
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
            # colorbar={'title':'T (°C)', 'bgcolor': 'rgba(255,255,255,0.5)', 'bordercolor':'rgba(0,0,0,0)', 'len':0.6, 'lenmode':'fraction','x':0.95, 'y':0.6},
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
            # mapbox_style='carto-positron'
        )
        )

    # fig.write_html(f'{param}.html')
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
    
