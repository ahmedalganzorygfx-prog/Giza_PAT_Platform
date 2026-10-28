import streamlit as st
import datetime
import os
import json
import base64
from zoneinfo import ZoneInfo

# ---------------------------------------------------------
# 🔑 كلمة المرور الخاصة بالإدارة للأنظمة المقيدة
# ---------------------------------------------------------
ADMIN_PASSWORD = 'giza2026'

# ---------------------------------------------------------
# 📁 إعدادات نظام ملفات JSON الدائمة
# ---------------------------------------------------------
DATA_FILE = 'edarat_data.json'
COMPLAINTS_FILE = 'complaints_data.json'

EDARAT_LIST = [
    'أبو النمرس', 'أطفيح', 'أكتوبر', 'أوسيم', 'البدرشين', 'الحوامدية',
    'الدقى', 'الشيخ زايد', 'الصف', 'العجوزة', 'العمرانية',
    'الهرم', 'الواحات البحرية', 'الوراق', 'بولاق الدكرور', 'جنوب الجيزة',
    'حدائق أكتوبر', 'ديوان المديرية', 'شمال الجيزة', 'كرداسة', 'منشأة القناطر'
]

def load_edarat_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    initial_data = {}
    for edara in EDARAT_LIST:
        initial_data[edara] = [{
            'mgr_name': 'غير محدد', 'mgr_phone': '01000000000',
            'hr_name': 'غير محدد', 'hr_phone': '01000000000',
            'stat_name': 'غير محدد', 'stat_phone': '01000000000'
        }]
    return initial_data

def save_edarat_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"حدث خطأ أثناء الحفظ: {e}")

