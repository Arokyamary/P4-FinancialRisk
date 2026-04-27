import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='Financial Risk Analytics', layout='wide')
st.title('Financial Risk Analytics Platform')

tab1, tab2 = st.tabs(['Credit Risk Scorecard', 'Portfolio VaR'])

with tab1:
    st.subheader('Loan Applicant Risk Scorer')
    col1, col2 = st.columns(2)
    with col1:
        loan_amt = st.number_input('Loan Amount (Rs)', 1000, 5000000, 10000, step=1000)
        income = st.number_input('Annual Income (Rs)', 10000, 10000000, 10000, step=10000)
        int_rate = st.slider('Interest Rate (%)', 5.0, 25.0, 11.0, step=0.5)
    with col2:
        lti = st.slider('Loan-to-Income Ratio', 0.05, 0.90, 0.30, step=0.05)
        cred_hist = st.number_input('Credit History Length (years)', 0, 30, 5)

    if st.button('Calculate Risk Score', type='primary'):
        risk_pct = min(max(int_rate * lti * 3, 5), 95)
        score = int(850 - risk_pct * 5)
        grade = 'A' if score>750 else 'B' if score>700 else 'C' if score>650 else 'D' if score>600 else 'E'
        fig = go.Figure(go.Indicator(
            mode='gauge+number', value=score, title={'text':'Credit Score'},
            gauge={'axis':{'range':[300,850]},
            'bar':{'color':'#00d4aa' if score>700 else '#f59e0b' if score>600 else '#f87171'}}
        ))
        fig.update_layout(template='plotly_dark', height=300)
        st.plotly_chart(fig, use_container_width=True)
        st.metric('Grade', grade)
        if score > 700: st.success('LOW RISK — Approve')
        elif score > 600: st.warning('MEDIUM RISK — Review')
        else: st.error('HIGH RISK — Decline')

with tab2:
    st.subheader('Portfolio Value at Risk')
    st.image('efficient_frontier.png', caption='10K Monte Carlo Simulations — NIFTY50 Portfolio')
    s