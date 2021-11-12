import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
import geopandas as gpd

pre= os.path.dirname(os.path.realpath(__file__))
fname = 'all_month.csv'
path = os.path.join(pre, fname)

df = pd.read_csv(path)

def h_diagram(f_df):
    geo_df = f_df
    geo_df = geo_df.sort_values('Clock', ascending=True)
    fig = px.scatter_geo(geo_df,lat=geo_df['latitude'],lon=geo_df['longitude'],
                         hover_name="place",color = 'mag',width=1000, height=600)
    return fig

def hours_mags(f_df):
    df_mag_hours = f_df
    df_droped = df_mag_hours.dropna()
    df_x_grouped = df_droped.groupby('Clock').sum().reset_index()
    df_x_grouped['mean'] = round(df_x_grouped.mag / df_x_grouped.ones, 2)

    fig = px.line(df_x_grouped, x='Clock', y='mean', labels={'mean':'Mean Magnitude'})
    return fig


def lands_vis(regions, mag_list):
    dff_a = df[(df['mag'] >= int(mag_list[0])) & (df['mag'] <= int(mag_list[1]))]
    y_v = []
    for region in regions:
        dff = dff_a[dff_a['place'].str.contains(region)]
        mean = dff['depth'].mean()
        y_v.append(mean)
    fig = go.Figure([go.Bar(y=y_v, x=regions)])
    fig.update_xaxes(side="top", title_text = 'Region')
    fig.update_yaxes(autorange='reversed',title_text = 'Mean Depth' )
    return fig

def mag_rms(f_df):
    df_mag_rms=f_df
    fig = px.scatter(df_mag_rms, x='mag', y='rms', trendline="ols", trendline_color_override="red",
                     labels={'mag':'Magnitude', 'rms':'Duration/rms'})
    return fig

def box_month_gab(f_df):
    df_month_gap=f_df
    #df_month_gap['Month'] = pd.DatetimeIndex(df_month_gap['time']).month
    fig = px.box(df_month_gap, x='Month', y='gap', labels = {'Month':'Month in Year 2021'})
    return fig

