import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_from_csv, load_from_excel, get_data
import plotly.graph_objects as go
import plotly.express as px

st.markdown("""
<div style="background:linear-gradient(160deg,#EEF2FF,#F5F0FF,#FFF5F0);
            border-radius:18px;padding:34px 36px;margin:0 0 24px 0;
            border:1px solid rgba(255,255,255,0.72);
            box-shadow:0 14px 38px rgba(31,59,96,0.06);
            text-align:center;">
    <div style="font-size:11px;font-weight:700;color:#4B7BF5;
                letter-spacing:4px;text-transform:uppercase;
                margin-bottom:16px;">
        COM6001 Final Year Project - BNU 2025-26
    </div>
    <div style="font-size:44px;font-weight:900;color:#1A1A6E;
                line-height:1.1;margin-bottom:12px;">LUMIQ</div>
    <div style="font-size:18px;color:#555;margin-bottom:16px;">
        Retail Business Intelligence Platform
    </div>
    <div style="font-size:14px;color:#666;max-width:520px;
                margin:0 auto 22px auto;line-height:1.7;">
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
c1.metric("Role Views", "6")
c2.metric("KPIs Tracked", "10+")
c3.metric("RFM Segments", "5")
c4.metric("Test Cases", "65")

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("""
    <div class="connect-title">Connect Your Data</div>
    <div class="connect-sub">
        Upload a file or connect a live API. Lumiq auto-detects your columns.
    </div>
    """, unsafe_allow_html=True)

    source = st.radio(
        "",
        ["Use Sample Data", "Upload CSV / Excel"],
        horizontal=True,
        label_visibility="collapsed",
        key="data_source_radio"
    )

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if source == "Upload CSV / Excel":
        _loaded = st.session_state.get("uploaded_df")
        if _loaded is not None:
            _lbl = st.session_state.get("data_label", "your file")
            st.success(
                f"Data loaded: **{_lbl}** — {len(_loaded):,} records active across all pages. "
                "Upload a new file below to replace it."
            )
        uploaded = st.file_uploader("Drop CSV or Excel file here", type=["csv", "xlsx", "xls"])
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
                st.session_state.data_label = uploaded.name[:20]
                st.success(f"{len(df):,} clean records loaded from **{uploaded.name}**")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Records", f"{len(df):,}")
                c2.metric(
                    "Date Range",
                    f"{df['InvoiceDate'].min().strftime('%b %Y')} - "
                    f"{df['InvoiceDate'].max().strftime('%b %Y')}"
                )
                c3.metric("Countries", f"{df['Country'].nunique():,}")
                c4.metric("Products", f"{df['StockCode'].nunique():,}")
                with st.expander("Preview data"):
                    st.dataframe(df.head(5), use_container_width=True)

    else:
        if 'uploaded_df' in st.session_state:
            del st.session_state['uploaded_df']
        st.session_state.data_label = "Sample Data"
        st.info("UCI Online Retail Dataset - 541,909 transactions, Dec 2010 to Dec 2011")

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

df = get_data()
label = st.session_state.get('data_label', 'Sample Data')

with st.container(border=True):
    st.markdown(f"""
    <div class="connect-title">Active Dataset - {label}</div>
    <div class="connect-sub">Currently loaded</div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Records", f"{len(df):,}")
    c2.metric("Customers", f"{df['CustomerID'].nunique():,}")
    c3.metric("Countries", f"{df['Country'].nunique():,}")
    c4.metric("Products", f"{df['StockCode'].nunique():,}")

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="connect-title">Auto Retail Insights</div>
<div class="connect-sub">
    Lumiq profiles the loaded retail data and creates the most relevant insights and visuals from the columns it finds.
</div>
""", unsafe_allow_html=True)

insights = []
if len(df) and 'Revenue' in df.columns:
    total_revenue = df['Revenue'].sum()
    insights.append(f"Total revenue is {total_revenue:,.0f} across {df['InvoiceNo'].nunique():,} orders.")
    if 'Category' in df.columns:
        cat_rev = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
        if len(cat_rev):
            insights.append(f"{cat_rev.index[0]} is the strongest category with {cat_rev.iloc[0]:,.0f} revenue.")
    if 'Country' in df.columns:
        market_rev = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
        if len(market_rev):
            insights.append(f"{market_rev.index[0]} is the leading market/location by revenue.")
    if 'CustomerID' in df.columns:
        repeat_rate = (df.groupby('CustomerID')['InvoiceNo'].nunique().gt(1).mean() * 100)
        insights.append(f"Repeat-purchase rate is {repeat_rate:.1f}% based on detected customer IDs.")

cols = st.columns(min(3, max(1, len(insights))))
for idx, text in enumerate(insights[:3]):
    with cols[idx]:
        st.markdown(f"""
        <div class="insight-card">
            <div class="insight-label">Auto Insight</div>
            <div class="insight-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Revenue Trends", "Category / Products", "Market / Customers"])

with tab1:
    if {'Month', 'Revenue'}.issubset(df.columns):
        monthly = (df.groupby('Month')['Revenue']
                   .sum().reset_index().sort_values('Month'))
        monthly['MonthStr'] = monthly['Month'].dt.strftime('%b %Y')
        fig = go.Figure(go.Scatter(
            x=monthly['MonthStr'], y=monthly['Revenue'],
            mode='lines+markers', fill='tozeroy',
            line=dict(color='#78C6D6', width=3),
            fillcolor='rgba(120,198,214,0.14)'
        ))
        fig.update_layout(
            height=320, plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False, tickangle=-30),
            yaxis=dict(showgrid=True, gridcolor='#EEF3F6'),
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Add a date and revenue/sales column to generate trend analysis.")

with tab2:
    left, right = st.columns(2)
    with left:
        if {'Category', 'Revenue'}.issubset(df.columns):
            cat = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(cat, x='Revenue', y='Category', orientation='h', color_discrete_sequence=['#C63D73'])
            fig.update_layout(height=320, plot_bgcolor='white', paper_bgcolor='white',
                              yaxis=dict(autorange='reversed'), margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category column detected.")
    with right:
        if {'Description', 'Revenue'}.issubset(df.columns):
            prod = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(prod, x='Revenue', y='Description', orientation='h', color_discrete_sequence=['#1F3B60'])
            fig.update_layout(height=320, plot_bgcolor='white', paper_bgcolor='white',
                              yaxis=dict(autorange='reversed'), margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No product/description column detected.")

with tab3:
    left, right = st.columns(2)
    with left:
        if {'Country', 'Revenue'}.issubset(df.columns):
            market = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(market, x='Revenue', y='Country', orientation='h', color_discrete_sequence=['#78C6D6'])
            fig.update_layout(height=320, plot_bgcolor='white', paper_bgcolor='white',
                              yaxis=dict(autorange='reversed'), margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No market/location column detected.")
    with right:
        if {'CustomerID', 'Revenue'}.issubset(df.columns):
            cust = df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(cust, x='Revenue', y='CustomerID', orientation='h', color_discrete_sequence=['#2ECC71'])
            fig.update_layout(height=320, plot_bgcolor='white', paper_bgcolor='white',
                              yaxis=dict(autorange='reversed'), margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No customer ID column detected.")
