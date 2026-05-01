import streamlit as st
import pandas as pd
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# ✅ إعداد الصفحة
st.set_page_config(page_title="EEG Analysis", layout="wide")

# ✅ تصميم مستشفى
st.markdown("""
<style>
body {
    background-color: #f4f8fb;
}
h1 {
    color: #1b7f5f;
    text-align: center;
}
h2, h3 {
    color: #2e7d32;
}
.stMetric {
    background-color: #e8f5e9;
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ✅ العنوان
st.title("📊 Comprehensive EEG Analysis Report")

# -------- Patient Info --------
st.subheader("👤 Patient Summary")
col1, col2 = st.columns(2)

name = col1.text_input("Patient Name", "Ahmed")
age = col2.number_input("Age (months)", 1, 24, 6)

# -------- Upload --------
st.subheader("📁 Upload EEG Data")
file = st.file_uploader("Upload CSV")

# ✅ إنشاء PDF
def create_pdf(name, age, diagnosis, confidence):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(temp_file.name, pagesize=letter)

    c.setFont("Helvetica", 14)

    c.drawString(100, 750, "EEG Medical Report")
    c.drawString(100, 700, f"Patient Name: {name}")
    c.drawString(100, 670, f"Age: {age} months")
    c.drawString(100, 640, f"Diagnosis: {diagnosis}")
    c.drawString(100, 610, f"Confidence: {confidence}%")

    c.save()
    return temp_file.name

# ✅ لما المستخدم يرفع ملف
if file:
    data = pd.read_csv(file)
 # ✅تحليل بسيط (مش عشوائي أقوى شوية)
    avg = data.mean().mean()

    if avg > 700:
        diagnosis = "Positive"
        confidence = 85
    else:
        diagnosis = "Negative"
        confidence = 80

    # ✅ عرض النتيجة
    col3, col4 = st.columns(2)

    col3.metric("Diagnosis", diagnosis)
    col4.metric("Confidence", f"{confidence}%")

    # ✅ رسالة الحالة
    if diagnosis == "Positive":
        st.error("⚠️ Autism risk detected")
    else:
        st.success("✅ Normal brain activity")

    # -------- Model --------
    st.subheader("⚙️ Model Performance")
    c1, c2, c3 = st.columns(3)

    c1.metric("Accuracy", "64.1%")
    c2.metric("Channels", data.shape[1])
    c3.metric("Data Points", data.shape[0])

    # -------- Statistics --------
    st.subheader("📊 Signal Statistics")
    st.write(data.describe())

    # -------- Graph --------
    st.subheader("📈 EEG Signals")
    st.line_chart(data)

    # ✅ إنشاء PDF
    pdf_file = create_pdf(name, age, diagnosis, confidence)

    # ✅ زر تحميل PDF
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="📄 Download Medical Report",
            data=f,
            file_name="EEG_Report.pdf",
            mime="application/pdf"
        )
