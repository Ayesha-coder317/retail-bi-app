import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_from_csv, load_from_excel, load_from_api, get_data

# ── HERO ──────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(160deg,#EEF2FF 0%,#F5F0FF 50%,#FFF5F0 100%);
            border-radius:20px;padding:64px 48px 56px 48px;
            text-align:center;margin-bottom:28px;">

    <div style="display:inline-flex;align-items:center;gap:12px;
                background:white;border-radius:12px;
                padding:10px 20px;margin-bottom:36px;
                box-shadow:0 2px 16px rgba(0,0,0,0.08);">
        <div style="width:32px;height:32px;background:#1A1A6E;
                    border-radius:8px;display:flex;align-items:center;
                    justify-content:center;font-size:14px;color:white;">
            ▶
        </div>
        <div style="text-align:left;">
            <div style="font-size:12px;font-weight:700;color:#1A1A6E;">
                COM6001 Final Year Project
            </div>
            <div style="font-size:10px;color:#999;
                        text-transform:uppercase;letter-spacing:0.5px;">
                Buckinghamshire New University · 2025–26
            </div>
        </div>
    </div>

    <div style="font-size:58px;font-weight:900;color:#1A1A6E;
                line-height:1.1;margin-bottom:20px;
                letter-spacing:-1px;">
        Retail Business<br>Intelligence &<br>Analytics Platform
    </div>

    <div style="font-size:16px;color:#666;max-width:560px;
                margin:0 auto 32px auto;line-height:1.8;">
        Transform raw transactional data into strategic intelligence.
        Role-based dashboards for every level of your organisation —
        powered by RFM segmentation and real-time data upload.
    </div>

    <div style="display:flex;justify-content:center;
                gap:10px;flex-wrap:wrap;margin-bottom:36px;">
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;
                     box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            CSV / Excel Upload
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;
                     box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            REST API Integration
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;
                     box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            RFM Segmentation
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;
                     box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            AI Business Insights
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;
                     box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            Interactive Charts
        </span>
        <span style="background:white;border:1px solid #E0E0E0;
                     border-radius:20px;padding:6px 16px;
                     font-size:12px;font-weight:500;color:#555;
                     box-shadow:0 1px 4px rgba(0,0,0,0.05);">
            Multi-Role Views
        </span>
    </div>

    <div style="display:flex;justify-content:center;
                gap:12px;flex-wrap:wrap;">
        <div style="background:white;border-radius:30px;
                    padding:8px 22px;font-size:13px;
                    font-weight:600;color:#1A1A6E;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);
                    border:1px solid rgba(26,26,110,0.1);">
            Ayesha Jahangir
        </div>
        <div style="background:white;border-radius:30px;
                    padding:8px 22px;font-size:13px;
                    font-weight:600;color:#1A1A6E;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);
                    border:1px solid rgba(26,26,110,0.1);">
            ID: 22504895
        </div>
        <div style="background:white;border-radius:30px;
                    padding:8px 22px;font-size:13px;
                    font-weight:600;color:#1A1A6E;
                    box-shadow:0 2px 12px rgba(0,0,0,0.08);
                    border:1px solid rgba(26,26,110,0.1);">
            Supervisor: Syeda Faiza Nasim
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── STATS ─────────────────────────────────────────────────────────
c1,c2,c3,c4 = st.columns(4)
c1.metric("Role Views",   "6")
c2.metric("KPIs Tracked", "10+")
c3.metric("RFM Segments", "5")
c4.metric("Test Cases",   "44")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── DATA CONNECT ──────────────────────────────────────────────────
st.markdown("""
<div style="background:white;border-radius:12px;
            padding:20px 24px;border:1px solid #EBEBEB;
            margin-bottom:16px;">
    <div style="font-size:13px;font-weight:700;color:#1A1A2E;
                margin-bottom:2px;">Connect Your Data</div>
    <div style="font-size:11px;color:#AAAAAA;margin-bottom:16px;">
        Upload a file or connect a live API.
        Lumiq auto-detects your columns automatically.
    </div>
""", unsafe_allow_html=True)

source = st.radio(
    "",
    ["Use Sample Data","Upload CSV / Excel","Connect via API URL"],
    horizontal=True,
    label_visibility="collapsed"
)

