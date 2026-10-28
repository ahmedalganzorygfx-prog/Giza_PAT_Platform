import glob

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common_theme import apply_theme, section, footer
import io
import os
import requests
import pandas as pd
import streamlit as st

import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="لوحة تحكم الامتحانات - فرع الجيزة",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_theme('الاختبارات والامتحانات', 'الحجز والمتابعة والنتائج والإحصائيات', '📝')


# 🛠️ تحميل وتسجيل الخط العربي تلقائياً
@st.cache_resource
def setup_arabic_font():
    font_path = "Amiri-Regular.ttf"
    if not os.path.exists(font_path):
        try:
            url = "https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                with open(font_path, "wb") as f:
                    f.write(response.content)
        except Exception:
            pass
            
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('Amiri', font_path))
            return True
        except Exception:
            return False
    return False

font_loaded = setup_arabic_font()

# 🛠️ دالة معالجة النصوص العربية لـ ReportLab
def process_arabic(text):
    if not text or str(text).strip() in ['-', '', 'nan', 'None']:
        return "-"
    reshaped = arabic_reshaper.reshape(str(text))
    return get_display(reshaped)

# 🎨 CSS لتنسيق الواجهة
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl;
    }
    [data-testid="stDataFrame"] div[role="columnheader"], [data-testid="stDataFrame"] div[role="gridcell"] {
        text-align: right !important;
        direction: rtl !important;
    }
    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: center !important;
    }
    .header-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
    .main-title {
        color: #ffffff !important;
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .sub-title {
        color: #38bdf8 !important;
        font-size: 18px;
        font-weight: 700;
    }
    .section-title-center {
        text-align: center !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin-top: 15px !important;
        margin-bottom: 15px !important;
    }
    .custom-metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 12px 8px;
        text-align: center;
        margin-bottom: 10px;
    }
    .custom-metric-title {
        background-color: #facc15 !important;
        color: #0f172a !important;
        padding: 3px 10px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        font-weight: 900 !important;
        display: inline-block !important;
        margin-bottom: 5px !important;
    }
    .custom-metric-value {
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: 900 !important;
        margin: 0 !important;
    }
    /* 🌟 الفوتر السخلي */
    .custom-footer {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-top: 2px solid #38bdf8;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        margin-top: 40px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .custom-footer-text {
        color: #cbd5e1;
        font-size: 15px;
        font-weight: 700;
    }
    .custom-footer-highlight {
        color: #38bdf8;
        font-weight: 800;
    }
    </style>
""", unsafe_allow_html=True)

# 2. الهيدر الرئيسي
st.markdown("""
<div class="header-card">
    <div class="main-title">🏛️ الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
    <div class="sub-title">📝 لوحة تحكم وإحصائيات الامتحانات أونلاين</div>
</div>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية
st.sidebar.markdown("<h3 style='text-align: center;'>🎯 البرامج التدريبية</h3>", unsafe_allow_html=True)
program_options = [
    "الكل",
    "تطبيقات تربوية للمعلم المساعد",
    "مدير ووكيل إدارة مدرسية",
    "مدير ووكيل إدارة تعليمية",
    "أساسيات التوجيه الفني"
]
selected_program = st.sidebar.radio(
    label="اختر البرنامج التدريبي:",
    options=program_options,
    index=0,
    label_visibility="collapsed"
)

# 4. تحميل بيانات الإكسيل
@st.cache_data
def load_data_from_project(file_path, mtime=None):
    try:
        df = pd.read_excel(file_path, dtype=str).fillna("-")
        df.columns = df.columns.str.strip()
        return df, None
    except Exception as e:
        return None, f"حدث خطأ أثناء قراءة الملف {file_path}: {e}"

excel_files = glob.glob("*.xlsx") + glob.glob("*.xls")

if not excel_files:
    st.error("⚠️ لم يتم العثور على أي ملف إكسيل (.xlsx أو .xls) في مجلد المشروع.")
    st.info("💡 الرجاء وضع ملف البيانات الإكسيل داخل مجلد المشروع وإعادة تشغيل الصفحة.")
    st.stop()

file_path = excel_files[0]
file_mtime = os.path.getmtime(file_path)
df, err_msg = load_data_from_project(file_path, file_mtime)

if err_msg:
    st.error(f"⚠️ {err_msg}")
    st.stop()

# 5. الفلاتر
col_period, col_branch, col_search, col_reset = st.columns([2.5, 1.5, 2, 1])

