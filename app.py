import streamlit as st
import pandas as pd
import joblib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# ✅ إعداد الصفحة
st.set_page_config(page_title="EEG Analysis", layout="wide")

# ✅ تصميم مستشفى
st.markdown("""
<style>
body {background-color: #f4f8fb;}
h1 {color: #1b7f5f; text-align: center;}
h2, h3 {color: #2e7d32;}
.stMetric {background-color: #e8f5e9; padding: 10px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# ✅ العنوان
st.title("📊 EEG Autism Detection Report")

# ✅ بيانات المريض
col1, col2 = st.columns(2)
name = col1.text_input("Patient Name", "Ahmed")
age = col2.number_input("Age (months)", 1, 24, 6)

# ✅ رفع الملف
file = st.file_uploader("📁 Upload EEG CSV")

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

# ✅ تشغيل النظام
if file:
    try:
        # ✅ حل مشكلة encoding
        data = pd.read_csv(file, encoding='latin1')

        # ✅ حذف الليبل لو موجود
        if "autism" in data.columns:
            data = data.drop(columns=["autism"])

        # ✅ اختيار الأعمدة الرقمية فقط (أهم سطر)
        data = data.select_dtypes(include=['number'])

        # ✅ تحميل الموديل
        model = joblib.load("autism_model.pkl")

        # ✅ التنبؤ
        pred = model.predict(data)
        prob = model.predict_proba(data)

        diagnosis = "Positive" if pred[0] == 1 else "Negative"
        confidence = round(max(prob[0]) * 100, 2)

        # ✅ عرض النتيجة
        col3, col4 = st.columns(2)
        col3.metric("Diagnosis", diagnosis)
        col4.metric("Confidence", f"{confidence}%")

        if diagnosis == "Positive":
            st.error("⚠️ Autism risk detected")
        else:
            st.success("✅ Normal brain activity")

        # ✅ معلومات إضافية
        st.subheader("Model Info")
        st.write("Model: Random Forest")
        st.write("Channels:", data.shape[1])
        st.write("Samples:", data.shape[0])

        # ✅ رسم
        st.subheader("📈 EEG Signals")
        st.line_chart(data)

        # ✅ PDF
        pdf_file = create_pdf(name, age, diagnosis, confidence)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "📄 Download Report",
                data=f,
                file_name="EEG_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error("⚠️ حصل خطأ في قراءة الملف - تأكدي إن CSV سليم")
