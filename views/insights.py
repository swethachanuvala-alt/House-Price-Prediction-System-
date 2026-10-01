import altair as alt
import pandas as pd
import streamlit as st
from utils import get_artifacts, clean_label

meta = get_artifacts()["meta"]
st.title("Market insights")
st.write("Median asking prices from the dataset, and how the models compared.")


def bar(data, title):
    df = pd.DataFrame({"label": [clean_label(k) for k in data], "price": list(data.values())})
    chart = (alt.Chart(df).mark_bar(color="#FF9F1C", cornerRadiusEnd=6)
             .encode(x=alt.X("price:Q", title="Median price (₹ lakh)"),
                     y=alt.Y("label:N", sort="-x", title=None),
                     tooltip=[alt.Tooltip("label:N", title="Name"), alt.Tooltip("price:Q", title="₹ lakh")])
             .properties(height=max(40 * len(df), 120)).configure_view(strokeWidth=0))
    st.markdown(f"### {title}")
    st.altair_chart(chart, use_container_width=True)


a, b = st.columns(2, gap="large")
with a:
    bar(meta["by_bhk"], "Median price by BHK")
with b:
    bar(meta["by_area"], "Median price by area type")
bar(meta["top_locations"], "Priciest locations (30+ listings)")

st.markdown("### Model comparison (tuned models, test set)")
df = pd.DataFrame(meta["models"])
st.dataframe(df, hide_index=True, use_container_width=True)
st.caption("Gradient Boosting has the highest R² and the lowest MAE and RMSE. Errors are in ₹ lakh.")
