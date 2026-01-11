import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Savings Scenarios",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# BASIC STYLING (mobile friendly)
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 18px;
}
h1 { font-size: 2.2rem; }
h2 { font-size: 1.6rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.title("Savings Scenarios")
st.markdown(
    "See how small increases in saving can make a big long-term difference."
)

# -----------------------------
# INPUTS
# -----------------------------
st.header("Inputs")

monthly_contribution = st.number_input(
    "Monthly contribution (R)",
    min_value=0.0,
    value=2000.0,
    step=100.0
)

annual_increase = st.number_input(
    "Annual increase in contribution (%)",
    min_value=0.0,
    value=5.0,
    step=0.5
)

years = st.number_input(
    "Years to invest",
    min_value=1,
    value=20,
    step=1
)

st.subheader("Assumed annual return")

conservative_return = st.slider(
    "Conservative (%)",
    4.0, 10.0, 6.0, 0.5
)

moderate_return = st.slider(
    "Moderate (%)",
    6.0, 12.0, 8.0, 0.5
)

optimistic_return = st.slider(
    "Optimistic (%)",
    8.0, 14.0, 10.0, 0.5
)

# -----------------------------
# SAVING BEHAVIOUR NUDGE
# -----------------------------
st.subheader("Saving behaviour")

show_extra = st.checkbox(
    "Show impact of saving R500 more per month"
)

EXTRA_MONTHLY = 500

# -----------------------------
# CALCULATION FUNCTION
# -----------------------------
def calculate_growth(
    monthly,
    annual_increase,
    annual_return,
    years
):
    months = years * 12
    monthly_rate = annual_return / 100 / 12
    increase_rate = annual_increase / 100

    balance = 0.0
    contribution = monthly
    balances = []

    for m in range(1, months + 1):
        if m % 12 == 1 and m > 1:
            contribution *= (1 + increase_rate)

        balance = balance * (1 + monthly_rate) + contribution
        balances.append(balance)

    return balances

# -----------------------------
