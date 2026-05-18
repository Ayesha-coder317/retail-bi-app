import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_from_csv, load_from_excel, load_from_api, get_data

# ── HERO — pure Streamlit only ────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(160deg,#EEF2FF,#F5F0FF,#FFF5F0);
            border-radius:16px;padding:48px;margin-bottom:28px;
            text-align:center;">
    <div style="font-size:11px;font-weight:700;color:#4B7BF5;
                letter-spacing:4px;text-transform:uppercase;
                margin-bottom:16px;">
        COM6001 Final Year Project · BNU 2025-26
    </div>
    <div style="font-size:52px;font-weight:900;color:#1A1A6E;
                line-height:1.1;margin-bottom:16px;">LUMIQ</div>
    <div style="font-size:18px;color:#555;margin-bottom:16px;">
        Retail Business Intelligence Platform
    </div>
    <div style="font-size:15px;color:#666;max-width:520px;
                margin:0 auto 28px auto;line-height:1.8;">
        Transform raw transactional data into strategic intelligence.
        Role-based dashboards powered by RFM segmentation
        and real-time data upload.
    </div>
    <div style="display:flex;justify-content:center;
                gap:10px;flex-wrap:wrap;margin-bottom:28px;">
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;">
            CSV / Excel Upload
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;">
            REST API
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;">
            RFM Segmentation
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;">
            AI Insights
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;">
            6 Role Views
        </span>
    </div>
    <div style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap;">
        <div style="background:white;border-radius:30px;padding:8px 20px;
                    font-size:13px;font-weight:600;color:#1A1A6E;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
            Ayesha Jahangir
        </div>
        <div style="background:white;border-radius:30px;padding:8px 20px;
                    font-size:13px;font-weight:600;color:#1A1A6E;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
            ID: 22504895
        </div>
        <div style="background:white;border-radius:30px;padding:8px 20px;
                    font-size:13px;font-weight:600;color:#1A1A6E;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);">
            Supervisor: Syeda Faiza Nasim
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Role Views",   "6")
c2.metric("KPIs Tracked", "10+")
c3.metric("RFM Segments", "5")
c4.metric("Test Cases",   "44")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="background:white;border-radius:12px;padding:20px 24px;
            border:1px solid #EBEBEB;margin-bottom:16px;">
    <div style="font-size:13px;font-weight:700;color:#1A1A2E;
                margin-bottom:4px;">Connect Your Data</div>
    <div style="font-size:11px;color:#AAAAAA;margin-bottom:16px;">
        Upload a file or connect a live API.
        Lumiq auto-detects your columns.
    </div>
""", unsafe_allow_html=True)

source = st.radio(
    "",
    ["Use Sample Data", "Upload CSV / Excel", "Connect via API URL"],
    horizontal=True,
    label_visibility="collapsed"
)

if source == "Upload CSV / Excel":
    uploaded = st.file_uploader("Drop file here",
                                type=["csv", "xlsx", "xls"])
    if uploaded:
        with st.spinner("Processing..."):
            if uploaded.name.endswith('.csv'):
                df, err = load_from_csv(uploaded)
            else:
                df, err = load_from_excel(uploaded)
        if err:
            st.error(f"Error: {err}")
        else:
            st.session_state.uploaded_df = df
            st.session_state.data_label  = uploaded.name[:20]
            st.success(f"{len(df):,} clean records loaded")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Records",   f"{len(df):,}")
            c2.metric("Date Range",
                      f"{df['InvoiceDate'].min().strftime('%b %Y')}"
                      f" - "
                      f"{df['InvoiceDate'].max().strftime('%b %Y')}")
            c3.metric("Countries", f"{df['Country'].nunique():,}")
            c4.metric("Products",  f"{df['StockCode'].nunique():,}")
            with st.expander("Preview data"):
                st.dataframe(df.head(5), use_container_width=True)

elif source == "Connect via API URL":
    api_url = st.text_input("API endpoint URL",
                            placeholder="https://your-api.com/data")
    if st.button("Connect", key="fetch_api"):
        if not api_url:
            st.warning("Enter a URL.")
        else:
            with st.spinner("Connecting..."):
                df, err = load_from_api(api_url)
            if err:
                st.error(f"Failed: {err}")
            else:
                st.session_state.uploaded_df = df
                st.session_state.data_label  = "API"
                st.success(f"Connected — {len(df):,} records")
else:
    if 'uploaded_df' in st.session_state:
        del st.session_state['uploaded_df']
    st.session_state.data_label = "Sample Data"
    st.info("UCI Online Retail Dataset — 541,909 transactions, Dec 2010 to Dec 2011")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

df    = get_data()
label = st.session_state.get('data_label', 'Sample Data')

st.markdown(f"""
<div style="background:white;border-radius:12px;padding:20px 24px;
            border:1px solid #EBEBEB;margin-bottom:16px;">
    <div style="font-size:13px;font-weight:700;color:#1A1A2E;
                margin-bottom:4px;">Active Dataset — {label}</div>
    <div style="font-size:11px;color:#AAAAAA;margin-bottom:16px;">
        Currently loaded
    </div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records",   f"{len(df):,}")
c2.metric("Customers", f"{df['CustomerID'].nunique():,}")
c3.metric("Countries", f"{df['Country'].nunique():,}")
c4.metric("Products",  f"{df['StockCode'].nunique():,}")

st.markdown("</div>", unsafe_allow_html=True)