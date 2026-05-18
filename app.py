import streamlit as st

st.set_page_config(
    page_title="Lumiq",
    page_icon="L",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: #0D1B2A;
        min-width: 200px !important;
        max-width: 200px !important;
    }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebarNav"] { display: none !important; }
    .stApp { background: #F5F6FA; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header[data-testid="stHeader"] { display: none !important; }
    footer { display: none !important; }

    div[data-testid="metric-container"] {
        background: white; border-radius: 12px;
        padding: 18px 20px; border: 1px solid #EBEBEB;
        box-shadow: none;
    }
    div[data-testid="metric-container"] label {
        font-size: 11px !important; font-weight: 600 !important;
        color: #999 !important; text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 24px !important; font-weight: 700 !important;
        color: #1A1A2E !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 12px !important; font-weight: 600 !important;
    }
    .chart-card {
        background: white; border-radius: 12px;
        padding: 20px 24px; border: 1px solid #EBEBEB;
        margin-bottom: 16px;
    }
    .chart-title { font-size:13px; font-weight:700; color:#1A1A2E; margin-bottom:2px; }
    .chart-sub   { font-size:11px; color:#AAAAAA; margin-bottom:12px; }
    .insight-card {
        background: #F0F4FF; border-radius: 12px;
        padding: 14px 18px; border-left: 4px solid #4B7BF5;
        margin-bottom: 10px;
    }
    .insight-text { font-size:13px; color:#1A1A2E; font-weight:500; line-height:1.5; }
    .insight-label { font-size:10px; font-weight:700; color:#4B7BF5;
                     text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px; }

    section[data-testid="stSidebar"] button {
        background: transparent !important;
        border: none !important; border-radius: 8px !important;
        width: 100% !important; height: 40px !important;
        padding: 0 12px !important; margin: 1px 0 !important;
        display: flex !important; align-items: center !important;
        font-size: 13px !important; font-weight: 500 !important;
        box-shadow: none !important;
        color: rgba(255,255,255,0.5) !important;
        transition: all 0.15s !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] button p {
        font-size: 13px !important; color: inherit !important;
        margin: 0 !important; text-align: left !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stRadio"] {
        display: none !important;
    }

    div[data-testid="stRadio"] > div {
        display: flex !important; flex-direction: row !important;
        gap: 0 !important; background: transparent !important;
        padding: 0 !important; border-radius: 0 !important;
    }
    div[data-testid="stRadio"] label {
        padding: 0 16px !important; border-radius: 0 !important;
        font-size: 13px !important; font-weight: 500 !important;
        color: #AAAAAA !important; cursor: pointer !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        white-space: nowrap !important;
        background: transparent !important; margin: 0 !important;
        height: 56px !important; display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] label:has(input:checked) {
        color: #1A1A2E !important; font-weight: 700 !important;
        border-bottom: 2px solid #1A1A2E !important;
    }
    div[data-testid="stRadio"] input { display: none !important; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0; background: transparent;
        border-bottom: 1px solid #EBEBEB;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px; font-size: 13px;
        font-weight: 500; color: #AAAAAA;
        border: none; background: transparent;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        color: #1A1A2E !important; font-weight: 700 !important;
        border-bottom: 2px solid #1A1A2E !important;
        background: transparent !important;
    }

    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #F5F6FA; }
    ::-webkit-scrollbar-thumb { background: #DDD; border-radius: 4px; }

    [data-testid="stDataFrame"] thead th {
        background: #F5F6FA !important; font-size: 11px !important;
        font-weight: 600 !important; color: #999 !important;
        text-transform: uppercase !important; letter-spacing: 0.5px !important;
    }
    [data-testid="stDataFrame"] tbody td {
        font-size: 13px !important; color: #1A1A2E !important;
    }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"

pages = {
    "home":     {"label": "Home",             "icon": "🏠", "desc": "Overview & Data Upload"},
    "exec":     {"label": "Executive",        "icon": "📊", "desc": "C-Suite Revenue Overview"},
    "sales":    {"label": "Sales Manager",    "icon": "📈", "desc": "Sales KPIs & Performance"},
    "trends":   {"label": "Sales Trends",     "icon": "📉", "desc": "Monthly Trends & Growth"},
    "customer": {"label": "Customer Analyst", "icon": "👥", "desc": "RFM & Customer Behaviour"},
    "product":  {"label": "Product Manager",  "icon": "📦", "desc": "Product & Country Analysis"},
}

page_files = {
    "home":     "pages/home.py",
    "exec":     "pages/executive.py",
    "sales":    "pages/kpi.py",
    "trends":   "pages/sales.py",
    "customer": "pages/customers.py",
    "product":  "pages/products.py",
}

current  = st.session_state.page
data_lbl = st.session_state.get('data_label', 'Sample Data')

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown("""
    <div style="padding:20px 16px 12px 16px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <svg viewBox="0 0 36 36" fill="none"
                 xmlns="http://www.w3.org/2000/svg"
                 style="width:30px;height:30px;flex-shrink:0;">
                <rect width="36" height="36" rx="9" fill="#4B7BF5"/>
                <polygon points="18,9 27,25 9,25" fill="none"
                         stroke="white" stroke-width="2.2"
                         stroke-linejoin="round"/>
                <circle cx="18" cy="25" r="2.5"
                        fill="white" fill-opacity="0.65"/>
            </svg>
            <div>
                <div style="font-size:14px;font-weight:900;
                            color:white;letter-spacing:2px;">LUMIQ</div>
                <div style="font-size:8px;color:rgba(255,255,255,0.35);
                            letter-spacing:1px;text-transform:uppercase;">
                    Retail Intelligence
                </div>
            </div>
        </div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.08);
                margin:0 16px 16px 16px;"></div>
    """, unsafe_allow_html=True)

    # Navigation label
    st.markdown("""
    <div style="font-size:9px;font-weight:700;
                color:rgba(255,255,255,0.3);
                text-transform:uppercase;letter-spacing:1.5px;
                padding:0 16px;margin-bottom:6px;">Navigation</div>
    """, unsafe_allow_html=True)

    # Nav buttons
    for key, p in pages.items():
        is_active = current == key
        if is_active:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:10px;
                        background:rgba(75,123,245,0.18);
                        border-left:3px solid #4B7BF5;
                        border-radius:8px;
                        padding:10px 12px;margin:1px 8px;
                        cursor:pointer;">
                <span style="font-size:16px;">{p['icon']}</span>
                <div>
                    <div style="font-size:13px;font-weight:700;
                                color:white;">{p['label']}</div>
                    <div style="font-size:10px;
                                color:rgba(255,255,255,0.4);
                                margin-top:1px;">{p['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"{p['icon']}  {p['label']}",
                         key=f"nav_{key}",
                         help=p['desc'],
                         use_container_width=True):
                st.session_state.page = key
                st.rerun()

    # Divider
    st.markdown("""
    <div style="height:1px;background:rgba(255,255,255,0.08);
                margin:16px 16px 16px 16px;"></div>
    """, unsafe_allow_html=True)

    # Dataset status
    st.markdown(f"""
    <div style="padding:0 16px;margin-bottom:16px;">
        <div style="font-size:9px;font-weight:700;
                    color:rgba(255,255,255,0.3);
                    text-transform:uppercase;letter-spacing:1.5px;
                    margin-bottom:8px;">Active Dataset</div>
        <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:6px;height:6px;background:#2ECC71;
                        border-radius:50%;flex-shrink:0;"></div>
            <div style="font-size:12px;color:rgba(255,255,255,0.6);
                        word-break:break-all;">{data_lbl[:22]}</div>
        </div>
    </div>
    <div style="height:1px;background:rgba(255,255,255,0.08);
                margin:0 16px 16px 16px;"></div>
    """, unsafe_allow_html=True)

    # Project info
    st.markdown("""
    <div style="padding:0 16px;">
        <div style="font-size:9px;font-weight:700;
                    color:rgba(255,255,255,0.3);
                    text-transform:uppercase;letter-spacing:1.5px;
                    margin-bottom:10px;">Project Info</div>

        <div style="margin-bottom:8px;">
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-bottom:2px;">Student</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);
                        font-weight:600;">Ayesha Jahangir</div>
        </div>

        <div style="margin-bottom:8px;">
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-bottom:2px;">Student ID</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);
                        font-weight:600;">22504895</div>
        </div>

        <div style="margin-bottom:8px;">
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-bottom:2px;">Supervisor</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);
                        font-weight:600;">Syeda Faiza Nasim</div>
        </div>

        <div style="margin-bottom:8px;">
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-bottom:2px;">Module</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);
                        font-weight:600;">COM6001 FYP</div>
        </div>

        <div style="margin-bottom:8px;">
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-bottom:2px;">University</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);
                        font-weight:600;">BNU 2025–26</div>
        </div>

        <div style="margin-bottom:0;">
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-bottom:2px;">Dataset</div>
            <div style="font-size:12px;color:rgba(255,255,255,0.75);
                        font-weight:600;">UCI Online Retail</div>
            <div style="font-size:10px;color:rgba(255,255,255,0.3);
                        margin-top:1px;">541,909 transactions</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── TOP BAR ───────────────────────────────────────────────────────
t1, t2, t3 = st.columns([2, 4, 2])

with t1:
    st.markdown("""
    <div style="background:white;border-bottom:1px solid #EBEBEB;
                height:56px;padding:0 20px;display:flex;
                align-items:center;">
        <div style="font-size:14px;font-weight:900;color:#1A1A2E;
                    letter-spacing:2px;">LUMIQ</div>
    </div>
    """, unsafe_allow_html=True)

with t2:
    st.markdown("""
    <div style="background:white;border-bottom:1px solid #EBEBEB;
                height:56px;display:flex;align-items:center;">
    </div>
    """, unsafe_allow_html=True)

    nav_labels = [p["label"] for p in pages.values()]
    nav_keys   = list(pages.keys())
    curr_idx   = nav_keys.index(current) if current in nav_keys else 0

    selected = st.radio(
        "", nav_labels, index=curr_idx,
        horizontal=True,
        label_visibility="collapsed"
    )
    new_key = nav_keys[nav_labels.index(selected)]
    if new_key != st.session_state.page:
        st.session_state.page = new_key
        st.rerun()

with t3:
    st.markdown(f"""
    <div style="background:white;border-bottom:1px solid #EBEBEB;
                height:56px;padding:0 20px;display:flex;
                align-items:center;justify-content:flex-end;gap:10px;">
        <div style="width:8px;height:8px;background:#2ECC71;
                    border-radius:50%;"></div>
        <div style="font-size:11px;color:#AAAAAA;
                    white-space:nowrap;">{data_lbl[:16]}</div>
        <div style="width:1px;height:16px;background:#EBEBEB;"></div>
        <div style="width:30px;height:30px;
                    background:linear-gradient(135deg,#4B7BF5,#2E4BCC);
                    border-radius:50%;display:flex;align-items:center;
                    justify-content:center;font-size:11px;
                    font-weight:700;color:white;">AJ</div>
    </div>
    """, unsafe_allow_html=True)

# ── CONTENT ───────────────────────────────────────────────────────
st.markdown('<div style="padding:28px 48px 48px 48px;">',
            unsafe_allow_html=True)

exec(open(page_files[current], encoding='utf-8').read())

st.markdown('</div>', unsafe_allow_html=True)