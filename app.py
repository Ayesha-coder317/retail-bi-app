import streamlit as st

st.set_page_config(
    page_title="Retail BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1B3A5C; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebarNav"] { display: none; }

    .section-title {
        font-size: 22px; font-weight: 700;
        color: #1B3A5C; margin-bottom: 16px;
        border-bottom: 2px solid #4A90D9;
        padding-bottom: 8px;
    }
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-left: 4px solid #4A90D9;
    }
    .sidebar-section {
        font-size: 10px; font-weight: 700;
        color: rgba(255,255,255,0.5);
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 16px 0 8px 0;
    }
    .info-row {
        font-size: 12px;
        color: rgba(255,255,255,0.85);
        padding: 3px 0;
    }
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.15);
        margin: 14px 0;
    }

    /* Force ALL sidebar buttons dark */
    section[data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.07) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 8px !important;
        width: 100% !important;
        text-align: left !important;
        padding: 10px 14px !important;
        font-size: 12px !important;
        box-shadow: none !important;
        margin-bottom: 6px !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: rgba(255,255,255,0.35) !important;
    }
    section[data-testid="stSidebar"] button p {
        color: white !important;
    }

    /* Radio buttons hidden — used only for state */
    div[data-testid="stSidebar"] div[data-testid="stRadio"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

roles = {
    "Executive": {
        "color":   "#4A90D9",
        "label":   "Viewing as: Executive",
        "desc":    "C-Suite high-level overview",
        "file":    "pages/executive.py",
    },
    "Sales Manager": {
        "color":   "#2ecc71",
        "label":   "Viewing as: Sales Manager",
        "desc":    "Revenue and sales performance",
        "file":    "pages/kpi.py",
    },
    "Customer Analyst": {
        "color":   "#e67e22",
        "label":   "Viewing as: Customer Analyst",
        "desc":    "RFM segmentation and behaviour",
        "file":    "pages/customers.py",
    },
    "Product Manager": {
        "color":   "#9b59b6",
        "label":   "Viewing as: Product Manager",
        "desc":    "Products and geographic analysis",
        "file":    "pages/products.py",
    },
}

if "selected_role" not in st.session_state:
    st.session_state.selected_role = "Executive"
if "show_home" not in st.session_state:
    st.session_state.show_home = False

with st.sidebar:

    # Logo as home button
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #4A90D9, #152744);
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 6px;
        cursor: default;
    ">
        <div style="font-size:26px; font-weight:900;
                    color:white; letter-spacing:3px;">BI</div>
        <div style="font-size:9px; color:rgba(255,255,255,0.6);
                    letter-spacing:3px; text-transform:uppercase;
                    margin-top:2px;">RETAIL</div>
        <div style="font-size:13px; font-weight:700;
                    color:white; margin-top:8px;">Retail BI App</div>
        <div style="font-size:10px; color:rgba(255,255,255,0.5);
                    margin-top:2px;">Sales Performance Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Home", key="home_btn"):
        st.session_state.show_home = True
        st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Select Your Role</div>',
                unsafe_allow_html=True)

    for role_name, role_data in roles.items():
        is_active = st.session_state.selected_role == role_name
        color     = role_data["color"]
        desc      = role_data["desc"]

        if is_active:
            st.markdown(f"""
            <div style="
                background: {color};
                border-radius: 8px;
                padding: 10px 14px;
                margin-bottom: 6px;">
                <div style="font-size:13px; font-weight:700;
                            color:white;">{role_name}</div>
                <div style="font-size:10px;
                            color:rgba(255,255,255,0.8);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            col = st.columns(1)[0]
            with col:
                clicked = st.button(
                    f"{role_name}\n{desc}",
                    key=f"role_{role_name}"
                )
                if clicked:
                    st.session_state.selected_role = role_name
                    st.session_state.show_home     = False
                    st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    selected_role = st.session_state.selected_role
    active_color  = roles[selected_role]["color"]
    st.markdown(f"""
    <div style="
        background: {active_color};
        border-radius: 20px;
        padding: 5px 14px;
        text-align: center;
        font-size: 12px;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;">
        {roles[selected_role]["label"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Project Info</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">Ayesha Jahangir</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">ID: 22504895</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">BNU - COM6001</div>',
                unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Dataset</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">UCI Online Retail</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">541,909 transactions</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">Dec 2010 - Dec 2011</div>',
                unsafe_allow_html=True)

# Load correct page
if st.session_state.show_home:
    exec(open("pages/home.py", encoding='utf-8').read())
else:
    page_file = roles[st.session_state.selected_role]["file"]
    exec(open(page_file, encoding='utf-8').read())