import streamlit as st
import sys
sys.path.append('.')
from io import BytesIO

from data_loader import clean_data, load_data, load_default_data
import plotly.graph_objects as go
from theme import COLORS, TEAL_NAVY_SCALE, apply_plotly_theme
import pandas as pd


def load_uploaded_file(uploaded_file):
    if uploaded_file.name.lower().endswith(".csv"):
        raw_df = pd.read_csv(uploaded_file)
    else:
        raw_df = pd.read_excel(uploaded_file, engine="openpyxl")
    return clean_data(raw_df)


@st.cache_data
def prepare_test_dataset_downloads():
    columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]
    test_df = load_default_data()[columns].head(2500).copy()
    test_df["InvoiceDate"] = test_df["InvoiceDate"].dt.strftime("%Y-%m-%d %H:%M:%S")

    csv_bytes = test_df.to_csv(index=False).encode("utf-8")
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        test_df.to_excel(writer, index=False, sheet_name="Lumiq Test Data")
    excel_bytes = excel_buffer.getvalue()
    return test_df, csv_bytes, excel_bytes


st.markdown(
    """
    <section class="home-hero">
        <div class="hero-grid">
            <div>
                <div class="hero-kicker">Retail Intelligence Platform</div>
                <h1 class="hero-title">LUMIQ</h1>
                <p class="hero-copy">
                    Convert raw retail transactions into executive KPIs, sales trends,
                    customer segments, product performance, and country-level opportunities
                    in one clean BI command center.
                </p>
                <div class="hero-actions">
                    <span class="hero-chip">Executive KPIs</span>
                    <span class="hero-chip">Sales Analysis</span>
                    <span class="hero-chip">RFM Segments</span>
                    <span class="hero-chip">CSV/XLSX Upload Supported</span>
                    <span class="hero-chip">API Integration Coming Soon</span>
                </div>
            </div>
            <div class="upload-card">
                <div class="eyebrow">Start Analysis</div>
                <h3>Upload retail data or use sample data</h3>
                <p>CSV and Excel upload is supported for the current retail transaction format. Broader CSV schema compatibility is in progress.</p>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

upload_col, sample_col = st.columns([2, 1])
with upload_col:
    uploaded_file = st.file_uploader("Upload supported CSV or Excel retail data", type=["csv", "xlsx"])
    st.caption("Supported now: CSV/XLSX files that match Lumiq's retail transaction fields. Broader CSV schema compatibility is in progress. API integration is coming soon.")
    if uploaded_file:
        try:
            uploaded_df = load_uploaded_file(uploaded_file)
            st.session_state["uploaded_df_clean"] = uploaded_df
            st.session_state["data_source"] = "uploaded"
            st.success(f"Uploaded dataset active - {len(uploaded_df):,} clean records ready for analysis")
        except Exception as exc:
            st.error(f"Unable to process this file: {exc}")

with sample_col:
    if st.button("Use sample retail data", width='stretch'):
        st.session_state.pop("uploaded_df_clean", None)
        st.session_state["data_source"] = "sample"
        st.success("Sample retail dataset selected")


with st.spinner("Loading dataset..."):
    df = load_data()
data_source_label = "Uploaded dataset" if st.session_state.get("data_source") == "uploaded" else "Sample retail dataset"

test_df, test_csv, test_excel = prepare_test_dataset_downloads()

st.markdown(
    f"""
    <div class="download-panel">
        <div>
            <div class="eyebrow">Test Dataset</div>
            <h3>Download sample files for upload testing</h3>
            <p>Use these files to test Lumiq's supported retail transaction upload flow. The files include {len(test_df):,} rows in the current supported schema.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

download_col1, download_col2 = st.columns(2)
with download_col1:
    st.download_button(
        "Download CSV test dataset",
        data=test_csv,
        file_name="lumiq_test_dataset.csv",
        mime="text/csv",
        width="stretch",
    )

with download_col2:
    st.download_button(
        "Download Excel test dataset",
        data=test_excel,
        file_name="lumiq_test_dataset.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        width="stretch",
    )

total_revenue = df['Revenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
total_products = df['StockCode'].nunique()
date_min = df['InvoiceDate'].min().strftime('%b %Y')
date_max = df['InvoiceDate'].max().strftime('%b %Y')

st.markdown(
    f"""
    <div class="home-stats">
        <div class="home-stat-card">
            <div class="home-stat-label">Active Source</div>
            <div class="home-stat-value">{data_source_label}</div>
            <div class="home-stat-note">{len(df):,} clean records</div>
        </div>
        <div class="home-stat-card">
            <div class="home-stat-label">Total Revenue</div>
            <div class="home-stat-value">£{total_revenue:,.0f}</div>
            <div class="home-stat-note">{total_orders:,} orders</div>
        </div>
        <div class="home-stat-card">
            <div class="home-stat-label">Customers</div>
            <div class="home-stat-value">{total_customers:,}</div>
            <div class="home-stat-note">{total_products:,} products</div>
        </div>
        <div class="home-stat-card">
            <div class="home-stat-label">Date Range</div>
            <div class="home-stat-value">{date_min}</div>
            <div class="home-stat-note">to {date_max}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Lumiq Dashboard Preview")
snapshot_col1, snapshot_col2 = st.columns([1, 1])

monthly_snapshot = df.groupby('Month')['Revenue'].sum().reset_index()
monthly_snapshot['Month'] = monthly_snapshot['Month'].dt.strftime('%b %Y')

with snapshot_col1:
    fig = go.Figure(go.Scatter(
        x=monthly_snapshot['Month'],
        y=monthly_snapshot['Revenue'],
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color=COLORS["navy"], width=2),
        fillcolor='rgba(120,198,214,0.22)',
        marker=dict(size=6, color=COLORS["teal"]),
    ))
    apply_plotly_theme(fig, height=300)
    fig.update_layout(title='Revenue Timeline')
    fig.update_yaxes(title='Revenue (£)')
    st.plotly_chart(fig, width='stretch')

with snapshot_col2:
    country_share = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(8).reset_index()
    fig2 = go.Figure(go.Bar(
        x=country_share['Country'],
        y=country_share['Revenue'],
        marker=dict(color=country_share['Revenue'], colorscale=TEAL_NAVY_SCALE, showscale=False),
        text=[f"£{value:,.0f}" for value in country_share['Revenue']],
        textposition='outside',
    ))
    apply_plotly_theme(fig2, height=300)
    fig2.update_layout(title='Top Markets by Revenue')
    fig2.update_xaxes(tickangle=-25)
    fig2.update_yaxes(title='Revenue (£)')
    st.plotly_chart(fig2, width='stretch')

st.markdown(
    """
    <div class="explain-grid">
        <div class="explain-card">
            <div class="eyebrow">Executive</div>
            <h3>Monitor performance</h3>
            <p>Track revenue, orders, average order value, product concentration, and country contribution.</p>
        </div>
        <div class="explain-card">
            <div class="eyebrow">Sales & Customers</div>
            <h3>Find patterns</h3>
            <p>Explore monthly growth, order timing, RFM segments, customer value, and retention signals.</p>
        </div>
        <div class="explain-card">
            <div class="eyebrow">Products</div>
            <h3>Prioritise action</h3>
            <p>Identify top products, efficient markets, revenue concentration, and geographic opportunities.</p>
        </div>
        <div class="explain-card">
            <div class="eyebrow">Data Access</div>
            <h3>Upload now, API soon</h3>
            <p>CSV/XLSX upload is supported today. API integration is coming soon, and broader CSV schema compatibility is in progress.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
