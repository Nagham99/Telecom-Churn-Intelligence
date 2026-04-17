import streamlit as st

dashboard_page = st.Page("app3.py", title="Dashboard", icon="📊", default=True)
prediction_page = st.Page("prediction.py", title="Churn Prediction", icon="🤖")


pg = st.navigation([dashboard_page, prediction_page])

st.set_page_config(page_title="Telecom Intelligence", layout="wide")

pg.run()
