import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.set_page_config(layout="wide")

st.title("Savings")

# INPUTS
lump = st.number_input("", 0.0, step=1000.0)
monthly = st.number_input("", 2000.0, step=100.0)
inc = st.number_input("", 5.0, step=0.5)
yrs = st.number_input("", 20, step=1)

low = st.slider("", 5.0, 9.0, 6.0, 0.5)
high = st.slider("", 9.0, 15.0, 11.0, 0.5)

extra = st.checkbox("")
ADD = 500

# CALC
def g(start, m, i, r, y):
    b = start
    c = m
    o = []
    for k in range(1, y * 12 + 1):
        if k % 12 == 1 and k > 1:
            c *= (1 + i / 100)
        b = b * (1 + r / 100 / 12) + c
        o.append(b)
    return o

# DATA
rows = []

a = g(lump, monthly, inc, low, yrs)
b = g(lump, monthly, inc, high, yrs)

for n, v in enumerate(a):
    rows.append({"x": (n + 1) / 12, "y": v, "z": 1})

for n, v in enumerate(b):
    rows.append({"x": (n + 1) / 12, "y": v, "z": 2})

if extra:
    c = g(lump, monthly + ADD, inc, low, yrs)
    d = g(lump, monthly + ADD, inc, high, yrs)

    for n, v in enumerate(c):
        rows.append({"x": (n + 1) / 12, "y": v, "z": 3})

    for n, v in enumerate(d):
        rows.append({"x": (n + 1) / 12, "y": v, "z": 4})

df = pd.DataFrame(rows)

# GRAPH
fig = px.line(df, x="x", y="y", color="z")
st.plotly_chart(fig, use_container_width=True)

# TOTALS
c1, c2 = st.columns(2)

with c1:
    st.write(a[-1])
    st.write(b[-1])

with c2:
    if extra:
        st.write(c[-1])
        st.write(d[-1])

# PDF
def p():
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    c.drawString(40, 800, str(a[-1]))
    c.drawString(40, 780, str(b[-1]))
    if extra:
        c.drawString(40, 760, str(c[-1]))
        c.drawString(40, 740, str(d[-1]))
    c.save()
    buf.seek(0)
    return buf

st.download_button("", p(), "s.pdf")
