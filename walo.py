import streamlit as st
import ast
import traceback
import sys
from io import StringIO

# إعدادات واجهة محلل الأكواد
st.set_page_config(page_title="WALO Code Debugger", page_icon="💻", layout="centered")

st.title("💻 محلل ومصحح الأكواد من WALO")
st.write("الِصق سكربت البايثون هنا عشان نفحصه، ونقشّع الأخطاء البرمجية ونعلمك كيف تصلحها")
st.markdown("---")

# خانة كتابة أو لصق كود بايثون
code_input = st.text_area("أدخل كود بايثون (Python Code) هنا للفحص:", height=300, placeholder="print('Hello' -> مثال لخطأ سينتكس")

if st.button("افحص السكربت وقفط الأخطاء 🚀", use_container_width=True):
    if not code_input.strip():
        st.warning("يا واد حط كود بايثون أول شي عشان نفحصه!")
    else:
        st.info("جاري تحليل الكود وفحص السنتكس والتركيب البرمجي...")
        
        # المرحلة الأولى: فحص الأخطاء الإملائية والتركيبية (Syntax Check)
        try:
            ast.parse(code_input)
            st.success("✅ فحص التركيب (Syntax): كودك سليم إملائياً وما فيه أخطاء قفل أقواس أو علامات ناقصة!")
            
            # المرحلة الثانية: تجربة تشغيل افتراضية لقنص أخطاء التشغيل (Runtime Errors)
            st.info("جاري محاكاة تشغيل الكود لقفط أخطاء التشغيل...")
            
            # تحويل المخرجات للتيرمينال الوهمي عشان ما يخرب الموقع
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            
            try:
                # تشغيل الكود في بيئة معزولة ونظيفة
                local_vars = {}
                exec(code_input, {}, local_vars)
                sys.stdout = old_stdout # إعادة المخرجات لطبيعتها
                
                st.success("🔥 كفو! الكود اشتغل بالكامل بدون أي خطأ في التشغيل (Runtime Error).")
                if redirected_output.getvalue():
                    st.subheader("📺 مخرجات تشغيل الكود (Output):")
                    st.code(redirected_output.getvalue(), language="python")
                    
            except Exception as e:
                sys.stdout = old_stdout # إعادة المخرجات لطبيعتها
                st.error("🚨 قفطنا خطأ أثناء تشغيل الكود (Runtime Error)! ")
                
                # استخراج تفاصيل الخطأ ومكانه
                exc_type, exc_value, exc_tb = sys.exc_info()
                error_details = traceback.format_exception(exc_type, exc_value, exc_tb)
                
                # عرض الخطأ بشكل مبسط
                st.markdown(f"**نوع الخطأ:** `{exc_type.__name__}`")
                st.markdown(f"**رسالة الخطأ:** {exc_value}")
                
                st.subheader("🔍 مكان المشكلة بالتفصيل:")
                st.code("".join(error_details[-2:]), language="python")
                st.caption("💡 نصيحة: تأكد من تعريف المتغيرات، أو استدعاء المكتبات الصح فوق، أو صحة العمليات الحسابية.")
                
        except SyntaxError as se:
            st.error("❌ قفطنا خطأ مصنعي في كتابة الكود (Syntax Error)!")
            st.markdown(f"**السبب:** `{se.msg}`")
            st.markdown(f"**رقم السطر اللي فيه البلا:** سطر رقم `{se.lineno}`")
            
            # عرض السطر المخرب
            if se.text:
                st.subheader("📍 السطر المسبب للمشكلة:")
                st.code(f"{se.text.strip()}", language="python")
                st.caption("💡 نصيحة: شيك على الأقواس، أو النقطتين الرأسية `:`، أو علامات التنصيص ناقصة في هذا السطر.")
