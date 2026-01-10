import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Savings Scenarios",
    page_icon="📈",
    layout="wide"
)


# --------------------
# STYLING
# --------------------
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

# --------------------
# TITLE
# --------------------
st.title("Savings Growth Scenarios")
st.markdown("Adjust the inputs to explore different outcomes.")

# --------------------
# INPUTS
# --------------------
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

conservative_return = st.slider("Conservative (%)", 0.0, 15.0, 6.0, 0.5)
moderate_return = st.slider("Moderate (%)", 0.0, 15.0, 8.0, 0.5)
optimistic_return = st.slider("Optimistic (%)", 0.0, 15.0, 10.0, 0.5)

# --------------------
# CALCULATION
# --------------------
def calculate_growth(monthly, annual_increase, annual_return, years):
    months = years * 12
    monthly_rate = annual_return / 100 / 12
    annual_increase_rate = annual_increase / 100

    balance = 0.0
    contribution = monthly
    balances = []
    total_contributions = 0.0

    for m in range(1, months + 1):
        if m % 12 == 1 and m > 1:
            contribution *= (1 + annual_increase_rate)

        balance = balance * (1 + monthly_rate) + contribution
        total_contributions += contribution
        balances.append(balance)

    return balances, total_contributions

# --------------------
# BUILD DATA
# --------------------
scenarios = {
    "Conservative": conservative_return,
    "Moderate": moderate_return,
    "Optimistic": optimistic_return
}

rows = []

for name, rate in scenarios.items():
    balances, total_contrib = calculate_growth(
        monthly_contribution,
        annual_increase,
        rate,
        years
    )

    for i, bal in enumerate(balances):
        rows.append({
            "Year": (i + 1) / 12,
            "Balance": bal,
            "Scenario": name
        })

df = pd.DataFrame(rows)

# --------------------
# OUTPUTS (FORCED)
# --------------------
st.header("Projected Growth")

st.write(f"DEBUG: data points = {len(df)}")

fig = px.line(
    df,
    x="Year",
    y="Balance",
    color="Scenario",
    labels={
        "Balance": "Portfolio Value (R)",
        "Year": "Years"
    }
)

st.plotly_chart(fig, use_container_width=True)

st.header("Summary at End of Period")

cols = st.columns(3)

for i, (name, rate) in enumerate(scenarios.items()):
    balances, total_contrib = calculate_growth(
        monthly_contribution,
        annual_increase,
        rate,
        years
    )

    with cols[i]:
        st.metric(
            label=name,
            value=f"R {balances[-1]:,.0f}",
            delta=f"Total contributed: R {total_contrib:,.0f}"
        )

