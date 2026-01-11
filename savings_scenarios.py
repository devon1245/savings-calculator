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

# -------------------------------------------------
# STYLING (mobile friendly)
# -------------------------------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 18px;
}
h1 { font-size: 2.2rem; }
h2 { font-size: 1.6rem; }
div[data-testid="stMetricValue"] {
    font-size: 1.8rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# TITLE
# -------------------------------------------------
st.title("Savings Scenarios")
st.markdown("Explore how small changes in saving behaviour can make a big difference.")

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
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
    "Conservative return (%)",
    min_value=4.0,
    max_value=10.0,
    value=6.0,
    step=0.5,
    format="%.1f%%"
)

moderate_return = st.slider(
    "Moderate return (%)",
    min_value=6.0,
    max_value=12.0,
    value=8.0,
    step=0.5,
    format="%.1f%%"
)

optimistic_return = st.slider(
    "Optimistic return (%)",
    min_value=8.0,
    max_value=14.0,
    value=10.0,
    step=0.5,
    format="%.1f%%"
)

# -------------------------------------------------
# BEHAVIOURAL NUDGE
# -------------------------------------------------
st.subheader("Saving behaviour")

show_extra_saving = st.checkbox(
    "Show impact of saving R500 more per month",
    value=False
)

EXTRA_MONTHLY = 500

# -------------------------------------------------
# CALCULATION FUNCTION
# -------------------------------------------------
def calculate_growth(monthly, annua_
