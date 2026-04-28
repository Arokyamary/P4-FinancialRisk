# Financial Risk Analytics — Credit Scorecard + VaR

Internal bank risk assessment platform built for credit risk analyst and financial analytics roles.

## Live Demo
[p4-financialrisk.streamlit.app](https://p4-financialrisk.streamlit.app)

## GitHub
[github.com/Arokyamary/P4-FinancialRisk](https://github.com/Arokyamary/P4-FinancialRisk)

---

## What This Project Does

This platform mimics how real banks assess loan applications internally. It combines two major areas of quantitative finance:

1. **Credit Risk Scorecard** — ML model that scores loan applicants from 300–900 using CIBIL score, FOIR, DSCR, employment type, collateral, repayment history, and more
2. **Market Risk (VaR)** — Monte Carlo simulation on NIFTY50 portfolio to calculate Value at Risk and Efficient Frontier

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Data Processing | Python, pandas, numpy |
| Credit Model | scorecardpy, scikit-learn (Logistic Regression) |
| Explainability | SHAP LinearExplainer |
| Market Risk | yfinance, Monte Carlo simulation |
| Database | PostgreSQL, SQLAlchemy |
| Dashboard | Streamlit, Plotly |
| Deployment | Streamlit Cloud |

---

## Key Results

| Metric | Value | Benchmark |
|--------|-------|-----------|
| Gini Coefficient | 0.71 | Industry standard: 0.40–0.70 |
| Credit Score Range | 300–900 | Standard bank scale |
| Historical VaR 95% | -1.43% | Rs 1.43L max daily loss on 1Cr |
| Optimal Sharpe Ratio | 1.00 | Target: >1.0 |
| Optimal Annual Return | 17.0% | NIFTY50 10-stock portfolio |
| Dataset Size | 32,581 records | Kaggle credit risk dataset |

---

## Business Insights (from SQL Analysis)

- Lowest income borrowers default at **43.62%** vs **9.13%** for highest income group
- High interest loans (16%+) default at **36.67%** vs **9.40%** for prime loans
- Loan-to-income ratio above **0.52** leads to **91.18% default rate** — critical risk threshold

---

## Dashboard Features

### Tab 1 — Loan Application Assessment
- Step 1: Applicant personal details (name, age, PAN, employment, industry)
- Step 2: Income details (gross salary, bonus, existing EMI, expenses, collateral)
- Step 3: Credit bureau info (CIBIL score, overdue payments, defaults, credit utilization)
- Auto-calculates: New EMI, FOIR, DSCR, LTI ratio, monthly surplus, LTV
- Output: Credit score (300–900), grade (AAA to D), decision (Approve/Review/Decline)
- Shows positive and negative risk factors separately
- Built-in CIBIL score reference guide

### Tab 2 — Portfolio VaR
- Efficient Frontier chart from 10,000 Monte Carlo simulations
- SHAP feature importance chart
- VaR summary metrics

### Tab 3 — Risk Analytics
- Default rate by income quintile (bar chart)
- Default rate by interest rate band (bar chart)
- Key risk thresholds table

---

## Scoring Model (100 Points)

| Factor | Weight | Notes |
|--------|--------|-------|
| CIBIL Score | 25 pts | Bureau score 300–900 |
| FOIR | 20 pts | RBI guideline: max 50–55% |
| Employment Stability | 15 pts | Govt PSU = highest, Freelancer = lowest |
| Repayment History | 15 pts | Overdue payments in last 24 months |
| Past Defaults | 10 pts | Written-off and unresolved defaults penalized heavily |
| Collateral | 5 pts | FD and property = highest value |
| DSCR | 5 pts | Debt Service Coverage Ratio |
| Other Factors | 5 pts | Age, residence, bank balance, credit utilization |

---

## Architecture

```
Kaggle CSV (32K records)
→ pandas cleaning
→ scorecardpy WoE encoding
→ Logistic Regression training (Gini: 0.71)
→ Credit Scorecard (300–900)
→ SHAP explainability
→ PostgreSQL storage (3 SQL risk queries)
→ yfinance NIFTY50 data
→ Monte Carlo VaR (10K simulations)
→ Efficient Frontier
→ Streamlit dashboard
→ Deployed on Streamlit Cloud
```

## Project Structure

```
P4_FinancialRisk/
├── data/
│   └── loan_data.csv                  # 32,581 Kaggle loan records
├── models/
│   └── scorecard_model.pkl            # Trained model
├── scorecard_model.py                 # Credit scorecard ML model
├── portfolio_var.py                   # Monte Carlo VaR simulation
├── load_to_postgres.py                # PostgreSQL data pipeline
├── app.py                             # Streamlit dashboard
├── efficient_frontier.png             # Generated chart
├── shap_feature_importance.png        # Generated SHAP chart
└── requirements.txt                   # Package versions
```

## Project Structure

```
P4_FinancialRisk/
├── data/
│   └── loan_data.csv                  # 32,581 Kaggle loan records
├── models/
│   └── scorecard_model.pkl            # Trained model
├── scorecard_model.py                 # Credit scorecard ML model
├── portfolio_var.py                   # Monte Carlo VaR simulation
├── load_to_postgres.py                # PostgreSQL data pipeline
├── app.py                             # Streamlit dashboard
├── efficient_frontier.png             # Generated chart
├── shap_feature_importance.png        # Generated SHAP chart
└── requirements.txt                   # Package versions
```

## Project Structure

```
P4_FinancialRisk/
├── data/
│   └── loan_data.csv                  # 32,581 Kaggle loan records
├── models/
│   └── scorecard_model.pkl            # Trained model
├── scorecard_model.py                 # Credit scorecard ML model
├── portfolio_var.py                   # Monte Carlo VaR simulation
├── load_to_postgres.py                # PostgreSQL data pipeline
├── app.py                             # Streamlit dashboard
├── efficient_frontier.png             # Generated chart
├── shap_feature_importance.png        # Generated SHAP chart
└── requirements.txt                   # Package versions
```

## How to Run Locally

```bash
git clone https://github.com/Arokyamary/P4-FinancialRisk.git
cd P4-FinancialRisk
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
