import streamlit as st
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


# Load the saved model
with open('cls.sav', 'rb') as f:
    model = pickle.load(f)

# Load the scaler
# Assuming you saved the scaler as well, otherwise you'll need to fit it again on the original training data
# For this example, I'll assume you saved it as 'scaler.sav'
# with open('scaler.sav', 'rb') as f:
#     scaler = pickle.load(f)

# If you didn't save the scaler, you need to re-fit it on the original training data.
# You'll need to load your original data (df) and fit the scaler like this:
# std = StandardScaler()
# X = df.drop('churn', axis=1)
# std.fit(X)


st.title('Bank Customer Churn Prediction')

st.sidebar.header('Customer Data')

# Collect user input
def user_input_features():
    credit_score = st.sidebar.slider('Credit Score', 350, 850, 600)
    country = st.sidebar.selectbox('Country', ('France', 'Germany', 'Spain'))
    gender = st.sidebar.selectbox('Gender', ('Female', 'Male'))
    age = st.sidebar.slider('Age', 18, 92, 40)
    tenure = st.sidebar.slider('Tenure (years)', 0, 10, 5)
    balance = st.sidebar.number_input('Balance', value=0.0)
    products_number = st.sidebar.slider('Number of Products', 1, 4, 2)
    credit_card = st.sidebar.selectbox('Has Credit Card', ('No', 'Yes'))
    active_member = st.sidebar.selectbox('Is Active Member', ('No', 'Yes'))
    estimated_salary = st.sidebar.number_input('Estimated Salary', value=0.0)

    data = {
        'credit_score': credit_score,
        'country': country,
        'gender': gender,
        'age': age,
        'tenure': tenure,
        'balance': balance,
        'products_number': products_number,
        'credit_card': 1 if credit_card == 'Yes' else 0,
        'active_member': 1 if active_member == 'Yes' else 0,
        'estimated_salary': estimated_salary
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# Map categorical features to numerical as done in training
country_mapping = {'France': 0, 'Germany': 1, 'Spain': 2}
gender_mapping = {'Female': 0, 'Male': 1}

input_df['country'] = input_df['country'].map(country_mapping)
input_df['gender'] = input_df['gender'].map(gender_mapping)

# Standardize the input data
# Use the same scaler fitted on the training data
# If you didn't save the scaler, you need to re-fit it on the original training data (X) before this step.
# For now, I'll use a placeholder if the scaler wasn't loaded:
try:
    sc = std.transform(input_df)
except NameError:
    st.warning("Scaler not loaded. Please ensure you have saved and loaded the StandardScaler or re-fit it on your training data.")
    # As a fallback for demonstration, you might re-fit the scaler here if you have access to the original training data (X)
    # std = StandardScaler()
    # X = ... # Load your original training data X here
    # std.fit(X)
    # sc = std.transform(input_df)
    sc = input_df.values # Fallback: use raw values if scaler is not available - this is not ideal for accurate predictions


# Make prediction
prediction = model.predict(sc)
prediction_proba = model.predict_proba(sc)

st.subheader('Prediction')
churn_status = 'Can be Churn' if prediction[0] == 1 else 'No Churn'
st.write(churn_status)

st.subheader('Prediction Probability')
st.write(f"Probability of No Churn: {prediction_proba[0][0]:.4f}")
st.write(f"Probability of Churn: {prediction_proba[0][1]:.4f}")