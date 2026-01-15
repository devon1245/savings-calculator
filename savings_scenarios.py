import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------
# PAGE SETUP
# ------------------
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

extra = st.checkbox("Show impact of saving R500 more per month")
EXTRA = 500

# ------------------
# CALCULATION
# ------------------
def grow(start, monthly, inc, rate, years):
    balance = start
    contribution = monthly
    values = []

    for m in range(1, years * 12 + 1):
        if m % 12 == 1 and m > 1:
            contribution *= (1 + inc / 100)
        balance = balance * (1 + rate / 100 / 12) + contribution
        values.append(balance)

    return values

# ------------------
# BUILD DATA
# ------------------
rows = []

base_low = grow(lump_sum, monthly, annual_inc, low_ret, years)
base_high = grow(lump_sum, monthly, annual_inc, high_ret, years)

for i in range(len(base_low)):
    rows.append({
        "Year": (i + 1) / 12,
        "Value": base_low[i],
        "Scenario": "Current – lower return"
    })
    rows.append({
        "Year": (i + 1) / 12,
        "Value": base_high[i],
        "Scenario": "Current – higher return"
    })

if extra:
    extra_low = grow(lump_sum, monthly + EXTRA, annual_inc, low_ret, years)
    extra_high = grow(lump_sum, monthly + EXTRA, annual_inc, high_ret, years)

    for i in range(len(extra_low)):
        rows.append({
            "Year": (i + 1) / 12,
            "Value": extra_low[i],
            "Scenario": "Save +R500 – lower return"
        })
        rows.append({
            "Year": (i + 1) / 12,
            "Value": extra_high[i],
            "Scenario": "Save +R500 – higher return"
        })

df = pd.DataFrame(rows)

# ------------------
# GRAPH
# ------------------
st.header("Projected growth")

fig = px.line(
    df,
    x="Year",
    y="Value",
    color="Scenario",
    markers=True
)

fig.update_layout(
    xaxis_title="Years",
    yaxis_title="Portfolio value (R)"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------
# TOTALS (COLOUR-CODED)
# ------------------
st.header("Value at end of period")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔵 Current saving")
    st.write("🔵", f"R {base_low[-1]:,.0f}")
    st.write("🟦", f"R {base_high[-1]:,.0f}")

with col2:
    st.subheader("🟧 Saving + R500")
    if extra:
        st.write("🟧", f"R {extra_low[-1]:,.0f}")
        st.write("🟥", f"R {extra_high[-1]:,.0f}")
    else:
        st.write("Enable comparison above")

# ------------------
# FOOTNOTE
# ------------------
st.caption("Illustrative only. Returns are not guaranteed.")
