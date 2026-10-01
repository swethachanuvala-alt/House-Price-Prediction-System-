"""Data cleaning, training and loading. Mirrors the steps in GGST_4.ipynb. No Streamlit imports here."""
import json, re
from pathlib import Path
import numpy as np, pandas as pd, joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

ROOT = Path(__file__).parent
CSV = ROOT / "Bengaluru_House_Data.csv"
ART = ROOT / "artifacts"
CAT_COLS = ["area_type", "availability", "location", "size", "society"]
FEATURES = CAT_COLS + ["total_sqft", "bath", "balcony"]

# Scores of the other tuned models, copied from the notebook's comparison table
OTHER_MODELS = [
    {"Model": "Linear Regression", "R2": -0.3226, "MAE": 119.62, "RMSE": 186.34},
    {"Model": "Decision Tree", "R2": 0.4483, "MAE": 40.85, "RMSE": 120.35},
    {"Model": "Random Forest", "R2": 0.6151, "MAE": 32.87, "RMSE": 100.53},
]


def _sqft(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip()
    try:
        if "-" in x:
            lo, hi = x.split("-")
            return (float(lo) + float(hi)) / 2
        if "Sq. Meter" in x:
            return float(re.findall(r"[\d.]+", x)[0]) * 10.7639
        if "Perch" in x:
            return float(re.findall(r"[\d.]+", x)[0]) * 272.25
        return float(x)
    except Exception:
        return np.nan


def _bhk(s):
    n = re.findall(r"\d+", s)
    return int(n[0]) if n else 0


def clean_data():
    df = pd.read_csv(CSV)
    for c in ["area_type", "availability", "location", "size"]:
        df[c] = df[c].fillna(df[c].mode()[0])
    df["society"] = df["society"].fillna("Unknown")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    for c in ["bath", "balcony", "price"]:
        df[c] = df[c].fillna(df[c].median())
    df["total_sqft"] = df["total_sqft"].apply(_sqft)
    df["total_sqft"] = df["total_sqft"].fillna(df["total_sqft"].median())
    return df


def build():
    clean = clean_data()
    df = clean.copy()
    encoders = {}
    for c in CAT_COLS:
        encoders[c] = LabelEncoder().fit(df[c])
        df[c] = encoders[c].transform(df[c])
    X, y = df.drop("price", axis=1), df["price"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler().fit(X_tr)
    # Best parameters from the notebook's GridSearchCV
    model = GradientBoostingRegressor(learning_rate=0.1, max_depth=5, min_samples_leaf=1,
                                      min_samples_split=10, n_estimators=300, random_state=42)
    model.fit(scaler.transform(X_tr), y_tr)
    p = model.predict(scaler.transform(X_te))
    gb = {"R2": round(float(r2_score(y_te, p)), 4),
          "MAE": round(float(mean_absolute_error(y_te, p)), 2),
          "RMSE": round(float(np.sqrt(mean_squared_error(y_te, p))), 2)}

    ln = clean.groupby("location").price.agg(["median", "count"])
    top = ln[ln["count"] >= 30].sort_values("median", ascending=False).head(8)
    meta = {
        "options": {
            "area_type": sorted(clean.area_type.unique()),
            "availability": ["Ready To Move"] + sorted(a for a in clean.availability.unique() if a != "Ready To Move"),
            "location": sorted(clean.location.unique()),
            "size": sorted(clean["size"].unique(), key=lambda s: (_bhk(s), s)),
            "society": sorted(s for s in clean.society.unique() if s != "Unknown"),
        },
        "defaults": {"bath": int(clean.bath.median()), "balcony": int(clean.balcony.median())},
        "gb": gb,
        "models": OTHER_MODELS + [{"Model": "Gradient Boosting", **gb}],
        "stats": {"listings": int(len(clean)), "locations": int(clean.location.nunique()),
                  "median_price": float(clean.price.median())},
        "by_area": clean.groupby("area_type").price.median().round(1).to_dict(),
        "top_locations": top["median"].round(1).to_dict(),
        "by_bhk": {f"{k} BHK": round(float(v), 1) for k, v in
                   clean.assign(b=clean["size"].map(_bhk)).query("1 <= b <= 5").groupby("b").price.median().items()},
    }
    return {"model": model, "scaler": scaler, "encoders": encoders, "meta": meta}


def save(art):
    ART.mkdir(exist_ok=True)
    joblib.dump(art["model"], ART / "house_price_predictor_model.pkl")
    joblib.dump(art["scaler"], ART / "house_price_predictor_scaler.pkl")
    joblib.dump(art["encoders"], ART / "label_encoders.pkl")
    (ART / "meta.json").write_text(json.dumps(art["meta"]))


def load_or_train():
    """Use the saved files; if they are missing or were made with another scikit-learn version, retrain."""
    try:
        return {"model": joblib.load(ART / "house_price_predictor_model.pkl"),
                "scaler": joblib.load(ART / "house_price_predictor_scaler.pkl"),
                "encoders": joblib.load(ART / "label_encoders.pkl"),
                "meta": json.loads((ART / "meta.json").read_text())}
    except Exception:
        art = build()
        try:
            save(art)
        except OSError:
            pass
        return art


def predict(art, location, size, area_type, availability, society, sqft, bath, balcony):
    enc = art["encoders"]
    if society not in enc["society"].classes_:
        society = "Unknown"
    cats = [location, area_type, availability, size, society]
    named = dict(zip(["location", "area_type", "availability", "size", "society"], cats))
    vec = [enc[c].transform([named[c]])[0] for c in CAT_COLS]
    x = pd.DataFrame([vec + [sqft, bath, balcony]], columns=FEATURES)
    price = max(float(art["model"].predict(art["scaler"].transform(x))[0]), 1.0)
    return price, price * 1e5 / sqft
