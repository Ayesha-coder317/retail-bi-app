import streamlit as st
import sys
sys.path.append('.')
from data_loader import get_data
import plotly.graph_objects as go
import pandas as pd

st.markdown('<div class="section-title">Sales Trends</div>',
            unsafe_allow_html=True)
st.markdown("#### Monthly Revenue, Growth Rate and Day Analysis")
st.markdown("---")

with st.spinner("Loading data..."):
    df = get_data()

col1, col2 = st.columns(2)
with col1:
    countries = ['All'] + sorted(df['Country'].unique().tolist())
    selected_country = st.selectbox("Country", countries)
with col2:
    years = ['All'] + sorted(df['Year'].unique().tolist())
    selected_year = st.selectbox("Year", years)

filtered = df.copy()
if selected_country != 'All':
    filtered = filtered[filtered['Country'] == selected_country]
if selected_year != 'All':
    filtered = filtered[filtered['Year'] == int(selected_year)]

st.markdown("---")
st.markdown("### Monthly Revenue")
monthly = (filtered.groupby(
    filtered['InvoiceDate'].dt.to_period('M'))
    .agg(Revenue=('Revenue','sum'),
         Orders=('InvoiceNo','nunique'))
    .reset_index())
monthly['Month']      = monthly['InvoiceDate'].dt.strftime('%b %Y')
monthly['GrowthRate'] = monthly['Revenue'].pct_change() * 100

fig = go.Figure()
fig.add_trace(go.Bar(
    x=monthly['Month'], y=monthly['Revenue'],
    name='Revenue', marker_color='#4A90D9', opacity=0.85))
fig.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Revenue'],
    mode='lines+markers', name='Trend',
    line=dict(color='#0D1B2A', width=2),
    marker=dict(size=5)))
fig.update_layout(
    height=380, plot_bgcolor='white', paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Revenue (£)'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Month-on-Month Growth Rate (%)")
fig2 = go.Figure(go.Bar(
    x=monthly['Month'], y=monthly['GrowthRate'],
    marker_color=['#2ecc71' if v >= 0 else '#e74c3c'
                  for v in monthly['GrowthRate'].fillna(0)],
    text=[f"{v:.1f}%" for v in monthly['GrowthRate'].fillna(0)],
    textposition='outside'))
fig2.update_layout(
    height=300, plot_bgcolor='white', paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Growth Rate (%)'),
    margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Revenue by Day of Week")
dow = (filtered.groupby(
    filtered['InvoiceDate'].dt.day_name())
    ['Revenue'].sum().reset_index())
day_order = ['Monday','Tuesday','Wednesday',
             'Thursday','Friday','Saturday','Sunday']
dow['InvoiceDate'] = pd.Categorical(
    dow['InvoiceDate'], categories=day_order, ordered=True)
dow = dow.sort_values('InvoiceDate')
fig3 = go.Figure(go.Bar(
    x=dow['InvoiceDate'], y=dow['Revenue'],
    marker_color='#e67e22'))
fig3.update_layout(
    height=300, plot_bgcolor='white', paper_bgcolor='white',
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0', title='Revenue (£)'),
    margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig3, use_container_width=True)