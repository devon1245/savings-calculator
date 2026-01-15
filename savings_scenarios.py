import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Savings Scenarios")
st.write("This illustration shows how saving behaviour matters, even when returns fluctuate.")

# ------------------
# INPUTS
# ------------------
lump_sum = st.number_input("Current savings (R)", value=0.0, step=1000.0)
monthly = st.number_input("Monthly contribution (R)", value=2000.0, step=100.0)
annual_inc = st.number_input("Annual increase (%)", value=5.0, step=0.5)
years = st.number_input("Years to invest", value=20, step=1)

low_ret = st.slider("Lower expected return (%)", 5.0, 9.0, 6.0, 0.5)
high_ret = st.slider("Higher expected return (%)", 9.0, 15.0, 11.0, 0.5)

extra = st.checkbox("Show impact of saving R500 mo
