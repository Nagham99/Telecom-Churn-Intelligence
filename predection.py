import streamlit as st
import pandas as pd
import joblib

def run_prediction_page():
    st.title("🤖 ML Churn Prediction")

    # 1. Load the saved model and encoders
    @st.cache_resource
    def load_ml_assets():
        model = joblib.load('churn_model.pkl')
        encoders = joblib.load('encoders.pkl')
        return model, encoders

    model, encoders = load_ml_assets()

    # 2. User Inputs (Features)
    st.subheader("Enter Customer Details")
    
    col1, col2 = st.columns(2)
    with col1:
        tenure = st.slider("Tenure in Months", 0, 72, 12)
        monthly_charge = st.number_input("Monthly Charge ($)", 0.0, 200.0, 70.0)
        referrals = st.number_input("Number of Referrals", 0, 20, 0)
    
    with col2:
        # These MUST match the options in your training data
        contract = st.selectbox("Contract Type", ["Month-to-Month", "One Year", "Two Year"])
        internet = st.selectbox("Internet Type", ["Fiber Optic", "DSL", "Cable", "None"])

    # 3. Prediction Trigger
    if st.button("Calculate Churn Risk"):
        # Create a dataframe for the input
        input_df = pd.DataFrame([{
            'tenure_in_months': tenure,
            'contract': contract,
            'monthly_charge': monthly_charge,
            'number_of_referrals': referrals,
            'internet_type': internet
        }])

        # Apply the SAME encoding we did in Jupyter
        for col, le in encoders.items():
            input_df[col] = le.transform(input_df[col])

        # Get Probability
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1] * 100

        # 4. Display Result
        st.divider()
        if prediction == 1:
            st.error(f"### 🚩 High Risk: {probability:.1f}% probability of Churn")
            st.write("This customer matches the 'Danger Zone' profile.")
        else:
            st.success(f"### ✅ Low Risk: {probability:.1f}% probability of Churn")
            st.write("This customer is likely to stay loyal.")

run_prediction_page()