import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_from_csv, load_from_excel, load_from_api, get_data

st.markdown("""
<div style="
    background: linear-gradient(135deg, #0D1B2A 0%, #1B3A5C 50%, #4A90D9 100%);
    border-radius: 20px;
    padding: 60px 48px;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute; top:-40px; right:-40px; width:300px;
                height:300px; background:rgba(74,144,217,0.15);
                border-radius:50%;"></div>
    <div style="position:absolute; bottom:-60px; right:100px; width:200px;
                height:200px; background:rgba(74,144,217,0.1);
                border-radius:50%;"></div>
    <div style="font-size:15px; font-weight:700; color:rgba(255,255,255,0.6);
                letter-spacing:4px; text-transform:uppercase;
                margin-bottom:12px;">Welcome to</div>
    <div style="font-size:72px; font-weight:900; color:white;
                letter-spacing:4px; line-height:1;
                margin-bottom:8px;">LUMIQ</div>
    <div style="font-size:22px; font-weight:400;
                color:rgba(255,255,255,0.75);
                margin-bottom:24px; letter-spacing:1px;">
        Retail Business Intelligence - Reimagined
    </div>
    <div style="font-size:16px; color:rgba(255,255,255,0.6);
                max-width:600px; line-height:1.8;">
        Transform your raw sales data into powerful, role-based insights.
        Upload your own dataset or connect via API - Lumiq adapts to any
        retail business instantly.
    </div>
    <div style="margin-top:32px; display:flex; gap:12px; flex-wrap:wrap;">
        <div style="background:rgba(255,255,255,0.12);
                    border:1px solid rgba(255,255,255,0.2);
                    border-radius:30px; padding:8px 20px;
                    font-size:13px; color:white; font-weight:600;">
            CSV / Excel Upload
        </div>
        <div style="background:rgba(255,255,255,0.12);
                    border:1px solid rgba(255,255,255,0.2);
                    border-radius:30px; padding:8px 20px;
                    font-size:13px; color:white; font-weight:600;">
            API Integration
        </div>
        <div style="background:rgba(255,255,255,0.12);
                    border:1px solid rgba(255,255,255,0.2);
                    border-radius:30px; padding:8px 20px;
                    font-size:13px; color:white; font-weight:600;">
            4 Role-Based Views
        </div>
        <div style="background:rgba(255,255,255,0.12);
                    border:1px solid rgba(255,255,255,0.2);
                    border-radius:30px; padding:8px 20px;
                    font-size:13px; color:white; font-weight:600;">
            RFM Segmentation
        </div>
        <div style="background:rgba(255,255,255,0.12);
                    border:1px solid rgba(255,255,255,0.2);
                    border-radius:30px; padding:8px 20px;
                    font-size:13px; color:white; font-weight:600;">
            Free Deployment
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats row
st.markdown("""
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr;
            gap:16px; margin-bottom:32px;">
    <div style="background:linear-gradient(135deg,#4A90D9,#2E5F8A);
                border-radius:14px; padding:24px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:white;">4</div>
        <div style="font-size:13px; color:rgba(255,255,255,0.8);
                    font-weight:600; margin-top:4px;">Role-Based Views</div>
    </div>
    <div style="background:linear-gradient(135deg,#2ecc71,#1a8a4a);
                border-radius:14px; padding:24px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:white;">7</div>
        <div style="font-size:13px; color:rgba(255,255,255,0.8);
                    font-weight:600; margin-top:4px;">Core KPIs Tracked</div>
    </div>
    <div style="background:linear-gradient(135deg,#e67e22,#c0392b);
                border-radius:14px; padding:24px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:white;">5</div>
        <div style="font-size:13px; color:rgba(255,255,255,0.8);
                    font-weight:600; margin-top:4px;">RFM Segments</div>
    </div>
    <div style="background:linear-gradient(135deg,#9b59b6,#6c3483);
                border-radius:14px; padding:24px; text-align:center;">
        <div style="font-size:36px; font-weight:900; color:white;">44</div>
        <div style="font-size:13px; color:rgba(255,255,255,0.8);
                    font-weight:600; margin-top:4px;">Automated Tests</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Data source
st.markdown("""
<div style="font-size:28px; font-weight:800; color:#0D1B2A;
            margin-bottom:8px;">Connect Your Data</div>
<div style="font-size:15px; color:#666; margin-bottom:20px;">
    Lumiq works with any retail dataset - upload a file or connect a live API.
</div>
""", unsafe_allow_html=True)

source = st.radio(
    "",
    ["Use Sample Data", "Upload CSV / Excel", "Connect via API URL"],
    horizontal=True,
    label_visibility="collapsed"
)

if source == "Upload CSV / Excel":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Required columns:**")
        st.markdown("""
        | Field | Accepted Names |
        |---|---|
        | Invoice | InvoiceNo, OrderID, TransactionID |
        | Quantity | Quantity, Qty, Units |
        | Price | UnitPrice, Price, Rate |
        | Date | InvoiceDate, OrderDate, SaleDate |
        """)
    with col2:
        st.markdown("**Optional columns:**")
        st.markdown("""
        | Field | Accepted Names |
        |---|---|
        | Customer | CustomerID, ClientID |
        | Country | Country, Region, Market |
        | Product | Description, Product, Item |
        | Code | StockCode, SKU, ProductCode |
        """)

    uploaded = st.file_uploader(
        "Drop your file here or click to browse",
        type=["csv", "xlsx", "xls"],
        help="Supports CSV and Excel files"
    )

    if uploaded:
        with st.spinner("Processing your dataset..."):
            if uploaded.name.endswith('.csv'):
                df, err = load_from_csv(uploaded)
            else:
                df, err = load_from_excel(uploaded)

        if err:
            st.error(f"Could not load file: {err}")
        else:
            st.session_state.uploaded_df = df
            st.session_state.data_label  = f"Custom: {uploaded.name}"
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#2ecc71,#1a8a4a);
                        border-radius:14px; padding:20px; margin:16px 0;">
                <div style="font-size:18px; font-weight:800; color:white;">
                    Dataset loaded successfully
                </div>
                <div style="font-size:14px; color:rgba(255,255,255,0.85);
                            margin-top:4px;">
                    {len(df):,} clean records from {uploaded.name}
                </div>
            </div>
            """, unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Records",    f"{len(df):,}")
            c2.metric("Date Range",
                      f"{df['InvoiceDate'].min().strftime('%b %Y')} - "
                      f"{df['InvoiceDate'].max().strftime('%b %Y')}")
            c3.metric("Countries",  f"{df['Country'].nunique():,}")
            c4.metric("Products",   f"{df['StockCode'].nunique():,}")
            with st.expander("Preview first 5 rows"):
                st.dataframe(df.head(5), use_container_width=True)

elif source == "Connect via API URL":
    st.markdown("""
    <div style="background:#F0F7FF; border:2px solid #4A90D9;
                border-radius:14px; padding:20px; margin:12px 0;">
        <div style="font-size:15px; font-weight:700; color:#0D1B2A;
                    margin-bottom:6px;">REST API Connection</div>
        <div style="font-size:14px; color:#666;">
            Your API must return JSON - either a list of records or a
            dictionary with a key containing a list.
            Column detection works the same as CSV upload.
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_url = st.text_input(
        "API endpoint URL",
        placeholder="https://your-api.com/sales/data"
    )

    if st.button("Connect to API", key="fetch_api"):
        if not api_url:
            st.warning("Please enter an API URL.")
        else:
            with st.spinner("Connecting..."):
                df, err = load_from_api(api_url)
            if err:
                st.error(f"Could not connect: {err}")
            else:
                st.session_state.uploaded_df = df
                st.session_state.data_label  = f"API: {api_url[:40]}..."
                st.success(f"Connected - {len(df):,} clean records fetched")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Records",   f"{len(df):,}")
                c2.metric("Date Range",
                          f"{df['InvoiceDate'].min().strftime('%b %Y')} - "
                          f"{df['InvoiceDate'].max().strftime('%b %Y')}")
                c3.metric("Countries", f"{df['Country'].nunique():,}")
                c4.metric("Products",  f"{df['StockCode'].nunique():,}")

else:
    if 'uploaded_df' in st.session_state:
        del st.session_state['uploaded_df']
    st.session_state.data_label = "UCI Online Retail (Sample)"
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0D1B2A,#1B3A5C);
                border-radius:14px; padding:20px; margin:16px 0;">
        <div style="font-size:16px; font-weight:700; color:white;">
            Using built-in sample dataset
        </div>
        <div style="font-size:14px; color:rgba(255,255,255,0.7);
                    margin-top:4px;">
            UCI Online Retail - 541,909 transactions from a UK-based
            retailer (Dec 2010 - Dec 2011)
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

df    = get_data()
label = st.session_state.get('data_label', 'UCI Online Retail (Sample)')

st.markdown(f"""
<div style="font-size:22px; font-weight:800; color:#0D1B2A;
            margin-bottom:16px;">
    Active Dataset - {label}
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Records",    f"{len(df):,}")
c2.metric("Unique Customers", f"{df['CustomerID'].nunique():,}")
c3.metric("Countries",        f"{df['Country'].nunique():,}")
c4.metric("Unique Products",  f"{df['StockCode'].nunique():,}")

st.markdown("---")

# Role cards
st.markdown("""
<div style="font-size:28px; font-weight:800; color:#0D1B2A;
            margin-bottom:8px;">Role-Based Intelligence</div>
<div style="font-size:15px; color:#666; margin-bottom:24px;">
    Each view is tailored to what that person actually needs to know.
    Select a role from the sidebar to get started.
</div>
""", unsafe_allow_html=True)

roles_display = [
    ("Executive",        "#4A90D9",
     "C-Suite overview",
     "Revenue totals, market distribution, global map, monthly trend"),
    ("Sales Manager",    "#2ecc71",
     "Sales performance",
     "KPIs, growth rate, day-of-week analysis, top countries"),
    ("Customer Analyst", "#e67e22",
     "Customer behaviour",
     "RFM segments, recency vs revenue, top customers table"),
    ("Product Manager",  "#9b59b6",
     "Product analysis",
     "Top products by revenue and quantity, country breakdown"),
]

cols = st.columns(4)
for col, (name, color, subtitle, desc) in zip(cols, roles_display):
    with col:
        st.markdown(f"""
        <div style="border:2px solid {color}; border-radius:14px;
                    padding:20px; min-height:180px;">
            <div style="width:10px; height:10px; background:{color};
                        border-radius:50%; margin-bottom:12px;"></div>
            <div style="font-size:16px; font-weight:800;
                        color:#0D1B2A; margin-bottom:4px;">{name}</div>
            <div style="font-size:12px; font-weight:600;
                        color:{color}; margin-bottom:10px;">{subtitle}</div>
            <div style="font-size:12px; color:#666;
                        line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# How it works
st.markdown("""
<div style="font-size:28px; font-weight:800; color:#0D1B2A;
            margin-bottom:24px;">How Lumiq Works</div>
""", unsafe_allow_html=True)

steps = [
    ("01", "#4A90D9", "Connect Your Data",
     "Upload CSV or Excel, connect a REST API, or use the sample dataset"),
    ("02", "#2ecc71", "Automatic Processing",
     "Lumiq detects your columns, cleans data and removes cancellations"),
    ("03", "#e67e22", "Select Your Role",
     "Choose Executive, Sales Manager, Customer Analyst or Product Manager"),
    ("04", "#9b59b6", "Explore Insights",
     "Interactive charts, RFM segments and revenue trends instantly"),
]

cols = st.columns(4)
for col, (num, color, title, desc) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="text-align:center; padding:20px 12px;">
            <div style="font-size:40px; font-weight:900; color:{color};
                        margin-bottom:12px;">{num}</div>
            <div style="font-size:15px; font-weight:800; color:#0D1B2A;
                        margin-bottom:8px;">{title}</div>
            <div style="font-size:13px; color:#666;
                        line-height:1.7;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Tech stack
st.markdown("""
<div style="font-size:22px; font-weight:800; color:#0D1B2A;
            margin-bottom:16px;">Built With</div>
""", unsafe_allow_html=True)

tech = [
    ("Python",          "#3776AB", "Core language"),
    ("Streamlit",       "#FF4B4B", "Web framework"),
    ("Plotly",          "#3F4F75", "Interactive charts"),
    ("Pandas",          "#150458", "Data processing"),
    ("Streamlit Cloud", "#4A90D9", "Free deployment"),
]

cols = st.columns(5)
for col, (name, color, role) in zip(cols, tech):
    with col:
        st.markdown(f"""
        <div style="background:{color}14; border:1px solid {color}40;
                    border-radius:10px; padding:14px; text-align:center;">
            <div style="font-size:14px; font-weight:800;
                        color:{color};">{name}</div>
            <div style="font-size:11px; color:#888;
                        margin-top:4px;">{role}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:40px 0 10px 0;
            font-size:13px; color:#999;">
    Lumiq - Built for COM6001 Final Year Project at BNU |
    Ayesha Jahangir (22504895) |
    Supervised by Syeda Faiza Nasim
</div>
""", unsafe_allow_html=True)