with col_period:
    period_scope = st.selectbox(
        "📊 نطاق الإحصائيات:",
        options=[
            "إحصائيات فترة (12-8-2026 إلى 10-9-2026)",
            "إحصائيات كامل التواريخ",
            "إحصائيات فترة (12-8 إلى 20-8) فقط"
        ],
        index=0
    )

with col_branch:
    branch_column = 'الفرع' if 'الفرع' in df.columns else ('الفرع الأصلي' if 'الفرع الأصلي' in df.columns else None)
    if branch_column:
        available_branches = ["الكل"] + sorted(list(df[branch_column].unique()))
        selected_branch = st.selectbox("🏢 اختر الفرع:", options=available_branches, index=0)
    else:
        selected_branch = "الكل"

with col_search:
    search_query = st.text_input("🔍 بحث بالرقم القومي أو كود المعلم:")

with col_reset:
    st.write(" ")
    st.write(" ")
    if st.button("🔄 إعادة تعيين", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# 6. تصفية البيانات
filtered_df = df.copy()

date_col = "وقت أداء الاختبار" if "وقت أداء الاختبار" in filtered_df.columns else ("تاريخ_الامتحان" if "تاريخ_الامتحان" in filtered_df.columns else None)

if date_col:
    temp_dates = pd.to_datetime(filtered_df[date_col], errors='coerce')
    
    if period_scope == "إحصائيات فترة (12-8-2026 إلى 10-9-2026)":
        start_date = pd.Timestamp("2026-08-12")
        end_date = pd.Timestamp("2026-09-10 23:59:59")
        filtered_df = filtered_df[(temp_dates >= start_date) & (temp_dates <= end_date)]
    elif period_scope == "إحصائيات فترة (12-8 إلى 20-8) فقط":
        filtered_df = filtered_df[(temp_dates.dt.month == 8) & (temp_dates.dt.day >= 12) & (temp_dates.dt.day <= 20)]

if selected_branch != "الكل" and branch_column:
    filtered_df = filtered_df[filtered_df[branch_column] == selected_branch]

if selected_program != "الكل" and "البرنامج" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["البرنامج"] == selected_program]

if search_query:
    cond_code = filtered_df["كود المعلم"].str.contains(search_query, case=False, na=False) if "كود المعلم" in filtered_df.columns else False
    cond_id = filtered_df["الرقم القومي"].str.contains(search_query, case=False, na=False) if "الرقم القومي" in filtered_df.columns else False
    filtered_df = filtered_df[cond_code | cond_id]


