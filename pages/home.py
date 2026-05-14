import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_data

st.markdown('<div class="section-title">Business Intelligence Dashboard</div>',
            unsafe_allow_html=True)
st.markdown("#### Retail Sales Performance & Customer Insight Analysis")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### About This Project
    This web application is part of a Research Project at BNU, supervised by
    **Syeda Faiza Nasim**. It presents a fully functional Business Intelligence
    system using the **UCI Online Retail Dataset** — real-world transactional
    data from a UK-based online retailer.
    """)
    st.markdown("### What Each Page Does")
    st.markdown("""
    | Page | Description |
    |---|---|
    | 📈 KPI Summary | Key performance indicators at a glance |
    | 📉 Sales Trends | Monthly revenue and growth rate over time |
    | 👥 Customer Insights | RFM segmentation and top customers |
    | 🛍️ Product & Country | Best performing products and geographic sales |
    """)

with col2:
    st.markdown("### Dataset Overview")
    st.info("""
    **Name:** UCI Online Retail Dataset\n
    **Records:** ~541,909 transactions\n
    **Period:** Dec 2010 – Dec 2011\n
    **Source:** UK-based online retailer\n
    **Variables:** InvoiceNo, StockCode,
    Quantity, UnitPrice, CustomerID,
    Country, InvoiceDate
    """)
    st.markdown("### Tech Stack")
    st.success("""
    🐍 Python\n
    🌐 Streamlit — Web framework\n
    📊 Plotly — Interactive charts\n
    🐼 Pandas — Data processing\n
    ☁️ Streamlit Cloud — Deployment
    """)

st.markdown("---")
st.markdown("### Research Pipeline")
cols = st.columns(7)
steps = [
    ("1", "Dataset\nCollection",     "#4A90D9"),
    ("2", "Data\nCleaning",          "#5B9BD5"),
    ("3", "KPI\nIdentification",     "#2E75B6"),
    ("4", "BI Data\nModelling",      "#1F4E79"),
    ("5", "Dashboard\nDevelopment",  "#2E5F8A"),
    ("6", "Web App\nDevelopment",    "#1B3A5C"),
    ("7", "Validation &\nEvaluation","#152744"),
]
for col, (num, label, color) in zip(cols, steps):
    with col:
        st.markdown(f"""
        <div style="background:{color}; border-radius:8px;
        padding:12px 8px; text-align:center; color:white;
        font-size:12px; font-weight:600; min-height:70px;">
            <div style="font-size:18px; font-weight:800;">{num}</div>
            {label.replace(chr(10),'<br>')}
        </div>""", unsafe_allow_html=True)

st.markdown("---")
with st.spinner("Loading dataset..."):
    df = load_data()
st.success(f"✅ Dataset loaded — {len(df):,} clean records ready for analysis")
