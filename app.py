import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='Financial Risk Analytics', layout='wide')
st.title('Financial Risk Analytics Platform')

tab1, tab2 = st.tabs(['Credit Risk Scorecard', 'Portfolio VaR'])

# ------------------- TAB 1 -------------------
with tab1:
    st.subheader('Loan Applicant Risk Scorer')

    col1, col2 = st.columns(2)

    with col1:
        loan_amt = st.number_input('Loan Amount (Rs)', 1000, 50000000, 500000, step=10000)
        income = st.number_input('Annual Income (Rs)', 10000, 10000000, 500000, step=10000)
        int_rate = st.slider('Interest Rate (%)', 5.0, 25.0, 11.0, step=0.5)

    with col2:
        cred_hist = st.number_input('Credit History Length (years)', 0, 30, 5)

    if st.button('Calculate Risk Score', type='primary'):

        # --- Derived Metrics ---
        if income > 0:
            actual_lti = loan_amt / income
        else:
            actual_lti = 10  # extreme risk fallback

        # --- Risk Components ---

        # 1. Loan-to-Income Risk (0–40)
        if actual_lti < 2:
            lti_risk = 5
        elif actual_lti < 5:
            lti_risk = 15
        elif actual_lti < 10:
            lti_risk = 30
        else:
            lti_risk = 40

        # 2. Credit History Risk (0–25)
        if cred_hist >= 10:
            hist_risk = 5
        elif cred_hist >= 5:
            hist_risk = 10
        elif cred_hist >= 2:
            hist_risk = 18
        else:
            hist_risk = 25

        # 3. Interest Rate Risk (0–20)
        if int_rate < 10:
            rate_risk = 5
        elif int_rate < 15:
            rate_risk = 10
        elif int_rate < 20:
            rate_risk = 15
        else:
            rate_risk = 20

        # 4. Income Adequacy (0–15)
        if income >= loan_amt * 0.5:
            income_risk = 5
        elif income >= loan_amt * 0.2:
            income_risk = 10
        else:
            income_risk = 15

        # --- Total Risk ---
        total_risk = lti_risk + hist_risk + rate_risk + income_risk

        # --- Credit Score ---
        score = int(850 - total_risk * 5.5)
        score = max(300, min(850, score))

        # --- Grade ---
        if score > 750:
            grade = 'A'
        elif score > 700:
            grade = 'B'
        elif score > 650:
            grade = 'C'
        elif score > 600:
            grade = 'D'
        else:
            grade = 'E'

        # --- Gauge Chart ---
        fig = go.Figure(go.Indicator(
            mode='gauge+number',
            value=score,
            title={'text': 'Credit Score'},
            gauge={
                'axis': {'range': [300, 850]},
                'bar': {
                    'color': '#00d4aa' if score > 700 else '#f59e0b' if score > 600 else '#f87171'
                }
            }
        ))

        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

        # --- Output ---
        st.metric('Grade', grade)
        st.write(f"Loan-to-Income Ratio: {actual_lti:.2f}")
        st.write(f"Risk Score: {total_risk}/100")

        # --- Decision ---
        if score > 700:
            st.success('LOW RISK — Approve')
        elif score > 600:
            st.warning('MEDIUM RISK — Review')
        else:
            st.error('HIGH RISK — Decline')


# ------------------- TAB 2 -------------------
with tab2:
    st.subheader('Portfolio Value at Risk')
    st.image('efficient_frontier.png', caption='10K Monte Carlo Simulations — Portfolio')
    st.image('shap_feature_importance.png', caption='Feature Importance')