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

def h_diagram(mag_list):
    geo_df = df[(df['mag'] >= int(mag_list[0])) &  (df['mag'] <= int(mag_list[1]))]
    geo_df['Clock'] = pd.DatetimeIndex(geo_df['time']).hour

    geo_df = geo_df.sort_values('Clock', ascending=True)

    fig = px.scatter_geo(geo_df,
                         lat=geo_df['latitude'],
                         lon=geo_df['longitude'],
                         hover_name="place",
                        #animation_frame='Clock',
                         color = 'mag',
                         width=1000, height=600
    )
    #fig.update_traces(marker={'size':5})
    return fig

def hours_mags(mag_list):
    df_mag_hours = df.copy()
    df_mag_hours = df_mag_hours[(df_mag_hours['mag'] >= int(mag_list[0])) & (df['mag'] <= int(mag_list[1]))]
    df_mag_hours['Clock'] = pd.DatetimeIndex(df_mag_hours['time']).hour
    df_droped = df_mag_hours.dropna()
    df_droped['mag_int'] = df_droped['mag']#.astype(int)
    df_x = df_droped[['Clock', 'mag_int']]
    df_x['ones'] = np.ones(len(df_x))
    df_x_grouped = df_x.groupby('Clock').sum().reset_index()
    df_x_grouped['mean'] = round(df_x_grouped.mag_int / df_x_grouped.ones, 2)

    fig = px.line(df_x_grouped, x='Clock', y='mean', labels={'mean':'Mean Magnitude'})
    """
    fig = go.Figure(go.Scatter(
        x=df_x_grouped['Clock'], y=df_x_grouped['mean'], text=df_x_grouped['mean'],
        mode='markers+lines+text',
        textposition='middle center',
        textfont=dict(color='black'),
        line=dict(color='blue'),
        marker=dict(symbol='circle', size=30, color='white',
                    line=dict(width=1))))
    """
    return fig



def lands_vis(l1, l2, mag_list):
    dff_a = df.copy()
    dff_a = dff_a[(dff_a['mag'] >= int(mag_list[0])) & (dff_a['mag'] <= int(mag_list[1]))]
    dff = dff_a[dff_a['place'].str.contains(l1)]
    dff_1 = dff_a[dff_a['place'].str.contains(l2)]
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

def mag_rms(mag_list):
    df_mag_rms = df.copy()
    df_mag_rms = df_mag_rms[(df_mag_rms['mag'] >= int(mag_list[0])) & (df['mag'] <= int(mag_list[1]))]
    fig = px.scatter(df_mag_rms, x='mag', y='rms', trendline="ols", trendline_color_override="red")
    return fig
def box_month_gab(mag_list):
    df_month_gap = df.copy()
    df_month_gap = df_month_gap[(df_month_gap['mag'] >= int(mag_list[0])) & (df['mag'] <= int(mag_list[1]))]
    df_month_gap['Month'] = pd.DatetimeIndex(df_month_gap['time']).month
    fig = px.box(df_month_gap, x='Month', y='gap', labels = {'Month':'Month in Year 2021'})

    return fig

