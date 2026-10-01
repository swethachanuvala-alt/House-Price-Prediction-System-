import streamlit as st
from utils import inject_css

st.set_page_config(page_title="HomeWorth · Bengaluru house prices", page_icon="🏠", layout="wide")
inject_css()

pages = [
    st.Page("views/home.py", title="Home", icon="🏠", default=True),
    st.Page("views/estimate.py", title="Estimate price", icon="💰"),
    st.Page("views/insights.py", title="Market insights", icon="📊"),
    st.Page("views/about.py", title="About the model", icon="🧠"),
]
st.navigation(pages).run()
