import pandas as pd
import numpy as np
import scorecardpy as sc
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import shap, joblib, matplotlib.pyplot as plt


print('Step 1: Loading data...')
df = pd.read_csv('data/loan_data.csv')
df['bad_flag'] = (df['loan_status'] == 1).astype(int)
print(f'Default rate: {df.bad_flag.mean()*100:.1f}%')

features = ['loan_amnt','person_income','loan_int_rate',
'loan_percent_income','cb_person_cred_hist_length']
df_model = df[features + ['bad_flag']].dropna()

print('Step 2: WoE binning...')
bins = sc.woebin(df_model, y='bad_flag', x=features, ignore_const_cols=False)
df_woe = sc.woebin_ply(df_model, bins)

X = df_woe[[c for c in df_woe.columns if c.endswith('_woe')]]
y = df_woe['bad_flag']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print('Step 3: Training Logistic Regression...')
lr = LogisticRegression(C=0.1, max_iter=1000)
lr.fit(X_train, y_train)
auc = roc_auc_score(y_test, lr.predict_proba(X_test)[:,1])
print(f'Gini: {(2*auc-1):.4f}')

print('Step 4: Credit scorecard 300-850...')
card = sc.scorecard(bins, lr, X_train.columns.tolist())
scores = sc.scorecard_ply(df_model, card)
print(f'Score range: {scores.score.min():.0f} to {scores.score.max():.0f}')

print('Step 5: SHAP explainability...')
explainer = shap.LinearExplainer(lr, X_train)
shap_vals = explainer.shap_values(X_test.iloc[:500])
shap.summary_plot(shap_vals, X_test.iloc[:500], show=False)
plt.savefig('shap_feature_importance.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved shap_feature_importance.png')

joblib.dump({'model':lr,'bins':bins,'card':card,'features':features},
'models/scorecard_model.pkl')
print('Model saved to models/scorecard_model.pkl')