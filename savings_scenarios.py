import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(layout="wide")

st.title("Savings Scenarios")
st.write("Showing how saving behaviour matters even when returns fluctuate.")

# ------------------
# INPUTS
# ------------------
lump_sum = st.number_input("Current savings (R)", 0.0, step=1000.0)
monthly = st.number_input("Monthly contribution (R)", 2000.0, step=100.0)
annual_inc = st.number_input("Annual increase (%)", 5.0, step=0.5)
years = st.number_input("Years to invest", 20, step=1)

low_ret = st.slider("Lower return (%)", 5.0, 9.0, 6.0, 0.5)
high_ret = st.slider("Higher return (%)", 9.0, 15.0, 11.0, 0.5)

extra = st.checkbox("Add R500 per month")
EXTRA = 500

# ------------------
# CALCULATION
# ------------------
def grow(start, monthly, inc, r, y):
    bal = start
    c = monthly
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

base_low = grow(lump_sum, monthly, annual_inc, low_ret, years)
base_high = grow(lump_sum, monthly, annual_inc, high_ret, years)

for i, v in enumerate(base_low):
    rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Current low"})

for i, v in enumerate(base_high):
    rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Current high"})

if extra:
    ext_low = grow(lump_sum, monthly + EXTRA, annual_inc, low_ret, years)
    ext_high = grow(lump_sum, monthly + EXTRA, annual_inc, high_ret, years)

    for i, v in enumerate(ext_low):
        rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Extra low"})

    for i, v in enumerate(ext_high):
        rows.append({"Year": (i + 1) / 12, "Value": v, "Line": "Extra high"})

df = pd.DataFrame(rows)

# ------------------
# GRAPH
# ------------------
colors = {
    "Current low": "#9ecae1",
    "Current high": "#08519c",
    "Extra low": "#fdae6b",
    "Extra high": "#d94801",
}

st.header("Projected growth")
fig = px.line(df, x="Year", y="Value", color="Line", color_discrete_map=colors)
st.plotly_chart(fig, use_container_width=True)

# ------------------
# TOTALS (NO METRIC, NO QUOTES RISK)
# ------------------
st.header("Value at end")

c1, c2 = st.columns(2)

with c1:
    st.subheader("🔵 Current saving")
    st.write("Lower return:", f"R {base_low[-1]:,.0f}")
    st.write("Higher return:", f"R {base_high[-1]:,.0f}")

with c2:
    st.subheader("🟧 Saving + R500")
    if extra:
        st.write("Lowe
