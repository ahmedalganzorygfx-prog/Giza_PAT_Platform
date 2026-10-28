import base64
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / 'logo.png'
if not LOGO.exists():
    LOGO = ROOT / 'assets' / 'images' / 'logo.png'

def _logo_data():
    try:
        return 'data:image/png;base64,' + base64.b64encode(LOGO.read_bytes()).decode()
    except Exception:
        return ''

def apply_theme(title, subtitle, icon='◈', tone='blue'):
    logo = _logo_data()
    st.markdown(f'''<style>
:root {{ --pat-navy:#10233f; --pat-blue:#1769aa; --pat-sky:#2d9cdb; --pat-gold:#c9a227; --pat-bg:#f4f7fb; --pat-text:#172033; --pat-muted:#64748b; }}
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{ direction:rtl; text-align:right; }}
.stApp {{ background:linear-gradient(180deg,#f8fbff 0%,#f3f6fa 100%) !important; }}
[data-testid="stHeader"] {{ background:transparent !important; }}
.block-container {{ max-width:1380px !important; padding-top:1.1rem !important; padding-bottom:3rem !important; }}
.pat-shell {{ background:linear-gradient(135deg,#10233f 0%,#173f69 58%,#1769aa 100%); border-radius:24px; padding:18px 24px; margin:0 0 24px; color:#fff; box-shadow:0 14px 35px rgba(16,35,63,.16); border:1px solid rgba(255,255,255,.12); position:relative; overflow:hidden; }}
.pat-shell:after {{ content:""; position:absolute; width:260px; height:260px; border-radius:50%; border:1px solid rgba(255,255,255,.09); left:-90px; top:-140px; }}
.pat-head {{ display:flex; align-items:center; gap:16px; position:relative; z-index:1; }}
.pat-logo {{ width:72px; height:72px; object-fit:contain; background:#fff; border-radius:18px; padding:7px; box-shadow:0 7px 18px rgba(0,0,0,.18); }}
.pat-icon {{ width:54px; height:54px; display:flex; align-items:center; justify-content:center; border-radius:16px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18); font-size:28px; }}
.pat-kicker {{ margin:0 0 3px; color:#d9e8f8; font-size:13px; font-weight:700; }}
.pat-title {{ margin:0; color:#fff; font-size:29px; line-height:1.3; font-weight:900; }}
.pat-sub {{ margin:6px 0 0; color:#e6eef7; font-size:14px; font-weight:500; }}
.pat-badge {{ margin-right:auto; background:rgba(255,255,255,.11); border:1px solid rgba(255,255,255,.18); padding:8px 13px; border-radius:999px; font-size:12px; font-weight:800; }}
.pat-section {{ margin:24px 0 12px; padding:12px 16px; background:#fff; border-right:5px solid #c9a227; border-radius:14px; box-shadow:0 5px 16px rgba(15,23,42,.05); color:#10233f; font-size:19px; font-weight:900; }}
[data-testid="stSidebar"] {{ background:#10233f !important; border-left:1px solid rgba(255,255,255,.08); }}
[data-testid="stSidebar"] * {{ color:#fff !important; }}
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {{ border-radius:12px !important; min-height:44px !important; font-weight:800 !important; border:1px solid #d8e1ec !important; transition:.2s ease !important; }}
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover {{ transform:translateY(-2px); box-shadow:0 8px 18px rgba(16,35,63,.12) !important; }}
input, textarea {{ border-radius:11px !important; }}
[data-testid="stDataFrame"] {{ border-radius:14px; overflow:hidden; box-shadow:0 5px 18px rgba(15,23,42,.06); }}
[data-testid="stMetric"] {{ background:#fff; border:1px solid #e4eaf2; border-radius:16px; padding:14px; box-shadow:0 5px 16px rgba(15,23,42,.05); }}
.pat-footer {{ margin-top:36px; padding:18px; text-align:center; color:#64748b; font-size:12px; border-top:1px solid #dfe6ef; }}
@media (max-width:700px) {{ .block-container{{padding: .65rem .65rem 2rem !important;}} .pat-shell{{padding:14px; border-radius:18px;}} .pat-head{{gap:10px;}} .pat-logo{{width:56px;height:56px;border-radius:14px;}} .pat-icon{{width:44px;height:44px;font-size:22px;}} .pat-title{{font-size:21px;}} .pat-sub{{font-size:12px;}} .pat-badge{{display:none;}} }}
</style>
<div class="pat-shell"><div class="pat-head">{('<img class="pat-logo" src="'+logo+'">') if logo else ''}<div class="pat-icon">{icon}</div><div><p class="pat-kicker">الأكاديمية المهنية للمعلمين • فرع الجيزة</p><h1 class="pat-title">{title}</h1><p class="pat-sub">{subtitle}</p></div><div class="pat-badge">منظومة رقمية موحدة</div></div></div>''', unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="pat-section">{title}</div>', unsafe_allow_html=True)

def footer(name):
    st.markdown(f'<div class="pat-footer">{name} • فرع الأكاديمية المهنية للمعلمين بالجيزة<br>✦ تصميم وتنفيذ أحمد الجنزوري ✦</div>', unsafe_allow_html=True)
