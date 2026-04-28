import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(page_title='Credit Risk Analyst Tool', layout='wide', page_icon='🏦')

st.markdown("""
<style>
.risk-header { background: #0d1b2a; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
.metric-card { background: #1e2433; padding: 15px; border-radius: 8px; border-left: 4px solid #00d4aa; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="risk-header"><h2 style="color:#00d4aa;margin:0">🏦 Credit Risk Analyst Platform</h2><p style="color:#94a3b8;margin:0">Internal Bank Risk Assessment Tool</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(['📋 Loan Application Assessment', '📊 Portfolio VaR', '📈 Risk Analytics'])

with tab1:
    st.markdown('### Applicant Information')
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('**Personal Details**')
        applicant_name = st.text_input('Applicant Name')
        age = st.number_input('Age', 18, 70, 30)
        employment_type = st.selectbox('Employment Type', [
            'Salaried - Government', 'Salaried - Private MNC',
            'Salaried - Private SME', 'Self-Employed Professional',
            'Business Owner', 'Freelancer/Consultant'
        ])
        employment_years = st.number_input('Years in Current Job', 0, 40, 2)
        residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Family Owned'])

    with c2:
        st.markdown('**Income Details**')
        loan_type = st.selectbox('Loan Type', ['Personal Loan', 'Home Loan', 'Business Loan', 'Vehicle Loan', 'Education Loan'])
        gross_monthly = st.number_input('Gross Monthly Income (Rs)', 10000, 2000000, 75000, step=5000)
        other_income = st.number_input('Other Monthly Income (Rs)', 0, 500000, 0, step=5000)
        existing_emi = st.number_input('Existing Monthly EMI (Rs)', 0, 500000, 0, step=1000)
        monthly_expenses = st.number_input('Monthly Living Expenses (Rs)', 5000, 500000, 20000, step=1000)

    with c3:
        st.markdown('**Loan Details**')
        loan_amount = st.number_input('Loan Amount Requested (Rs)', 10000, 50000000, 500000, step=10000)
        tenure_months = st.slider('Tenure (months)', 6, 360, 60)
        interest_rate = st.slider('Interest Rate (% p.a.)', 7.0, 24.0, 11.0, step=0.25)
        collateral = st.selectbox('Collateral Available', ['None', 'Property', 'Gold', 'FD/Shares', 'Vehicle'])
        collateral_value = st.number_input('Collateral Value (Rs)', 0, 100000000, 0, step=10000) if collateral != 'None' else 0

    st.markdown('### Credit History')
    ch1, ch2, ch3, ch4 = st.columns(4)
    with ch1:
        cibil_score = st.number_input('CIBIL Score', 300, 900, 720)
    with ch2:
        cred_hist_years = st.number_input('Credit History (years)', 0, 30, 4)
    with ch3:
        overdue = st.selectbox('Overdue Payments (12 months)', ['None', '1 instance', '2 instances', '3+ instances'])
    with ch4:
        loan_defaults = st.selectbox('Past Loan Defaults', ['None', '1 default', '2+ defaults'])

    if st.button('🔍 Assess Credit Risk', type='primary', use_container_width=True):

        # ── Calculations ──────────────────────────────────────────────
        r = interest_rate / 12 / 100
        new_emi = loan_amount * r * (1+r)**tenure_months / ((1+r)**tenure_months - 1) if r > 0 else loan_amount / tenure_months
        total_income = gross_monthly + other_income
        net_income = total_income * 0.78
        total_emi = existing_emi + new_emi
        foir = (total_emi / total_income) * 100
        lti = loan_amount / (total_income * 12)
        disposable = net_income - total_emi - monthly_expenses
        ltv = (loan_amount / collateral_value * 100) if collateral_value > 0 else 100

        # ── Scoring ───────────────────────────────────────────────────
        score = 0

        # CIBIL Score (30% weight)
        if cibil_score >= 800: score += 30
        elif cibil_score >= 750: score += 25
        elif cibil_score >= 700: score += 18
        elif cibil_score >= 650: score += 10
        elif cibil_score >= 600: score += 3
        else: score -= 15

        # FOIR (25% weight — industry max 50-55%)
        if foir <= 30: score += 25
        elif foir <= 40: score += 18
        elif foir <= 50: score += 10
        elif foir <= 60: score += 2
        else: score -= 20

        # Employment (15% weight)
        emp_map = {
            'Salaried - Government': 15,
            'Salaried - Private MNC': 13,
            'Salaried - Private SME': 9,
            'Self-Employed Professional': 7,
            'Business Owner': 5,
            'Freelancer/Consultant': 2
        }
        score += emp_map[employment_type]

        # Employment stability
        if employment_years >= 5: score += 8
        elif employment_years >= 3: score += 5
        elif employment_years >= 1: score += 2
        else: score -= 5

        # Overdue payments (15% weight)
        due_map = {'None': 15, '1 instance': 3, '2 instances': -8, '3+ instances': -20}
        score += due_map[overdue]

        # Defaults (10% weight)
        def_map = {'None': 10, '1 default': -15, '2+ defaults': -30}
        score += def_map[loan_defaults]

        # Collateral (5% weight)
        col_map = {'None': 0, 'Gold': 3, 'Vehicle': 2, 'FD/Shares': 4, 'Property': 5}
        score += col_map[collateral]

        # LTI adjustment
        if lti < 2: score += 5
        elif lti < 4: score += 0
        elif lti < 6: score -= 5
        else: score -= 15

        # Age adjustment
        if 25 <= age <= 50: score += 3
        elif age > 60: score -= 5

        # Residence
        if residence_type == 'Owned': score += 4
        elif residence_type == 'Family Owned': score += 2

        # Disposable income check
        if disposable < 0: score -= 20
        elif disposable < 5000: score -= 10
        elif disposable > 20000: score += 5

        # Normalize to 300-900
        raw = score
        final_score = int(300 + (raw / 130) * 600)
        final_score = max(300, min(900, final_score))

        grade = 'AAA' if final_score>=850 else 'AA' if final_score>=800 else 'A' if final_score>=750 else 'BBB' if final_score>=700 else 'BB' if final_score>=650 else 'B' if final_score>=600 else 'C' if final_score>=550 else 'D'
        risk_level = 'LOW' if final_score>=700 else 'MEDIUM' if final_score>=600 else 'HIGH'
        decision = 'APPROVE' if final_score>=700 else 'MANUAL REVIEW' if final_score>=600 else 'DECLINE'
        dec_color = 'green' if decision=='APPROVE' else 'orange' if decision=='MANUAL REVIEW' else 'red'

        st.markdown('---')
        st.markdown(f'### Assessment Result — {applicant_name if applicant_name else "Applicant"}')

        # Gauge
        g1, g2 = st.columns([1, 1])
        with g1:
            fig = go.Figure(go.Indicator(
                mode='gauge+number',
                value=final_score,
                title={'text': 'Credit Risk Score', 'font': {'size': 16}},
                gauge={
                    'axis': {'range': [300, 900]},
                    'steps': [
                        {'range': [300, 600], 'color': '#fee2e2'},
                        {'range': [600, 700], 'color': '#fef9c3'},
                        {'range': [700, 900], 'color': '#dcfce7'},
                    ],
                    'bar': {'color': '#00d4aa' if final_score>=700 else '#f59e0b' if final_score>=600 else '#ef4444'},
                    'threshold': {'line': {'color': 'white', 'width': 3}, 'value': final_score}
                }
            ))
            fig.update_layout(height=280, margin=dict(t=40, b=10))
            st.plotly_chart(fig, use_container_width=True)

        with g2:
            st.markdown(f'<h2 style="color:{dec_color}">Decision: {decision}</h2>', unsafe_allow_html=True)
            st.markdown(f'**Risk Grade:** {grade}')
            st.markdown(f'**Risk Level:** {risk_level}')
            st.markdown(f'**Loan Type:** {loan_type}')
            st.markdown(f'**Amount:** Rs {loan_amount:,.0f}')
            st.markdown(f'**Tenure:** {tenure_months} months @ {interest_rate}%')

        # Key metrics
        st.markdown('### Financial Ratios')
        km1, km2, km3, km4, km5 = st.columns(5)
        km1.metric('New EMI', f'Rs {new_emi:,.0f}', 'per month')
        km2.metric('FOIR', f'{foir:.1f}%', '✅ Safe' if foir<=50 else '⚠️ High')
        km3.metric('Loan-to-Income', f'{lti:.2f}x', '✅ OK' if lti<=4 else '⚠️ High')
        km4.metric('Monthly Surplus', f'Rs {disposable:,.0f}', '✅ Positive' if disposable>0 else '❌ Negative')
        km5.metric('LTV Ratio', f'{ltv:.0f}%' if collateral != 'None' else 'No Collateral', '✅ Good' if ltv<=80 else '⚠️ High')

        # Risk factors
        st.markdown('### Risk Factor Summary')
        rf1, rf2 = st.columns(2)
        with rf1:
            st.markdown('**Positive Factors**')
            if cibil_score >= 700: st.success(f'✅ Good CIBIL Score: {cibil_score}')
            if foir <= 50: st.success(f'✅ FOIR within limit: {foir:.1f}%')
            if overdue == 'None': st.success('✅ No overdue payments')
            if loan_defaults == 'None': st.success('✅ No past defaults')
            if collateral != 'None': st.success(f'✅ Collateral available: {collateral}')
            if employment_years >= 3: st.success(f'✅ Stable employment: {employment_years} years')
            if disposable > 0: st.success(f'✅ Positive disposable income: Rs {disposable:,.0f}')

        with rf2:
            st.markdown('**Risk Factors**')
            if cibil_score < 650: st.error(f'❌ Low CIBIL Score: {cibil_score}')
            if foir > 50: st.error(f'❌ High FOIR: {foir:.1f}% (max 50%)')
            if overdue != 'None': st.warning(f'⚠️ Overdue payments: {overdue}')
            if loan_defaults != 'None': st.error(f'❌ Past defaults: {loan_defaults}')
            if disposable < 0: st.error(f'❌ Negative disposable income: Rs {disposable:,.0f}')
            if lti > 5: st.warning(f'⚠️ High loan-to-income: {lti:.2f}x')
            if employment_years < 1: st.warning('⚠️ Less than 1 year in current job')

with tab2:
    st.subheader('Portfolio Value at Risk — NIFTY50')
    st.image('efficient_frontier.png', caption='10K Monte Carlo Simulations — Efficient Frontier')
    st.image('shap_feature_importance.png', caption='SHAP Feature Importance — Credit Model')

with tab3:
    st.subheader('Risk Analytics — SQL Insights')
    st.markdown('### Key Findings from 32,581 Loan Records')

    data = {
        'Income Group': ['Quintile 1 (Lowest)', 'Quintile 2', 'Quintile 3', 'Quintile 4', 'Quintile 5 (Highest)'],
        'Default Rate %': [43.62, 22.74, 19.03, 14.55, 9.13]
    }
    df = pd.DataFrame(data)
    fig1 = px.bar(df, x='Income Group', y='Default Rate %', color='Default Rate %',
                  color_continuous_scale='RdYlGn_r', title='Default Rate by Income Group')
    st.plotly_chart(fig1, use_container_width=True)

    data2 = {
        'Rate Band': ['Prime (<8%)', 'Standard (8-12%)', 'Sub-Prime (12-16%)', 'High Risk (16%+)'],
        'Default Rate %': [9.40, 15.66, 31.23, 36.67]
    }
    df2 = pd.DataFrame(data2)
    fig2 = px.bar(df2, x='Rate Band', y='Default Rate %', color='Default Rate %',
                  color_continuous_scale='RdYlGn_r', title='Default Rate by Interest Rate Band')
    st.plotly_chart(fig2, use_container_width=True)