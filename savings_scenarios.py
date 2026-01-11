import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Savings Scenarios",
    page_icon="📈",
    layout="wide"
)

st.title("Savings Scenarios")
st.write(
    "Demonstrating how saving behaviour and market variability "
    "impact long-term outcomes."
)

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
st.header("Inputs")

monthly = st.number_input(
    "Monthly contribution (R)",
    value=2000.0,
    step=100.0
)

annual_increase = st.number_input(
    "Annual increase in contribution (%)",
    value=5.0,
    step=0.5
)

years = st.number_input(
    "Years to invest",
    value=20,
    step=1
)

st.subheader("Return assumptions")

lower_return = st.slider(
    "Lower expected return (%)",
    min_value=5.0,
    max_value=9.0,
    value=6.0,
    step=0.5
)

higher_return = st.slider(
    "Higher expected return (%)",
    min_value=9.0,
    max_value=15.0,
    v
