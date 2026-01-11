import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------
# PAGE SETUP
# ------------------
st.set_page_config(
    page_title="Savings Scenarios",
    page_icon="📈",
    layout="wide"
)

st.title("Savings Scenarios")
st.write(
    "This illustration shows how saving behaviour matters "
    "even when investment returns fluctuate."
)

# ------------------
# INPUTS
# ------------------
st.header("Inputs")

monthly = st.number_input(
    "Monthly contribution (R)",
    2000.0,
    step=100.0
)

annual_increase = st.number_input(
    "Annual increase in contribution (%)",
    5.0,
    step=0.5
)

years = st.number_input(
    "Years to invest",
    20,
    step=1
)

st.subheader("Return assumptions")

lower_return = st.slider(
    "Lower expected return (%)",
    5.0, 9.0, 6.0, 0.5
)

higher_return = st.slider(
    "Higher expected return (%)",
    9.0, 15.0, 11.0, 0.5
)

show_extra = st.checkbox(
    "Show impact of saving R500 more per month"
)

EXTRA = 500

# ------------------
# CALCULATION
# ------------------
def grow(monthly, annual_inc, rate, years):
    bal = 0.0
    contrib = monthly
    out = []

    for m in range(1, years * 12 + 1):
        if m % 12 == 1 and m > 1:
            contrib *= (1 + annual_inc / 100)

        bal = bal * (1 + rate / 100 / 12) + contrib
        out.append(bal)

    return out

# ------------------
# BUILD DATA
# ------------------
rows = []

base_low = grow(monthly, annual_increase, lower_return, years)
base_high = grow(monthly, annual_increase, higher_return, years)

for i, b in enumerate(base_low):
    rows.append({
        "Year": (i + 1) / 12,
        "Balance": b,
        "Scenario": "Current saving – lower return"
    })

for i, b in enumerate(base_high):
    rows.append({
        "Year": (i + 1) / 12,
        "Balance": b,
        "Sc
