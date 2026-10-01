import streamlit as st
from utils import get_artifacts

meta = get_artifacts()["meta"]
g = meta["gb"]
st.title("About the model")
st.write("How HomeWorth turns listing details into a price.")

cards = [
    ("Data", f"{meta['stats']['listings']:,} Bengaluru listings with area type, availability, location, size, society, total area, bathrooms, balconies and price in lakh."),
    ("Preparation", "Missing categories filled with the most common value, missing numbers with the median. Area ranges are averaged and square metres and perches converted to square feet. Categories are label-encoded and all features standard-scaled."),
    ("Model", "Gradient Boosting Regressor with 300 trees, depth 5 and learning rate 0.1, chosen by grid search with 5-fold cross-validation. It beat linear regression, decision tree and random forest."),
    ("Score", f"R² {g['R2']}, MAE ₹{g['MAE']} lakh and RMSE ₹{g['RMSE']} lakh on a 20% held-out test set."),
]
for row in (cards[:2], cards[2:]):
    cols = st.columns(2, gap="large")
    for col, (t, d) in zip(cols, row):
        col.markdown(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>', unsafe_allow_html=True)
    st.write("")

st.markdown('<div class="card"><h3>Limits</h3><p>Prices are asking prices, not sale prices. Society names are mostly missing in the data, so leaving it blank is normal. Estimates are less reliable for luxury homes, where the data is thin.</p></div>', unsafe_allow_html=True)
