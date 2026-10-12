# PhishPrint 🔍
> Digital Footprint Analysis of Malicious URLs Using Feature-Engineered ML Pipelines

## About
PhishPrint is an ML-based phishing URL detector that analyzes the digital 
footprint of URLs through 87 hand-crafted features including lexical, domain, 
and security-based patterns. Built using Random Forest and XGBoost classifiers.

## Dataset
[Web Page Phishing Detection Dataset](https://www.kaggle.com/datasets/shashwatwork/web-page-phishing-detection-dataset)
- 11,430 URLs (50% phishing, 50% legitimate)
- 87 features

## Tech Stack
- Python 3.10+
- Pandas, NumPy
- Scikit-learn, XGBoost
- Matplotlib, Seaborn, SHAP
- Streamlit

## Project Structure
PhishPrint/
├── data/ # Dataset (not pushed)
├── notebooks/ # Jupyter notebooks (EDA, preprocessing, training)
├── src/ # Python scripts
├── models/ # Saved models
├── app/ # Streamlit UI
└── results/ # Plots and evaluation outputs

## Progress
- [x] Day 0 — Project setup
- [x] Day 1 — EDA
- [x] Day 2 — Preprocessing + Feature Engineering
- [ ] Day 3 — Model Training
- [ ] Day 4 — Evaluation + SHAP
- [ ] Day 5 — Streamlit UI
- [ ] Day 6 — Testing + Presentation

## Setup
pip install -r requirements.txt

## Run
streamlit run app/streamlit_app.py

## Results
(To be updated after training)