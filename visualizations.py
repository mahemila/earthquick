import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import numpy as np
#import geopandas as gpd

pre= os.path.dirname(os.path.realpath(__file__))
fname = 'all_month.csv'
path = os.path.join(pre, fname)

df = pd.read_csv(path)


def h_diagram(geo_df):
    geo_df = geo_df.sort_values('Clock', ascending=True)
    fig = px.scatter_geo(geo_df,lat=geo_df['latitude'],lon=geo_df['longitude'],
                         hover_name="place",color = 'mag',width=800, height=600,
                         title='Erdbeben pro Magnitude Weltweit')
    return fig

def hours_mags(df_mag_hours):
    df_droped = df_mag_hours.dropna()
    df_x_grouped = df_droped.groupby('Clock').sum().reset_index()
    df_x_grouped['mean'] = round(df_x_grouped.mag / df_x_grouped.ones, 2)
    df_x_grouped.Clock = [str(h)+':00' for h in df_x_grouped.Clock]


    fig = px.line(df_x_grouped, x='Clock', y='mean', labels={'mean':'Durchschnittliche Magnitude', 'Clock':'Uhrzeit'}
                  ,title='Durchschnittliche Magnitude pro Uhrzeit')
    fig.update_layout(font=dict(size=12, family="Arial"))
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
    fig.update_yaxes(autorange='reversed',title_text = 'Durchschnittliche Tiefe in Kilometer' )
    fig.update_layout(title='Durchschnittliche Erdbeben pro Länder', font=dict(size=12, family="Arial"))
    return fig

def mag_rms(df_mag_rms):
    fig = px.scatter(df_mag_rms, x='mag', y='rms', trendline="ols", trendline_color_override="red",
                     labels={'mag':'Magnitude', 'rms':'Dauer/rms'},
                     title='Zusammenhang zwischen Erdbeben und Magnitude')
    fig.update_layout(font=dict(size=12, family="Arial"))#title_font_size=12, title_font_family="Arial")
    return fig

def box_month_gab(df_month_gap):
    mon = ['September' if x == 9 else 'October' for x in df_month_gap['Month']]
    fig = px.box(df_month_gap, x=mon, y='gap', labels = {'x':'Monat im Jahr 2021', 'y':'Gap'},
                 title='Boxplot zur Datenverteilung Gap/Monat')
    fig.update_layout(font=dict(size=12, family="Arial"))
    return fig

