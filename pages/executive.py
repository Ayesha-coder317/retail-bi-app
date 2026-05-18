import streamlit as st
import sys
sys.path.append('.')
from data_loader import get_data
import plotly.graph_objects as go
import plotly.express as px

st.markdown('<div class="section-title">Executive Overview</div>',
            unsafe_allow_html=True)
st.markdown("##### High-Level Business Performance")
st.markdown("---")

with st.spinner("Loading data..."):
    df = get_data()

total_revenue   = df['Revenue'].sum()
total_orders    = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
total_products  = df['StockCode'].nunique()
avg_order_value = total_revenue / total_orders
top_country     = df.groupby('Country')['Revenue'].sum().idxmax()
top_product     = df.groupby('Description')['Revenue'].sum().idxmax()
best_month      = df.groupby('MonthStr')['Revenue'].sum().idxmax()

st.markdown("### Business at a Glance")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue",   f"£{total_revenue:,.0f}")
c2.metric("Total Orders",    f"{total_orders:,}")
c3.metric("Total Customers", f"{total_customers:,}")
c4.metric("Unique Products", f"{total_products:,}")

st.markdown("---")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Avg Order Value", f"£{avg_order_value:,.2f}")
c6.metric("Top Market",      top_country)
c7.metric("Top Product",     top_product[:25] + "...")
c8.metric("Peak Month",      best_month)

st.markdown("---")

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### Monthly Revenue Trend")
    monthly = (df.groupby('MonthStr')['Revenue']
               .sum().reset_index().sort_values('MonthStr'))
    monthly['Growth'] = monthly['Revenue'].pct_change() * 100
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly['MonthStr'], y=monthly['Revenue'],
        name='Revenue', marker_color='#2E86AB', opacity=0.75))
    fig.add_trace(go.Scatter(
        x=monthly['MonthStr'], y=monthly['Revenue'],
        mode='lines+markers', name='Trend',
        line=dict(color='#D4AF37', width=2),
        marker=dict(size=5, color='#D4AF37')))
    fig.update_layout(
        height=300, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Revenue (£)'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Top 5 Markets")
    country_rev = (df.groupby('Country')['Revenue']
                   .sum().sort_values(ascending=False)
                   .head(5).reset_index())
    fig2 = go.Figure(go.Bar(
        x=country_rev['Revenue'],
        y=country_rev['Country'],
        orientation='h',
        marker=dict(color=country_rev['Revenue'],
                    colorscale='Blues', showscale=False),
        text=[f"£{v:,.0f}" for v in country_rev['Revenue']],
        textposition='outside'))
    fig2.update_layout(
        height=300, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(autorange='reversed'),
        margin=dict(l=0, r=80, t=10, b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Orders vs Revenue by Month")
    orders_monthly = (df.groupby('MonthStr')['InvoiceNo']
                      .nunique().reset_index())
    orders_monthly.columns = ['MonthStr', 'Orders']
    merged = monthly.merge(orders_monthly, on='MonthStr')
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=merged['MonthStr'], y=merged['Revenue'],
        name='Revenue', marker_color='#2E86AB', opacity=0.8))
    fig3.add_trace(go.Scatter(
        x=merged['MonthStr'], y=merged['Orders'],
        mode='lines+markers', name='Orders',
        line=dict(color='#D4AF37', width=2),
        yaxis='y2'))
    fig3.update_layout(
        height=300, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(title='Revenue (£)', showgrid=True,
                   gridcolor='#f0f0f0'),
        yaxis2=dict(title='Orders', overlaying='y', side='right'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(l=0, r=60, t=10, b=0))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("### Month-on-Month Growth Rate")
    fig4 = go.Figure(go.Bar(
        x=monthly['MonthStr'],
        y=monthly['Growth'],
        marker_color=['#3BB273' if v >= 0 else '#E84855'
                      for v in monthly['Growth'].fillna(0)],
        text=[f"{v:.1f}%" for v in monthly['Growth'].fillna(0)],
        textposition='outside'))
    fig4.update_layout(
        height=300, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                   title='Growth (%)'),
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("### Global Revenue Distribution")
country_all = df.groupby('Country')['Revenue'].sum().reset_index()
fig5 = px.choropleth(
    country_all, locations='Country',
    locationmode='country names', color='Revenue',
    color_continuous_scale='Blues',
    labels={'Revenue': 'Revenue (£)'})
fig5.update_layout(
    height=400, paper_bgcolor='white',
    geo=dict(showframe=False, showcoastlines=True),
    margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig5, use_container_width=True)