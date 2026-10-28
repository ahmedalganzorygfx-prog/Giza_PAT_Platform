import base64

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_theme import apply_theme, section, footer
import os
import re
from io import BytesIO
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون متمركزة في المنتصف (Centered Layout)
st.set_page_config(
    page_title="الاستعلام عن الشهادات - فرع الجيزة",
    layout="centered",
    page_icon="🏛️",
)
apply_theme('الاستعلام عن الشهادات', 'استعلام سريع عن الجديد والتجديد وبدل الفاقد', '📜')



# دالة حساب وعرض عدد الزوار مع استثناء الآدمن
def get_and_update_visitor_count():
    count_file = "visitors.txt"

    # التحقق من وجود المعاملات في الرابط (Query Params)
    query_params = st.query_params

    # 1. حالة التصفير عبر الرابط (?reset=true)
    if query_params.get("reset") == "true":
        st.toast("🧹 تم تصفير عداد الزيارات بنجاح!")
        return reset_visitor_count()

    # 2. حالة الدخول كآدمن (?admin=true)
    if query_params.get("admin") == "true":
        st.session_state["is_admin_mode"] = True

    # إنشاء الملف إن لم يكن موجوداً
    if not os.path.exists(count_file):
        with open(count_file, "w") as f:
            f.write("0")

    # قراءة العدد الحالي
    try:
        with open(count_file, "r") as f:
            content = f.read().strip()
            count = int(content) if content.isdigit() else 0
    except Exception:
        count = 0

    # زيادة العداد فقط إذا لم تكن هذه الجلسة جلسة آدمن ولم تُحتسب من قبل
    is_admin = st.session_state.get("authenticated_admin", False)
    if not is_admin and not st.session_state.get("counted_this_session", False):
        count += 1
        st.session_state["counted_this_session"] = True
        try:
            with open(count_file, "w") as f:
                f.write(str(count))
        except Exception:
            pass

    return count


# تسجيل وتنفيذ الزيارة
visitor_count = get_and_update_visitor_count()

# تفعيل تتبع Google Analytics
ga_id = "G-2V7DFZWVXJ"
ga_script = f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', '{ga_id}');
    </script>
