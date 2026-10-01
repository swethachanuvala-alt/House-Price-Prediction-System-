import streamlit as st
import pipeline


@st.cache_resource(show_spinner="Loading the model...")
def get_artifacts():
    return pipeline.load_or_train()


def lakh(v):
    """Dataset prices are in lakhs of rupees; show crore above 100 lakh."""
    return f"₹{v / 100:.2f} crore" if v >= 100 else f"₹{v:.1f} lakh"


def clean_label(s):
    return " ".join(str(s).split())


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Figtree:wght@400;500;700&display=swap');
html, body, [class*="st-"], .stApp { font-family: 'Figtree', sans-serif; }
h1, h2, h3 { font-family: 'Fraunces', Georgia, serif !important; color: #3B2314 !important; letter-spacing: -0.01em; }
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 2.5rem; max-width: 1100px; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #FFC93C, #FF9F1C); }
[data-testid="stSidebar"] * { color: #3B2314 !important; font-weight: 700; }
.stButton > button, .stFormSubmitButton > button, [data-testid="stPageLink"] a {
  background: #E85D04; color: #fff; border: 0; border-radius: 12px; font-weight: 700;
  box-shadow: 0 4px 0 #A83F00; padding: .6rem 1.4rem; }
.stButton > button:hover, .stFormSubmitButton > button:hover { background: #F46D12; color: #fff; }
.hero h1 { font-size: clamp(2.3rem, 5vw, 3.8rem); font-weight: 800; line-height: 1.05; margin: 0 0 1rem; }
.hero p { font-size: 1.1rem; max-width: 34rem; color: #5a3d27; }
.tag { position: relative; background: linear-gradient(160deg, #FFC93C, #FF9F1C); color: #3B2314;
  border-radius: 18px 18px 18px 60px; padding: 3rem 2rem 2rem; transform: rotate(3deg);
  box-shadow: 0 14px 0 -4px rgba(232,93,4,.25); }
.tag::before { content: ""; position: absolute; top: 1rem; left: 50%; width: 22px; height: 22px;
  margin-left: -11px; border-radius: 50%; background: #FFF6DC; box-shadow: inset 0 2px 4px rgba(0,0,0,.3); }
.tag small { display: block; font-weight: 700; }
.tag strong { display: block; font: 800 clamp(2.2rem, 4vw, 3.2rem) 'Fraunces', serif; margin: .3rem 0; }
.card { background: #FFFDF6; border: 2px solid #F3D88B; border-radius: 18px; padding: 1.3rem 1.5rem; height: 100%; }
.card h3 { margin-top: 0; font-size: 1.15rem; }
.card p { margin: 0; color: #5a3d27; }
.band { display: flex; flex-wrap: wrap; justify-content: space-around; gap: 1rem; background: #3B2314;
  color: #FFF6DC; border-radius: 20px; padding: 1.8rem; text-align: center; margin: 2rem 0; }
.band strong { display: block; font: 800 2rem 'Fraunces', serif; color: #FFC93C; }
.result { background: linear-gradient(160deg, #FFFDF6, #FFE9A8); border: 2px solid #FF9F1C; border-radius: 18px; padding: 1.6rem; }
.result.empty { border-color: #F3D88B; background: #FFFDF6; }
.result small { color: #7A5A3C; font-weight: 700; }
.result .big { display: block; font: 800 clamp(2.4rem, 5vw, 3.3rem) 'Fraunces', serif; color: #E85D04; margin: .2rem 0 .6rem; }
.result p { color: #5a3d27; margin: .3rem 0; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)