if source == "Upload CSV / Excel":
    st.markdown("""
    <div style="background:#F8F9FF;border:1px solid #EBEBEB;
                border-radius:10px;padding:14px 18px;margin:12px 0;">
        <div style="font-size:12px;color:#888;line-height:1.7;">
            Lumiq automatically detects your columns.
            Your file needs at least an invoice number,
            quantity, price and date field.
        </div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("Drop file here",
                                type=["csv","xlsx","xls"])
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
            c1,c2,c3,c4 = st.columns(4)
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
    st.markdown("""
    <div style="background:#F0F4FF;border-left:3px solid #4B7BF5;
                border-radius:8px;padding:12px 16px;margin:12px 0;">
        <div style="font-size:13px;font-weight:600;color:#1A1A2E;">
            UCI Online Retail Dataset
        </div>
        <div style="font-size:12px;color:#888;margin-top:2px;">
            541,909 transactions — UK retailer —
            Dec 2010 to Dec 2011
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── ACTIVE DATASET ────────────────────────────────────────────────
df    = get_data()
label = st.session_state.get('data_label','Sample Data')

st.markdown(f"""
<div style="background:white;border-radius:12px;
            padding:20px 24px;border:1px solid #EBEBEB;
            margin-bottom:16px;">
    <div style="font-size:13px;font-weight:700;color:#1A1A2E;
                margin-bottom:2px;">Active Dataset — {label}</div>
    <div style="font-size:11px;color:#AAAAAA;
                margin-bottom:16px;">Currently loaded data</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.metric("Records",   f"{len(df):,}")
c2.metric("Customers", f"{df['CustomerID'].nunique():,}")
c3.metric("Countries", f"{df['Country'].nunique():,}")
c4.metric("Products",  f"{df['StockCode'].nunique():,}")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ── ROLE CARDS ────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:11px;font-weight:700;color:#AAAAAA;
            text-transform:uppercase;letter-spacing:1px;
            margin-bottom:16px;">Available Dashboard Views</div>
""", unsafe_allow_html=True)

roles = [
    ("exec",     "📊", "#4B7BF5", "Executive",
     "C-Suite Overview",
     "Revenue totals, global map, MoM growth, AI insights"),
    ("sales",    "📈", "#2ECC71", "Sales Manager",
     "Sales Performance",
     "KPIs, country breakdown, AOV trend, top products"),
    ("trends",   "📉", "#F39C12", "Sales Trends",
     "Trend Analysis",
     "Monthly trends, growth rate, order volume"),
    ("customer", "👥", "#E74C3C", "Customer Analyst",
     "RFM Segmentation",
     "Segments, recency scatter, retention rate"),
    ("product",  "📦", "#9B59B6", "Product Manager",
     "Product Analysis",
     "Revenue rankings, geo map, price distribution"),
]

cols = st.columns(5)
for col, (key, icon, color, name, subtitle, desc) in \
        zip(cols, roles):
    with col:
        st.markdown(f"""
        <div style="background:white;border-radius:14px;
                    padding:20px 16px;
                    border:1px solid #EBEBEB;
                    border-top:3px solid {color};
                    min-height:160px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.04);">
            <div style="font-size:24px;margin-bottom:10px;">
                {icon}
            </div>
            <div style="font-size:14px;font-weight:700;
                        color:#1A1A2E;margin-bottom:4px;">
                {name}
            </div>
            <div style="font-size:10px;font-weight:700;
                        color:{color};text-transform:uppercase;
                        letter-spacing:0.5px;margin-bottom:10px;">
                {subtitle}
            </div>
            <div style="font-size:11px;color:#AAAAAA;
                        line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Open {name}",
                     key=f"open_{key}",
                     use_container_width=True):
            st.session_state.page = key
            st.rerun()

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1A1A2E;border-radius:14px;
            padding:28px 36px;display:flex;
            justify-content:space-between;
            align-items:center;flex-wrap:wrap;gap:12px;">
    <div>
        <div style="font-size:18px;font-weight:900;
                    color:white;letter-spacing:2px;">LUMIQ</div>
        <div style="font-size:11px;
                    color:rgba(255,255,255,0.3);margin-top:3px;">
            Retail Business Intelligence Platform
        </div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap;">
        <div style="background:rgba(255,255,255,0.06);
                    border:1px solid rgba(255,255,255,0.1);
                    border-radius:20px;padding:5px 14px;
                    font-size:12px;color:rgba(255,255,255,0.6);">
            Ayesha Jahangir
        </div>
        <div style="background:rgba(255,255,255,0.06);
                    border:1px solid rgba(255,255,255,0.1);
                    border-radius:20px;padding:5px 14px;
                    font-size:12px;color:rgba(255,255,255,0.6);">
            ID: 22504895
        </div>
        <div style="background:rgba(255,255,255,0.06);
                    border:1px solid rgba(255,255,255,0.1);
                    border-radius:20px;padding:5px 14px;
                    font-size:12px;color:rgba(255,255,255,0.6);">
            COM6001 FYP · BNU · 2025–26
        </div>
        <div style="background:rgba(255,255,255,0.06);
                    border:1px solid rgba(255,255,255,0.1);
                    border-radius:20px;padding:5px 14px;
                    font-size:12px;color:rgba(255,255,255,0.6);">
            Supervisor: Syeda Faiza Nasim
        </div>
    </div>
</div>
""", unsafe_allow_html=True)