import streamlit as st
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.title("📊 Naive Bayes Model Evaluation")

# --- דיוק המודל ---
st.header("✅ Model Accuracy")
try:
    response = requests.get(f"{API_URL}/evaluation")
    if response.status_code == 200:
        result = response.json()
        st.metric("Accuracy", f"{result['accuracy_percent']:.2f}%")
        st.write("Correct Predictions:", result['correct'])
        st.write("Incorrect Predictions:", result['incorrect'])
    else:
        st.error("Failed to fetch accuracy data.")
except Exception as e:
    st.error(f"Error connecting to API: {e}")

# --- Confusion Matrix ---
st.header("🔍 Confusion Matrix")
try:
    response = requests.get(f"{API_URL}/confusion_matrix")
    if response.status_code == 200:
        cm_dict = response.json()
        cm_df = pd.DataFrame(cm_dict)
        st.dataframe(cm_df)

        # מציג תרשים heatmap
        fig, ax = plt.subplots()
        sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues", ax=ax)
        plt.ylabel("True Label")
        plt.xlabel("Predicted Label")
        st.pyplot(fig)
    else:
        st.error("Failed to fetch confusion matrix.")
except Exception as e:
    st.error(f"Error connecting to API: {e}")
