import streamlit as st
import statsmodels.api as sm
from data_utils import *
st.set_page_config(page_title="Tetuan Power Consumption", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

data = load_data('Tetuan City power consumption.csv')
data = get_timestamp(data, "DateTime")
data = extract_dates(data, 'date_day')  # call methods
data = drop_uneeded(data, ['year', 'DateTime', 'date_day'])
data.rename(columns={"Zone 1 Power Consumption": "Zone1", "Zone 2  Power Consumption": "Zone2", "Zone 3  Power Consumption": "Zone3"}, inplace=True)

feature_cols = ['Temperature', 'Humidity', 'Wind Speed', 'general diffuse flows', 'diffuse flows']
zone_cols = ['Zone1', 'Zone2', 'Zone3']

mean_monthly_consumption = data[['month','Zone1', 'Zone2', 'Zone3']].groupby("month").mean()

mean_data = data.groupby("month").mean()
# mean_data.rename(columns={"Zone 1 Power Consumption": "Zone1", "Zone 2  Power Consumption": "Zone2", "Zone 3  Power Consumption": "Zone3"}, inplace=True)
model = sm.formula.ols('Zone3 ~ Temperature + Humidity + Temperature:Humidity', data = mean_data).fit()
# Extract our table
aov_table = sm.stats.anova_lm(model, typ=2)


# ********************************************************APP**********************************************************************************

st.title("""
    Tetuan Daily Power Consumption For The Year 2017
""")

# create 2 columns
col1, col2 = st.columns(2, gap='large')

# plot monthly consumption in column 1
with col1:
    st.subheader("Mean Monthly Power Consumption")
    st.line_chart(mean_monthly_consumption)

# add a space between the 2 columns
st.write("")

# explain the data in column 2
with col2:
    st.write("")
    st.header("Effect  Of Temperature and Humidity on Power Consumption in Zone 3")
    st.write(aov_table)
    st.write("""
        The p-value of the interaction variables is greater than 0.05, therefore, we can conclude that there is no interaction between the variables.
    """)

st.subheader("Monthly Power Consumption with environmental conditions")

# select the feature to investigate and the kind of plot
col1, col2 = st.columns([1, 3], gap='large')
with col1:
    st.write("")
    feature = st.selectbox("Select environ Feature", feature_cols)
    kind = st.selectbox("Select Plot Type", ["line", "density"])

with col2:
    st.write("")
    st.write(investigate_zones(data, feature, kind), use_container_width=True)


