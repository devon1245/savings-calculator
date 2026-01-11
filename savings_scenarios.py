import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------
# PAGE SETUP
# ------------------
st.set_page_config(layout="wide")
st.title("Savings Scenarios – Step B")

st.write(
    "Showing how saving behaviour and market variability "
    "affect long-term outcomes."
)

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
# BUILD DATA FOR GRAPH
# ------------------
rows = []

# Base saving scenarios
base_low = grow(monthly, annual_increase, lower_return, years)
base_high = grow(monthly, annual_increase, higher_return, years)

for i, b in enumerate(base_low):
    rows.append({
        "Year": (i + 1) / 12,
        "Balance": b,
        "Scenario": "Current – lower return"
    })

for i, b in enumerate(base_high):
    rows.append({
        "Year": (i + 1) / 12,
        "Balance": b,
        "Scenario": "Current – higher return"
    })

# Extra saving scenarios (optional)
if show_extra:
    extra_low = grow(monthly + EXTRA, annual_increase, lower_return, years)
    extra_high = grow(monthly + EXTRA, annual_increase, higher_return, years)

    for i, b in enumerate(extra_low):
        rows.append({
            "Year": (i + 1) / 12,
            "Balance": b,
            "Scenario": "+R500 – lower return"
        })

    for i, b in enumerate(extra_high):
        rows.append({
            "Year": (i + 1) / 12,
            "Balance": b,
            "Scenario": "+R500 – higher return"
        })

df = pd.DataFrame(rows)

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

# ------------------
# TOTALS
# ------------------
st.header("Value at end of period")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Current saving")

    st.metric(
        "Lower return",
        f"R {base_low[-1]:,.0f}"
    )

    st.metric(
        "Higher return",
        f"R {base_high[-1]:,.0f}"
    )

with col2:
    st.subheader("Saving + R500")

    if show_extra:
        st.metric(
            "Lower return",
            f"R {extra_low[-1]:,.0f}"
        )

        st.metric(
            "Higher return",
            f"R {extra_high[-1]:,.0f}"
        )
    else:
        st.info("Tick the checkbox above to see this comparison.")

st.caption(
    "Illustrative calculations only. Returns are not guaranteed."
)
