import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_from_csv, load_from_excel, load_from_api, get_data

st.markdown("""
<div style="background:#1A1A2E; border-radius:16px; padding:40px 48px;
            margin-bottom:24px;">
    <div style="font-size:11px; font-weight:600; color:rgba(255,255,255,0.4);
                letter-spacing:3px; text-transform:uppercase;
                margin-bottom:12px;">Business Intelligence Platform</div>
    <div style="font-size:48px; font-weight:800; color:white;
                letter-spacing:1px; margin-bottom:12px;">LUMIQ</div>
    <div style="font-size:15px; color:rgba(255,255,255,0.55);
                max-width:520px; line-height:1.8; margin-bottom:28px;">
        Transform raw retail transaction data into strategic intelligence.
        Upload your dataset or connect via API.
    </div>
    <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <span style="border:1px solid rgba(255,255,255,0.15);
                     border-radius:6px; padding:5px 14px;
                     font-size:12px; color:rgba(255,255,255,0.6);">
            CSV / Excel Upload
        </span>
        <span style="border:1px solid rgba(255,255,255,0.15);
                     border-radius:6px; padding:5px 14px;
                     font-size:12px; color:rgba(255,255,255,0.6);">
            REST API
        </span>
        <span style="border:1px solid rgba(255,255,255,0.15);
                     border-radius:6px; padding:5px 14px;
                     font-size:12px; color:rgba(255,255,255,0.6);">
            RFM Segmentation
        </span>
        <span style="border:1px solid rgba(255,255,255,0.15);
                     border-radius:6px; padding:5px 14px;
                     font-size:12px; color:rgba(255,255,255,0.6);">
            4 Role Views
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Role Views",   "4")
c2.metric("KPIs Tracked", "7+")
c3.metric("RFM Segments", "5")
c4.metric("Test Cases",   "44")

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

st.markdown('<div class="chart-card"><div class="chart-title">Connect Your Data</div><div class="chart-sub">Upload a file or connect a live API endpoint</div>', unsafe_allow_html=True)

source = st.radio("", ["Use Sample Data","Upload CSV / Excel",
                        "Connect via API URL"],
                  horizontal=True, label_visibility="collapsed")

if source == "Upload CSV / Excel":
    st.markdown("""
    <div style="background:#F8F9FF; border:1px solid #EBEBEB;
                border-radius:12px; padding:20px 24px;
                margin-bottom:16px;">
        <div style="font-size:13px; font-weight:600;
                    color:#1A1A2E; margin-bottom:6px;">
            Auto Column Detection
        </div>
        <div style="font-size:12px; color:#AAAAAA; line-height:1.7;">
            Lumiq automatically detects your columns.
            Your file needs at least an invoice number,
            quantity, price and date column —
            any naming format is accepted.
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Drop your file here or click to browse",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded:
        with st.spinner("Processing..."):
            if uploaded.name.endswith('.csv'):
                df, err = load_from_csv(uploaded)
            else:
                df, err = load_from_excel(uploaded)

        if err:
            st.error(f"Could not load file: {err}")
        else:
            st.session_state.uploaded_df = df
            st.session_state.data_label  = uploaded.name[:20]
            st.success(f"{len(df):,} clean records loaded from {uploaded.name}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Records",   f"{len(df):,}")
            c2.metric("Date Range",
                      f"{df['InvoiceDate'].min().strftime('%b %Y')} - "
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
    st.info("Using UCI Online Retail Dataset — 541,909 transactions, Dec 2010 to Dec 2011")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

df    = get_data()
label = st.session_state.get('data_label','Sample Data')

st.markdown(f'<div class="chart-card"><div class="chart-title">Active Dataset — {label}</div><div class="chart-sub">Currently loaded data summary</div>', unsafe_allow_html=True)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Records",   f"{len(df):,}")
c2.metric("Customers", f"{df['CustomerID'].nunique():,}")
c3.metric("Countries", f"{df['Country'].nunique():,}")
c4.metric("Products",  f"{df['StockCode'].nunique():,}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

st.markdown('<div class="chart-card"><div class="chart-title">Dashboard Views</div><div class="chart-sub">Select a view from the top navigation or click below</div>', unsafe_allow_html=True)

roles = [
    ("exec",     "Executive",         "C-Suite revenue overview and global map"),
    ("sales",    "Sales Performance",  "KPIs, country breakdown, top products"),
    ("trends",   "Sales Trends",       "Monthly trends and growth rate analysis"),
    ("customer", "Customer Insights",  "RFM segmentation and customer behaviour"),
    ("product",  "Product & Country",  "Product rankings and geographic distribution"),
]

cols = st.columns(5)
for col, (key, name, desc) in zip(cols, roles):
    with col:
        st.markdown(f"""
        <div style="border:1px solid #EBEBEB; border-radius:12px;
                    padding:18px; min-height:120px; background:#FAFAFA;">
            <div style="font-size:13px; font-weight:700;
                        color:#1A1A2E; margin-bottom:6px;">{name}</div>
            <div style="font-size:11px; color:#AAAAAA;
                        line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open", key=f"open_{key}",
                     use_container_width=True):
            st.session_state.page = key
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)