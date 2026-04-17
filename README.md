## 🚀 Telecom Customer Churn Intelligence Dashboard
This project is a comprehensive End-to-End Data Science & Analytics solution designed to identify, analyze, and predict customer churn for a telecommunications provider. It features an interactive Streamlit dashboard with high-level EDA (Exploratory Data Analysis) and a Machine Learning prediction engine.
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]https://telecom-churn-intelligence-6vmdtoq2aurl4mxkfq6fuc.streamlit.app/)
## 📊 Project Overview
The primary goal was to uncover why customers leave and build a tool that allows business stakeholders to predict churn risk for individual accounts.

Key Business Discovery: During analysis, I identified a "Referral Loyalty Loop"—customers who refer at least one friend are 50% less likely to churn, suggesting that brand advocacy is a stronger retention tool than price discounts.

## 🛠️ Tech Stack
Analysis & ML: Python (Pandas, NumPy, Scikit-Learn)

Visualizations: Plotly Express (Interactive), Seaborn, Matplotlib

Web Framework: Streamlit (Multipage App)

Models: Random Forest Classifier (current), XGBoost (experimental)


## 🛠️ Tech Stack
Analysis & ML: Python (Pandas, NumPy, Scikit-Learn)

Visualizations: Plotly Express (Interactive), Seaborn, Matplotlib

Web Framework: Streamlit (Multipage App)

Models: Random Forest Classifier (current), XGBoost (experimental)

## 📈 Features
1. Executive Dashboard (EDA)
Churn Segmentation: Analysis of churn by contract type, internet service, and demographics.

Referral Impact: A deep dive into how "Brand Ambassadors" stay loyal compared to non-referrers.

Revenue Analysis: Tracking the financial impact of customer status changes.

2. ML Prediction Engine
Interactive Inputs: Adjust tenure, contract type, and monthly charges to see real-time risk scores.

Probability Mapping: Provides a percentage-based churn risk rather than a simple Yes/No.

