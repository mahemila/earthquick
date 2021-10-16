import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os
import visualizations as vis

pre= os.path.dirname(os.path.realpath(__file__))
fname = 'all_month.csv'
path = os.path.join(pre, fname)
df = pd.read_csv(path)

dd_mag = [{'label':str(i), 'value':int(i)} for i in sorted(df['mag'].dropna().unique())]
lands = list(set([i.split(', ')[0] if len(i.split(', '))==1 else i.split(', ')[1] for i in df['place']]))
dd_land = [{'label':i, 'value':i} for i in sorted(lands)]
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
                )

app.layout = html.Div([
        html.Div(style={'height':'10vh'}),
        dbc.Row(
             dbc.Col([
                 dbc.Row([
                     dbc.Col(['Magnitude',
                              dcc.Dropdown(id='mag_num',
                              options=dd_mag,
                              value = min([x['value'] for x in dd_mag])
                              )],
                             width={"size": 3, "offset": 2}),
                     #html.Br,
                     dbc.Button('Alle Jahre anzeigen',n_clicks=0,style={'margin-left':'20px'} ),
                    dbc.Button('Anzeige Zurücksetzen',n_clicks=0 ,style={'margin-left':'20px'})]

                     )
                 ,
                 dcc.Graph(id='haupt_vis')],
                width={"size": 8, "offset": 2})
        ),

        html.Div(style={'height':'10vh'}),

        dbc.Container(
            dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col(['Land 1',
                            dcc.Dropdown(

                            id='land1',
                            options=dd_land,
                            value=sorted(lands)[0],
                        )], width={"size": 4, "offset": 2},),
                            dbc.Col(
                                ['Land 2',
                                dcc.Dropdown(
                                    id='land2',
                                    options=dd_land,
                                    value=sorted(lands)[1],
                                )], width=4)
                        ]
                    ),

                            dcc.Graph(id='land_depth')], width=10, lg=6),
                    dbc.Col([
                        html.Div(style={'height':'8vh'}),
                        dcc.Graph(
                            figure=vis.mag_type_error()
                        )], width=10,lg=6),
                        ]
                    ), {'width':10} #, style={'border-style': 'dotted','border-color':'red'}
        ),

        html.Div(style={'height':'10vh'}),
        dbc.Row([
                dbc.Col(dcc.Graph(
                        figure=vis.mag_rms()
                    ), width={"size": 5, "offset": 1}),


                dbc.Col([
                    dcc.Graph(
                        figure=px.scatter(x=[1,2,3], y=[10,20,30])
                    )], width={"size": 5}),
            ]
        ),
])

@app.callback(
    Output('haupt_vis', 'figure'),
    [Input('mag_num', 'value')]
)
def get_mag(mag_list):
    return vis.h_diagram(mag_list)

@app.callback(
    Output('land_depth', 'figure'),
    [Input('land1', 'value'),
     Input('land2', 'value')]
)
def get_lands(l1,l2):
    if l1=='':
        l1==sorted(lands)[0]
    if l2=='':
        l1 == sorted(lands)[1]
    return vis.lands_vis(l1,l2)

if __name__ == '__main__':
    app.run_server(debug=True)