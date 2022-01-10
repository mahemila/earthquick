import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os
import visualizations as vis

pre= os.path.dirname(os.path.realpath(__file__))
fname = 'all_month.csv'
path = os.path.join(pre, fname)
df = pd.read_csv(path)

#Add Columns
dff = df.copy()
dff['Clock']=pd.DatetimeIndex(dff['time']).hour
dff['Month'] = pd.DatetimeIndex(dff['time']).month
add_ones_column = dff.loc[:,'ones'] = 1


#prepare slider
mag_list = set(int(i) for i in sorted(df['mag'].dropna().unique()))
dd_mag = [{'label':str(int(i)), 'value':int(i)} for i in mag_list if i>=0]
slider = {i:str(i) for i in mag_list}

#prepare dropdown
lands = list(set([i.split(', ')[0] if len(i.split(', '))==1 else i.split(', ')[1] for i in df['place']]))
dd_land = [{'label':i, 'value':i} for i in sorted(lands)]
sorted_lands = sorted(lands)

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    #top Bar
        html.Div(
            html.P('Earthquick - BOMBOM', style={'color':'white', 'padding-left':'100px', 'padding-top':'2vh'}),
            style={'height':'5vh', 'background-color':'black', 'margin-lef':'30%'}),
        html.Br(),

    #Slider => controls all diagramms
        dbc.Row([
                dbc.Col(['Magnitude',
                        dcc.RangeSlider(
                            id='mag_num',
                            min=min([x['value'] for x in dd_mag]),
                            max=max([x['value'] for x in dd_mag]),
                            marks=slider,
                            value=[min([x['value'] for x in dd_mag]), max([x['value'] for x in dd_mag])]
                        )
                    ], width={"size": 4, 'offset':4}),
                dbc.Col(dbc.Button('Informations', outline=True, color="info", className="me-1",id='infoButton', n_clicks=0),
                        width={"size": 2, 'offset':2})
        ]),
    dbc.Modal([dbc.ModalHeader(html.H4('Willkommen auf dem Dashboard zur Visualisierung von Erdbebendaten')),
               dbc.ModalBody(html.Div([
                   html.P([dcc.Markdown('''
                   Auf diesem Dashboard werden Daten zu Erdbeben der USGS (https://earthquake.usgs.gov/) in verschiedenen 
                   Diagrammen visualisiert. Mithilfe einer Magnitude-Slide lassen sich die Daten in den Diagrammen 
                   einheitlich anpassen. Im Diagramm zur Visualisierung der durchschnittlichen Erdbebentiefe pro Land 
                   lassen sich zudem durch manuelle Anpassungen verschiedene Länder bezüglich ihrer durchschnittlichen 
                   Erdbebentiefe vergleichen. 
                   Wir hoffen sehr, mit diesem Dashboard einen interessanten Einblick in die Welt der Seismologie geben zu können.
                   ''')])

               ])),
            dbc.ModalFooter(
                            [html.P('Developed by I.Kilchenmann, S.Weber-Martin and M.Hemila 2021-2022',
                                    style={'margin-left':0, 'margin-right':'auto'}),
                                html.P(''),
                                dbc.Button(
                                "Close", id="close", className="ms-auto", n_clicks=0
                            )]
                        )

               ],
                id="modal",
                scrollable=True,
                is_open=False,
                size="lg"
),
    #=====================
    # START DIAGRAMMS
    # Structure:
        # 1 Row => 3 Columns
        # Col 1,3 => 2 Rows
        # Col 2 => 1 Row
    #=====================

        dbc.Row([
#First column
            dbc.Col([
                dbc.Row(
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(['Choose Regions',
                                dcc.Dropdown(
                                id='lands',
                                options=dd_land,
                                value=[sorted_lands[0],sorted_lands[1]],
                                multi=True
                                )], width={"size": 8, "offset": 2})
                        ]),
                        dbc.Row(
                            dbc.Col(dcc.Graph(id='land_depth',config={'displayModeBar': False}),width={"size": 12}))
                    ]),
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='mag_hour'), width={"size": 12})
                ),

            ],width={"size": 3}),

#Seconed column: Main diagramm
            dbc.Col([
                html.Div(style={'height':'12vh'}),
                dbc.Row(dbc.Col(
                    dcc.Graph(id='haupt_vis')
                    ,width={"size": 10}))
            ],width={"size": 5}),

#Third column
            dbc.Col([
                html.Div(style={'height':'10vh'}),
                dbc.Row([#'Zusammenhang zwischen Erdbeben und Magnitude',
                    dbc.Col(dcc.Graph(id='mag_rms'), width={"size": 12})]),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='box_plot'), width={"size": 12})
                ),
            ], width={"size": 3, "offset": 1})
        ]),

])
#========================================
# End of App-Layout / Start of Callbacks
#========================================

@app.callback(
    [Output('haupt_vis', 'figure'),
     Output('mag_hour', 'figure'),
     Output('mag_rms', 'figure'),
     Output('box_plot', 'figure')],
    [Input('mag_num', 'value')])
def get_figures(mag_list):
    ff_df = dff[(dff['mag'] >= int(mag_list[0])) &  (dff['mag'] <= int(mag_list[1]))]

    return vis.h_diagram(ff_df),\
           vis.hours_mags(ff_df),\
           vis.mag_rms(ff_df),\
           vis.box_month_gab(ff_df)


@app.callback(
    Output('land_depth', 'figure'),
    [Input('lands', 'value'),
     Input('mag_num', 'value')]
)
def get_lands(lands_dd, mag_list):
    return vis.lands_vis(lands_dd, mag_list)

@app.callback(
    Output("modal", "is_open"),
    [Input("infoButton", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_info(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


#=============
#End Callbacks
#=============

if __name__ == '__main__':
    app.run_server(debug=True)