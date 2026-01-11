import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Savings Scenarios")

# ------------------
# INPUTS
# ------------------
monthly = st.number_input("Monthly contribution", 2000.0, step=100.0)
annual_inc = st.number_input("Annual increase percent", 5.0, step=0.5)
years = st.number_input("Years to invest", 20, step=1)

low_ret = st.slider("Lower return percent", 5.0, 9.0, 6.0, 0.5)
high_ret = st.slider("Higher return percent", 9.0, 15.0, 11.0, 0.5)

extra = st.checkbox("Add R500 per month")
EXTRA = 500

# ------------------
# CALCULATION
# ------------------
def grow(m, inc, r, y):
    bal = 0.0
    c = m
    out = []
    for i in range(1, y * 12 + 1):
        if i % 12 == 1 and i > 1:
            c *= (1 + inc / 100)
        bal = bal * (1 + r / 100 / 12) + c
        out.append(bal)
    return out

# ------------------
# DATA
# ------------------
rows = []

base_low = grow(monthly, annual_inc, low_ret, years)
base_high = grow(monthly, annual_inc, high_ret, years)

for i, v in enumerate(base_low):
    rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Base low"})

for i, v in enumerate(base_high):
    rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Base high"})

if extra:
    ext_low = grow(monthly + EXTRA, annual_inc, low_ret, years)
    ext_high = grow(monthly + EXTRA, annual_inc, high_ret, years)

    for i, v in enumerate(ext_low):
        rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Extra low"})

    for i, v in enumerate(ext_high):
        rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Extra high"})

df = pd.DataFrame(rows)

# ------------------
# GRAPH
# ------------------
fig = px.line(df, x="Year", y="Value", color="Line")
st.plotly_chart(fig, use_container_width=True)

# ------------------
# TOTALS
# ------------------
st.header("Totals at end")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Current")
    st.metr
