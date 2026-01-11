import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Smoke Test")

st.write("If you see a graph below, Streamlit is running THIS file.")

df = pd.DataFrame({
    "Year": [1, 2, 3, 4, 5],
    "Value": [10, 20, 15, 30, 40],
    "Scenario": ["A", "A", "A", "A", "A"]
})

fig = px.line(df, x="Year", y="Value", title="Test Graph")

st.plotly_chart(fig, use_container_width=True)

st.write("END OF FILE")
