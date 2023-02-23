import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# @st.cache(allow_output_mutation=True)
def load_data(file_path: str):
    df = pd.read_csv(file_path)
    return df

def get_timestamp(df: pd.DataFrame, col: str):
    df["date_day"] = (df[col].str.split(" ")).str[0]
    df["Time_day"] = (df[col].str.split(" ")).str[1]
    return df

# cleaning the dates
def extract_dates(df: pd.DataFrame, col: str):
    df["day"] = pd.to_datetime(df[col]).dt.dayofweek
    df["month"] = pd.to_datetime(df[col]).dt.month
    df["year"] = pd.to_datetime(df[col]).dt.year
    return df

# drop columns DateTime, date_day and year: DateTime is no longer needed and the data is for only 2017
def drop_uneeded(df: pd.DataFrame, cols: list):
    df.drop(cols, axis=1, inplace=True)
    return df

feature_cols = ['Temperature', 'Humidity', 'Wind Speed', 'general diffuse flows', 'diffuse flows', 'month']
zone_cols = ['Zone1', 'Zone2', 'Zone3']

def investigate_zones(data: pd.DataFrame ,feature: str, kind: str = "line"):
    c_palette = ['#2acf2a', '#ff0000', '#2626c7']
    data = data[zone_cols + [feature]].groupby(feature, as_index=False).mean().reset_index()
    # make the data logaritmic and temperature the index
    data = np.log(data)
    # data.set_index(feature, inplace=True)

    if kind == "line":
        # use plotly to plot the data
        # fig = st.line_chart(data, use_container_width=True)
        fig = go.Figure()
    # # add trace for each zone
        for zone in zone_cols:
            fig.add_trace(go.Scatter(x=data[feature], y=data[zone], mode='lines', name=zone, line=dict(color=c_palette.pop())))
        fig.update_layout(title=f"{feature} vs Power Consumption", xaxis_title=feature, yaxis_title="Power Consumption")

    if kind == 'density':
        fig = go.Figure()
        for zone in zone_cols:
            fig.add_trace(go.Histogram(x=data[zone], name=zone))
        fig.update_layout(title=f"{feature} vs Power Consumption", xaxis_title=feature, yaxis_title="Power Consumption")

    fig.update_layout(width=1100, height=650)
    return fig