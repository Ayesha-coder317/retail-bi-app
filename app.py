import streamlit as st

st.set_page_config(
    page_title="Lumiq - Retail Intelligence",
    page_icon="L",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #0D1B2A; }
    [data-testid="stSidebar"] * { color: white !important; }
    [data-testid="stSidebarNav"] { display: none; }

    .section-title {
        font-size: 26px; font-weight: 800;
        color: #0D1B2A; margin-bottom: 16px;
        border-bottom: 3px solid #4A90D9;
        padding-bottom: 10px;
    }
    div[data-testid="metric-container"] {
        background: white;
        border-radius: 14px;
        padding: 20px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border-left: 5px solid #4A90D9;
    }
    div[data-testid="metric-container"] label {
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #666 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div[data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 28px !important;
        font-weight: 800 !important;
        color: #0D1B2A !important;
    }
    .sidebar-section {
        font-size: 10px; font-weight: 700;
        color: rgba(255,255,255,0.4);
        text-transform: uppercase; letter-spacing: 2px;
        margin: 16px 0 8px 0;
    }
    .info-row {
        font-size: 12px;
        color: rgba(255,255,255,0.8);
        padding: 3px 0;
    }
    .divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 14px 0;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"]:first-child > button {
        background: linear-gradient(135deg, #4A90D9 0%, #0D1B2A 100%) !important;
        border-radius: 14px !important;
        border: none !important;
        padding: 22px 16px !important;
        width: 100% !important;
        text-align: center !important;
        box-shadow: 0 6px 20px rgba(74,144,217,0.35) !important;
        margin-bottom: 4px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        letter-spacing: 3px !important;
        line-height: 1.5 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stButton"]:first-child > button:hover {
        box-shadow: 0 8px 28px rgba(74,144,217,0.5) !important;
    }
    section[data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.06) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        width: 100% !important;
        text-align: left !important;
        padding: 10px 14px !important;
        font-size: 12px !important;
        box-shadow: none !important;
        margin-bottom: 6px !important;
    }
    section[data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.25) !important;
    }
    section[data-testid="stSidebar"] button p {
        color: white !important;
    }
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
    st.session_state.show_home = True

with st.sidebar:

    if st.button("LUMIQ\nRetail Intelligence", key="home_btn"):
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
            <div style="background:{color}; border-radius:10px;
                        padding:10px 14px; margin-bottom:6px;">
                <div style="font-size:13px; font-weight:700;
                            color:white;">{role_name}</div>
                <div style="font-size:10px;
                            color:rgba(255,255,255,0.8);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"{role_name}  -  {desc}",
                         key=f"role_{role_name}"):
                st.session_state.selected_role = role_name
                st.session_state.show_home     = False
                st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    selected_role = st.session_state.selected_role
    active_color  = roles[selected_role]["color"]
    st.markdown(f"""
    <div style="background:{active_color}; border-radius:20px;
        padding:5px 14px; text-align:center; font-size:12px;
        font-weight:700; color:white; margin-bottom:8px;">
        {roles[selected_role]["label"]}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    data_label = st.session_state.get('data_label', 'UCI Online Retail (Sample)')
    st.markdown('<div class="sidebar-section">Active Dataset</div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="info-row">{data_label[:35]}</div>',
                unsafe_allow_html=True)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Project Info</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">Ayesha Jahangir</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">ID: 22504895</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="info-row">BNU - COM6001</div>',
                unsafe_allow_html=True)

if st.session_state.show_home:
    exec(open("pages/home.py", encoding='utf-8').read())
else:
    page_file = roles[st.session_state.selected_role]["file"]
    exec(open(page_file, encoding='utf-8').read())