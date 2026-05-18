import importlib
import streamlit as st
import data_loader

data_loader = importlib.reload(data_loader)

st.set_page_config(
    page_title="Lumiq",
    page_icon="L",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pages = {
    "home": {"label": "Home", "short": "Home", "desc": "Overview & Data Upload"},
    "exec": {"label": "Executive Summary", "short": "Executive", "desc": "C-Suite KPI Overview"},
    "sales": {"label": "Sales Analysis", "short": "Sales", "desc": "Sales KPIs & Performance"},
    "trends": {"label": "Forecasting / Trends", "short": "Trends", "desc": "Monthly Trends & Growth"},
    "customer": {"label": "Customer Insights", "short": "Customers", "desc": "RFM & Customer Behaviour"},
    "product": {"label": "Product Performance", "short": "Products", "desc": "Product & Country Analysis"},
}

page_files = {
    "home": "pages/home.py",
    "exec": "pages/executive.py",
    "sales": "pages/kpi.py",
    "trends": "pages/sales.py",
    "customer": "pages/customers.py",
    "product": "pages/products.py",
}

query_page = st.query_params.get("page")
if "page" not in st.session_state:
    st.session_state.page = "home"
if query_page in pages:
    st.session_state.page = query_page

current = st.session_state.page
data_lbl = st.session_state.get("data_label", "Sample Data")

st.markdown("""
<style>
    :root {
        --navy: #1F3B60;
        --ink: #172033;
        --muted: #8B96A8;
        --line: #E8EDF3;
        --panel: #FFFFFF;
        --page: #EEF3F6;
        --accent: #78C6D6;
        --rose: #C63D73;
        --green: #2ECC71;
    }

    .stApp {
        background: #CAD2DF;
    }
    .block-container {
        max-width: 1180px !important;
        padding: 14px 18px 28px 18px !important;
    }
    header[data-testid="stHeader"],
    footer,
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }

    .dashboard-shell {
        background: var(--page);
        border-radius: 26px;
        overflow: hidden;
        box-shadow: 0 24px 60px rgba(31,59,96,0.18);
        border: 1px solid rgba(255,255,255,0.65);
    }
    .top-nav {
        height: 76px;
        background: var(--navy);
        color: white;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
    }
    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 180px;
    }
    .brand-mark {
        width: 34px;
        height: 34px;
        border-radius: 10px;
        background: rgba(120,198,214,0.14);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .brand-name {
        font-size: 15px;
        font-weight: 900;
        letter-spacing: 4px;
    }
    .nav-links {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        flex: 1;
    }
    .nav-links a {
        color: rgba(255,255,255,0.78);
        text-decoration: none;
        font-size: 13px;
        font-weight: 600;
        padding: 27px 12px 24px 12px;
        position: relative;
    }
    .nav-links a.active {
        color: white;
    }
    .nav-links a.active:after {
        content: "";
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #E6E95E;
        position: absolute;
        left: 50%;
        bottom: 18px;
        transform: translateX(-50%);
    }
    .nav-actions {
        min-width: 180px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 10px;
        color: rgba(255,255,255,0.72);
        font-size: 16px;
    }
    .nav-actions a {
        width: 30px;
        height: 30px;
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255,255,255,0.76);
        text-decoration: none;
        font-size: 15px;
        font-weight: 800;
        border: 1px solid transparent;
    }
    .nav-actions a:hover {
        color: white;
        background: rgba(255,255,255,0.10);
        border-color: rgba(255,255,255,0.14);
    }
    .avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: white;
        color: var(--navy);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: 900;
    }
    .content-surface {
        padding: 26px 34px 36px 34px;
    }
    .page-titlebar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
        color: var(--ink);
        background: transparent;
    }
    .page-title {
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 1.4px;
        text-transform: uppercase;
    }
    .dataset-pill {
        display: flex;
        align-items: center;
        gap: 9px;
        background: white;
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 8px 14px;
        color: var(--muted);
        font-size: 12px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--green);
    }

    div[data-testid="metric-container"] {
        background: white;
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid var(--line);
        box-shadow: 0 10px 30px rgba(31,59,96,0.06);
    }
    div[data-testid="metric-container"] label {
        color: #6F7A8D !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        color: #283147 !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 12px !important;
        font-weight: 700 !important;
    }

    .chart-card {
        background: white;
        border-radius: 16px;
        padding: 22px 24px;
        border: 1px solid var(--line);
        box-shadow: 0 10px 30px rgba(31,59,96,0.06);
        margin-bottom: 18px;
    }
    .chart-title {
        font-size: 15px;
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 5px;
    }
    .chart-sub {
        font-size: 12px;
        color: var(--muted);
        margin-bottom: 14px;
    }
    .insight-card {
        background: #F6FAFE;
        border-radius: 16px;
        padding: 18px 20px;
        border-left: 4px solid var(--accent);
        border-top: 1px solid var(--line);
        border-right: 1px solid var(--line);
        border-bottom: 1px solid var(--line);
        box-shadow: 0 10px 30px rgba(31,59,96,0.05);
        margin-bottom: 12px;
    }
    .insight-label {
        color: var(--accent);
        font-size: 10px;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin-bottom: 8px;
    }
    .insight-text {
        color: var(--ink);
        font-size: 13px;
        line-height: 1.6;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab-list"] {
        border-bottom: 1px solid var(--line);
        gap: 18px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #9AA4B5;
        font-size: 13px;
        font-weight: 700;
        padding: 13px 0;
    }
    .stTabs [aria-selected="true"] {
        color: var(--ink) !important;
        border-bottom: 3px solid var(--rose) !important;
    }
    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }
    [data-testid="stDataFrame"] thead th {
        background: #F5F7FA !important;
        color: #7E8898 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
    }
    div[data-testid="stTextInput"] input {
        background: white !important;
        color: #172033 !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px !important;
        pointer-events: auto !important;
        user-select: text !important;
    }
    div[data-testid="stTextInput"],
    div[data-testid="stTextInput"] * {
        pointer-events: auto !important;
    }
    div[data-testid="stTextArea"] textarea {
        background: white !important;
        color: #172033 !important;
        border: 1px solid var(--line) !important;
        border-radius: 12px !important;
        pointer-events: auto !important;
        user-select: text !important;
        -webkit-user-select: text !important;
        cursor: text !important;
    }
    div[data-testid="stTextArea"],
    div[data-testid="stTextArea"] * {
        pointer-events: auto !important;
    }
    .connect-card {
        background: white;
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid var(--line);
        box-shadow: 0 10px 30px rgba(31,59,96,0.06);
        margin-bottom: 16px;
    }
    .connect-title {
        font-size: 15px;
        font-weight: 800;
        color: var(--ink);
        margin-bottom: 5px;
    }
    .connect-sub {
        font-size: 12px;
        color: var(--muted);
        margin-bottom: 16px;
    }

    @media (max-width: 900px) {
        .block-container {
            padding: 12px !important;
        }
        .dashboard-shell {
            border-radius: 18px;
        }
        .top-nav {
            height: auto;
            padding: 16px;
            flex-wrap: wrap;
            gap: 12px;
        }
        .brand, .nav-actions {
            min-width: auto;
        }
        .nav-links {
            order: 3;
            width: 100%;
            justify-content: flex-start;
            overflow-x: auto;
        }
        .content-surface {
            padding: 22px 16px 28px 16px;
        }
    }
</style>
""", unsafe_allow_html=True)

nav_links = "".join(
    f'<a class="{("active" if key == current else "")}" href="?page={key}" target="_self">{page["short"]}</a>'
    for key, page in pages.items()
)

st.markdown(f"""
<div class="dashboard-shell">
    <div class="top-nav">
        <a class="brand" href="?page=home" target="_self" style="text-decoration:none;color:white;">
            <div class="brand-mark">
                <svg viewBox="0 0 36 36" fill="none" width="24" height="24"
                     xmlns="http://www.w3.org/2000/svg">
                    <polygon points="18,5 31,29 5,29" fill="none"
                             stroke="#78C6D6" stroke-width="2.2"
                             stroke-linejoin="round"/>
                    <path d="M18 5 L13 29" stroke="#C63D73" stroke-width="1.4"/>
                    <path d="M18 5 L24 29" stroke="#E6E95E" stroke-width="1.4"/>
                </svg>
            </div>
            <div class="brand-name">LUMIQ</div>
        </a>
        <div class="nav-links">{nav_links}</div>
        <div class="nav-actions">
            <a href="?page=home" target="_self" title="Open data upload">≡</a>
            <a href="?page=exec" target="_self" title="Open executive dashboard">□</a>
            <a href="?page=trends" target="_self" title="Open forecasting view">⌁</a>
            <div class="avatar">AJ</div>
        </div>
    </div>
    <div class="content-surface">
""", unsafe_allow_html=True)

exec(open(page_files[current], encoding="utf-8").read())

st.markdown("""
    </div>
</div>
""", unsafe_allow_html=True)
