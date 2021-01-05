import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

earthquak = pd.read_csv(DATA_PATH.joinpath('database.csv'))

earthquak['Date'] = pd.to_datetime(earthquak['Date'])
earthquak['Date'] = earthquak['Date'].values.astype('datetime64')
earthquak['Year'] = pd.to_datetime(earthquak['Date']).dt.strftime('%Y')
earthquak['Year'] = earthquak['Year'].astype(int)

layout = html.Div([

html.Div([
        html.Div([


            html.P('All Countries: Covid - 19 data 2020-01-22 to 2020-12-25', className = 'fix_label', style = {'color': 'black', 'margin-top': '2px'}),
            html.P('Select Year:', className='fix_label',  style={'color': 'black', 'margin-top': '2px'}),
            dcc.RangeSlider(id='select_years1',
                            min=1965,
                            max=2016,
                            dots=True,
                            value=[2010, 2016],
                            marks={str(yr): str(yr) for yr in range(1965, 2016, 10)},
                            className = 'dcc_compon'),

            ], className = "create_container2 four columns", style = {'margin-bottom': '20px', "margin-top": "20px"}),

    ], className = "row flex-display"),

            html.Div([
                html.Div([

                    dcc.Graph(id = 'map_3',
                              config = {'displayModeBar': 'hover'}),

                ], className = "create_container2 nine columns", style = {'height': '580px'}),

            ], className = "row flex-display"),




], id="mainContainer", style={"display": "flex", "flex-direction": "column"})


@app.callback(Output('map_3', 'figure'),
              [Input('select_years1', 'value')])
def update_graph(select_years1):
    earthquak1 = earthquak.groupby(['Year', 'Time', 'Date', 'Latitude', 'Longitude'])['Magnitude'].sum().reset_index()
    earthquak2 = earthquak1[(earthquak1['Year'] >= select_years1[0]) & (earthquak1['Year'] <= select_years1[1])]



    return {
            'data': [go.Densitymapbox(
                lon = earthquak2['Longitude'],
                lat = earthquak2['Latitude'],
                z = earthquak2['Magnitude'],
                radius = 10,
                colorscale = 'HSV',
                showscale = False,

                # hoverinfo = 'text',
                # hovertext =
                # '<b>Year</b>: ' + earthquak2['Year'].astype(str) + '<br>' +
                # '<b>Time</b>: ' + earthquak2['Time'].astype(str) + '<br>' +
                # '<b>Date</b>: ' + earthquak2['Date'].astype(str) + '<br>'
                # '<b>Lat</b>: ' + [f'{x:.4f}' for x in earthquak2['Latitude']] + '<br>' +
                # '<b>Long</b>: ' + [f'{x:.4f}' for x in earthquak2['Longitude']] + '<br>' +
                # '<b>Magnitude</b>: ' + [f'{x:,.0f}' for x in earthquak2['Magnitude']] + '<br>'

            )],

            'layout': go.Layout(
                height = 550,
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                hovermode='closest',
                mapbox=dict(
                  accesstoken = 'pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',  # Create free account on Mapbox site and paste here access token
                  center=go.layout.mapbox.Center(lat=36, lon=-5.4),
                  # style='stamen-terrain',
                  style = 'open-street-map',
                  # style='dark',
                  zoom=1.2
                       ),
                autosize=True,

             )

       }
