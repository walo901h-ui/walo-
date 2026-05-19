import streamlit as st
import requests
from urllib.parse import urljoin

# إعدادات واجهة الموقع
st.set_page_config(page_title="WALO Scanner", page_icon="🥷", layout="centered")

st.title("🥷 WALO Vulnerability Error Scanner")
st.write("أداة مخصصة لفحص الروابط وتقفيط أخطاء السيرفرات وقواعد البيانات")

# خانة إدخال الرابط المستهدف
target_url = st.text_input("أدخل الرابط المستهدف (مثال: http://example.com/page.php?id=1):")

# قائمة الكلمات الدلالية والأخطاء الشهيرة اللي نبحث عنها في استجابة السيرفر
ERROR_SIGNATURES = [
    "SQL syntax", "MySQLServer", "PostgreSQL Query", "Oracle Error",
    "Driver", "OLE DB", "ODBC SQL", "MariaDB serverversion",
    "Syntax error", "Fatal error", "Warning: include", "Stack Trace"
]

if st.button("ابدأ الفحص والتخمين 🚀"):
    if not target_url:
        st.warning("تكفى حط الرابط أولاً عشان نفحصه!")
    else:
        st.info(f"جاري إرسال الطلبات وفحص الاستجابة لـ: {target_url}")
        
        try:
            # إرسال طلب للموقع وقراءة النتيجة
            response = requests.get(target_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            html_content = response.text
            
            # قفط الأخطاء داخل الـ HTML
            found_errors = []
            for signature in ERROR_SIGNATURES:
                if signature.lower() in html_content.lower():
                    found_errors.append(signature)
            
            # عرض النتائج بناءً على اللي لقطناه
            if found_errors:
                st.error(f"🚨 قفطنا مشاكل! السيرفر يسرب أخطاء برمجية قد تكون ثغرة:")
                for err in found_errors:
                    st.write(f"⚠️ خطأ لقطناه: **{err}**")
            else:
                st.success("✅ الفحص الأولي انتهى: السيرفر لم يرجع أي أخطاء برمجية واضحة في هذه الصفحة.")
                
        except requests.exceptions.RequestException as e:
            st.error(f"❌ تعذر الاتصال بالموقع المستهدف. تأكد من الرابط أو البروتوكول (http/https).")
