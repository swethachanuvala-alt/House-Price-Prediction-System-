# HomeWorth – Bengaluru house price predictor (Streamlit)

Multipage Streamlit app (Home, Estimate price, Market insights, About the model) powered by a
Gradient Boosting Regressor trained on Bengaluru_House_Data.csv.

## Run locally (Windows cmd)

    cd house-price-streamlit
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    streamlit run app.py

The app opens at http://localhost:8501.

## Push to GitHub

Create an empty repository on github.com first (no README), then:

    git init
    git add .
    git commit -m "House price predictor"
    git branch -M main
    git remote add origin https://github.com/<your-username>/<your-repo>.git
    git push -u origin main

## Deploy on Streamlit Community Cloud

1. Go to share.streamlit.io and sign in with GitHub.
2. Select "Create app", pick your repository and the main branch.
3. Set the main file path to `app.py`, then select "Deploy".

## Files

- app.py: entry point, page navigation and styling
- views/: the four pages
- pipeline.py: cleaning, training, prediction (same steps as GGST_4.ipynb)
- utils.py: model loading and shared CSS
- artifacts/: saved model, scaler and encoders. If they do not load on the server
  (for example a scikit-learn version difference) the app retrains from the CSV automatically.
- train_model.py: optional, rebuilds the files in artifacts/
