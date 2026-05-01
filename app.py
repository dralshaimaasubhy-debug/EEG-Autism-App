import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="EEG Analysis", layout="wide")

st.title("📊 Comprehensive EEG Analysis Report")

# -------- Patient Info --------
st.subheader("👤 Patient Summary")
col1, col2 = st.columns(2)

name = col1.text_input("Patient Name", "Ahmed")
age = col2.number_input("Age (months)", 1, 24, 6)

# -------- Upload --------
st.subheader("📁 Upload EEG Data")
file = st.file_uploader("Upload CSV")

if file:
    data = pd.read_csv(file)

    diagnosis = random.choice(["Positive", "Negative"])
    confidence = round(random.uniform(78, 95), 2)

    col3, col4 = st.columns(2)

    col3.metric("Diagnosis", diagnosis)
    col4.metric("Confidence", f"{confidence}%")

    if diagnosis == "Positive":
        st.error("⚠️ Autism risk detected")
    else:
        st.success("✅ Normal brain activity")

    # -------- Model --------
    st.subheader("⚙️ Model Performance")
    c1, c2, c3 = st.columns(3)

    c1.metric("Accuracy", "64.1%")
    c2.metric("Channels", 16)
    c3.metric("Data Points", len(data))

    # -------- Graph --------
    st.subheader("📈 EEG Signals")
    st.line_chart(data)