def load_complaints_data():
    if os.path.exists(COMPLAINTS_FILE):
        try:
            with open(COMPLAINTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_complaints_data(data):
    try:
        with open(COMPLAINTS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"حدث خطأ أثناء حفظ الشكاوي: {e}")

def get_local_image_data(image_name, fallback_url=''):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(script_dir, "images")
    extensions = ['.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG']
    possible_names = [image_name, f"staff_{image_name}"]
    
    for name in possible_names:
        for ext in extensions:
            img_path = os.path.join(images_dir, name + ext)
            if os.path.exists(img_path):
                try:
                    with open(img_path, "rb") as f:
                        encoded = base64.b64encode(f.read()).decode()
                        mime_type = 'image/png' if ext.lower() == '.png' else ('image/webp' if ext.lower() == '.webp' else 'image/jpeg')
                        return f"data:{mime_type};base64,{encoded}"
                except Exception:
                    pass
    return fallback_url

def get_logo_data(logo_name="Logo.png"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dirs_to_check = [script_dir, os.path.join(script_dir, "images"), os.path.join(script_dir, "apps")]
    possible_names = [logo_name, logo_name.lower(), 'pat_logo.png', 'pat_main_logo.png', 'Logo.jpg', 'logo.jpg', 'Logo.jpeg']
    
    for d in dirs_to_check:
        if os.path.exists(d):
            for name in possible_names:
                p = os.path.join(d, name)
                if os.path.exists(p):
                    try:
                        with open(p, "rb") as f:
                            encoded = base64.b64encode(f.read()).decode()
                            ext = os.path.splitext(p)[1].lower()
                            mime_type = 'image/png' if ext == '.png' else 'image/jpeg'
                            return f"data:{mime_type};base64,{encoded}"
                    except Exception:
                        pass
    return None

logo_data = get_logo_data("Logo.png")
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_file_path = None
for d in [script_dir, os.path.join(script_dir, "images")]:
    for fname in ["Logo.png", "logo.png", "Logo.jpg", "logo.jpg"]:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            logo_file_path = p
            break
    if logo_file_path:
        break

try:
    cairo_tz = ZoneInfo("Africa/Cairo")
    now = datetime.datetime.now(cairo_tz)
except Exception:
    now = datetime.datetime.now()

days_ar = {'Monday': 'الإثنين', 'Tuesday': 'الثلاثاء', 'Wednesday': 'الأربعاء', 'Thursday': 'الخميس', 'Friday': 'الجمعة', 'Saturday': 'السَّبت', 'Sunday': 'الأحد'}
months_ar = {1: 'يناير', 2: 'فبراير', 3: 'مارس', 4: 'أبريل', 5: 'مايو', 6: 'يونيو', 7: 'يوليو', 8: 'أغسطس', 9: 'سبتمبر', 10: 'أكتوبر', 11: 'نوفمبر', 12: 'ديسمبر'}

day_name = days_ar.get(now.strftime('%A'), now.strftime('%A'))
month_name = months_ar.get(now.month, now.month)
period = "ص" if now.hour < 12 else "م"
hour_12 = now.hour % 12
if hour_12 == 0: hour_12 = 12
time_str = f"{hour_12:02d}:{now.minute:02d}:{now.second:02d} {period}"
current_date_time_str = f"{day_name} {now.day} {month_name} {now.year} | 🕒 {time_str}"

st.set_page_config(
    page_title="الأكاديمية المهنية للمعلمين - فرع الجيزة",
    page_icon=logo_file_path if logo_file_path else "🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SUB_APP_URLS = {
    'archive': 'https://archive-system-7xswjqgbpq3gagt4zyxida.streamlit.app/',
    'attendance': 'https://attendance-system-j3v9exhmjethurcyz4k3jb.streamlit.app/',
    'certificates': 'https://tagdeed-certificates-dpp2otmfte7i9wxwnft3ye.streamlit.app/',
    'exams': 'https://pat-giza-exams-25c8krndjcfxvsuaz9zwfm.streamlit.app/'
}

if 'auth_states' not in st.session_state:
    st.session_state['auth_states'] = {'archive': False, 'attendance': False, 'exams': False, 'complaints_admin': False}
else:
    for k in ['archive', 'attendance', 'exams', 'complaints_admin']:
        if k not in st.session_state['auth_states']:
            st.session_state['auth_states'][k] = False

IMG_STAFF_GENZOURY = get_local_image_data('genzoury', 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=300&q=80')
IMG_STAFF_KHALED = get_local_image_data('khaled', 'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=300&q=80')
IMG_STAFF_OMAR = get_local_image_data('omar', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&q=80')

ABOUT_GIZA_BRANCH_IMG = get_local_image_data('about_giza_branch', 'https://images.unsplash.com/photo-1562774053-701939374585?w=800&q=80')
DIGITAL_TRANSFORMATION_IMG = get_local_image_data('digital_transformation', 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80')

CARD_IMG_PROMOTION = get_local_image_data('card_promotion', 'https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=400&q=80')
CARD_IMG_JOB_CHANGE = get_local_image_data('card_job_change', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&q=80')
CARD_IMG_EXAMS = get_local_image_data('card_exams', 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&q=80')
CARD_IMG_TRAINING = get_local_image_data('card_training', 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=400&q=80')
CARD_IMG_ACCREDITATION = get_local_image_data('card_accreditation', 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400&q=80')
CARD_IMG_ASSISTANT = get_local_image_data('card_assistant', 'https://images.unsplash.com/photo-1577896851231-70ef18881754?w=400&q=80')
CARD_IMG_CERTIFICATES = get_local_image_data('card_certificates', 'https://images.unsplash.com/photo-1589330694653-ded6df03f754?w=400&q=80')
CARD_IMG_LEADERSHIP = get_local_image_data('card_leadership', 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=400&q=80')

ACADEMY_URL = "https://pat.edu.eg/"
BRANCH_MAP_URL = "https://www.google.com/maps/place/30%C2%B004'34.3%22N+31%C2%B013'07.5%22E/@30.076194,31.2209387,17z/data=!3m1!4b1!4m4!3m3!8m2!3d30.076194!4d31.21875?entry=ttu&g_ep=EgoyMDI2MTAxMS4wIKXMDSoASAFQAw%3D%3D"

def load_external_css(css_path="assets/css/style.css"):
    """تحميل تنسيقات الواجهة من ملف CSS خارجي مع إبقاء منطق Streamlit منفصلًا."""
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), css_path)
    try:
        with open(full_path, "r", encoding="utf-8") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("تعذر تحميل ملف تصميم المنصة.")

load_external_css()


if 'current_tab' not in st.session_state:
    st.session_state['current_tab'] = 'الرئيسية'

logo_img = get_logo_data("Logo.png")
logo_img_tag = f'<img src="{logo_img}" class="header-logo-img-large" alt="شعار الأكاديمية" />' if logo_img else '<span style="font-size: 3.5rem;">🎓</span>'

st.markdown(f"""<div class="top-bar">
<div class="top-bar-right">
<span>📅 {current_date_time_str}</span>
</div>
<div class="top-bar-center">
<span>🌱 معاً نحو تطوير مهني وتحول رقمي مستدام</span>
</div>
<div class="top-bar-left">
<a href="#">👤 تسجيل الدخول</a> | 
<a href="#">👤 إنشاء حساب</a>
</div>
</div>

<div class="header-branding-container">
<div class="header-vision-box">
<div class="header-box-title">🎯 رؤيتنا</div>
<div class="header-box-desc">الريادة في تقديم خدمات مهنية ورقمية متطورة للمعلمين، وبناء بيئة عمل حديثة تواكب التطور التكنولوجي وتدعم جودة الأداء المؤسسي.</div>
</div>

<div class="header-logo-center">
<div>{logo_img_tag}</div>
<div class="brand-main-title">الأكاديمية المهنية للمعلمين</div>
<div class="brand-sub-title">فرع الجيزة</div>
<div class="brand-slogan-flash">خبرة تتطور، وخدمة تستمر، ورؤية تتجه نحو المستقبل</div>
</div>

<div class="header-mission-box">
<div class="header-box-title">🚀 رسالتنا</div>
<div class="header-box-desc">تقديم خدمات متميزة للكوادر التعليمية، وتوظيف التكنولوجيا والتحول الرقمي لتبسيط الإجراءات، ورفع كفاءة الأداء، وتحسين تجربة المستفيدين من خدمات الفرع.</div>
</div>
</div>""", unsafe_allow_html=True)

tabs_list = [
    'الرئيسية',
    'عن الفرع',
    'فريق العمل',
    'الادارات التعليمية',
    'خدمات الأكاديمية',
    'أحدث التعليمات والقرارات',
    'الشكاوى والمقترحات'
]

st.markdown('<div style="padding: 8px 1.5rem;">', unsafe_allow_html=True)
tab_cols = st.columns(len(tabs_list))

for idx, t_name in enumerate(tabs_list):
    with tab_cols[idx]:
        if st.button(t_name, key=f"fast_tab_{idx}", use_container_width=True):
            st.session_state['current_tab'] = t_name
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

current_tab = st.session_state['current_tab']

if current_tab == 'الرئيسية':
    
    st.markdown("""<div class="hero-banner">
<div class="blink-text">مرحباً بكم في المنصة الرقمية</div>
<div class="hero-title">الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
<div class="hero-subtitle">نحو خدمات تعليمية أكثر كفاءة .. وتحول رقمي مستدام</div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="leadership-banner-card">
<div>
    <div class="leadership-info-title">
        <span>📜</span>
        <span>نظام الاستعلام عن وصول الشهادة للفرع (جديد - تجديد - بدل فاقد)</span>
        <span class="card-badge-new">جديد</span>
    </div>
    <div class="leadership-info-desc">
        خدمة مخصصة لتمكين المعلمين من الاستعلام عن وصول شهاداتهم إلى الفرع، سواء كانت شهادة تجديد أو بدل فاقد أو جديد، لبرامج القيادة والإشراف، وذلك للتأكد من جاهزية الشهادة واستلامها من الفرع بكل سهولة ويسر، دون الحاجة إلى مراجعة الفرع قبل التأكد من وصولها.
    </div>
</div>
<div>
    <a href="{SUB_APP_URLS["certificates"]}" target="_blank" class="leadership-btn-action">🔍 استعلم الآن ↗️</a>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown('<div class="services-title-wrapper"><span>📱</span><span>خدماتنا الإلكترونية</span></div>', unsafe_allow_html=True)
    
    st.markdown(f"""<div class="services-grid-new">
<a href="{SUB_APP_URLS["certificates"]}" target="_blank" class="service-card-link">
    <div class="service-card-new card-red" style="background-image: url('{CARD_IMG_LEADERSHIP}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge">
            <span class="service-title-text"><span class="card-badge-new">جديد</span> الاستعلام عن وصول الشهادات</span>
        </div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-purple" style="background-image: url('{CARD_IMG_PROMOTION}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">الترقيات</span></div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-blue" style="background-image: url('{CARD_IMG_JOB_CHANGE}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">تغيير المسمى</span></div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-orange" style="background-image: url('{CARD_IMG_EXAMS}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">الاختبارات</span></div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-green" style="background-image: url('{CARD_IMG_TRAINING}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">التدريب</span></div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-pink" style="background-image: url('{CARD_IMG_ACCREDITATION}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">الاعتماد</span></div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-cyan" style="background-image: url('{CARD_IMG_ASSISTANT}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">المعلم المساعد</span></div>
    </div>
</a>

<a href="{ACADEMY_URL}" target="_blank" class="service-card-link">
    <div class="service-card-new card-purple" style="background-image: url('{CARD_IMG_CERTIFICATES}');">
        <div class="card-overlay"></div>
        <div class="service-title-badge"><span class="service-title-text">الشهادات</span></div>
    </div>
</a>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="content-layout-grid">
<div class="info-card-box-about">
<div class="card-box-header"><span>🏛️</span><span>عن فرع الأكاديمية بالجيزة</span></div>
<img src="{ABOUT_GIZA_BRANCH_IMG}" class="card-banner-img" alt="عن فرع الأكاديمية المهنية للمعلمين بالجيزة" />
<p style="font-size: 0.88rem; color: #334155; line-height: 1.9; margin-bottom: 12px; font-weight: 400;">أُنشئ فرع الأكاديمية المهنية للمعلمين بالجيزة عام 2017 ليكون مركزًا متخصصًا لخدمة المعلمين والكوادر التعليمية بمحافظة الجيزة، ودعم مسيرتهم المهنية من خلال تقديم الخدمات والإجراءات المرتبطة والتنمية المهنية والترقي والاعتماد.</p>
<p style="font-size: 0.88rem; color: #334155; line-height: 1.9; margin: 0; font-weight: 400;">ومنذ إنشائه، يعمل الفرع على تيسير حصول المعلمين على الخدمات المهنية، وتوفير المعلومات والإرشادات الخاصة بالإجراءات والمواعيد، وتنظيم أعمال الاختبارات والتدريب ومتابعة المستفيدين، بما يحقق سرعة الإنجاز ودقة تقديم الخدمة.</p>
</div>

<div class="info-card-box">
<div class="card-box-header"><span>📢</span><span>أحدث الأخبار والإعلانات</span></div>
<div class="news-item">
<div class="news-date">2026-09-22</div>
<div class="news-title">وصول شهادات مٌعد برامج تدريبية إلى الفرع</div>
<div class="news-desc">يرجى من السادة المجتازين إحضار طابع شهيد فئة 5 جنيهات من البريد لاستلام الشهادة.</div>
</div>
<div class="news-item">
<div class="news-date">2026-08-24</div>
<div class="news-title">تنويه بموعد حجز اختبار المعلمين</div>
<div class="news-desc">نهاية حجز الاختبار يوم 9/9/2026 حتى الساعة 2:00 ظهراً.</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown(f"""<div class="content-layout-grid">
<div class="info-card-box-about" style="border-right-color: #0080FF;">
<div class="card-box-header"><span>🌟</span><span>أبرز خدمات الفرع</span></div>
<ul class="services-two-columns-grid">
<li>التدريب والتنمية المهنية للمعلمين والكوادر التعليمية.</li>
<li>خدمات الترقي واستكمال الإجراءات والاختبارات المرتبطة بها.</li>
<li>اختبارات المعلمين وتنظيم إجراءات الحضور والامتحانات.</li>
<li>خدمات تغيير المسمى الوظيفي وفق الإجراءات والضوابط المنظمة.</li>
<li>خدمات المعلم المساعد ومتابعة الإجراءات الخاصة به.</li>
<li>الاعتماد والشهادات وتسليم الشهادات الخاصة بالبرامج التدريبية.</li>
<li>تقديم الإرشادات والاستفسارات المتعلقة بخدمات الأكاديمية.</li>
<li>إدارة البيانات والإحصائيات الخاصة بأعمال الفرع والمستفيدين.</li>
<li style="grid-column: span 2;">التحول الرقمي وتطوير الأرشيف والخدمات الإلكترونية لتقليل الإجراءات الورقية وتحسين سرعة الوصول إلى المعلومات.</li>
</ul>
<p style="font-size: 0.82rem; color: #1e3a8a; line-height: 1.7; margin-top: 10px; font-weight: 700; background: #f8fafc; padding: 10px 14px; border-radius: 10px; border-right: 4px solid #0080FF;">ويواصل فرع الأكاديمية المهنية للمعلمين بالجيزة العمل على تطوير خدماته وتوظيف التكنولوجيا والتحول الرقمي، بهدف بناء بيئة عمل أكثر تنظيمًا وكفاءة، وتقديم تجربة أفضل للمعلمين والكوادر التعليمية، بما يتوافق مع متطلبات التطوير المؤسسي وجودة الخدمات.</p>
</div>

<div class="info-card-box-digital">
<div class="card-box-header"><span>💻</span><span>نحو التحول الرقمي</span></div>
<img src="{DIGITAL_TRANSFORMATION_IMG}" class="card-banner-img" alt="التحول الرقمي" />
<p style="font-size: 0.85rem; color: #334155; line-height: 1.8; margin-bottom: 8px;">وفى ظل التطور المتسارع في مجال التكنولوجيا، يتجه فرع الأكاديمية المهنية للمعلمين بالجيزة إلى تعزيز التحول الرقمي في بيئة العمل، والاستفادة من الحلول التقنية في تنظيم البيانات والإجراءات والخدمات.</p>
<p style="font-size: 0.85rem; color: #334155; line-height: 1.8; margin-bottom: 8px;">ويمثل التحول الرقمي فرصة مهمة لتطوير الأداء الإداري، من خلال تقليل الاعتماد على الإجراءات الورقية، وتحسين سرعة الوصول إلى المعلومات، وتنظيم عمليات الحفظ والأرشفة، ودعم إعداد التقارير والإحصائيات.</p>
<p style="font-size: 0.85rem; color: #334155; line-height: 1.8; margin: 0;">كما يعمل الفرع على الاستفادة من التطبيقات والمنظومات الرقمية في مجالات متعددة، مثل الأرشيف الإلكتروني، وتنظيم سجلات الحضور، وإدارة بيانات الاختبارات، ومتابعة خدمات الدعم.</p>
</div>
</div>""", unsafe_allow_html=True)

    # =========================================================
    # إحصائيات الصفحة الرئيسية - الأرقام الواردة من إدارة الفرع
    # =========================================================
    st.markdown("""
    <style>
    .stats-main-wrap { direction:rtl; width:min(92%, 980px); margin:14px auto 12px !important; color:#172b4d; display:flex; flex-direction:column; align-items:center; }
    .stats-main-wrap > .stats-section { width:100%; box-sizing:border-box; }
    .stats-main-wrap .stats-section-title { display:block; width:fit-content; max-width:min(94%, 720px); min-width:min(280px, 94%); margin:0 auto 10px !important; text-align:center !important; }
    .stats-main-wrap .stats-subtitle { width:100%; text-align:center !important; margin:0 auto 10px !important; }
    .stats-main-wrap .metric-grid,
    .stats-main-wrap .program-grid,
    .stats-main-wrap .indicator-grid { width:100%; max-width:900px; margin-left:auto !important; margin-right:auto !important; justify-content:center; justify-items:stretch; }
    .stats-main-wrap .metric-card,
    .stats-main-wrap .program-summary,
    .stats-main-wrap .mini-metric,
    .stats-main-wrap .indicator-card { text-align:center !important; align-items:center; justify-content:center; }
    .stats-main-wrap .program-summary h4,
    .stats-main-wrap .metric-label,
    .stats-main-wrap .metric-value,
    .stats-main-wrap .mini-metric span,
    .stats-main-wrap .mini-metric b,
    .stats-main-wrap .indicator-card span,
    .stats-main-wrap .indicator-card b { text-align:center !important; width:100%; }
    .stats-section { background:linear-gradient(145deg,#ffffff 0%,#f4f8fc 100%); border:2px solid #3b82b8; border-radius:16px; padding:12px; margin:8px auto; box-shadow:0 5px 16px rgba(20,45,80,.065); text-align:center; }
    .stats-section-exams { border-color:#45a6d9 !important; }
    .stats-section-program-heading, .stats-section-programs { border-color:#52a7a0 !important; }
    .stats-section-indicators { border-color:#7c6ac8 !important; }
    .stats-section-cpd { border-color:#d39a35 !important; }
    .stats-section-title { background:linear-gradient(110deg,#10233f 0%,#174a82 58%,#176ca3 100%); color:#fff; border-radius:11px; padding:10px 14px; font-size:1.06rem; font-weight:800; text-align:center; margin:0 auto 14px; max-width:720px; box-shadow:0 4px 12px rgba(16,42,86,.14); letter-spacing:.1px; }
    .stats-subtitle { text-align:center; color:#42617f; font-weight:700; margin:0 auto 15px; line-height:1.6; }
    .metric-grid { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:8px; max-width:960px; margin:0 auto; justify-content:center; }
    .cpd-total-grid { display:grid !important; grid-template-columns:repeat(4,minmax(150px,1fr)) !important; width:fit-content !important; max-width:100% !important; margin:0 auto 16px !important; justify-content:center !important; justify-items:stretch !important; }
    .metric-card { background:linear-gradient(145deg,#173e70,#102743); color:#fff; border:1px solid #45a6d9; border-top:3px solid #45a6d9; border-radius:12px; padding:12px 8px; text-align:center; min-height:88px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px; box-shadow:0 4px 12px rgba(15,57,116,.09); }
    .metric-card:nth-child(5n+2) { background:linear-gradient(145deg,#176ca3,#14527d); border-color:#65c7e8; border-top-color:#65c7e8; }
    .metric-card:nth-child(5n+3) { background:linear-gradient(145deg,#087f8c,#075c68); border-color:#52c7bc; border-top-color:#52c7bc; }
    .metric-card:nth-child(5n+4) { background:linear-gradient(145deg,#b94a55,#873342); border-color:#f49aa2; border-top-color:#f49aa2; }
    .metric-card:nth-child(5n+5) { background:linear-gradient(145deg,#b77922,#8a5415); border-color:#f4c46a; border-top-color:#f4c46a; }
    .cpd-total-grid .metric-card:nth-child(1) { border-color:#45a6d9; }
    .cpd-total-grid .metric-card:nth-child(2) { border-color:#52c7bc; }
    .cpd-total-grid .metric-card:nth-child(3) { border-color:#f49aa2; }
    .cpd-total-grid .metric-card:nth-child(4) { border-color:#f4c46a; }
    .metric-label { font-size:.82rem; font-weight:750; line-height:1.5; text-align:center; }
    .metric-value { font-size:1.42rem; font-weight:900; color:#fff; line-height:1.25; text-align:center; font-variant-numeric:tabular-nums; }
    .program-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:9px; max-width:960px; margin:0 auto; justify-content:center; }
    .program-summary { background:linear-gradient(155deg,#ffffff,#f4f8fc); border:1px solid #d7e2ed; border-top:3px solid #2675a8; border-radius:13px; padding:12px; box-shadow:0 4px 12px rgba(16,42,86,.055); text-align:center; }
    .program-summary:nth-child(4n+2) { border-top-color:#0e9c9a; }
    .program-summary:nth-child(4n+3) { border-top-color:#7c6ac8; }
    .program-summary:nth-child(4n+4) { border-top-color:#d39a35; }
    .program-summary h4 { color:#183b60; text-align:center; margin:0 auto 11px; font-size:.94rem; line-height:1.55; font-weight:800; }
    .mini-metrics { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
    .mini-metric { background:linear-gradient(145deg,#28557d,#173a5b); border:1px solid #d6e3ef; border-radius:9px; padding:9px 6px; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:65px; }
    .mini-metric:nth-child(4n+2) { background:linear-gradient(145deg,#236f93,#164d69); border-color:#c6e5f2; }
    .mini-metric:nth-child(4n+3) { background:linear-gradient(145deg,#17756f,#10534f); border-color:#c6e9dc; }
    .mini-metric:nth-child(4n+4) { background:linear-gradient(145deg,#8d4650,#65313a); border-color:#f4d4d1; }
    .mini-metric span { display:block; color:#fff; font-size:.76rem; line-height:1.45; text-align:center; }
    .mini-metric b { display:block; color:#fff !important; font-size:1.15rem; font-weight:900; margin:4px auto 0; line-height:1.25; text-align:center; text-shadow:0 1px 3px rgba(0,0,0,.45); }
    .indicator-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; max-width:960px; margin:0 auto; justify-content:center; }
    .indicator-card { background:linear-gradient(145deg,#edf5fc,#e2edf7); border:1px solid #d2e1ef; border-right:4px solid #2675a8; border-radius:11px; padding:12px 9px; text-align:center; display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:88px; }
    .indicator-card:nth-child(6n+2) { background:linear-gradient(145deg,#f0edfc,#e7e1fa); border-right-color:#7c6ac8; }
    .indicator-card:nth-child(6n+3) { background:linear-gradient(145deg,#e8f7f5,#d9f0ed); border-right-color:#0e9c9a; }
    .indicator-card:nth-child(6n+4) { background:linear-gradient(145deg,#fff5e8,#ffebd2); border-right-color:#d39a35; }
    .indicator-card:nth-child(6n+5) { background:linear-gradient(145deg,#fff0f1,#fce0e3); border-right-color:#d65b68; }
    .indicator-card:nth-child(6n+6) { background:linear-gradient(145deg,#e9f5fb,#d9edf8); border-right-color:#3894c4; }
    .indicator-card span { display:block; font-size:.82rem; font-weight:750; color:#244763; line-height:1.5; text-align:center; }
    .indicator-card b { display:block; font-size:1.35rem; color:#163b60; margin:6px auto 0; text-align:center; }
    @media(min-width:1100px){ .program-grid{grid-template-columns:repeat(2,minmax(0,1fr)); max-width:880px;} .indicator-grid{max-width:880px;} .metric-grid{max-width:880px;} }
    @media(max-width:900px){ .metric-grid{grid-template-columns:repeat(3,minmax(0,1fr));} .program-grid{grid-template-columns:repeat(2,minmax(0,1fr));} .indicator-grid{grid-template-columns:repeat(2,minmax(0,1fr));} }
    @media(max-width:560px){ .stats-main-wrap{width:96%;} .stats-section{padding:10px;} .metric-grid{grid-template-columns:repeat(2,minmax(0,1fr));} .cpd-total-grid{grid-template-columns:repeat(2,minmax(0,1fr)) !important; width:100% !important;} .program-grid{grid-template-columns:1fr;} .indicator-grid{grid-template-columns:repeat(2,minmax(0,1fr));} .stats-section-title{font-size:1rem; min-width:0;} }
    </style>
    <div class="stats-main-wrap"><div class="stats-section stats-section-exams">
    <div class="stats-section-title">📊 إحصائيات الاختبارات العامة</div>
    <div class="stats-subtitle">إحصائيات فترة (12-8-2026 إلى 10-9-2026)</div>
    <div class="metric-grid">
      <div class="metric-card"><div class="metric-label">📊 إجمالي الممتحنين</div><div class="metric-value">559</div></div>
      <div class="metric-card"><div class="metric-label">🎟️ حجز اختبار</div><div class="metric-value">1</div></div>
      <div class="metric-card"><div class="metric-label">✅ ناجحين</div><div class="metric-value">554</div></div>
      <div class="metric-card"><div class="metric-label">❌ راسبين</div><div class="metric-value">0</div></div>
      <div class="metric-card"><div class="metric-label">⏳ قيد الاختبار</div><div class="metric-value">4</div></div>
    </div></div></div>
    """, unsafe_allow_html=True)

    exam_programs = {
        'تطبيقات تربوية للمعلم المساعد': {'total': 428, 'booking': 0, 'passed': 428, 'failed': 0, 'pending': 0},
        'مدير ووكيل إدارة مدرسية': {'total': 85, 'booking': 1, 'passed': 82, 'failed': 0, 'pending': 2},
        'مدير ووكيل إدارة تعليمية': {'total': 7, 'booking': 0, 'passed': 7, 'failed': 0, 'pending': 0},
        'أساسيات التوجيه الفني': {'total': 7, 'booking': 0, 'passed': 7, 'failed': 0, 'pending': 0},
    }
    st.markdown('<div class="stats-main-wrap"><div class="stats-section stats-section-program-heading"><div class="stats-section-title">🎓 إحصائيات كل برنامج تدريبي</div></div></div>', unsafe_allow_html=True)
    cards_html = '<div class="stats-main-wrap"><div class="stats-section stats-section-programs"><div class="program-grid">'
    for program_name, values in exam_programs.items():
        cards_html += f'''<div class="program-summary"><h4>{program_name}</h4><div class="mini-metrics">
        <div class="mini-metric"><span>📊 إجمالي الممتحنين</span><b>{values['total']}</b></div>
        <div class="mini-metric"><span>🎟️ حجز اختبار</span><b>{values['booking']}</b></div>
        <div class="mini-metric"><span>✅ ناجحين</span><b>{values['passed']}</b></div>
        <div class="mini-metric"><span>❌ راسبين</span><b>{values['failed']}</b></div>
        <div class="mini-metric" style="grid-column:1/-1"><span>⏳ قيد الاختبار</span><b>{values['pending']}</b></div>
        </div></div>'''
    cards_html += '</div></div></div>'
    st.markdown(cards_html, unsafe_allow_html=True)

    indicators = [('معد البرامج التدريبية', 80), ('إعادة التعيين (قرار 160)', 136), ('المسمى الوظيفي', 565), ('معلم مساعد (الدفعة الأولى)', 1110), ('التسكين على الكادر الإجمالي', 30), ('معلم مساعد (الدفعة الثانية)', 956)]
    indicators_html = ''.join(f'<div class="indicator-card"><span>{name}</span><b>{value:,}</b></div>' for name, value in indicators)
    st.markdown('<div class="stats-main-wrap"><div class="stats-section stats-section-indicators"><div class="stats-section-title">📌 مؤشرات الإحصاء العامة لبرامج الفرع</div><div class="indicator-grid">' + indicators_html + '</div></div></div>', unsafe_allow_html=True)

    cpd_groups = [
        ('📚 التطبيقات التربوية للمعلم المساعد 2025/2026', 655, 644, 0, 11),
        ('👔 تدريب القيادات / التوجيه الفني 2025/2026', 62, 44, 0, 18),
        ('🏫 تدريب القيادات مدير/وكيل إدارة مدرسية 2025/2026', 251, 207, 2, 42),
        ('🏢 تدريب القيادات مدير/وكيل إدارة تعليمية 2025/2026', 18, 8, 0, 10),
    ]
    cpd_html = '''<div class="stats-main-wrap"><div class="stats-section stats-section-cpd"><div class="stats-section-title">📊 نتيجة منصة CPD حتى 12-5-2026</div>
    <div class="stats-subtitle">🌟 الإجمالي العام لجميع برامج منصة الوزارة CPD</div><div class="metric-grid cpd-total-grid">
    <div class="metric-card"><div class="metric-label">إجمالي المتدربين</div><div class="metric-value">986</div></div>
    <div class="metric-card"><div class="metric-label">إجمالي الاجتياز</div><div class="metric-value">903</div></div>
    <div class="metric-card"><div class="metric-label">إجمالي عدم الاجتياز</div><div class="metric-value">2</div></div>
    <div class="metric-card"><div class="metric-label">إجمالي عدم الحضور</div><div class="metric-value">81</div></div></div><div class="program-grid">'''
    for title, total, passed, failed, absent in cpd_groups:
        cpd_html += f'''<div class="program-summary"><h4>{title}</h4><div class="mini-metrics">
        <div class="mini-metric"><span>الإجمالي</span><b>{total}</b></div><div class="mini-metric"><span>اجتياز</span><b>{passed}</b></div>
        <div class="mini-metric"><span>عدم اجتياز</span><b>{failed}</b></div><div class="mini-metric"><span>عدم حضور</span><b>{absent}</b></div>
        </div></div>'''
    cpd_html += '</div></div></div>'
    st.markdown(cpd_html, unsafe_allow_html=True)

elif current_tab == 'خدمات الأكاديمية':
    st.markdown("""
    <section class="systems-hero">
        <div class="systems-hero-icon">⚙️</div>
        <div>
            <div class="systems-kicker">بوابة الأنظمة الرقمية</div>
            <h2>خدمات الأكاديمية والمنظومات الإلكترونية</h2>
            <p>الوصول السريع إلى منظومات فرع الجيزة لإدارة الأرشيف، الحضور، الشهادات، والاختبارات من واجهة موحدة.</p>
        </div>
    </section>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="systems-note">
        <span class="systems-note-icon">💡</span>
        <div><b>ملاحظة:</b> الأنظمة الإدارية محمية بكلمة مرور، بينما خدمة الاستعلام عن وصول الشهادات متاحة للمعلمين مباشرة.</div>
    </div>
    """, unsafe_allow_html=True)

    systems = [
        {
            'key':'archive','title':'الأرشيف الرقمي','short':'الوارد والصادر','icon':'📁',
            'theme':'system-blue','desc':'إدارة المكاتبات والوثائق إلكترونيًا مع البحث، التسجيل، المتابعة، وإرفاق الملفات.',
            'url':SUB_APP_URLS['archive'],'protected':True,'button':'فتح منظومة الأرشيف'
        },
        {
            'key':'attendance','title':'أسبقية الحضور','short':'الحضور والتذاكر','icon':'🎫',
            'theme':'system-violet','desc':'تنظيم أرقام الحضور وتسجيل بيانات المستفيدين وإدارة سجلات اليوم بطريقة رقمية.',
            'url':SUB_APP_URLS['attendance'],'protected':True,'button':'فتح منظومة الحضور'
        },
        {
            'key':'certificates','title':'الاستعلام عن الشهادات','short':'جديد • تجديد • بدل فاقد','icon':'📜',
            'theme':'system-green','desc':'الاستعلام عن وصول شهادات القيادة والإشراف إلى فرع الجيزة قبل التوجه للاستلام.',
            'url':SUB_APP_URLS['certificates'],'protected':False,'button':'استعلام عن الشهادة'
        },
        {
            'key':'exams','title':'الاختبارات والامتحانات','short':'الحجز والنتائج والإحصائيات','icon':'📝',
            'theme':'system-orange','desc':'إدارة بيانات الممتحنين، متابعة الاختبارات، النتائج، والإحصائيات الخاصة بالبرامج.',
            'url':SUB_APP_URLS['exams'],'protected':True,'button':'فتح منظومة الاختبارات'
        },
    ]

    # عرض المنظومات في عمودين ثابتين على سطح المكتب
    system_columns = st.columns(2, gap="medium")
    for idx, sys in enumerate(systems):
        with system_columns[idx % 2]:
            badge = 'إدارة' if sys['protected'] else 'متاح للمعلمين'
            lock = '🔒' if sys['protected'] else '🌐'
            st.markdown(f"""
            <div class="system-card {sys['theme']}">
                <div class="system-card-top">
                    <div class="system-icon">{sys['icon']}</div>
                    <span class="system-badge">{lock} {badge}</span>
                </div>
                <div class="system-card-content">
                    <div class="system-short">{sys['short']}</div>
                    <h3>{sys['title']}</h3>
                    <p>{sys['desc']}</p>
                </div>
            """, unsafe_allow_html=True)

            if not sys['protected']:
                st.markdown(f'<a class="system-action system-action-open" href="{sys["url"]}" target="_blank">{sys["button"]} <span>↗</span></a>', unsafe_allow_html=True)
            else:
                if st.session_state['auth_states'].get(sys['key'], False):
                    st.markdown(f'<div class="system-auth-ok">✓ تم التحقق من صلاحية الدخول</div>', unsafe_allow_html=True)
                    st.markdown(f'<a class="system-action" href="{sys["url"]}" target="_blank">{sys["button"]} <span>↗</span></a>', unsafe_allow_html=True)
                else:
                    pwd = st.text_input('كلمة المرور', type='password', key=f"v4_pwd_{sys['key']}", placeholder='أدخل كلمة المرور للدخول', label_visibility='collapsed')
                    if st.button('🔓 التحقق والدخول', key=f"v4_login_{sys['key']}", use_container_width=True):
                        if pwd == ADMIN_PASSWORD:
                            st.session_state['auth_states'][sys['key']] = True
                            st.rerun()
                        else:
                            st.error('❌ كلمة المرور غير صحيحة.')

            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="systems-bottom-grid">
        <div class="systems-feature">
            <div class="systems-feature-icon">🔎</div>
            <div><h4>واجهة موحدة</h4><p>جميع الأنظمة متاحة من مكان واحد مع هوية بصرية موحدة وسهولة في الوصول.</p></div>
        </div>
        <div class="systems-feature">
            <div class="systems-feature-icon">🛡️</div>
            <div><h4>حماية الصلاحيات</h4><p>الأنظمة الإدارية لا تُفتح إلا بعد التحقق من كلمة مرور الإدارة.</p></div>
        </div>
        <div class="systems-feature">
            <div class="systems-feature-icon">📊</div>
            <div><h4>بيانات وتقارير</h4><p>دعم المتابعة والإحصائيات والبحث لتسهيل أعمال الفرع اليومية.</p></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif current_tab == 'عن الفرع':
    st.html("""
    <div style="padding: 20px 1.5rem; max-width: 1000px; margin: 0 auto;">
        <div class="info-card-box-about" style="padding: 32px; border-right: 6px solid #0080FF;">
            <div style="font-size: 1.35rem; font-weight: 800; color: #1e3a8a; margin-bottom: 22px; display: flex; align-items: center; gap: 10px;">
                <span>🏛️</span>
                <span>عن فرع الأكاديمية المهنية للمعلمين بمحافظة الجيزة</span>
            </div>
            
            <div style="background: #f8fafc; border-radius: 14px; padding: 20px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
                <div style="font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                    <span>🏛️</span>
                    <span>التأسيس والانطلاقة</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; line-height: 1.95; margin: 0;">
                    أُنشئ فرع الأكاديمية المهنية للمعلمين بمحافظة الجيزة في عام 2017 ليكون الحاضنة الرئيسية لتطوير وتمكين الكوادر التعليمية والتربوية بالمحافظة، وتقديم الخدمات الاعتمادية والتدريبية وفق أعلى معايير الجودة.
                </p>
            </div>

            <div style="background: #f8fafc; border-radius: 14px; padding: 20px; border: 1px solid #e2e8f0; margin-bottom: 20px;">
                <div style="font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                    <span>📜</span>
                    <span>مرحلة البناء (2017 - 2023)</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; line-height: 1.95; margin-bottom: 12px;">
                    شهدت إرساء القواعد التنظيمية والإدارية للفرع تحت قيادة الأستاذة / أمل عبد المقصود (مدير الفرع)، بمعاونة فريق تكنولوجيا المعلومات:
                </p>
                <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                    <li style="font-size: 0.88rem; color: #334155; display: flex; align-items: center; gap: 8px; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <span>💻</span> <b>أ . أحمد حسني الجنزوري</b> (IT)
                    </li>
                    <li style="font-size: 0.88rem; color: #334155; display: flex; align-items: center; gap: 8px; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <span>💻</span> <b>أ . خالد عبد الحكيم هارون</b> (IT)
                    </li>
                </ul>
            </div>

            <div style="background: #f8fafc; border-radius: 14px; padding: 20px; border: 1px solid #e2e8f0;">
                <div style="font-size: 1.05rem; font-weight: 800; color: #1e3a8a; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                    <span>🚀</span>
                    <span>التطوير الرقمي (2023 - الآن)</span>
                </div>
                <p style="font-size: 0.9rem; color: #334155; line-height: 1.95; margin-bottom: 12px;">
                    انطلاقة الكترونية برئاسة الأستاذ / أحمد حسني الجنزوري مديراً للفرع، لميكنة الخدمات وتيسير البرامج بالتعاون مع فريق العمل:
                </p>
                <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 8px;">
                    <li style="font-size: 0.88rem; color: #334155; display: flex; align-items: center; gap: 8px; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <span>🤝</span> <b>أ . خالد عبد الحكيم</b> (موارد بشرية و IT)
                    </li>
                    <li style="font-size: 0.88rem; color: #334155; display: flex; align-items: center; gap: 8px; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <span>🎯</span> <b>أ . أحمد محمد عمر</b> (التنمية المهنية)
                    </li>
                    <li style="font-size: 0.88rem; color: #334155; display: flex; align-items: center; gap: 8px; background: #ffffff; padding: 10px 14px; border-radius: 10px; border: 1px solid #e2e8f0;">
                        <span>🎯</span> <b>أ . أمينة فوزي</b> (التنمية المهنية)
                    </li>
                </ul>
            </div>
        </div>
    </div>
    """)

elif current_tab == 'فريق العمل':
    st.markdown('<div style="padding: 15px 1.5rem; text-align: center;"><h3 style="color: #1e3a8a; font-weight: 800; margin-bottom: 25px;">👥 إدارة الأفراد وفريق العمل بالفرع</h3></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 0 1.5rem;">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="team-card">
            <div>
                <div class="team-img-wrapper" style="background-image: url('{IMG_STAFF_GENZOURY}');"></div>
                <div class="team-name">أ/ أحمد الجنزوري</div>
                <div class="team-role">مدير الفرع</div>
            </div>
            <a href="https://wa.me/201069996245" target="_blank" class="team-whatsapp-btn">
                <span>💬</span> <span>01069996245</span>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="team-card">
            <div>
                <div class="team-img-wrapper" style="background-image: url('{IMG_STAFF_KHALED}');"></div>
                <div class="team-name">أ/ خالد هارون</div>
                <div class="team-role">عضو تكنولوجيا المعلومات</div>
            </div>
            <a href="https://wa.me/201120807631" target="_blank" class="team-whatsapp-btn">
                <span>💬</span> <span>01120807631</span>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="team-card">
            <div>
                <div class="team-img-wrapper" style="background-image: url('{IMG_STAFF_OMAR}');"></div>
                <div class="team-name">أ/ أحمد عمر</div>
                <div class="team-role">عضو التنمية المهنية</div>
            </div>
            <a href="https://wa.me/201201109892" target="_blank" class="team-whatsapp-btn">
                <span>💬</span> <span>01201109892</span>
            </a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif current_tab == 'الادارات التعليمية':
    if 'edarat_db' not in st.session_state:
        st.session_state['edarat_db'] = load_edarat_data()

    if 'selected_edara' not in st.session_state:
        st.session_state['selected_edara'] = None

    if 'search_query' not in st.session_state:
        st.session_state['search_query'] = ''

    st.markdown("""
        <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0080FF 100%); color: #ffffff; padding: 20px 18px; border-radius: 14px; margin: 0 auto 22px auto; box-shadow: 0 6px 18px rgba(0,128,255,0.2); text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; box-sizing: border-box;">
            <h4 style="width:100%; margin: 0; font-size: 1.15rem; font-weight: 800; color: #ffffff; text-align: center;">🏛️ دليل الإدارات التعليمية ومسؤولي الخدمات</h4>
            <p style="width:100%; max-width:900px; margin: 9px auto 0 auto; padding: 0 8px; font-size: 0.82rem; line-height: 1.8; color: #e0f2fe; text-align: center; align-self: center;">استعرض بيانات مسؤولي الإدارات التعليمية التابعة لمحافظة الجيزة وطرق التواصل الرسمية</p>
        </div>
    """, unsafe_allow_html=True)

    if 'platform_admin_authenticated' not in st.session_state:
        st.session_state['platform_admin_authenticated'] = False

    if not st.session_state['platform_admin_authenticated']:
        if st.session_state['selected_edara']:
            selected_for_login = st.session_state['selected_edara']
            st.markdown(f"""
                <div style="max-width:620px; margin:24px auto; padding:24px; background:#eff6ff; border:1px solid #93c5fd; border-radius:16px; text-align:center;">
                    <div style="font-size:1.2rem; font-weight:800; color:#1d4ed8; margin-bottom:8px;">🔐 دخول إدارة المنصة</div>
                    <div style="color:#334155; font-size:.95rem;">لعرض بيانات المسؤولين الخاصة بـ <b>إدارة {selected_for_login}</b>، يرجى تسجيل الدخول بصلاحية إدارة المنصة.</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("⬅️ العودة إلى أسماء الإدارات التعليمية", use_container_width=True, key="back_to_public_edarat"):
                st.session_state['selected_edara'] = None
                st.rerun()
            with st.form("platform_admin_login_form"):
                platform_pwd = st.text_input("كلمة مرور إدارة المنصة", type="password", placeholder="أدخل كلمة المرور")
                platform_login = st.form_submit_button("🔓 تسجيل الدخول", use_container_width=True)
            if platform_login:
                if platform_pwd == ADMIN_PASSWORD:
                    st.session_state['platform_admin_authenticated'] = True
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة.")
        else:
            col_s1, col_s2 = st.columns([4, 1], gap="small")
            with col_s1:
                input_query = st.text_input("بحث عن إدارة تعليمية", placeholder="اكتب اسم الإدارة (مثال: الهرم، الدقي، أكتوبر...)", value=st.session_state['search_query'], label_visibility="collapsed", key="public_edara_search")
            with col_s2:
                search_clicked = st.button("🔍 بحث", use_container_width=True, key="public_edara_search_btn")
            if search_clicked:
                st.session_state['search_query'] = input_query
                st.rerun()
            search_edara_query = st.session_state['search_query']
            filtered_edarat = [ed for ed in EDARAT_LIST if not search_edara_query or search_edara_query.strip() in ed]
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if not filtered_edarat:
                st.warning("لم يتم العثور على إدارة تعليمية تطابق بحثك.")
            else:
                num_cols = 5
                rows = [filtered_edarat[i:i + num_cols] for i in range(0, len(filtered_edarat), num_cols)]
                edara_icons = ["🏫", "🎓", "🏢", "📚", "🏛️"]
                for row_idx, row in enumerate(rows):
                    cols = st.columns(len(row))
                    for idx, edara in enumerate(row):
                        with cols[idx]:
                            edara_icon = edara_icons[(row_idx * num_cols + idx) % len(edara_icons)]
                            if st.button(f"{edara_icon} إدارة {edara}", key=f"public_edara_name_{row_idx}_{idx}_{edara}", use_container_width=True):
                                st.session_state['selected_edara'] = edara
                                st.rerun()
    else:
        logout_col1, logout_col2 = st.columns([5, 1])
        with logout_col2:
            if st.button("تسجيل الخروج", key="platform_admin_logout"):
                st.session_state['platform_admin_authenticated'] = False
                st.session_state['selected_edara'] = None
                st.rerun()
        if st.session_state['selected_edara']:
            current_edara = st.session_state['selected_edara']
        
            if st.button("⬅️ العودة إلى قائمة كافة الإدارات التعليمية"):
                st.session_state['selected_edara'] = None
                st.rerun()

            st.markdown(f"""
                <div style="background: #ffffff; border-right: 6px solid #0080FF; padding: 15px 20px; border-radius: 12px; margin: 15px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.03);">
                    <h4 style="margin:0; color:#1e3a8a; font-weight:800;">📍 لوحة تحكم وعرض بيانات مسؤولي إدارة: {current_edara}</h4>
                </div>
            """, unsafe_allow_html=True)

            edara_records = st.session_state['edarat_db'].get(current_edara, [])

            for idx, record in enumerate(edara_records):
                with st.expander(f"📁 سجل المسؤولين والقيادات رقم ({idx + 1})", expanded=(idx == 0)):
                    with st.form(key=f"form_edit_v3_{current_edara}_{idx}"):
                        col_e1, col_e2 = st.columns(2, gap="medium")
                        with col_e1:
                            m_name = st.text_input("مدير الإدارة - الاسم", value=record.get('mgr_name', ''))
                            h_name = st.text_input("مدير شؤون العاملين - الاسم", value=record.get('hr_name', ''))
                            s_name = st.text_input("مدير الإحصاء - الاسم", value=record.get('stat_name', ''))
                        with col_e2:
                            m_phone = st.text_input("مدير الإدارة - تليفون / واتس", value=record.get('mgr_phone', ''))
                            h_phone = st.text_input("مدير شؤون العاملين - تليفون / واتس", value=record.get('hr_phone', ''))
                            s_phone = st.text_input("مدير الإحصاء - تليفون / واتس", value=record.get('stat_phone', ''))
                    
                        st.markdown("---")
                        col_save, col_del = st.columns(2)
                        submitted = col_save.form_submit_button("💾 حفظ التعديلات المعتمدة", use_container_width=True)
                        deleted = col_del.form_submit_button("🗑️ حذف هذا السجل", use_container_width=True)

                        if submitted:
                            st.session_state['edarat_db'][current_edara][idx] = {
                                'mgr_name': m_name, 'mgr_phone': m_phone,
                                'hr_name': h_name, 'hr_phone': h_phone,
                                'stat_name': s_name, 'stat_phone': s_phone
                            }
                            save_edarat_data(st.session_state['edarat_db'])
                            st.success("✅ تم تحديث وحفظ بيانات السجل بنجاح!")
                            st.rerun()

                        if deleted:
                            if len(edara_records) > 1:
                                del st.session_state['edarat_db'][current_edara][idx]
                                save_edarat_data(st.session_state['edarat_db'])
                                st.success("🗑️ تم حذف السجل بنجاح!")
                                st.rerun()
                            else:
                                st.warning("⚠️ عذراً، لا يمكن حذف السجل الأخير، يمكنك تعديل بياناته.")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ إضافة سجل مسؤولي إدارة جديد", use_container_width=True):
                st.session_state['edarat_db'][current_edara].append({
                    'mgr_name': 'الاسم', 'mgr_phone': '01000000000',
                    'hr_name': 'الاسم', 'hr_phone': '01000000000',
                    'stat_name': 'الاسم', 'stat_phone': '01000000000'
                })
                save_edarat_data(st.session_state['edarat_db'])
                st.rerun()

        else:
            col_s1, col_s2 = st.columns([4, 1], gap="small")
            with col_s1:
                input_query = st.text_input("بحث بالاسم", placeholder="اكتب اسم الإدارة (مثال: الهرم، الدقي، أكتوبر...)", value=st.session_state['search_query'], label_visibility="collapsed")
            with col_s2:
                search_clicked = st.button("🔍 بحث", use_container_width=True)
        
            if search_clicked:
                st.session_state['search_query'] = input_query
                st.rerun()

            search_edara_query = st.session_state['search_query']
            st.markdown("<br>", unsafe_allow_html=True)
        
            filtered_edarat = [ed for ed in EDARAT_LIST if not search_edara_query or search_edara_query.strip() in ed]

            if not filtered_edarat:
                st.warning("⚠️ عذراً، لم يتم العثور على إدارة تعليمية تطابق بحثك.")
            else:
                num_cols = 4
                rows = [filtered_edarat[i:i + num_cols] for i in range(0, len(filtered_edarat), num_cols)]
            
                card_colors = [
                    "linear-gradient(135deg, #eff6ff 0%, #ffffff 100%)",
                    "linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%)",
                    "linear-gradient(135deg, #faf5ff 0%, #ffffff 100%)",
                    "linear-gradient(135deg, #fff7ed 0%, #ffffff 100%)"
                ]
            
                for r_idx, row in enumerate(rows):
                    cols = st.columns(len(row))
                    for idx, edara in enumerate(row):
                        bg_color = card_colors[(r_idx * num_cols + idx) % len(card_colors)]
                        with cols[idx]:
                            st.markdown(f"""
                                <div style="background: {bg_color}; border: 1px solid #cbd5e1; border-radius: 14px; padding: 20px 15px; text-align: center; margin-bottom: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.04); display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 120px;">
                                    <div style="font-size: 2.1rem; margin-bottom: 8px; text-align: center;">🏫</div>
                                    <div style="font-size: 1.05rem; font-weight: 800; color: #1e3a8a; text-align: center; width: 100%;">إدارة {edara}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                            if st.button(f"📂 استعراض المسؤولين", key=f"card_btn_{edara}", use_container_width=True):
                                st.session_state['selected_edara'] = edara
                                st.rerun()

elif current_tab == 'أحدث التعليمات والقرارات':
    st.markdown("""<div style="padding: 20px 1.5rem;">
<div class="info-card-box-about" style="padding: 28px;">
<div style="font-size: 1.2rem; font-weight: 800; color: #1e3a8a; margin-bottom: 16px; direction: rtl; text-align: right;">📜 أحدث التعليمات والقرارات الوزارية والمؤسسية</div>
</div>
</div>""", unsafe_allow_html=True)

elif current_tab == 'الشكاوى والمقترحات':
    st.markdown("""
      <style>
      div[data-baseweb="tab-list"] {
          gap: 12px !important;
          background: #f1f5f9 !important;
          padding: 8px !important;
          border-radius: 16px !important;
          margin: 4px 0 24px 0 !important;
          border: 1px solid #e2e8f0 !important;
      }
      button[data-baseweb="tab"] {
          flex: 1 1 0 !important;
          min-height: 58px !important;
          border-radius: 12px !important;
          background: #ffffff !important;
          border: 1px solid #dbe4f0 !important;
          color: #334155 !important;
          font-weight: 800 !important;
          justify-content: center !important;
          box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04) !important;
      }
      button[data-baseweb="tab"] p, button[data-baseweb="tab"] div, button[data-baseweb="tab"] span {
          text-align: center !important;
          justify-content: center !important;
          color: inherit !important;
          font-weight: 800 !important;
      }
      button[data-baseweb="tab"][aria-selected="true"] {
          background: linear-gradient(135deg, #0080FF 0%, #0060df 100%) !important;
          color: #ffffff !important;
          border-color: #0080FF !important;
          box-shadow: 0 8px 18px rgba(0, 128, 255, 0.24) !important;
      }
      div[data-baseweb="tab-highlight"] {display: none !important;}
      div[data-baseweb="tab-border"] {display: none !important;}
      @media (max-width: 700px) {
          div[data-baseweb="tab-list"] {gap: 6px !important; padding: 6px !important;}
          button[data-baseweb="tab"] {min-height: 64px !important; padding: 8px 6px !important;}
          button[data-baseweb="tab"] p {font-size: 0.72rem !important; white-space: normal !important; line-height: 1.45 !important;}
      }
      </style>
      """, unsafe_allow_html=True)

    st.markdown('<div style="max-width: 920px; margin: 28px auto; direction: rtl !important;">', unsafe_allow_html=True)
    
    st.markdown("""
      <div style="position:relative; overflow:hidden; background:linear-gradient(135deg,#0f3b82 0%,#1d4ed8 55%,#0080FF 100%); border-radius:22px; padding:32px 28px; margin-bottom:18px; box-shadow:0 16px 35px rgba(30,64,175,.22); text-align:center !important;">
          <div style="position:absolute; width:190px; height:190px; border-radius:50%; background:rgba(255,255,255,.07); top:-95px; left:-55px;"></div>
          <div style="position:absolute; width:120px; height:120px; border-radius:50%; background:rgba(255,255,255,.06); bottom:-65px; right:-25px;"></div>
          <div style="position:relative; z-index:2; width:62px; height:62px; margin:0 auto 13px auto; border-radius:18px; background:rgba(255,255,255,.16); border:1px solid rgba(255,255,255,.25); display:flex; align-items:center; justify-content:center; font-size:1.8rem;">💬</div>
          <div style="position:relative; z-index:2; width:100%; display:flex; align-items:center; justify-content:center; color:#ffffff; font-size:1.55rem; font-weight:800; text-align:center !important; margin:0 auto 8px auto;">بوابة الشكاوى والمقترحات</div>
          <div style="position:relative; z-index:2; color:#dbeafe; font-size:.92rem; line-height:1.9; max-width:680px; margin:0 auto; text-align:center !important;">نحن هنا دائماً لسماع مقترحاتكم وحل مشكلاتكم لتقديم أفضل خدمة تعليمية</div>
      </div>

      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:0 0 22px 0;">
          <div style="background:#ffffff; border:1px solid #dbeafe; border-radius:15px; padding:14px 12px; text-align:center !important; box-shadow:0 5px 14px rgba(15,23,42,.04);">
              <div style="font-size:1.35rem; margin-bottom:5px;">📝</div>
              <div style="font-size:.82rem; font-weight:800; color:#1e3a8a; text-align:center !important;">أرسل طلبك</div>
              <div style="font-size:.72rem; color:#64748b; margin-top:3px; text-align:center !important;">سجّل الشكوى أو المقترح بسهولة</div>
          </div>
          <div style="background:#ffffff; border:1px solid #dbeafe; border-radius:15px; padding:14px 12px; text-align:center !important; box-shadow:0 5px 14px rgba(15,23,42,.04);">
              <div style="font-size:1.35rem; margin-bottom:5px;">🎫</div>
              <div style="font-size:.82rem; font-weight:800; color:#1e3a8a; text-align:center !important;">احتفظ برقم التذكرة</div>
              <div style="font-size:.72rem; color:#64748b; margin-top:3px; text-align:center !important;">يصدر لك رقم متابعة تلقائياً</div>
          </div>
          <div style="background:#ffffff; border:1px solid #dbeafe; border-radius:15px; padding:14px 12px; text-align:center !important; box-shadow:0 5px 14px rgba(15,23,42,.04);">
              <div style="font-size:1.35rem; margin-bottom:5px;">🔎</div>
              <div style="font-size:.82rem; font-weight:800; color:#1e3a8a; text-align:center !important;">تابع حالة الطلب</div>
              <div style="font-size:.72rem; color:#64748b; margin-top:3px; text-align:center !important;">اطّلع على الحالة ورد الإدارة</div>
          </div>
      </div>
      """, unsafe_allow_html=True)

    tab_c_user, tab_c_search, tab_c_management = st.tabs([
        "📝  تقديم شكوى أو مقترح",
        "🔍  الاستعلام عن تذكرة",
        "🔐  لوحة تحكم الإدارة"
    ])

    with tab_c_user:
        st.markdown("""
        <div style="background:#ffffff; border:1px solid #e2e8f0; border-right:5px solid #0080FF; border-radius:14px; padding:16px 18px; margin-bottom:16px; box-shadow:0 5px 14px rgba(15,23,42,.04);">
            <div style="font-size:1rem; font-weight:800; color:#1e3a8a;">📝 تقديم شكوى أو مقترح جديد</div>
            <div style="font-size:.78rem; color:#64748b; margin-top:5px; line-height:1.7;">يرجى إدخال البيانات بدقة، وسيتم إنشاء رقم تذكرة خاص بك فور إرسال الطلب.</div>
        </div>
        """, unsafe_allow_html=True)
        with st.form("complaint_form"):
            col_c1, col_c2 = st.columns(2, gap="medium")
            with col_c1:
                c_name = st.text_input("اسم المعلم رباعي *")
                c_edara = st.selectbox("الإدارة التعليمية *", EDARAT_LIST, key="c_edara")
                c_type = st.selectbox("نوع الطلب *", ['شكوى', 'مقترح', 'استفسار إداري'], key="c_type")
            with col_c2:
                c_phone = st.text_input("رقم الهاتف / الواتساب *", key="c_phone")
                c_school = st.text_input("المدرسة / جهة العمل *", key="c_school")
            
            c_details = st.text_area("تفاصيل الشكوى أو المقترح أو الطلب *", key="c_details")
            
            submitted_complaint = st.form_submit_button("🚀 إرسال الطلب وتوليد رقم التذكرة", use_container_width=True)
            
            if submitted_complaint:
                if not c_name.strip() or not c_phone.strip() or not c_school.strip() or not c_details.strip():
                    st.error("⚠️ عذراً، يرجى استكمال كافة الحقول الإلزامية قبل الإرسال!")
                else:
                    complaints_list = load_complaints_data()
                    ticket_id = f"GIZA-{datetime.datetime.now().strftime('%Y%m%d')}-{len(complaints_list) + 1:03d}"
                    date_str = now.strftime('%Y-%m-%d %H:%M')
                    
                    new_complaint = {
                        'ticket_id': ticket_id, 'name': c_name, 'edara': c_edara,
                        'type': c_type, 'phone': c_phone, 'school': c_school,
                        'details': c_details, 'date': date_str,
                        'status': 'قيد المراجعة', 'reply': 'لم يتم الرد بعد'
                    }
                    
                    complaints_list.append(new_complaint)
                    save_complaints_data(complaints_list)
                    
                    st.success("🎉 تم تقديم طلبك بنجاح وتوليد رقم تذكرة تعريفي خاص بك!")
                    st.markdown(f"""
                        <div style="background: #f0fdf4; border: 2px dashed #16a34a; border-radius: 12px; padding: 18px; text-align: center; margin-top: 15px; direction: rtl;">
                            <div style="font-size: 0.9rem; color: #166534; font-weight: 700; direction: rtl; text-align: right;">رقم التذكرة الخاصة بك:</div>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #15803d; margin: 6px 0; direction: ltr; text-align: center;">{ticket_id}</div>
                            <div style="font-size: 0.8rem; color: #475569; direction: rtl; text-align: center;">يرجى الاحتفاظ برقم التذكرة لمتابعة حالة الطلب في أي وقت.</div>
                        </div>
                    """, unsafe_allow_html=True)

    with tab_c_search:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#eff6ff 0%,#ffffff 100%); border:1px solid #bfdbfe; border-right:5px solid #0080FF; padding:20px; border-radius:15px; margin-bottom:18px; box-shadow:0 6px 16px rgba(0,128,255,.06);">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:42px; height:42px; border-radius:12px; background:#dbeafe; display:flex; align-items:center; justify-content:center; font-size:1.2rem;">🔍</div>
                <div>
                    <div style="font-size:1.08rem; font-weight:800; color:#1e3a8a;">الاستعلام عن حالة تذكرة</div>
                    <div style="font-size:.8rem; color:#64748b; margin-top:3px;">أدخل رقم التذكرة لمتابعة حالة الطلب والاطلاع على رد الإدارة.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        search_ticket = st.text_input("أدخل رقم التذكرة (مثال: GIZA-2026...)", placeholder="اكتب رقم التذكرة هنا...", label_visibility="collapsed")
        
        complaints_db = load_complaints_data()
        
        if search_ticket:
            found = [item for item in complaints_db if search_ticket.strip().lower() in item['ticket_id'].lower()]
            if found:
                for item in found:
                    st.markdown(f"""
                        <div style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 12px; padding: 18px; margin-top: 12px; border-right: 5px solid #0080FF; direction: rtl; text-align: right;">
                            <div style="display: flex; justify-content: space-between; font-weight: 800; color: #1e3a8a; margin-bottom: 8px; direction: rtl;">
                                <span>🎫 التذكرة: {item['ticket_id']}</span>
                                <span style="color: #d97706;">الحالة: {item['status']}</span>
                            </div>
                            <div style="font-size: 0.88rem; color: #334155; line-height: 1.6; direction: rtl; text-align: right;">
                                <b>الاسم:</b> {item['name']} | <b>الإدارة:</b> {item['edara']}<br>
                                <b>نوع الطلب:</b> {item['type']} | <b>التاريخ:</b> {item['date']}<br>
                                <b>التفاصيل:</b> {item['details']}<br>
                                <hr style="margin: 8px 0; border: 0; border-top: 1px solid #e2e8f0;">
                                <b>رد الإدارة:</b> <span style="color: #16a34a;">{item['reply']}</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ عذراً، لم يتم العثور على تذكرة بهذا الرقم.")

    with tab_c_management:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); color:#ffffff; padding:20px; border-radius:15px; margin:4px 0 18px 0; box-shadow:0 9px 22px rgba(15,23,42,.18); border:1px solid #334155;">
            <div style="display:flex; align-items:center; gap:11px;">
                <div style="width:44px; height:44px; border-radius:12px; background:rgba(56,189,248,.12); border:1px solid rgba(56,189,248,.25); display:flex; align-items:center; justify-content:center; font-size:1.25rem;">🔐</div>
                <div>
                    <div style="font-size:1.08rem; font-weight:800; color:#7dd3fc;">لوحة تحكم الإدارة</div>
                    <div style="font-size:.79rem; color:#cbd5e1; margin-top:4px;">دخول مخصص للمسؤولين لمتابعة الطلبات والرد عليها وتحديث حالتها وتصدير التقارير.</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state['auth_states'].get('complaints_admin', False):
            st.success("✅ تم تسجيل دخول الإدارة بنجاح!")
            if complaints_db:
                st.markdown(f"<b>إجمالي الطلبات الواردة:</b> {len(complaints_db)} طلب", unsafe_allow_html=True)
                for idx, item in enumerate(complaints_db):
                    with st.expander(f"تذكرة ({item['ticket_id']}) - {item['name']} ({item['type']})"):
                        st.write(f"**الإدارة:** {item['edara']} | **المدرسة:** {item['school']}")
                        st.write(f"**رقم الهاتف:** {item['phone']} | **التاريخ:** {item['date']}")
                        st.write(f"**تفاصيل الطلب:** {item['details']}")
                        
                        with st.form(key=f"reply_form_{idx}"):
                            new_status = st.selectbox("تحديث الحالة", ['قيد المراجعة', 'قيد التنفيذ', 'تم الحل وإغلاق التذكرة'], index=(0 if item['status']=='قيد المراجعة' else (1 if item['status']=='قيد التنفيذ' else 2)))
                            new_reply = st.text_area("رد الإدارة / الإجراء المتبع", value=item['reply'])
                            if st.form_submit_button("💾 حفظ الرد وتحديث الحالة"):
                                complaints_db[idx]['status'] = new_status
                                complaints_db[idx]['reply'] = new_reply
                                save_complaints_data(complaints_db)
                                st.success("✅ تم تحديث بيانات التذكرة بنجاح!")
                                st.rerun()
                        
                        pdf_html = f"""
                        <html dir="rtl" lang="ar">
                        <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ font-family: 'Alexandria', Arial, sans-serif; padding: 30px; color: #0f172a; direction: rtl; text-align: right; }}
                            .header {{ text-align: center; border-bottom: 2px solid #1e3a8a; padding-bottom: 15px; margin-bottom: 20px; }}
                            .title {{ font-size: 18px; font-weight: bold; color: #1e3a8a; }}
                            .box {{ border: 1px solid #cbd5e1; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #f8fafc; }}
                            .label {{ font-weight: bold; color: #0080FF; }}
                        </style>
                        </head>
                        <body>
                            <div class="header">
                                <div class="title">الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
                                <div>سجل الوارد والرد على الشكاوى والطلبات</div>
                            </div>
                            <div class="box">
                                <p><span class="label">رقم التذكرة:</span> {item['ticket_id']}</p>
                                <p><span class="label">تاريخ التقديم:</span> {item['date']}</p>
                                <p><span class="label">اسم المعلم:</span> {item['name']}</p>
                                <p><span class="label">الإدارة التعليمية:</span> {item['edara']} | <span class="label">المدرسة:</span> {item['school']}</p>
                                <p><span class="label">نوع الطلب:</span> {item['type']} | <span class="label">الحالة:</span> {item['status']}</p>
                                <p><span class="label">التفاصيل:</span> {item['details']}</p>
                                <hr>
                                <p><span class="label">رد الإدارة:</span> {item['reply']}</p>
                            </div>
                        </body>
                        </html>
                        """
                        
                        try:
                            from weasyprint import HTML
                            pdf_bytes = HTML(string=pdf_html).write_pdf()
                            st.download_button(
                                label="📥 تحميل التذكرة ورد الإدارة (PDF)",
                                data=pdf_bytes,
                                file_name=f"Ticket_{item['ticket_id']}.pdf",
                                mime="application/pdf",
                                key=f"pdf_dl_{idx}"
                            )
                        except Exception:
                            st.download_button(
                                label="📥 تحميل التذكرة ورد الإدارة (ملف للطباعة PDF)",
                                data=pdf_html,
                                file_name=f"Ticket_{item['ticket_id']}.html",
                                mime="text/html",
                                key=f"html_dl_{idx}"
                            )
            else:
                st.info("ℹ️ لا توجد شكاوى أو مقترحات مسجلة حتى الآن.")
        else:
            with st.form("admin_login_form_comp"):
                admin_pwd_input = st.text_input("كلمة مرور لوحة الإدارة للشكاوى", type="password", key="admin_complaints_pwd", placeholder="أدخل كلمة المرور...")
                if st.form_submit_button("🔓 دخول لوحة الإدارة", use_container_width=True):
                    if admin_pwd_input == ADMIN_PASSWORD:
                        st.session_state['auth_states']['complaints_admin'] = True
                        st.rerun()
                    else:
                        st.error("❌ كلمة المرور غير صحيحة!")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""<div class="footer-section">
<div class="footer-grid">
<div class="footer-col">
<div class="footer-title">الأكاديمية المهنية للمعلمين - فرع الجيزة</div>
<p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.85; margin-bottom: 0; text-align: center;">
📍 إمبابة - شارع المحطة - خلف قسم شرطة إمبابة بجوار مدرسة باحثة البادية التجارية بنات<br>
☎️ تليفون - فاكس : 0237107294<br>
✉️ البريد الإلكتروني: giza@moe.edu.eg
</p>
</div>

<div class="footer-col-center">
<div class="footer-title-center">موقع الفرع على الخريطة</div>
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3453.694695027589!2d31.21875!3d30.076194!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sMzDCsDA0JzM0LjMiTiAzMcKwMTMnMDcuNSJF!5e0!3m2!1sar!2seg!4v1650000000000!5m2!1sar!2seg" class="footer-map-embed" allowfullscreen="" loading="lazy"></iframe>
<div class="map-location-btn-wrapper">
    <a href="{BRANCH_MAP_URL}" target="_blank" class="map-location-btn">
        <span>عرض الموقع على خرائط جوجل</span>
        <span style="font-size: 0.88rem;">📍</span>
    </a>
</div>
</div>

<div class="footer-col-left">
<div class="footer-title-left">تواصل معنا عبر الواتس آب</div>
<div class="footer-wa-list">
<a href="https://wa.me/201069996245" target="_blank" class="footer-wa-item"><span>01069996245</span> <span>💬</span></a>
<a href="https://wa.me/201120807631" target="_blank" class="footer-wa-item"><span>01120807631</span> <span>💬</span></a>
<a href="https://wa.me/201201109892" target="_blank" class="footer-wa-item"><span>01201109892</span> <span>💬</span></a>
</div>
</div>
</div>

<div class="footer-copyright">
جميع الحقوق محفوظة © 2026 - الأكاديمية المهنية للمعلمين - فرع الجيزة | تصميم وتنفيذ: أحمد الجنزوري
</div>
</div>""", unsafe_allow_html=True)
