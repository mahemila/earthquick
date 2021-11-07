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

mag_list = set(int(i) for i in sorted(df['mag'].dropna().unique()))
dd_mag = [{'label':str(int(i)), 'value':int(i)} for i in mag_list if i>=0]
lands = list(set([i.split(', ')[0] if len(i.split(', '))==1 else i.split(', ')[1] for i in df['place']]))
dd_land = [{'label':i, 'value':i} for i in sorted(lands)]
#slider = {i:str(i*10) for i in range(0,11)}
slider = {i:str(i) for i in mag_list}
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ]
                )

app.layout = html.Div([
        html.Div(
            html.P('Earthquick - BOMBOM', style={'color':'white', 'padding-left':'100px', 'padding-top':'2vh'}),
            style={'height':'5vh', 'background-color':'black', 'margin-lef':'30%'}),
        html.Br(),

        #dbc.Row([
         #   dbc.Col([
          #      'Choose Continent',
           #     dbc.Select(
            #        options=dd_mag,
             #       value=min([x['value'] for x in dd_mag])
              #  )
        #    ],width={"size": 2, "offset": 4}),
         #   dbc.Col(['Choose time frame',
         #       dcc.RangeSlider(
          #          min=min(slider.keys()),
           #         max=max(slider.keys()),
            #        marks=slider,
             #       value=[min(slider.keys()), max(slider.keys())]
              #  )
            #], width={"size": 4}),
        #]),


        dbc.Row([
#col1
            dbc.Col([

                dbc.Row(
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
                        dbc.Row(
                            dbc.Col(dcc.Graph(id='land_depth'),width={"size": 12}))
                    ]),
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='mag_hour'), width={"size": 12})
                ),

            ],width={"size": 3}) ,
#col2
            dbc.Col([
                #html.Br(),
                #html.Div(style={'height':'10vh'}),
                dbc.Row([
                    #[dbc.Col([
                     #   'Magnitude ab',
                      #      dbc.Select(
                       #         id='mag_num',
                        #        options=dd_mag,
                         #       value=min([x['value'] for x in dd_mag])
                          #  )
                        #],width={"size": 3, 'offset':1}),

                        dbc.Col(['Magnitude',#'Time frame',
                            dcc.RangeSlider(
                                id='mag_num',
                                min=min([x['value'] for x in dd_mag]),#min(slider.keys()),
                                max=max([x['value'] for x in dd_mag]),#max(slider.keys()),
                                marks=slider,
                                value=[min([x['value'] for x in dd_mag]), max([x['value'] for x in dd_mag])]
                                #[min(slider.keys()), max(slider.keys())]
                            )
                        ], width={"size": 8, 'offset':1})]),
                html.Br(),
                dbc.Row(dbc.Col(
                    dcc.Graph(id='haupt_vis')
                       # figure=px.bar(x=[1,2,3], y=[10,20,30], height=900)
                    ,width={"size": 12}))
            ],width={"size": 6}),
            #dbc.Col(dcc.Graph(
             #   figure=px.bar(x=[1,2,3], y=[10,20,30], height=900)
            #),width={"size": 6}),

#col 3
            dbc.Col([
                html.Div(style={'height':'10vh'}),
                #html.Br(),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='mag_rms'), width={"size": 12})),
                dbc.Row(
                    dbc.Col(dcc.Graph(id='box_plot'), width={"size": 12})
                ),
            ])
        ]),

])

@app.callback(
    Output('haupt_vis', 'figure'),
    [Input('mag_num', 'value')]
)
def get_mag(mag_list):
    return vis.h_diagram(mag_list)

@app.callback(
    Output('mag_hour', 'figure'),
    [Input('mag_num', 'value')]
)
def get_box_plot(mag_list):
    return vis.hours_mags(mag_list)

@app.callback(
    Output('land_depth', 'figure'),
    [Input('land1', 'value'),
     Input('land2', 'value'),
     Input('mag_num', 'value')]
)
def get_lands(l1,l2,mag_list):
    if l1=='':
        l1==sorted(lands)[0]
    if l2=='':
        l1 == sorted(lands)[1]
    return vis.lands_vis(l1,l2, mag_list)

@app.callback(
    Output('mag_rms', 'figure'),
    [Input('mag_num', 'value')]
)
def get_box_plot(mag_list):
    return vis.mag_rms(mag_list)

@app.callback(
    Output('box_plot', 'figure'),
    [Input('mag_num', 'value')]
)
def get_box_plot(mag_list):
    return vis.box_month_gab(mag_list)

if __name__ == '__main__':
    app.run_server(debug=True)