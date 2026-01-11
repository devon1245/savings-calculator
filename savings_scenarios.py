import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------
# PAGE SETUP
# ------------------
st.set_page_config(
    page_title="Savings Scenarios",
    page_icon="📈",
    layout="wide"
)

st.title("Savings Scenarios")
st.write("Showing how saving behaviour matters, even when returns fluctuate.")

# ------------------
# INPUTS
# ------------------
monthly = st.number_input("Monthly contribution (R)", 2000.0, step=100.0)
annual_inc = st.number_input("Annual increase (%)", 5.0, step=0.5)
years = st.number_input("Years to invest", 20, step=1)

low_ret = st.slider("Lower expected return (%)", 5.0, 9.0, 6.0, 0.5)
high_ret = st.slider("Higher expected return (%)", 9.0, 15.0, 11.0, 0.5)

extra = st.checkbox("Show impact of saving R500 more per month")
EXTRA = 500

# ------------------
# CALCULATION
# ------------------
def grow(monthly, inc, rate, years):
    bal = 0.0
    contrib = monthly
    out = []

    for m in range(1, years * 12 + 1):
        if m % 12 == 1 and m > 1:
            contrib *= (1 + inc / 100)

        bal = bal * (1 + rate / 100 / 12) + contrib
        out.append(bal)

    return out

# ------------------
# BUILD DATA
# ------------------
rows = []

base_low = grow(monthly, annual_inc, low_ret, years)
base_high = grow(monthly, annual_inc, high_ret, years)

for i, v in enumerate(base_low):
    rows.append({
        "Year": (i + 1) / 12,
        "Value": v,
        "Line": "Current low"
    })

for i, v in enumerate(base_high):
    rows.append({
        "Year": (i + 1) / 12,
        "Value": v,
        "Line": "Current high"
    })

if extra:
    ext_low = grow(monthly + EXTRA, annual_inc, low_ret, years)
    ext_high = grow(monthly + EXTRA, annual_inc, high_ret, years)

    for i, v in enumerate(ext_low):
        rows.append({
            "Year": (i + 1) / 12,
            "Value": v,
            "Line": "Extra low"
        })

    for i, v in enumerate(ext_high):
        rows.append({
            "Year": (i + 1) / 12,
            "Value": v,
            "Line": "Extra high"
        })

df = pd.DataFrame(rows)

# ------------------
# COLOUR GROUPING
# ------------------
color_map = {
    "Current low": "#9ecae1",    # light blue
    "Current high": "#08519c",   # dark blue
    "Extra low": "#fdae6b",      # light orange
    "Extra high": "#d94801",     # dark orange
}

# ------------------
# GRAPH
# ------------------
st.header("Projected growth")

fig = px.line(
    df,
    x="Year",
    y="Value",
    color="Line",
    color_discrete_map=color_map,
    labels={
        "Value": "Portfolio value (R)",
        "Year": "Years"
    }
)

fig.update_layout(
    legend_title_text="",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------
# TOTALS
# ------------------
st.header("Value at end of period")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Current saving")
    st.metric("Lower return", f"R {base_low[-1]:,.0f}")
    st.metric("Higher return", f"R {base_high[-1]:,.0f}")

with c2:
    st.subheader("Saving + R500")
    if extra:
        st.metric("Lower return", f"R {ext_low[-1]:,.0f}")
        st.metric("Higher return", f"R {ext_high[-1]:,.0f}")
    else:
        st.write("Tick the checkbox above to see this comparison.")

# ------------------
# FOOTNOTE
# ------------------
st.caption("Illustrative only. Returns are not guaranteed.")
