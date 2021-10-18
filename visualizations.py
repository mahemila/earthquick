import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import geopandas as gpd

pre= os.path.dirname(os.path.realpath(__file__))
fname = 'all_month.csv'
path = os.path.join(pre, fname)

df = pd.read_csv(path)

def h_diagram(mag_list):
    geo_df = df[df['mag'] >= mag_list]
    geo_df['Clock'] = pd.DatetimeIndex(geo_df['time']).hour

    geo_df = geo_df.sort_values('Clock', ascending=True)

    fig = px.scatter_geo(geo_df,
                         lat=geo_df['latitude'],
                         lon=geo_df['longitude'],
                         hover_name="place",
                        #animation_frame='Clock',
                         color = 'mag'
    )
    #fig.update_traces(marker={'size':5})
    return fig

def lands_vis(l1, l2):
    dff = df[df['place'].str.contains(l1)]
    dff_1 = df[df['place'].str.contains(l2)]
    mean_1 = dff['depth'].mean()
    mean_2 = dff_1['depth'].mean()

    #fig = px.bar(x=[mean_1, mean_2], y=[l1, l2], orientation='h',
     #            labels={'x':'Mean Depth', 'y':'Region'})
    fig = go.Figure([go.Bar(y=[mean_1, mean_2], x=[l1, l2])])
    fig.update_xaxes(side="top", title_text = 'Region')
    fig.update_yaxes(autorange='reversed',title_text = 'Mean Depth' )
    return fig

def mag_type_error():
    df_magType = df[['magType', 'magError']]
    df_magType['num'] = [1 for i in range(len(df_magType))]

    df_magType_1 = df_magType.dropna().groupby('magType').sum().reset_index()
    df_magType_1['Mean Error'] = df_magType_1['magError'] / df_magType_1['num']

    fig = px.bar(df_magType_1, x='magType', y='Mean Error')

    return fig

def mag_rms():
    fig = px.scatter(df, x='mag', y='rms', trendline="ols", trendline_color_override="black")
    return fig