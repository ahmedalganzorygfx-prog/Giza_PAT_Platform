import base64

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_theme import apply_theme, section, footer
import datetime
import os
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# 1️⃣ دالة جلب وقراءة اللوجو من جميع المسارات
# ---------------------------------------------------------
def get_attendance_logo():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))

  dirs_to_check = [
      script_dir,
      os.path.join(script_dir, 'images'),
      parent_dir,
      os.path.join(parent_dir, 'images'),
  ]
  possible_names = ['Logo.png', 'logo.png', 'Logo.jpg', 'logo.jpg', 'PAT.png']

  for d in dirs_to_check:
    if os.path.exists(d):
      for name in possible_names:
        p = os.path.join(d, name)
        if os.path.exists(p):
          try:
            with open(p, 'rb') as f:
              encoded = base64.b64encode(f.read()).decode()
              ext = os.path.splitext(p)[1].lower()
              mime = 'image/png' if ext == '.png' else 'image/jpeg'
              return f'data:{mime};base64,{encoded}'
          except Exception:
            pass
  return None


# ---------------------------------------------------------
# 2️⃣ دالة قراءة قاعدة البيانات تبحث ذكياً في كافة المسارات
# ---------------------------------------------------------
@st.cache_data
def load_teachers_db():
  script_dir = os.path.dirname(os.path.abspath(__file__))
  parent_dir = os.path.abspath(os.path.join(script_dir, '..', '..'))

  # جميع المجلدات المحتملة التي قد يوجد بها ملف data.xlsx
  dirs_to_search = [
      script_dir,
      os.path.join(parent_dir, 'apps', 'attendance-system-main'),
      parent_dir,
      os.getcwd(),
  ]

  possible_files = ['data.xlsx', 'teachers.xlsx', 'data.csv', 'teachers.csv']
  file_path = None

  for d in dirs_to_search:
    if os.path.exists(d):
      for f in possible_files:
        p = os.path.join(d, f)
        if os.path.exists(p):
          file_path = p
          break
      if file_path:
        break

  if file_path:
    try:
      if file_path.endswith('.csv'):
        df = pd.read_csv(file_path, dtype=str)
      else:
        df = pd.read_excel(file_path, dtype=str)

      # تنظيف الأسطر والمسافات الزائدة وتحويلها إلى نصوص
      for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
      return df, file_path
    except Exception as e:
      st.error(f'⚠️ حدث خطأ أثناء قراءة ملف البيانات (`{file_path}`): {e}')
      return pd.DataFrame(), None

  return pd.DataFrame(), None


# ---------------------------------------------------------
# 3️⃣ الواجهة الرئيسية للنظام الفرعي
# ---------------------------------------------------------
logo_data = get_attendance_logo()
if logo_data:
  st.markdown(
      f"""
    <div style="text-align: center; margin-bottom: 10px;">
        <img src="{logo_data}" style="height: 120px; object-fit: contain;">
    </div>
    """,
      unsafe_allow_html=True,
  )

st.markdown(
    """
<div style="text-align: center; margin-bottom: 20px;">
    <h2 style="color: #0f172a; font-weight: 800; margin-bottom: 5px;">الأكاديمية المهنية للمعلمين - فرع الجيزة</h2>
    <h4 style="color: #475569; font-weight: 600; margin-top: 0;">نظام إصدار تذاكر أسبقية الحضور</h4>
</div>
<hr style="border: 0.5px solid #e2e8f0; margin-bottom: 20px;">
""",
    unsafe_allow_html=True,
)

df_teachers, loaded_path = load_teachers_db()

# قسم البحث
st.markdown(
    "<h3 style='text-align: center; color: #0f172a; font-weight: 700;"
    " margin-bottom: 15px;'>البحث عن المعلم (فرع الجيزة)</h3>",
    unsafe_allow_html=True,
)

col_btn, col_input = st.columns([1, 3])

with col_input:
  search_query = st.text_input(
      '',
      placeholder='أدخل الكود أو الرقم القومي...',
      key='att_search_input',
      label_visibility='collapsed',
  )

with col_btn:
  search_clicked = st.button(
      'بحث 🔍', key='btn_att_search', use_container_width=True
  )

if search_clicked or search_query:
  query = str(search_query).strip()

  if not query:
    st.warning('⚠️ يرجى إدخال الكود أو الرقم القومي للبحث.')
  elif df_teachers.empty:
    st.error(
        '❌ لم يتم العثور على قاعدة البيانات `data.xlsx` في أي من المسارات'
        ' التالية:\n- `apps/attendance-system-main/data.xlsx`\n-'
        ' `data.xlsx` في المجلد الرئيسي.'
    )
  else:
    # المطابقة على الأعمدة
    col_code = (
        'كود المعلم' if 'كود المعلم' in df_teachers.columns else df_teachers.columns[0]
    )
    col_nid = (
        'الرقم القومي'
        if 'الرقم القومي' in df_teachers.columns
        else (df_teachers.columns[1] if len(df_teachers.columns) > 1 else col_code)
    )

    # بحث مطابق بدقة
    matched = df_teachers[
        (df_teachers[col_code] == query) | (df_teachers[col_nid] == query)
    ]

    if not matched.empty:
      teacher_data = matched.iloc[0]

      st.markdown(
          '<br><h3 style="text-align: center; color: #0f172a; font-weight:'
          ' 700;">بيانات المعلم المسجل</h3>',
          unsafe_allow_html=True,
      )

      t_code = teacher_data.get(col_code, '---')
      t_name = teacher_data.get('الاسم', teacher_data.get('اسم المعلم', '---'))
      t_nid = teacher_data.get(col_nid, '---')
      t_prog = teacher_data.get(
          'البرنامج', teacher_data.get('اسم البرنامج', '---')
      )

      st.markdown(
          f"""
        <div style="background-color: #f8fafc; padding: 20px 25px; border-radius: 12px; border: 1px solid #cbd5e1; direction: rtl; text-align: right; line-height: 1.9; font-size: 1rem; color: #0f172a; margin-bottom: 20px;">
            <div><b>كود المعلم:</b> {t_code}</div>
            <div><b>الاسم:</b> {t_name}</div>
            <div><b>الرقم القومي:</b> {t_nid}</div>
            <div><b>البرنامج:</b> {t_prog}</div>
        </div>
        """,
          unsafe_allow_html=True,
      )

      if st.button(
          '🎟️ تأكيد الحضور وإصدار التذكرة النهائية',
          key='confirm_ticket',
          use_container_width=True,
      ):
        ticket_num = f'A-{datetime.datetime.now().strftime("%S%M")}'
        st.success(
            f'🎉 تم تسجيل الحضور وإصدار التذكرة بنجاح! رقم الأسبقية:'
            f' **{ticket_num}**'
        )

    else:
      st.error(
          f'❌ لا توجد نتائج مطابقة للكود أو الرقم القومي المخل (`{query}`).'
      )
