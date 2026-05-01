import streamlit as st
import pandas as pd
import joblib
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

# ================== إعداد الصفحة ==================
st.set_page_config(page_title="EEG Autism Detection", layout="wide")

st.markdown("""
<style>
body {background-color:#f4f8fb;}
h1 {color:#1b7f5f; text-align:center;}
.stMetric {background-color:#e8f5e9; padding:10px; border-radius:10px;}
</style>
""", unsafe_allow_html=True)

st.title("📊 EEG Autism Detection Report")

# ================== بيانات المريض ==================
c1, c2 = st.columns(2)
name = c1.text_input("Patient Name", "Ahmed")
age = c2.number_input("Age (months)", 1, 24, 6)

# ================== رفع الملف ==================
file = st.file_uploader("📁 Upload EEG CSV")

# ================== PDF ==================
def create_pdf(name, age, diagnosis, confidence):
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    c = canvas.Canvas(tmp.name, pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, "EEG Medical Report")
    c.drawString(100, 700, f"Patient Name: {name}")
    c.drawString(100, 670, f"Age (months): {age}")
    c.drawString(100, 640, f"Diagnosis: {diagnosis}")
    c.drawString(100, 610, f"Confidence: {confidence}%")
    c.save()
    return tmp.name

# ================== التشغيل ==================
if file:
    try:
        # ✅ قراءة CSV (حل encoding)
        data = pd.read_csv(file, encoding="latin1")

        # ✅ لو الملف من التدريب → نشيل الليبل
        if "autism" in data.columns:
            data = data.drop(columns=["autism"])

        # ✅ نختار الأرقام فقط
        data = data.select_dtypes(include=["number"])

        # ✅ تحميل الموديل
        model = joblib.load("autism_model.pkl")

        # ✅ أهم سطر: نفس أعمدة التدريب وبنفس الترتيب
        data = data[model.feature_names_in_]

        # ✅ التنبؤ
        pred = model.predict(data)
        prob = model.predict_proba(data)

        diagnosis = "Positive" if pred[0] == 1 else "Negative"
        confidence = round(max(prob[0]) * 100, 2)

        # ✅ عرض النتيجة
        r1, r2 = st.columns(2)
        r1.metric("Diagnosis", diagnosis)
        r2.metric("Confidence", f"{confidence}%")

        if diagnosis == "Positive":
            st.error("⚠️ Autism risk detected")
        else:
            st.success("✅ Normal brain activity")

        # ✅ رسم الإشارات
        st.subheader("📈 EEG Signals")
        st.line_chart(data)

        # ✅ PDF
        pdf_path = create_pdf(name, age, diagnosis, confidence)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download Medical Report",
                data=f,
                file_name="EEG_Report.pdf",
                mime="application/pdf"
            )

    except Exception:
        st.error("⚠️ حصل خطأ في قراءة الملف، تأكدي إن CSV صحيح ومتوافق مع النموذج.")
