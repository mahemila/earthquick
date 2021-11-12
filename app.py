import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
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

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    #top Bar
        html.Div(
            html.P('Earthquick - BOMBOM', style={'color':'white', 'padding-left':'100px', 'padding-top':'2vh'}),
            style={'height':'5vh', 'background-color':'black', 'margin-lef':'30%'}),
        html.Br(),

    #Slider => controls all diagramms
        dbc.Row(
                dbc.Col(['Magnitude',
                        dcc.RangeSlider(
                            id='mag_num',
                            min=min([x['value'] for x in dd_mag]),
                            max=max([x['value'] for x in dd_mag]),
                            marks=slider,
                            value=[min([x['value'] for x in dd_mag]), max([x['value'] for x in dd_mag])]
                        )
                    ], width={"size": 4, 'offset':4}),
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
                                value=[sorted(lands)[0],sorted(lands)[1]],
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
                    ,width={"size": 12}))
            ],width={"size": 6}),

#Third column
            dbc.Col([
                html.Div(style={'height':'10vh'}),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='mag_rms'), width={"size": 12})),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='box_plot'), width={"size": 12})
                ),
            ])
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
def get_lands(lands, mag_list):
    return vis.lands_vis(lands, mag_list)

#=============
#End Callbacks
#=============

if __name__ == '__main__':
    app.run_server(debug=True)