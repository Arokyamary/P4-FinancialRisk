import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:admin123@localhost:5432/financial_risk')
df = pd.read_csv('data/loan_data.csv')
df['bad_flag'] = (df['loan_status'] == 1).astype(int)
df.rename(columns={'cb_person_cred_hist_length': 'cred_hist_length'}, inplace=True)
cols = ['loan_amnt','person_income','loan_int_rate','loan_percent_income','cred_hist_length','bad_flag']
df[cols].to_sql('loan_applications', engine, if_exists='replace', index=False)
print('Loaded', len(df), 'records')