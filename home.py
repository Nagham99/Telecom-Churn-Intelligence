import streamlit as st

# Define the pages
dashboard_page = st.Page("app3.py", title="Dashboard", icon="📊", default=True)
prediction_page = st.Page("prediction.py", title="Churn Prediction", icon="🤖")

# Initialize Navigation
pg = st.navigation([dashboard_page, prediction_page])

# Shared Page Config (so you don't repeat it in every file)
st.set_page_config(page_title="Telecom Intelligence", layout="wide")

# Run the selected page
pg.run()
