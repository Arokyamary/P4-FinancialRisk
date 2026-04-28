import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='Financial Risk Analytics', layout='wide')
st.title('Financial Risk Analytics Platform')

tab1, tab2 = st.tabs(['Credit Risk Scorecard', 'Portfolio VaR'])

with tab1:
    st.subheader('Loan Applicant Risk Scorer')

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('#### Loan Details')
        loan_amt = st.number_input('Loan Amount (Rs)', 1000, 5000000, 200000, step=1000)
        loan_tenure = st.slider('Loan Tenure (months)', 6, 360, 60)
        int_rate = st.slider('Interest Rate (% per annum)', 5.0, 25.0, 11.0, step=0.5)

    with col2:
        st.markdown('#### Applicant Profile')
        gross_income = st.number_input('Gross Monthly Income (Rs)', 10000, 1000000, 50000, step=5000)
        existing_emi = st.number_input('Existing Monthly EMI Obligations (Rs)', 0, 500000, 0, step=1000)
        employment_type = st.selectbox('Employment Type', ['Salaried', 'Self-Employed', 'Business Owner', 'Freelancer'])
        cred_hist = st.slider('Credit History Length (years)', 0, 30, 3)
        due_payments = st.selectbox('Any Overdue Payments in Last 12 Months?', ['No', 'Yes - 1 time', 'Yes - 2 times', 'Yes - 3+ times'])

    # Auto calculations
    monthly_rate = int_rate / 12 / 100
    if monthly_rate > 0:
        new_emi = loan_amt * monthly_rate * (1 + monthly_rate)**loan_tenure / ((1 + monthly_rate)**loan_tenure - 1)
    else:
        new_emi = loan_amt / loan_tenure

    net_income = gross_income * 0.75  # approx 25% deductions
    total_emi = existing_emi + new_emi
    foir = (total_emi / gross_income) * 100  # Fixed Obligation to Income Ratio
    lti = loan_amt / (gross_income * 12)

    st.markdown('---')
    m1, m2, m3, m4 = st.columns(4)
    m1.metric('New EMI (Rs/month)', f'{new_emi:,.0f}')
    m2.metric('Net Monthly Income (Rs)', f'{net_income:,.0f}')
    m3.metric('FOIR %', f'{foir:.1f}%', delta='Good' if foir < 50 else 'High')
    m4.metric('Loan-to-Income Ratio', f'{lti:.2f}', delta='Safe' if lti < 3 else 'Risky')

    if st.button('Calculate Risk Score', type='primary'):

        # Realistic scoring logic
        score = 750  # base score

        # FOIR impact (most important — industry standard max 50%)
        if foir < 30:
            score += 50
        elif foir < 40:
            score += 20
        elif foir < 50:
            score -= 10
        elif foir < 60:
            score -= 50
        else:
            score -= 120

        # Interest rate impact
        if int_rate < 10:
            score += 30
        elif int_rate < 14:
            score += 10
        elif int_rate < 18:
            score -= 20
        else:
            score -= 60

        # Credit history impact
        if cred_hist >= 7:
            score += 40
        elif cred_hist >= 4:
            score += 20
        elif cred_hist >= 2:
            score += 0
        else:
            score -= 40

        # Employment type impact
        emp_score = {'Salaried': 30, 'Business Owner': 10, 'Self-Employed': 0, 'Freelancer': -20}
        score += emp_score[employment_type]

        # Overdue payments impact
        due_score = {'No': 20, 'Yes - 1 time': -30, 'Yes - 2 times': -80, 'Yes - 3+ times': -150}
        score += due_score[due_payments]

        # LTI impact
        if lti < 2:
            score += 20
        elif lti < 4:
            score += 0
        elif lti < 6:
            score -= 30
        else:
            score -= 70

        score = max(300, min(900, score))

        grade = 'A' if score > 750 else 'B' if score > 700 else 'C' if score > 650 else 'D' if score > 600 else 'E'

        fig = go.Figure(go.Indicator(
            mode='gauge+number',
            value=score,
            title={'text': 'Credit Score'},
            gauge={
                'axis': {'range': [300, 900]},
                'steps': [
                    {'range': [300, 600], 'color': '#fee2e2'},
                    {'range': [600, 700], 'color': '#fef9c3'},
                    {'range': [700, 900], 'color': '#dcfce7'},
                ],
                'bar': {'color': '#00d4aa' if score > 700 else '#f59e0b' if score > 600 else '#ef4444'}
            }
        ))
        fig.update_layout(template='plotly_dark', height=320)
        st.plotly_chart(fig, use_container_width=True)

        r1, r2 = st.columns(2)
        r1.metric('Credit Grade', grade)
        r2.metric('Monthly Surplus After EMI', f'Rs {net_income - total_emi:,.0f}')

        if score > 700:
            st.success('LOW RISK — Loan Approved')
        elif score > 600:
            st.warning('MEDIUM RISK — Needs Manual Review')
        else:
            st.error('HIGH RISK — Loan Declined')

        # Breakdown
        st.markdown('#### Score Breakdown')
        b1, b2, b3 = st.columns(3)
        b1.info(f'FOIR: {foir:.1f}% (max 50% is safe)')
        b2.info(f'Total EMI Burden: Rs {total_emi:,.0f}/month')
        b3.info(f'Loan-to-Annual Income: {lti:.2f}x')

with tab2:
    st.subheader('Portfolio Value at Risk')
    st.image('efficient_frontier.png', caption='10K Monte Carlo Simulations — NIFTY50 Portfolio')
    st.image('shap_feature_importance.png', caption='SHAP Feature Importance')