"""
components.html(ga_script, height=0, width=0)

# تطبيق التنسيق عبر CSS لشاشة العرض
st.markdown(
    """
    <style>
    /* تقليص وتوسيط حاوية المحتوى الرئيسية */
    .block-container {
        max-width: 800px !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        margin: 0 auto !important;
    }

    /* إخفاء زر القلم والتعديل فقط */
    button[title="Edit"], 
    [data-testid="stHeaderEditButton"],
    button[aria-label="Edit"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* تغيير خلفية التطبيق بالكامل لتصبح داكنة */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif, Arial;
        color: #e0e0e0;
    }
    /* حاوية مخصصة لتوسيط الشعار واسم الفرع في المنتصف */
    .logo-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin-top: 15px;
        margin-bottom: 10px;
        width: 100%;
        text-align: center;
    }
    .logo-container img {
        width: 180px;
        height: auto;
        display: block;
        margin: 0 auto 10px auto;
    }
    .branch-name-top {
        color: #ffffff;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 15px;
        text-align: center;
    }
    /* ضبط حجم الصورة لتتطابق تماماً مع أبعاد وحجم بطاقات المعلمين */
    .hand-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 5px;
        margin-bottom: 25px;
        width: 100%;
        box-sizing: border-box;
    }
    .hand-container img {
        width: 100%;
        max-width: 100%;
        height: auto;
        border-radius: 12px;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
        border: 1px solid #30363d;
        display: block;
        object-fit: cover;
    }
    /* تصميم رأس الصفحة بلون كحلي داكن فاخر ومتمركز */
    .header-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    /* تكبير وتنسيق العنوان الرئيسي بالترتيب الجديد */
    .header-box .main-title {
        color: #58a6ff;
        font-size: 24px !important;
        font-weight: bold !important;
        margin-bottom: 12px;
        line-height: 1.4;
    }
    .header-box p {
        color: #8b949e;
        font-size: 14px;
        margin: 0;
    }
    .highlight-red {
        color: #ffc107 !important;
        font-weight: bold;
    }
    .programs-text {
        color: #ffc107 !important;
        font-weight: bold;
    }
    .pickup-instructions {
        font-size: 16px !important;
        color: #ffc107 !important;
        font-weight: bold;
        margin-top: 8px;
        display: block;
    }
    .stAlert {
        direction: rtl;
        text-align: right;
    }

    [data-testid="stAlert"] * {
        color: #ffc107 !important;
        font-weight: bold !important;
        font-size: 17px !important;
    }

    /* زر البحث */
    .stFormSubmitButton > button {
        background-color: #21262d;
        color: white;
        width: 100%;
        border-radius: 6px;
        border: 1px solid #30363d;
        font-weight: bold;
    }
    .stFormSubmitButton > button:hover {
        background-color: #30363d;
        border-color: #8b949e;
    }


    /* زر تنزيل ملف Excel XLSX */
    [data-testid="stDownloadButton"] > button {
        background-color: #238636 !important;
        color: #ffffff !important;
        border: 1px solid #2ea043 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        width: 100% !important;
        min-height: 45px !important;
        opacity: 1 !important;
        text-align: center !important;
    }

    [data-testid="stDownloadButton"] > button:hover {
        background-color: #2ea043 !important;
        color: #ffffff !important;
        border-color: #3fb950 !important;
    }

    [data-testid="stDownloadButton"] > button p,
    [data-testid="stDownloadButton"] > button span,
    [data-testid="stDownloadButton"] > button div {
        color: #ffffff !important;
        font-weight: bold !important;
        opacity: 1 !important;
    }
    .stTextInput label {
        color: #ffffff !important;
        font-weight: bold !important;
    }
    .stTextInput input {
        background-color: #161b22 !important;
        color: white !important;
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
    }
    
    /* تصميم بطاقة بيانات المعلم الداكنة للشاشة */
    .teacher-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.4);
        text-align: right;
        direction: rtl;
        width: 100%;
        box-sizing: border-box;
    }
    .card-row {
        font-size: 17px;
        margin-bottom: 12px;
        color: #ffffff !important;
        font-weight: 500;
        text-align: right;
        direction: rtl;
    }
    .card-row b {
        color: #ffc107 !important;
        font-weight: bold !important;
    }

    /* ضبط شريط Expander: النص متصل بعلامة الاستفهام العربية والسهم يسار */
    [data-testid="stExpander"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        margin-top: 15px !important;
        margin-bottom: 20px !important;
        direction: rtl !important;
    }
    [data-testid="stExpander"] details {
        background-color: #161b22 !important;
        border-radius: 8px !important;
        direction: rtl !important;
    }
    [data-testid="stExpander"] summary {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        direction: rtl !important;
        text-align: right !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 12px 18px !important;
        border-radius: 8px !important;
        display: flex !important;
        flex-direction: row !important;
        justify-content: space-between !important;
        align-items: center !important;
    }
    [data-testid="stExpander"] summary span p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #58a6ff !important;
        margin: 0 !important;
        direction: rtl !important;
        text-align: right !important;
        unicode-bidi: isolate;
    }
    [data-testid="stExpander"] summary svg {
        fill: #58a6ff !important;
        margin-right: auto !important;
        margin-left: 0 !important;
    }

    .faq-answer-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-right: 5px solid #58a6ff;
        padding: 18px;
        border-radius: 8px;
        margin-top: 8px;
        margin-bottom: 15px;
        line-height: 1.9;
        font-size: 17px;
        color: #e0e0e0;
        direction: rtl !important;
        text-align: right !important;
    }
    .faq-highlight-yellow {
        color: #ffc107 !important;
        font-weight: bold !important;
    }
    
    /* تنسيق صناديق الحالات المخصصة */
    .status-red {
        background-color: rgba(255, 193, 7, 0.15);
        color: #ffc107;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #ffc107;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(255, 193, 7, 0.2);
        border-bottom: 1px solid rgba(255, 193, 7, 0.2);
        border-left: 1px solid rgba(255, 193, 7, 0.2);
    }
    .status-green {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        padding: 16px;
        border-radius: 8px;
        border-right: 5px solid #2ea043;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(46, 160, 67, 0.2);
        border-bottom: 1px solid rgba(46, 160, 67, 0.2);
        border-left: 1px solid rgba(46, 160, 67, 0.2);
    }
    .status-blue {
        background-color: rgba(56, 139, 253, 0.15);
        color: #58a6ff;
        padding: 14px;
        border-radius: 8px;
        border-right: 5px solid #388bfd;
        margin-top: 10px;
        margin-bottom: 15px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        direction: rtl;
        border-top: 1px solid rgba(56, 139, 253, 0.2);
        border-bottom: 1px solid rgba(56, 139, 253, 0.2);
        border-left: 1px solid rgba(56, 139, 253, 0.2);
    }

    @keyframes colorPulseGlow {
        0% { color: #3fb950; transform: scale(1); }
        50% { color: #ffc107; transform: scale(1.06); }
        100% { color: #3fb950; transform: scale(1); }
    }
    .pulse-text {
        display: inline-block;
        animation: colorPulseGlow 1.2s infinite ease-in-out;
        font-size: 20px !important;
        font-weight: 900 !important;
        margin-bottom: 5px;
    }

    .action-btn-container {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 15px;
        margin-bottom: 15px;
    }
    .share-whatsapp-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 8px 18px;
        background-color: #238636;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
        text-decoration: none;
        font-size: 14px;
        transition: background-color 0.2s;
    }
    .share-whatsapp-btn:hover { background-color: #2ea043; }

    /* صندوق مواعيد استلام الشهادات */
    .working-hours-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-right: 5px solid #58a6ff;
        padding: 18px 22px;
        border-radius: 10px;
        margin-top: 25px;
        margin-bottom: 20px;
        text-align: right;
        color: #ffffff;
        font-size: 16px;
        line-height: 1.8;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    .working-hours-title {
        color: #58a6ff;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .working-hours-highlight {
        color: #ffc107 !important;
        font-weight: bold;
        font-size: 17px;
    }

    .whatsapp-container {
        display: flex;
        justify-content: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 10px;
        margin-bottom: 15px;
    }
    .whatsapp-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background-color: #25d366;
        color: white !important;
        font-weight: bold;
        border-radius: 20px;
        text-decoration: none;
        font-size: 14px;
    }
    .custom-footer {
        margin-top: 40px;
        padding: 20px;
        text-align: center;
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        color: #8b949e;
        font-size: 14px;
        direction: rtl;
        line-height: 1.8;
    }
    .map-container {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #30363d;
        margin-top: 15px;
        margin-bottom: 20px;
    }
    .map-btn {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 18px;
        background-color: #238636;
        color: white !important;
        font-weight: bold;
        border-radius: 6px;
        text-decoration: none;
    }
    .visitor-badge {
        display: inline-block;
        margin-top: 15px;
        padding: 6px 18px;
        background-color: #0d1117;
        border: 1px solid #30363d;
        border-radius: 20px;
        color: #8b949e;
        font-size: 13px;
        font-weight: bold;
    }
    .director-badge {
        display: inline-block;
        margin-top: 12px;
        padding: 8px 20px;
        background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-right: 4px solid #ffc107;
        border-radius: 8px;
        color: #e0e0e0;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# دالة قراءة الشعار وتحويله إلى Base64
def get_image_base64(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    for file in os.listdir("."):
        if file.lower().startswith("logo") and file.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            with open(file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                ext = file.split(".")[-1].lower()
                return f"data:image/{ext};base64,{encoded_string}"
    return "https://cdn-icons-png.flaticon.com/512/3135/3135755.png"


# دالة قراءة صورة استلام الشهادة وتحويلها إلى Base64
def get_hand_image_base64():
    for filename in ["certificate_hand.png", "hand.png", "hand.jpg", "hand.jpeg"]:
        if os.path.exists(filename):
            with open(filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                ext = filename.split(".")[-1].lower()
                return f"data:image/{ext};base64,{encoded_string}"
    return "https://cdn-icons-png.flaticon.com/512/2912/2912761.png"


logo_src = get_image_base64("logo.png")
hand_src = get_hand_image_base64()

# عرض اللوجو متبوعاً باسم الفرع ثم الصورة التعبيرية بمقاس البطاقة
st.markdown(
    f"""
    <div class="logo-container">
        <img src="{logo_src}" alt="Logo">
        <div class="branch-name-top">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
    </div>
    <div class="hand-container">
        <img src="{hand_src}" alt="استلام الشهادة">
    </div>
    """,
    unsafe_allow_html=True,
)

# صندوق العنوان الرئيسي
st.markdown(
    """
    <div class="header-box">
        <div class="main-title">الاستعلام عن شهادة القيادة والإشراف <span class="highlight-red">(جديد - تجديد - بدل فاقد)</span></div>
        <p><b>البرامج التدريبية :</b> <span class="programs-text">مدير ووكيل إدارة تعليمية &nbsp;|&nbsp; مدير ووكيل إدارة مدرسية &nbsp;|&nbsp; أساسيات التوجيه الفني</span></p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")


# دالة قراءة البيانات
@st.cache_data(ttl=600)
def load_data(file_path):
    if not os.path.exists(file_path):
        return None
    df = pd.read_excel(file_path, dtype=str)
    df.columns = df.columns.astype(str).str.strip()
    return df


# إنشاء نسخة Excel في الذاكرة لتوفير زر تنزيل XLSX
def dataframe_to_excel_bytes(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="الشهادات")
    output.seek(0)
    return output.getvalue()


excel_file = "certificates.xlsx"
df = load_data(excel_file)

# ==========================================
# لوحة الإدارة المحمية بكلمة مرور لتعديل وإضافة الشهادات
# ==========================================
ADMIN_PASSWORD = "Giza2026Admin"  # كلمة المرور السرية

if st.session_state.get("is_admin_mode", False):
    st.markdown("### 🔒 تسجيل دخول لوحة إدارة البيانات")
    
    if not st.session_state.get("authenticated_admin", False):
        with st.form("admin_login_form"):
            input_pass = st.text_input("🔑 أدخل كلمة المرور السرية للوصول للبيانات:", type="password")
            login_submit = st.form_submit_button("🔓 تسجيل الدخول")
            if login_submit:
                if input_pass == ADMIN_PASSWORD:
                    st.session_state["authenticated_admin"] = True
                    st.success("✅ تم التحقق بنجاح! جاري فتح لوحة التحكم...")
                    st.rerun()
                else:
                    st.error("❌ كلمة المرور غير صحيحة!")
    else:
        st.markdown("### ⚙️ لوحة إدارة البيانات وتعديل ملف الأكسيل مباشر")
        if df is not None:

            # زر تنزيل قاعدة البيانات كاملة بصيغة Excel XLSX
            excel_download = dataframe_to_excel_bytes(df)
            st.download_button(
                label="⬇️ تنزيل قاعدة البيانات — Excel (XLSX)",
                data=excel_download,
                file_name="certificates.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                help="تنزيل نسخة Excel كاملة من قاعدة بيانات الشهادات."
            )

            tab_view, tab_add = st.tabs(["📝 تعديل وحفظ الجدول المباشر", "➕ إضافة معلم/شهادة جديدة"])
            
            with tab_view:
                st.info("💡 يمكنك تعديل أي خلية مباشرة في الجدول أدناه ثم اضغط 'حفظ التعديلات'.")
                edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
                if st.button("💾 حفظ التعديلات المباشرة في ملف الأكسيل"):
                    try:
                        edited_df.to_excel(excel_file, index=False)
                        st.cache_data.clear()
                        st.success("✅ تم حفظ التعديلات بنجاح في قاعدة البيانات!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ حدث خطأ أثناء الحفظ: {e}")
                        
            with tab_add:
                st.markdown("#### إضافة شهادة جديدة إلى الكشف:")
                with st.form("add_teacher_form"):
                    cols = list(df.columns)
                    new_data = {}
                    for c in cols:
                        new_data[c] = st.text_input(f"أدخل {c}:")
                    submit_new = st.form_submit_button("➕ إضافة وتحديث الملف")
                    
                    if submit_new:
                        new_row_df = pd.DataFrame([new_data])
                        updated_df = pd.concat([df, new_row_df], ignore_index=False)
                        try:
                            updated_df.to_excel(excel_file, index=False)
                            st.cache_data.clear()
                            st.success("🎉 تم إضافة الشهادة الجديدة بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ حدث خطأ أثناء الحفظ: {e}")
        st.markdown("---")

if df is not None:
    # تحديد عمود الرقم القومي
    id_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["قومي", "الرقم", "ID"]):
            id_column = col
            break
    if id_column is None:
        id_column = df.columns[0]

    # تحديد عمود نوع الشهادة
    type_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["نوع", "النوع"]):
            type_column = col
            break

    # تحديد عمود حالة الشهادة
    status_column = None
    for col in df.columns:
        if any(keyword in col for keyword in ["حالة", "الشهادة"]):
            status_column = col
            break

    st.markdown(
        '<div style="text-align: right; direction: rtl; font-size: 17px; font-weight: bold; margin-bottom: 10px; color: #ffffff;">💡 أدخل الرقم القومي الخاص بك (14 رقماً أو آخر 4 أرقام من جهة اليمين) ثم اضغط على زر بحث:</div>',
        unsafe_allow_html=True,
    )

    with st.form(key="search_form"):
        search_query = st.text_input("الرقم القومي (أو آخر 4 أرقام):", max_chars=14).strip()
        submit_button = st.form_submit_button(label="🔍 بحث")

    # ==========================================
    # قسم الأسئلة الشائعة والدعم الذاتي (تمييز عناوين النقاط الفرعية باللون الأصفر)
    # ==========================================
    with st.expander("الأسئلة الشائعة ودليل خدمات الاستلام (اضغط للتفاصيل) ؟"):
        st.markdown(
            """
            <div class="faq-answer-box">
                <b style="color:#58a6ff; font-size:18px;">📄 1. ما هي الأوراق والمستندات المطلوبة للاستلام؟</b><br>
                🔸 <span class="faq-highlight-yellow">شهادة جديدة (أول مرة):</span> إحضار صورة بطاقة الرقم القومي سارية + الأصل للاطلاع.<br>
                🔸 <span class="faq-highlight-yellow">تجديد الشهادة:</span> إحضار صحيفة أحوال إلكترونية حديثة + صورة بطاقة الرقم القومي سارية.<br>
                🔸 <span class="faq-highlight-yellow">بدل فاقد:</span> إحضار صحيفة أحوال إلكترونية حديثة + صورة بطاقة الرقم القومي + نموذج طلب بدل الفاقد من الفرع.
            </div>
            
            <div class="faq-answer-box">
                <b style="color:#58a6ff; font-size:18px;">📜 2. هل يجوز استلام الشهادة بالإنابة عن المعلم؟</b><br>
                • <b>نعم، يجوز فقط في الحالات التالية:</b><br>
                &nbsp;&nbsp;1. وجود <b>تفويض رسمي لاستلام الشهادة معتمد بشعار المدرسة أو التوجيه</b> + صورة بطاقة المفَوِّض والمفَوَّض إليه.<br>
                &nbsp;&nbsp;2. أقارب الدرجة الأولى (الوالد/الوالدة، الزوج/الزوجة، الأبناء) مع إثبات درجة القرابة وصورة بطاقة الرقم القومي لكل منهما.
            </div>

            <div class="faq-answer-box">
                <b style="color:#58a6ff; font-size:18px;">⏳ 3. ماذا تفعل إذا كانت حالة الشهادة "لم تصل إلى الفرع حتى الآن"؟</b><br>
                • تعني هذه الحالة أن ملفات ودفعات الشهادات الصادرة من المقر الرئيسي ما زالت قيد الطباعة أو الاعتماد المالي والتوزيع.<br>
                • <b>المتابعة:</b> يُرجى إعادة الاستعلام عبر البوابة أسبوعياً حيث يتم تحديث قاعدة البيانات فور وصول أي دفعات جديدة إلى الفرع.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if submit_button:
        if search_query:
            df[id_column] = (
                df[id_column]
                .astype(str)
                .str.replace(r"\.0$", "", regex=True)
                .str.strip()
            )

            # البحث بالرقم القومي الكلي أو بآخر 4 أرقام من الجهة اليمنى
            if len(search_query) == 14:
                result = df[df[id_column] == search_query]
            else:
                result = df[df[id_column].str.endswith(search_query, na=False)]

            if result.empty:
                result = df[df[id_column].str.contains(search_query, na=False)]

            if not result.empty:
                num_results = len(result)
                if num_results > 1:
                    st.success(f"🎉 تم العثور على ({num_results}) شهادة مرتبطة بالرقم القومي:")
                else:
                    st.success("🎉 تم العثور على بيانات الشهادة بنجاح:")

                # المرور على جميع الشهادات المعثور عليها
                for idx, row in result.iterrows():
                    name_val = "غير متوفر"
                    for c in df.columns:
                        if any(
                            k in c for k in ["اسم", "الاسم", "المعلم", "السيد"]
                        ) and not any(
                            k in c for k in ["قومي", "إدارة", "الادارة", "نوع"]
                        ):
                            name_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    admin_val = "غير متوفر"
                    for c in df.columns:
                        if "الادارة" in c or "الإدارة" in c:
                            admin_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    prog_val = "غير متوفر"
                    for c in df.columns:
                        if any(k in c for k in ["البرنامج", "الترقي", "التدريب"]):
                            prog_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    serial_val = "غير متوفر"
                    for c in df.columns:
                        if "مسلسل" in c or c.strip() == "م":
                            serial_val = str(row[c]) if pd.notna(row[c]) else "غير متوفر"
                            break

                    cert_type_val = "جديد"
                    if type_column and pd.notna(row[type_column]):
                        val_str = str(row[type_column]).strip()
                        if val_str:
                            cert_type_val = val_str

                    card_id = f"print-teacher-card-{idx}"
                    status_id = f"print-status-box-{idx}"

                    # 1. عرض بطاقة بيانات الشهادة
                    card_code = f"""
                    <div class="teacher-card" id="{card_id}">
                        <div class="card-row"><b>رقم المسلسل:</b> {serial_val}</div>
                        <div class="card-row"><b>اسم المعلم:</b> {name_val}</div>
                        <div class="card-row"><b>الرقم القومي:</b> {row[id_column]}</div>
                        <div class="card-row"><b>الإدارة التعليمية:</b> {admin_val}</div>
                        <div class="card-row"><b>البرنامج التدريبي:</b> {prog_val}</div>
                        <div class="card-row"><b>نوع الشهادة:</b> {cert_type_val}</div>
                    </div>
                    """
                    st.markdown(card_code, unsafe_allow_html=True)

                    # تحديد المستندات المطلوب إحضارها بحسب نوع الشهادة (تجديد/بدل فاقد vs جديد)
                    if any(kw in cert_type_val for kw in ["تجديد", "فاقد"]):
                        required_docs_text = "📌 يرجى التوجه لمقر الفرع لاستلامها مع احضار صحيفة أحوال إلكترونية حديثة + صورة البطاقة."
                    else:
                        required_docs_text = "📌 يرجى التوجه لمقر الفرع لاستلامها مع احضار صورة البطاقة."

                    # 2. فحص حالة الشهادة الحالية وعرضها
                    status_html = ""
                    is_available = False

                    if status_column and pd.notna(row[status_column]):
                        status_val = str(row[status_column]).strip()
                        if "لم تصل" in status_val:
                            status_html = f"""
                            <div class="status-red" id="{status_id}">
                                🟡 لم تصل إلى الفرع حتى الآن<br>
                                <span style="font-weight: normal; font-size: 13px;">يرجى الاستعلام في وقت لاحق.</span>
                            </div>
                            """
                        elif "موجودة" in status_val:
                            is_available = True
                            status_html = f"""
                            <div class="status-green" id="{status_id}">
                                <span class="pulse-text">🟢 الشهادة موجودة بالفرع</span><br>
                                <span class="pickup-instructions">{required_docs_text}</span>
                            </div>
                            """
                        elif "تسليم" in status_val:
                            status_html = f"""
                            <div class="status-blue" id="{status_id}">
                                🔵 تم تسليم الشهادة للمعلم
                            </div>
                            """
                        else:
                            status_html = f'<div class="status-blue" id="{status_id}">حالة الشهادة: {status_val}</div>'

                    st.markdown(status_html, unsafe_allow_html=True)

                    # 3. إظهار زر الطباعة وإمكانية طباعة نموذج التفويض المباشر
                    if is_available:
                        components.html(
                            f"""
                            <div style="display: flex; justify-content: center; gap: 12px; width: 100%; flex-wrap: wrap; margin-bottom: 25px;">
                                <button onclick="printIsolatedCard_{idx}()" style="
                                    background-color: #1f6beb;
                                    color: white;
                                    font-weight: bold;
                                    border-radius: 8px;
                                    border: none;
                                    padding: 10px 20px;
                                    font-size: 14px;
                                    cursor: pointer;
                                    font-family: 'Cairo', sans-serif, Arial;
                                    box-shadow: 0 4px 12px rgba(31,107,235,0.4);
                                ">🖨️ طباعة إفادة الاستعلام</button>
                                
                                <button onclick="printAuthForm_{idx}()" style="
                                    background-color: #238636;
                                    color: white;
                                    font-weight: bold;
                                    border-radius: 8px;
                                    border: none;
                                    padding: 10px 20px;
                                    font-size: 14px;
                                    cursor: pointer;
                                    font-family: 'Cairo', sans-serif, Arial;
                                    box-shadow: 0 4px 12px rgba(35,134,54,0.4);
                                ">📄 طباعة صيغة التفويض (PDF)</button>
                            </div>

                            <script>
                            function printIsolatedCard_{idx}() {{
                                var cardElem = window.parent.document.getElementById('{card_id}');
                                var statusElem = window.parent.document.getElementById('{status_id}');
                                
                                var cardHtml = cardElem ? cardElem.outerHTML : '';
                                var statusHtml = statusElem ? statusElem.outerHTML : '';
                                
                                var printWin = window.open('', '', 'width=650,height=850');
                                printWin.document.write(`
                                    <!DOCTYPE html>
                                    <html dir="rtl" lang="ar">
                                    <head>
                                        <meta charset="utf-8">
                                        <title>إفادة استعلام - فرع الجيزة</title>
                                        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
                                        <style>
                                            @page {{ size: 15cm 20cm; margin: 0.3cm; }}
                                            html, body {{ margin: 0; padding: 0; background-color: #fff; color: #000; font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }}
                                            body {{ padding: 10px 12px; box-sizing: border-box; }}
                                            .container {{ width: 100%; max-width: 14cm; margin: 0 auto; }}
                                            .print-header {{ text-align: center; margin-bottom: 12px; margin-top: 5px; }}
                                            .print-header img {{ width: 110px; height: auto; margin-bottom: 6px; }}
                                            .print-header-title {{ color: #0d233a; font-size: 16px; font-weight: 800; margin-bottom: 4px; }}
                                            .print-header-subtitle {{ color: #d32f2f; font-size: 14px; font-weight: 700; margin-bottom: 10px; }}
                                            .teacher-card {{ border: 2px solid #0d233a; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; }}
                                            .card-row {{ font-size: 13px; font-weight: 600; margin-bottom: 6px; color: #111; }}
                                            .card-row b {{ color: #d32f2f; }}
                                            .status-green {{ background-color: #f0fdf4; color: #15803d; border: 1.5px solid #15803d; padding: 8px; border-radius: 6px; text-align: center; font-size: 12px; font-weight: bold; margin-bottom: 8px; }}
                                            .working-hours-print {{ background-color: #fafafa; border: 1.5px solid #0d233a; border-right: 5px solid #d32f2f; color: #111; padding: 8px 12px; border-radius: 6px; font-size: 11px; line-height: 1.5; margin-bottom: 12px; }}
                                            .print-footer-signature {{ display: flex; justify-content: center; align-items: center; width: 100%; margin-top: 8px; text-align: center; }}
                                            .signature-box {{ text-align: center; font-size: 13px; font-weight: bold; color: #0d233a; }}
                                            .signature-box b {{ color: #d32f2f; font-size: 15px; }}
                                        </style>
                                    </head>
                                    <body>
                                        <div class="container">
                                            <div class="print-header">
                                                <img src="{logo_src}" alt="شعار الأكاديمية">
                                                <div class="print-header-title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
                                                <div class="print-header-subtitle">إفادة استعلام عن شهادة القيادة والإشراف</div>
                                            </div>
                                            ${{cardHtml}}
                                            ${{statusHtml}}
                                            <div class="working-hours-print">
                                                <b>⏰ مواعيد استلام الشهادات:</b> من الأحد للخميس (10:00 ص حتى 2:00 ظ) بمقر الفرع.
                                            </div>
                                            <div class="print-footer-signature">
                                                <div class="signature-box">مدير إدارة الفرع<br><b>أ. أحمد الجنزوري</b></div>
                                            </div>
                                        </div>
                                        <script>window.onload = function() {{ window.print(); setTimeout(function() {{ window.close(); }}, 500); }};<\/script>
                                    </body>
                                    </html>
                                `);
                                printWin.document.close();
                            }}

                            function printAuthForm_{idx}() {{
                                var printWin = window.open('', '', 'width=750,height=950');
                                printWin.document.write(`
                                    <!DOCTYPE html>
                                    <html dir="rtl" lang="ar">
                                    <head>
                                        <meta charset="utf-8">
                                        <title>نموذج تفويض استلام شهادة - فرع الجيزة</title>
                                        <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
                                        <style>
                                            @page {{ size: A4; margin: 1.2cm; }}
                                            body {{ font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; color: #000; line-height: 1.8; padding: 10px; }}
                                            .header {{ text-align: center; border-bottom: 2px solid #000; padding-bottom: 12px; margin-bottom: 20px; }}
                                            .header img {{ width: 100px; height: auto; }}
                                            .title {{ font-size: 20px; font-weight: bold; margin-top: 6px; }}
                                            .subtitle {{ font-size: 16px; font-weight: bold; color: #d32f2f; margin-bottom: 10px; }}
                                            .section-box {{ border: 1.5px solid #000; padding: 15px; border-radius: 8px; margin-bottom: 18px; }}
                                            .field-line {{ font-size: 15px; font-weight: 600; margin-bottom: 12px; }}
                                            .docs-title {{ font-size: 16px; font-weight: bold; color: #0d233a; margin-top: 10px; border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
                                            .signature-grid {{ display: flex; justify-content: space-between; margin-top: 25px; text-align: center; font-weight: bold; }}
                                            .stamp-box {{ border: 2px dashed #000; width: 150px; height: 100px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #555; margin: 0 auto; }}
                                        </style>
                                    </head>
                                    <body>
                                        <div class="header">
                                            <img src="{logo_src}" alt="شعار الأكاديمية">
                                            <div class="title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
                                            <div class="subtitle">نموذج وتفويض رسمي لاستلام شهادة القيادة والإشراف</div>
                                        </div>

                                        <div class="section-box">
                                            <div class="field-line">أقر أنا المعلم/ <b>{name_val}</b></div>
                                            <div class="field-line">الرقم القومي: <b>{row[id_column]}</b> &nbsp;&nbsp;|&nbsp;&nbsp; الإدارة التعليمية: <b>{admin_val}</b></div>
                                            <div class="field-line">بأنني قمت بتفويض السيد/ ........................................................................................................</div>
                                            <div class="field-line">الرقم القومي: (..................................................) &nbsp;&nbsp;|&nbsp;&nbsp; صلة القرابة/الصفة: .......................................</div>
                                            <div class="field-line">وذلك لاستلام شهادة القيادة والإشراف الخاصة بي لبرنامج: <b>{prog_val}</b> ({cert_type_val}).</div>
                                        </div>

                                        <div class="docs-title">📋 المستندات والأوراق المطلوبة المرفقة مع هذا التفويض:</div>
                                        <ul style="font-size: 13px; font-weight: 600; padding-right: 20px;">
                                            <li><b>1. الشهادة الجديدة (أول مرة):</b> صورة بطاقة الرقم القومي سارية للمُفوِّض والمُفوَّض إليه + اعتماد التفويض بخاتم الشعار.</li>
                                            <li><b>2. تجديد الشهادة / بدل الفاقد:</b> صحيفة أحوال إلكترونية حديثة معتمدة + صورة بطاقة الرقم القومي سارية للطرفين + الاعتماد بخاتم الشعار.</li>
                                        </ul>

                                        <div class="signature-grid">
                                            <div>توقيع المعلم (المُفوِّض)<br><br>.........................................</div>
                                            <div>توقيع المُفوَّض إليه<br><br>.........................................</div>
                                            <div>
                                                اعتماد جهة العمل (المدرسة / التوجيه)<br>
                                                <br>
                                                <div class="stamp-box">خاتم الشعار الرسمى</div>
                                            </div>
                                        </div>

                                        <script>window.onload = function() {{ window.print(); setTimeout(function() {{ window.close(); }}, 500); }};<\/script>
                                    </body>
                                    </html>
                                `);
                                printWin.document.close();
                            }}
                            </script>
                            """,
                            height=60,
                        )

                    # خط فاصل بين الشهادات في حالة وجود أكثر من نتيجة
                    if num_results > 1 and idx != result.index[-1]:
                        st.markdown("<hr style='border: 1px dashed #30363d; margin: 20px 0;'>", unsafe_allow_html=True)
            else:
                st.error(
                    "❌ عذراً، لم يتم العثور على بيانات بهذا الرقم القومي. تأكد من صحة الرقم المُدخل."
                )
        else:
            st.warning("⚠️ برجاء كتابة الرقم القومي أولاً قبل الضغط على بحث.")
else:
    st.warning(
        "⚠️ جاري تجهيز قاعدة البيانات أو أن ملف الكشف غير متوفر حالياً. برجاء التأكد من رفع ملف (certificates.xlsx) في مجلد المشروع على GitHub."
    )

# زر مشاركة رابط البوابة عبر الواتساب مع المعلمين
whatsapp_share_text = "https://wa.me/?text=" + pd.Series([
    "🏛️ بوابة الاستعلام عن شهادات القيادة والإشراف - فرع الجيزة:\nاستعلم عن حالة شهادتك الآن من الرابط التالي:\nhttps://giza-academy.streamlit.app"
]).str.replace(" ", "%20").iloc[0]

# صندوق مواعيد استلام الشهادات في البوابة
st.markdown(
    """
    <div class="working-hours-box">
        <div class="working-hours-title">⏰ مواعيد استلام الشهادات:</div>
        • من الأحد إلى الخميس: من الساعة <span class="working-hours-highlight">10:00 صباحاً</span> حتى الساعة <span class="working-hours-highlight">2:00 ظهراً</span>.<br>
        • الإجازات الرسمية: <span class="working-hours-highlight">الجمعة والسبت</span> والعطلات الرسمية بالدولة.
    </div>
    """,
    unsafe_allow_html=True,
)

# تذييل الصفحة المطور مع الأزرار التفاعلية
st.markdown(
    f"""
    <div class="custom-footer">
        <div class="action-btn-container">
            <a href="{whatsapp_share_text}" target="_blank" class="share-whatsapp-btn">
                📲 مشاركة رابط البوابة مع الزملاء عبر واتس آب
            </a>
        </div>
        <br>
        💬 <b>أرقام الدعم الفني للتواصل عبر واتس آب:</b>
        <div class="whatsapp-container">
            <a href="https://wa.me/201069996245" target="_blank" class="whatsapp-btn">🟢 01069996245</a>
            <a href="https://wa.me/201120807631" target="_blank" class="whatsapp-btn">🟢 01120807631</a>
            <a href="https://wa.me/201201109892" target="_blank" class="whatsapp-btn">🟢 01201109892</a>
        </div>
        <br>
        📍 <b>عنوان الفرع:</b> الأكاديمية المهنية للمعلمين - فرع الجيزة<br>
        🏢 ش المحطة - إمبابة (بجوار مدرسة باحثة البادية التجارية بنات)<br>
        <a href="https://maps.app.goo.gl/akdNyovrEbWLJmBu9" target="_blank" class="map-btn">
            🗺️ فتح الموقع والتوجيه المباشر في تطبيق Google Maps
        </a>
        <div class="map-container">
            <iframe 
                src="https://maps.google.com/maps?q=30.06776,31.20915&hl=ar&z=17&output=embed" 
                width="100%" 
                height="350" 
                style="border:0;" 
                allowfullscreen="" 
                loading="lazy" 
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>
        <div class="visitor-badge">
            👁️ إجمالي عدد زيارات البوابة: <span>{visitor_count:,}</span> زيارة
        </div>
        <br>
        <div class="director-badge">
            👔 تصميم وتنفيذ <b>أحمد الجنزوري</b> - مدير إدارة الفرع
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
