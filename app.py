import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Credit Risk Analyst Tool', layout='wide', page_icon='🏦')

st.markdown("""
<style>
.main { background-color: #f8fafc; }
.stTabs [data-baseweb="tab-list"] { background-color: #0d1b2a; border-radius: 8px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #94a3b8; }
.stTabs [aria-selected="true"] { color: #00d4aa !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:#0d1b2a;padding:20px;border-radius:8px;margin-bottom:20px">
<h2 style="color:#00d4aa;margin:0">🏦 Credit Risk Analyst Platform</h2>
<p style="color:#94a3b8;margin:4px 0 0 0">Internal Bank Risk Assessment Tool — All Loan Types</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(['📋 Loan Application Assessment', '📊 Portfolio VaR', '📈 Risk Analytics'])

with tab1:
    st.markdown('### Step 1 — Applicant Personal Details')
    c1, c2, c3 = st.columns(3)

    with c1:
        applicant_name = st.text_input('Applicant Full Name')
        age = st.number_input('Age', 21, 65, 32)
        pan_number = st.text_input('PAN Number (e.g. ABCDE1234F)')
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Family Owned', 'Company Provided'])
        dependents = st.number_input('Number of Dependents', 0, 10, 1)

    with c2:
        employment_type = st.selectbox('Employment Type', [
            'Salaried — Government/PSU',
            'Salaried — Private MNC',
            'Salaried — Private SME',
            'Self-Employed Professional (Doctor/CA/Lawyer)',
            'Business Owner',
            'Freelancer / Consultant'
        ])
        employer_name = st.text_input('Employer / Business Name')
        employment_years = st.number_input('Total Work Experience (years)', 0, 40, 4)
        current_job_years = st.number_input('Years in Current Job/Business', 0, 40, 2)
        industry = st.selectbox('Industry Sector', [
            'IT/Software', 'Banking/Finance', 'Healthcare',
            'Manufacturing', 'Education', 'Government',
            'Real Estate', 'Retail/Trading', 'Other'
        ])

    with c3:
        loan_type = st.selectbox('Loan Type', [
            'Personal Loan', 'Home Loan', 'Vehicle Loan',
            'Business Loan', 'Education Loan', 'Loan Against Property'
        ])
        loan_amount = st.number_input('Loan Amount Requested (Rs)', 10000, 100000000, 500000, step=10000)
        tenure_months = st.slider('Loan Tenure (months)', 6, 360, 60)
        interest_rate = st.slider('Rate of Interest (% p.a.)', 7.0, 24.0, 11.5, step=0.25)
        loan_purpose = st.text_input('Purpose of Loan')

    st.markdown('### Step 2 — Income & Financial Details')
    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown('**Monthly Income**')
        gross_monthly = st.number_input('Gross Monthly Salary/Income (Rs)', 10000, 5000000, 80000, step=5000)
        other_income = st.number_input('Other Monthly Income (Rs)', 0, 1000000, 0, step=5000)
        annual_bonus = st.number_input('Annual Bonus/Incentive (Rs)', 0, 5000000, 0, step=10000)

    with f2:
        st.markdown('**Monthly Obligations**')
        existing_emi = st.number_input('Total Existing EMI per Month (Rs)', 0, 500000, 0, step=1000)
        monthly_expenses = st.number_input('Monthly Living Expenses (Rs)', 5000, 500000, 25000, step=1000)
        insurance_premium = st.number_input('Monthly Insurance Premium (Rs)', 0, 50000, 0, step=500)

    with f3:
        st.markdown('**Assets & Collateral**')
        collateral = st.selectbox('Collateral Type', [
            'None', 'Residential Property', 'Commercial Property',
            'Gold', 'Fixed Deposit', 'Shares/MF', 'Vehicle'
        ])
        collateral_value = st.number_input('Collateral Market Value (Rs)', 0, 100000000, 0, step=50000) if collateral != 'None' else 0
        bank_balance = st.number_input('Average Bank Balance (Rs)', 0, 10000000, 50000, step=10000)
        existing_loans = st.number_input('Number of Active Loans', 0, 10, 0)

    st.markdown('### Step 3 — Credit Bureau Information')
    cb1, cb2, cb3, cb4 = st.columns(4)

    with cb1:
        cibil_score = st.number_input('CIBIL Score (from bureau report)', 300, 900, 725)
        st.caption('300–549: Poor | 550–649: Fair | 650–749: Good | 750–900: Excellent')

    with cb2:
        overdue_payments = st.selectbox('Overdue Payments (last 24 months)', [
            'None', '1–2 instances (30 days)', '3–4 instances (60 days)', '5+ instances / 90+ days'
        ])
        written_off = st.selectbox('Any Written-Off Accounts?', ['No', 'Yes — 1 account', 'Yes — 2+ accounts'])

    with cb3:
        past_defaults = st.selectbox('Past Loan Defaults', [
            'None', '1 default (resolved)', '1 default (unresolved)', '2+ defaults'
        ])
        credit_cards = st.number_input('Number of Credit Cards', 0, 20, 1)

    with cb4:
        credit_utilization = st.slider('Credit Card Utilization %', 0, 100, 30)
        cred_hist_years = st.number_input('Credit History Length (years)', 0, 30, 5)

    if st.button('🔍 Generate Risk Assessment', type='primary', use_container_width=True):

        r = interest_rate / 12 / 100
        new_emi = loan_amount * r * (1+r)**tenure_months / ((1+r)**tenure_months - 1) if r > 0 else loan_amount / tenure_months
        total_monthly_income = gross_monthly + other_income + (annual_bonus / 12)
        net_income = total_monthly_income * 0.78
        total_obligations = existing_emi + new_emi + insurance_premium
        foir = (total_obligations / total_monthly_income) * 100
        lti = loan_amount / (total_monthly_income * 12)
        disposable = net_income - total_obligations - monthly_expenses
        ltv = (loan_amount / collateral_value * 100) if collateral_value > 0 else 100
        dscr = (net_income - monthly_expenses) / new_emi if new_emi > 0 else 0

        score = 0

        if cibil_score >= 800: score += 25
        elif cibil_score >= 750: score += 20
        elif cibil_score >= 700: score += 14
        elif cibil_score >= 650: score += 8
        elif cibil_score >= 600: score += 3
        elif cibil_score >= 550: score -= 5
        else: score -= 15

        if foir <= 30: score += 20
        elif foir <= 40: score += 15
        elif foir <= 50: score += 8
        elif foir <= 55: score += 2
        elif foir <= 65: score -= 10
        else: score -= 20

        emp_pts = {
            'Salaried — Government/PSU': 15,
            'Salaried — Private MNC': 12,
            'Salaried — Private SME': 8,
            'Self-Employed Professional (Doctor/CA/Lawyer)': 9,
            'Business Owner': 6,
            'Freelancer / Consultant': 3
        }
        score += emp_pts[employment_type]
        if current_job_years >= 5: score += 5
        elif current_job_years >= 3: score += 3
        elif current_job_years >= 1: score += 1
        else: score -= 4

        due_pts = {'None': 15, '1–2 instances (30 days)': 6, '3–4 instances (60 days)': -4, '5+ instances / 90+ days': -15}
        score += due_pts[overdue_payments]

        def_pts = {'None': 10, '1 default (resolved)': -5, '1 default (unresolved)': -15, '2+ defaults': -25}
        score += def_pts[past_defaults]

        wo_pts = {'No': 5, 'Yes — 1 account': -10, 'Yes — 2+ accounts': -20}
        score += wo_pts[written_off]

        col_pts = {'None': 0, 'Fixed Deposit': 5, 'Residential Property': 5, 'Gold': 4, 'Shares/MF': 3, 'Commercial Property': 4, 'Vehicle': 2}
        score += col_pts[collateral]

        if dscr >= 2.0: score += 5
        elif dscr >= 1.5: score += 3
        elif dscr >= 1.2: score += 1
        elif dscr >= 1.0: score -= 2
        else: score -= 8

        if credit_utilization <= 30: score += 3
        elif credit_utilization <= 50: score += 1
        elif credit_utilization > 80: score -= 5

        if cred_hist_years >= 7: score += 3
        elif cred_hist_years >= 4: score += 1

        if residence_type == 'Owned': score += 3
        elif residence_type == 'Company Provided': score += 1

        if bank_balance >= loan_amount * 0.1: score += 2

        if disposable < 0: score -= 15
        elif disposable < 5000: score -= 5

        final_score = int(300 + ((score + 50) / 150) * 600)
        final_score = max(300, min(900, final_score))

        if final_score >= 850: grade = 'AAA'; risk = 'VERY LOW'
        elif final_score >= 800: grade = 'AA'; risk = 'LOW'
        elif final_score >= 750: grade = 'A'; risk = 'LOW'
        elif final_score >= 700: grade = 'BBB'; risk = 'MODERATE'
        elif final_score >= 650: grade = 'BB'; risk = 'MEDIUM'
        elif final_score >= 600: grade = 'B'; risk = 'MEDIUM-HIGH'
        elif final_score >= 550: grade = 'C'; risk = 'HIGH'
        else: grade = 'D'; risk = 'VERY HIGH'

        if final_score >= 700: decision = 'APPROVE'; dec_color = '#00d4aa'
        elif final_score >= 600: decision = 'MANUAL REVIEW'; dec_color = '#f59e0b'
        else: decision = 'DECLINE'; dec_color = '#ef4444'

        st.markdown('---')
        st.markdown(f'## Assessment Report — {applicant_name if applicant_name else "Applicant"}')

        g1, g2 = st.columns([1, 1])
        with g1:
            fig = go.Figure(go.Indicator(
                mode='gauge+number',
                value=final_score,
                title={'text': 'Credit Risk Score', 'font': {'size': 15}},
                gauge={
                    'axis': {'range': [300, 900], 'tickwidth': 1},
                    'steps': [
                        {'range': [300, 550], 'color': '#fee2e2'},
                        {'range': [550, 650], 'color': '#fef3c7'},
                        {'range': [650, 750], 'color': '#fef9c3'},
                        {'range': [750, 900], 'color': '#dcfce7'},
                    ],
                    'bar': {'color': dec_color},
                }
            ))
            fig.update_layout(height=300, margin=dict(t=50, b=10, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            st.markdown(f'<h1 style="color:{dec_color};font-size:36px">✦ {decision}</h1>', unsafe_allow_html=True)
            st.markdown(f'**Credit Grade:** {grade} &nbsp;&nbsp; **Risk Level:** {risk}')
            st.markdown(f'**Loan Type:** {loan_type}')
            st.markdown(f'**Amount:** Rs {loan_amount:,.0f} for {tenure_months} months @ {interest_rate}%')
            st.markdown(f'**New EMI:** Rs {new_emi:,.0f} / month')
            if collateral != 'None':
                st.markdown(f'**Collateral:** {collateral} — Rs {collateral_value:,.0f} (LTV: {ltv:.0f}%)')

        st.markdown('### Key Financial Ratios')
        km1, km2, km3, km4, km5 = st.columns(5)
        km1.metric('New EMI', f'Rs {new_emi:,.0f}', 'per month')
        km2.metric('FOIR', f'{foir:.1f}%', '✅ Safe' if foir <= 50 else '⚠️ Above Limit')
        km3.metric('DSCR', f'{dscr:.2f}x', '✅ Good' if dscr >= 1.5 else '⚠️ Low')
        km4.metric('Loan-to-Income', f'{lti:.1f}x', '✅ OK' if lti <= 4 else '⚠️ High')
        km5.metric('Monthly Surplus', f'Rs {disposable:,.0f}', '✅ Positive' if disposable > 0 else '❌ Negative')

        st.markdown('### Risk Factor Analysis')
        pos_col, neg_col = st.columns(2)

        with pos_col:
            st.markdown('**✅ Positive Factors**')
            if cibil_score >= 700: st.success(f'CIBIL Score: {cibil_score} — Good standing')
            if foir <= 50: st.success(f'FOIR {foir:.1f}% — Within RBI limit of 50%')
            if overdue_payments == 'None': st.success('No overdue payments in 24 months')
            if past_defaults == 'None': st.success('No past loan defaults')
            if written_off == 'No': st.success('No written-off accounts')
            if collateral != 'None': st.success(f'Collateral available: {collateral}')
            if current_job_years >= 3: st.success(f'Stable employment: {current_job_years} years')
            if dscr >= 1.5: st.success(f'Strong DSCR: {dscr:.2f}x')
            if disposable > 10000: st.success(f'Healthy surplus: Rs {disposable:,.0f}/month')
            if credit_utilization <= 30: st.success(f'Low credit utilization: {credit_utilization}%')

        with neg_col:
            st.markdown('**⚠️ Risk Factors**')
            if cibil_score < 650: st.error(f'Low CIBIL Score: {cibil_score}')
            if foir > 50: st.error(f'FOIR {foir:.1f}% exceeds RBI 50% guideline')
            if overdue_payments != 'None': st.warning(f'Overdue payments: {overdue_payments}')
            if past_defaults != 'None': st.error(f'Past defaults: {past_defaults}')
            if written_off != 'No': st.error(f'Written-off accounts: {written_off}')
            if disposable < 0: st.error(f'Negative monthly surplus: Rs {disposable:,.0f}')
            if lti > 5: st.warning(f'High loan-to-income ratio: {lti:.1f}x')
            if credit_utilization > 70: st.warning(f'High credit utilization: {credit_utilization}%')
            if existing_loans >= 3: st.warning(f'Multiple active loans: {existing_loans}')
            if current_job_years < 1: st.warning('Less than 1 year in current job')
            if dscr < 1.2: st.error(f'Low DSCR: {dscr:.2f}x — repayment concern')

        st.markdown('### CIBIL Score Reference Guide')
        st.dataframe(pd.DataFrame({
            'Score Range': ['750–900', '700–749', '650–699', '600–649', '550–599', '300–549'],
            'Rating': ['Excellent', 'Good', 'Fair', 'Below Average', 'Poor', 'Very Poor'],
            'Loan Decision': ['Approve — Best rates', 'Approve — Standard rates', 'Review — Higher rate', 'Careful review', 'Likely decline', 'Decline'],
            'Typical Interest Rate': ['7–9%', '9–11%', '12–15%', '16–18%', '20–24%', 'Not offered'],
        }), use_container_width=True, hide_index=True)

with tab2:
    st.subheader('Portfolio Value at Risk — NIFTY50 Analysis')
    col1, col2 = st.columns(2)
    with col1:
        st.image('efficient_frontier.png', caption='Efficient Frontier — 10K Monte Carlo Simulations')
    with col2:
        st.image('shap_feature_importance.png', caption='SHAP Feature Importance — Credit Model')
    st.markdown('### VaR Summary')
    v1, v2, v3 = st.columns(3)
    v1.metric('Historical VaR 95%', '-1.43%', 'Max daily loss on 1Cr portfolio')
    v2.metric('Max Daily Loss', 'Rs 1,43,000', 'On Rs 1 Crore portfolio')
    v3.metric('Optimal Sharpe Ratio', '1.00', 'Optimal Return: 17%')

with tab3:
    st.subheader('Risk Analytics — Insights from 32,581 Loan Records')
    df1 = pd.DataFrame({
        'Income Group': ['Quintile 1 (Lowest)', 'Quintile 2', 'Quintile 3', 'Quintile 4', 'Quintile 5 (Highest)'],
        'Default Rate %': [43.62, 22.74, 19.03, 14.55, 9.13]
    })
    fig1 = px.bar(df1, x='Income Group', y='Default Rate %', color='Default Rate %',
                  color_continuous_scale='RdYlGn_r', title='Default Rate by Income Group', text='Default Rate %')
    fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    df2 = pd.DataFrame({
        'Rate Band': ['Prime (<8%)', 'Standard (8–12%)', 'Sub-Prime (12–16%)', 'High Risk (16%+)'],
        'Default Rate %': [9.40, 15.66, 31.23, 36.67]
    })
    fig2 = px.bar(df2, x='Rate Band', y='Default Rate %', color='Default Rate %',
                  color_continuous_scale='RdYlGn_r', title='Default Rate by Interest Rate Band', text='Default Rate %')
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown('### Key Risk Thresholds')
    st.dataframe(pd.DataFrame({
        'Risk Factor': ['LTI Ratio > 0.52', 'Interest Rate > 16%', 'Income Quintile 1', 'FOIR > 60%'],
        'Default Rate': ['91.18%', '36.67%', '43.62%', 'Very High'],
        'Recommended Action': ['Decline or require collateral', 'Strict credit check mandatory', 'Require guarantor', 'Reject application']
    }), use_container_width=True, hide_index=True)