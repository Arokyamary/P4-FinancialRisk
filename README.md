# Financial Risk Analytics — Credit Scorecard + VaR

Industry-standard credit risk modeling platform built for financial analytics and risk assessment roles.

## Live Demo
[p4-financialrisk.streamlit.app](https://p4-financialrisk.streamlit.app)

## Tech Stack
Python · scorecardpy · scikit-learn · SHAP · yfinance · PostgreSQL · Streamlit · Plotly

## Key Results
- Gini Coefficient: **0.71** (industry benchmark: 0.40–0.70)
- Credit Score Range: 300–850
- Historical VaR 95%: **-1.43%** (Rs 1.43L max daily loss on 1Cr portfolio)
- Optimal Sharpe Ratio: **1.00** | Optimal Return: **17%**

## Business Insights
- Lowest income borrowers default at **43.62%** vs **9.13%** for highest income group
- High risk loans (16%+ interest) default at **36.67%** vs **9.40%** for prime loans
- Loan-to-income ratio above 0.52 leads to **91% default rate**

## Architecture
Data (Kaggle 32K records) → WoE Encoding → Logistic Regression → Credit Scorecard → SHAP Explainability → PostgreSQL → Monte Carlo VaR → Streamlit Dashboard

## Project Structure
- `scorecard_model.py` — Credit scorecard with WoE + Logistic Regression + SHAP
- `portfolio_var.py` — Monte Carlo VaR + Efficient Frontier (10K simulations)
- `load_to_postgres.py` — PostgreSQL data pipeline
- `app.py` — Interactive Streamlit dashboard
