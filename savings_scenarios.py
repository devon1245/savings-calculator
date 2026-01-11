import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------
# PAGE SETUP
# ------------------
st.set_page_config(layout="wide")
st.title("Savings Scenarios – Step A")

st.write("Step A: verifying calculations + checkbox + graph")

# ------------------
# INPUTS
# ------------------
monthly = st.number_input("Monthly contribution (R)", 2000.0, step=100.0)
annual_increase = st.number_input("Annual increase (%)", 5.0, step=0.5)
years = st.number_input("Years to invest", 20, step=1)

lower_return = st.slider("Lower expected return (%)", 5.0, 9.0, 6.0, 0.5)
higher_return = st.slider("Higher expected return (%)", 9.0, 15.0, 11.0, 0.5)

show_extra = st.checkbox("Show impact of saving R500 more per month")
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

# Always include base scenario
for rate, label in [
    (lower_return, "Current – lower return"),
    (higher_return, "Current – higher return")
]:
    balances = grow(monthly, annual_increase, rate, years)
    for i, b in enumerate(balances):
        rows.append({
            "Year": (i + 1) / 12,
            "Balance": b,
            "Scenario": label
        })

# Optional extra saving
if show_extra:
    for rate, label in [
        (lower_return, "+R500 – lower return"),
        (higher_return, "+R500 – higher return")
    ]:
        balances = grow(monthly + EXTRA, annual_increase, rate, years)
        for i, b in enumerate(balances):
            rows.append({
                "Year": (i + 1) / 12,
                "Balance": b,
                "Scenario": label
            })

df = pd.DataFrame(rows)

st.write("DEBUG rows:", len(df))

# ------------------
# GRAPH
# ------------------
fig = px.line(
    df,
    x="Year",
    y="Balance",
    color="Scenario"
)

st.plotly_chart(fig, use_container_width=True)
