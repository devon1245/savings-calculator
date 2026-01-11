import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Savings Scenarios",
    page_icon="📈",
    layout="wide"
)

st.title("Savings Scenarios")

# -----------------------------
# INPUTS
# -----------------------------
monthly = st.number_input(
    "Monthly contribution (R)",
    value=2000.0,
    step=100.0
)

annual_increase = st.number_input(
    "Annual increase (%)",
    value=5.0,
    step=0.5
)

years = st.number_input(
    "Years",
    value=20,
    step=1
)

conservative = st.slider("Conservative (%)", 4.0, 10.0, 6.0, 0.5)
moderate = st.slider("Moderate (%)", 6.0, 12.0, 8.0, 0.5)
optimistic = st.slider("Optimistic (%)", 8.0, 14.0, 10.0, 0.5)

show_extra = st.checkbox("Show impact of saving R500 more per month")
EXTRA = 500

# -----------------------------
# CALCULATION
# -----------------------------
def calc(monthly, annual_inc, rate, years):
    bal = 0
    contrib = monthly
    rows = []

    for m in range(1, years * 12 + 1):
        if m % 12 == 1 and m > 1:
            contrib *= (1 + annual_inc / 100)

        bal = bal * (1 + rate / 100 / 12) + contrib
        rows.append(bal)

    return rows

rows = []

scenarios = {
    "Conservative": conservative,
    "Moderate": moderate,
    "Optimistic": optimistic
}

for name, rate in scenarios.items():
    balances = calc(monthly, annual_increase, rate, years)
    for i, b in enumerate(balances):
        rows.append({
            "Year": (i + 1) / 12,
            "Balance": b,
            "Scenario": name
        })

if show_extra:
    for name, rate in scenarios.items():
        balances = calc(monthly + EXTRA, annual_increase, rate, years)
        for i, b in enumerate(balances):
            rows.append({
                "Year": (i + 1) / 12,
                "Balance": b,
                "Scenario": name + " (+R500)"
            })

df = pd.DataFrame(rows)

# -----------------------------
# DEBUG (VERY IMPORTANT)
# -----------------------------

# -----------------------------
# GRAPH (FORCED)
# -----------------------------
st.header("Projected Growth")

fig = px.line(
    df,
    x="Year",
    y="Balance",
    color="Scenario"
)

st.plotly_chart(fig, use_container_width=True)

