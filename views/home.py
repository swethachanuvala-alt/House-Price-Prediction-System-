import streamlit as st
from utils import get_artifacts, lakh

meta = get_artifacts()["meta"]

left, right = st.columns([1.3, 1], gap="large", vertical_alignment="center")
with left:
    st.markdown(f"""<div class="hero"><h1>What is your Bengaluru home worth?</h1>
<p>Enter the area, location and rooms. A gradient boosting model trained on {meta['stats']['listings']:,}
listings gives you an estimate in seconds.</p></div>""", unsafe_allow_html=True)
    b1, b2, _ = st.columns([1, 1, 1])
    b1.page_link("views/estimate.py", label="Estimate a price")
    b2.page_link("views/insights.py", label="See the market")
with right:
    st.markdown(f"""<div class="tag"><small>Median asking price</small>
<strong>{lakh(meta['stats']['median_price'])}</strong>
<span>across {meta['stats']['locations']} locations</span></div>""", unsafe_allow_html=True)

st.markdown("## Three steps to an estimate")
c1, c2, c3 = st.columns(3)
steps = [("1. Describe the property", "Pick the location, size in BHK and area type, then add square feet, bathrooms and balconies."),
         ("2. Run the model", "Your inputs are encoded and scaled exactly as in training, then passed to the model."),
         ("3. Read the estimate", "You get the total price, the price per square foot and the typical error.")]
for col, (t, d) in zip((c1, c2, c3), steps):
    col.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>', unsafe_allow_html=True)

g = meta["gb"]
st.markdown(f"""<div class="band">
<div><strong>{g['R2']}</strong>R² on unseen listings</div>
<div><strong>₹{g['MAE']} lakh</strong>average error (MAE)</div>
<div><strong>{meta['stats']['locations']}</strong>locations covered</div></div>""", unsafe_allow_html=True)