# 📄 7. دالة تقرير PDF المنسق رأساً
def generate_pdf_report(data_df, program_filter, scope_name, branch_filter="الكل"):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25
    )

    font_name = 'Amiri' if font_loaded else 'Helvetica'

    title_style = ParagraphStyle(
        name='ArabicTitle',
        fontName=font_name,
        fontSize=13.5,
        leading=17,
        alignment=1,
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        name='ArabicSubTitle',
        fontName=font_name,
        fontSize=9,
        leading=12,
        alignment=1,
        spaceAfter=10
    )
    heading_style = ParagraphStyle(
        name='ArabicHeading',
        fontName=font_name,
        fontSize=10.5,
        leading=14,
        alignment=2,
        spaceAfter=5
    )
    cell_style = ParagraphStyle(
        name='ArabicCell',
        fontName=font_name,
        fontSize=8.5,
        leading=11,
        alignment=1
    )
    header_cell_style = ParagraphStyle(
        name='ArabicHeaderCell',
        fontName=font_name,
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.whitesmoke
    )
    signature_style = ParagraphStyle(
        name='ArabicSignature',
        fontName=font_name,
        fontSize=9.5,
        leading=13,
        alignment=1
    )

    elements = []

    # 1. العنوان الرئيسي الهيدر
    branch_str = f" - فرع: {branch_filter}" if branch_filter != "الكل" else ""
    elements.append(Paragraph(process_arabic(f"تقرير إحصائيات الامتحانات والمنتدبين{branch_str} - ({scope_name})"), title_style))
    
    now_str = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
    prog_str = f"البرنامج: {program_filter}" if program_filter != "الكل" else "جميع البرامج التدريبية"
    elements.append(Paragraph(process_arabic(f"تاريخ استخراج التقرير: {now_str}  |  {prog_str}"), subtitle_style))
    elements.append(Spacer(1, 8))

    # 2. الإحصائيات العامة
    pdf_total = len(data_df)
    if "الحالة" in data_df.columns:
        pdf_status = data_df["الحالة"].astype(str).str.strip()
        pdf_reserved = len(pdf_status[pdf_status.isin(["محجوز", "حجز اختبار", "لم يختبر", "حجز", "لم يجتز"])])
        pdf_passed = len(pdf_status[pdf_status.isin(["اجتاز", "ناجح", "ناجحين"])])
        pdf_failed = len(pdf_status[pdf_status.isin(["راسب", "راسبين"])])
        pdf_pending = len(pdf_status[pdf_status.isin(["قيد الاختبار", "جاري الاختبار"])])
    else:
        pdf_reserved = pdf_passed = pdf_failed = pdf_pending = 0

    elements.append(Paragraph(process_arabic("1. الإحصائيات العامة للممتحنين:"), heading_style))
    stats_headers = ["قيد الاختبار", "راسبين", "ناجحين", "حجز اختبار", "إجمالي الممتحنين"]
    stats_data_row = [pdf_pending, pdf_failed, pdf_passed, pdf_reserved, pdf_total]
    
    t1 = Table(
        [[Paragraph(process_arabic(h), header_cell_style) for h in stats_headers],
         [Paragraph(process_arabic(str(val)), cell_style) for val in stats_data_row]],
        colWidths=[109, 109, 109, 109, 109]
    )
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e293b')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#f8fafc')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t1)
    elements.append(Spacer(1, 10))

    # 3. بيان المنتدبين
    b_col = 'الفرع' if 'الفرع' in data_df.columns else ('الفرع الأصلي' if 'الفرع الأصلي' in data_df.columns else None)
    name_col = 'اسم المعلم' if 'اسم المعلم' in data_df.columns else ('الاسم' if 'الاسم' in data_df.columns else None)
    code_col = 'كود المعلم' if 'كود المعلم' in data_df.columns else ('الكود' if 'الكود' in data_df.columns else None)

    if b_col:
        delegated_df = data_df[~data_df[b_col].astype(str).str.contains("الجيزة", na=False)]
        elements.append(Paragraph(process_arabic(f"2. بيان المنتدبين من خارج فرع الجيزة (العدد الإجمالي: {len(delegated_df)}):"), heading_style))
        
        if not delegated_df.empty:
            display_delegated = delegated_df.head(3)
            del_table_rows = [[Paragraph(process_arabic(h), header_cell_style) for h in ["الفرع الأصلي", "اسم المعلم", "كود المعلم"]]]
            
            for _, row in display_delegated.iterrows():
                del_table_rows.append([
                    Paragraph(process_arabic(str(row[b_col]) if b_col else "-"), cell_style),
                    Paragraph(process_arabic(str(row[name_col]) if name_col else "-"), cell_style),
                    Paragraph(process_arabic(str(row[code_col]) if code_col else "-"), cell_style)
                ])
                
            if len(delegated_df) > 3:
                del_table_rows.append([
                    Paragraph(process_arabic(f"... تم إدراج أول 3 من إجمالي {len(delegated_df)} منتدب"), cell_style),
                    Paragraph("", cell_style),
                    Paragraph("", cell_style)
                ])

            t_del = Table(del_table_rows, colWidths=[160, 225, 160])
            t_del_style = [
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#b91c1c')),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fef2f2')]),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ]
            if len(delegated_df) > 3:
                t_del_style.append(('SPAN', (0, -1), (2, -1)))
            t_del.setStyle(TableStyle(t_del_style))
            elements.append(t_del)
        else:
            elements.append(Paragraph(process_arabic("لا يوجد منتدبون من خارج فرع الجيزة في البيانات الحالية."), cell_style))
            
        elements.append(Spacer(1, 10))

    # 4. توزيع الإحصائيات حسب التواريخ (مرتبة تصاعدياً من 12/8 إلى 10/9)
    if date_col and not data_df.empty:
        elements.append(Paragraph(process_arabic("3. توزيع الإحصائيات حسب التواريخ:"), heading_style))
        temp_df = data_df.copy()
        
        parsed_dates = pd.to_datetime(temp_df[date_col], errors='coerce')
        temp_df["التاريخ_المصنع"] = parsed_dates.dt.strftime("%Y-%m-%d")
        
        date_group = temp_df.groupby("التاريخ_المصنع").size().reset_index(name="إجمالي الممتحنين")
        date_group = date_group.sort_values("التاريخ_المصنع", ascending=True)
        
        date_table_rows = [[Paragraph(process_arabic(h), header_cell_style) for h in ["إجمالي الممتحنين", "التاريخ"]]]
        
        for _, row in date_group.iterrows():
            d_str = str(row["التاريخ_المصنع"]) if pd.notna(row["التاريخ_المصنع"]) else "-"
            date_table_rows.append([
                Paragraph(process_arabic(str(row["إجمالي الممتحنين"])), cell_style),
                Paragraph(process_arabic(d_str), cell_style)
            ])
            
        t2 = Table(date_table_rows, colWidths=[272, 273])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f1f5f9')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(t2)
        elements.append(Spacer(1, 10))

    # 5. توزيع الممتحنين حسب البرنامج التدريبي
    if "البرنامج" in data_df.columns:
        elements.append(Paragraph(process_arabic("4. توزيع الممتحنين حسب البرنامج التدريبي:"), heading_style))
        prog_group = data_df.groupby("البرنامج").size().reset_index(name="عدد الممتحنين")
        
        prog_table_rows = [[Paragraph(process_arabic(h), header_cell_style) for h in ["عدد الممتحنين", "البرنامج التدريبي"]]]
        for _, row in prog_group.iterrows():
            prog_table_rows.append([
                Paragraph(process_arabic(str(row["عدد الممتحنين"])), cell_style),
                Paragraph(process_arabic(str(row["البرنامج"])), cell_style)
            ])
            
        t3 = Table(prog_table_rows, colWidths=[160, 385])
        t3.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#334155')),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ]))
        elements.append(t3)

    # 6. التوقيعات
    elements.append(Spacer(1, 12))
    signatures_data = [
        [
            Paragraph(process_arabic("<b>مدير الفرع</b><br/><br/><br/>أحمد الجنزوري"), signature_style),
            Paragraph(process_arabic("<b>المختص</b><br/><br/><br/>..........................."), signature_style)
        ]
    ]
    
    sig_table = Table(signatures_data, colWidths=[272, 273])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    elements.append(sig_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer


# 8. عرض الواجهة والأزرار
col_title, col_pdf = st.columns([3, 1])
with col_title:
    st.markdown(f'<div class="section-title-center">📊 الإحصائيات العامة ({period_scope})</div>', unsafe_allow_html=True)

with col_pdf:
    st.write(" ")
    try:
        pdf_bytes = generate_pdf_report(filtered_df, selected_program, period_scope, selected_branch)
        st.download_button(
            label="📄 استخراج تقرير PDF",
            data=pdf_bytes,
            file_name=f"تقرير_الامتحانات_{pd.Timestamp.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"خطأ أثناء تجهيز ملف PDF: {e}")

total = len(filtered_df)
if "الحالة" in filtered_df.columns:
    status_series = filtered_df["الحالة"].astype(str).str.strip()
    reserved = len(status_series[status_series.isin(["محجوز", "حجز اختبار", "لم يختبر", "حجز", "لم يجتز"])])
    passed = len(status_series[status_series.isin(["اجتاز", "ناجح", "ناجحين"])])
    failed = len(status_series[status_series.isin(["راسب", "راسبين"])])
    pending = len(status_series[status_series.isin(["قيد الاختبار", "جاري الاختبار"])])
else:
    reserved = passed = failed = pending = 0

metrics_data = [
    ("📊 إجمالي الممتحنين", total),
    ("🎟️ حجز اختبار", reserved),
    ("✅ ناجحين", passed),
    ("❌ راسبين", failed),
    ("⏳ قيد الاختبار", pending)
]

cols = st.columns(5)
for i, (title, val) in enumerate(metrics_data):
    with cols[i]:
        card_html = f"""
        <div class="custom-metric-card">
            <div class="custom-metric-title">{title}</div>
            <div class="custom-metric-value">{val}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

# 9. عرض الجدول
st.markdown('<div class="section-title-center">📋 جدول بيانات المعلمين</div>', unsafe_allow_html=True)
desired_order_rtl = [
    "وقت أداء الاختبار", "الحالة", "البرنامج", "المحافظة",
    "الفرع", "الفرع الأصلي", "الرقم القومي", "اسم المعلم", "كود المعلم"
]
columns_to_show = [col for col in desired_order_rtl if col in filtered_df.columns]

if not filtered_df.empty:
    st.dataframe(filtered_df[columns_to_show], use_container_width=True, hide_index=True)
else:
    st.info("لا توجد نتائج تطابق خيارات البحث والتصفية لهذا البرنامج.")

# 10. الفوتر السخلي (Footer)
st.markdown("""
<div class="custom-footer">
    <div class="custom-footer-text">
        💻 تصميم وتنفيذ: <span class="custom-footer-highlight">أحمد الجنزوري</span> - مدير الفرع
    </div>
</div>
""", unsafe_allow_html=True)
