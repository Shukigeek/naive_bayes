import streamlit as st
import requests
from fetch_model_data.fetch_options import GetOptions

URL_PREDICT = "http://127.0.0.1:8001/prediction"


features_info = GetOptions().options
def predict_single_row(features_info):
    st.subheader("Enter values for each feature:")
    user_input = {}

    for feature, allowed_vals in features_info.items():
        user_input[feature] = st.selectbox(f"{feature}", allowed_vals)

    if st.button("Predict"):
        res = requests.post(URL_PREDICT, json=user_input)
        if res.ok:
            prediction = res.json().get("prediction")
            st.success(f"✅ Prediction result: {prediction}")
        else:
            st.error("❌ Failed to send request to the prediction server.")



st.set_page_config(page_title="Prediction App", layout="centered", page_icon="🤖")

st.title("🤖 Machine Learning Prediction App")

predict_single_row(features_info)
