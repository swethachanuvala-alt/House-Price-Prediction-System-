import streamlit as st
import pipeline
from utils import get_artifacts, lakh, clean_label

art = get_artifacts()
meta = art["meta"]
o = meta["options"]


def idx(options, wanted):
    return options.index(wanted) if wanted in options else 0


st.title("Estimate a price")
st.write("Fill in the property details. Society is optional.")

form_col, result_col = st.columns([1.2, 1], gap="large")

with form_col:
    with st.form("estimate"):
        location = st.selectbox("Location", o["location"], index=idx(o["location"], "Whitefield"),
                                help="Click and type to search all locations.")
        c1, c2 = st.columns(2)
        size = c1.selectbox("Size", o["size"], index=idx(o["size"], "2 BHK"))
        area_type = c2.selectbox("Area type", o["area_type"], format_func=clean_label,
                                 index=idx(o["area_type"], "Super built-up  Area"))
        sqft = c1.number_input("Total area (sq ft)", min_value=200, max_value=20000, value=1200, step=50)
        availability = c2.selectbox("Availability", o["availability"])
        bath = c1.number_input("Bathrooms", min_value=1, max_value=20, value=meta["defaults"]["bath"])
        balcony = c2.number_input("Balconies", min_value=0, max_value=10, value=meta["defaults"]["balcony"])
        society = st.selectbox("Society (optional)", ["Not sure"] + o["society"])
        go = st.form_submit_button("Estimate price", use_container_width=True)

with result_col:
    if go:
        price, per_sqft = pipeline.predict(art, location, size, area_type, availability, society,
                                           float(sqft), float(bath), float(balcony))
        st.markdown(f"""<div class="result"><small>Estimated price</small>
<span class="big">{lakh(price)}</span>
<p>About ₹{per_sqft:,.0f} per sq ft for {sqft:,} sq ft in {location}.</p>
<p>The model is off by about ₹{meta['gb']['MAE']} lakh on average, so treat this as a starting point,
especially for premium properties.</p></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div class="result empty"><small>Your estimate</small>
<p>Fill in the form and select <b>Estimate price</b>. The result appears here.</p></div>""",
                    unsafe_allow_html=True)
