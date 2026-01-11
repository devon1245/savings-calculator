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
# TITLE
# -------------------------------------------------
st.title("Savings Scenarios")
st.markdown(
    "This illustration shows how saving behaviour and market conditions "
    "both affect long-term outcomes."
)

# -------------------------------------------------
# INPUTS
# -------------------------------------------------
st.header("Inputs")

monthly_contribution = st.number_input(
    "Monthly contribution (R)",
    value=2000.0,
    step=100.0
)

annual_increase = st.number_input(
    "Annual increase in contribution (%)",
    value=5.0,
    step=0.5
)

years = st.number_input(
    "Years to invest",
    value=20,
    step=1
)

st.subheader("Return assumptions")

lower_return = st.slider(
    "Lower expected return (%)",
    min_value=5.0,
    max_value=8.0,
    value=6.0,
    step=0.5
)

higher_return = st.slider(
    "Higher expected return (%)",
    min_value=8.0,
    max_value=11.0,
    value=9.0,
    step=0.5
)

EXTRA_MONTHLY = 500

# -------------------------------------------------
# CALCULATION FUNCTION
# -------------------------------------------------
def calculate_growth(monthly, annual_increase, annual_return, years):
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

# -------------------------------------------------
# BUILD DATA
# -------------------------------------------------
rows = []

scenarios = [
    ("Current saving – lower return", monthly_contribution, lower_return),
    ("Current saving – higher return", monthly_contribution, higher_return),
    ("+R500 saving – lower return", monthly_contribution + EXTRA_MONTHLY, lower_return),
    ("+R500 saving – higher return", monthly_contribution + EXTRA_MONTHLY, higher_return),
]

for label, contrib, rate in scenarios:
    balances = calculate_growth(
        contrib,
        annual_increase,
        rate,
        years
    )

    for i, bal in enumerate(balances):
        rows.append({
            "Year": (i + 1) / 12,
            "Balance": bal,
            "Scenario": label
        })

df = pd.DataFrame(rows)

# -------------------------------------------------
# GRAPH
# -------------------------------------------------
st.header("Projected growth")

color_map = {
    "Current saving – lower return": "#6baed6",
    "Current saving – higher return": "#08519c",
    "+R500 saving – lower return": "#74c476",
    "+R500 saving – higher return": "#006d2c",
}

fig = px.line(
    df,
    x="Year",
    y="Balance",
    color="Scenario",
    color_discrete_map=color_map,
    labels={
        "Balance": "Portfolio value (R)",
        "Year": "Years"
    }
)

fig.update_layout(
    legend_title_text="",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# TOTALS (MATCHING COLOURS)
# -------------------------------------------------
st.header("Value at end of period")

col1, col2 = st.columns(2)

# Current saving totals
with col1:
    st.subheader("Current saving")

    low_base = calculate_growth(
        monthly_contribution, annual_increase, lower_return, years
    )[-1]

    high_base = calculate_growth(
        monthly_contribution, annual_increase, higher_return, years
    )[-1]

    st.markdown(
        f"<span style='color:#6baed6'>Lower return:</span> "
        f"<strong>R {low_base:,.0f}</strong>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<span style='color:#08519c'>Higher return:</span> "
        f"<strong>R {high_base:,.0f}</strong>",
        unsafe_allow_html=True
    )

# +R500 saving totals
with col2:
    st.subheader("Saving + R500")

    low_extra = calculate_growth(
        monthly_contribution + EXTRA_MONTHLY, annual_increase, lower_return, years
    )[-1]

    high_extra = calculate_growth(
        monthly_contribution + EXTRA_MONTHLY, annual_increase, higher_return, years
    )[-1]

    st.markdown(
        f"<span style='color:#74c476'>Lower return:</span> "
        f"<strong>R {low_extra:,.0f}</strong>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<span style='color:#006d2c'>Higher return:</span> "
        f"<strong>R {high_extra:,.0f}</strong>",
        unsafe_allow_html=True
    )

# -------------------------------------------------
# FOOTNOTE
# -------------------------------------------------
st.caption(
    "Illustrative calculations only. Returns are not guaranteed. "
    "This tool supports financial planning discussions."
)
