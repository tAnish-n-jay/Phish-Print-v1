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
- [x] Day 3 — Model Training
- [x] Day 4 — Evaluation + SHAP
- [x] Day 5 — Streamlit UI
- [x] Day 6 — Testing + Presentation

## Setup
pip install -r requirements.txt

## Run
streamlit run app/streamlit_app.py

## Results

| Model | Accuracy | ROC-AUC |
|---|---|---|
| Random Forest | 95.32% | 0.9909 |
| XGBoost | 96.28% | 0.9927 |
| Ensemble | 96.15% | 0.9927 |

**Best Model: XGBoost** with 96.28% accuracy and 0.9927 ROC-AUC

### Top Features (SHAP Analysis)
| Rank | Feature | Impact |
|---|---|---|
| 1 | google_index | 0.1380 |
| 2 | page_rank | 0.1024 |
| 3 | nb_hyperlinks | 0.0693 |
| 4 | nb_www | 0.0512 |
| 5 | phish_hints | 0.0213 |

### Key Insights
- Domain reputation features (`google_index`, `page_rank`) are the strongest phishing signals
- Phishing URLs are consistently longer with more special characters
- Model achieves near-perfect AUC of 0.9927 — excellent discrimination ability

## Future Work
- Brand similarity detection for typosquatting attacks
- Real-time Google Safe Browsing API integration
- Monthly retraining with fresh PhishTank data
- FastAPI backend for production deployment

## Limitations
- Features like `google_index` and `page_rank` default to 0 in live demo
- Cannot detect typosquatting attacks (e.g. rnicrosoft.com)
- Zero-day phishing domains with no suspicious patterns may bypass detection