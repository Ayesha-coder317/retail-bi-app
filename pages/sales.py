import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_data
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from theme import COLORS, apply_plotly_theme, page_title

page_title("Sales Performance Dashboard")

with st.spinner("Loading data..."):
    df = load_data()

st.markdown('<div class="executive-section-label">Filters</div>', unsafe_allow_html=True)
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

monthly = filtered.groupby(filtered['InvoiceDate'].dt.to_period('M')).agg(
    Revenue=('Revenue', 'sum'),
    Orders=('InvoiceNo', 'nunique')
).reset_index()
monthly['Month'] = monthly['InvoiceDate'].dt.strftime('%b %Y')
monthly['GrowthRate'] = monthly['Revenue'].pct_change() * 100
monthly['AverageOrderValue'] = monthly['Revenue'] / monthly['Orders']

st.markdown('<div class="executive-section-label">Revenue Momentum</div>', unsafe_allow_html=True)
momentum_col1, momentum_col2 = st.columns([1.35, 1])

fig = go.Figure()
fig.add_trace(go.Bar(
    x=monthly['Month'], y=monthly['Revenue'],
    name='Revenue', marker_color='#78C6D6',
    opacity=0.85
))
fig.add_trace(go.Scatter(
    x=monthly['Month'], y=monthly['Revenue'],
    mode='lines+markers', name='Trend',
    line=dict(color='#1F3B60', width=2),
    marker=dict(size=5)
))
fig.update_layout(
    height=340, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#182232'),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#E5EDF2', title='Revenue (£)'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
    margin=dict(l=0, r=0, t=64, b=0)
)
with momentum_col1:
    st.plotly_chart(fig, width='stretch')

fig2 = go.Figure(go.Bar(
    x=monthly['Month'],
    y=monthly['GrowthRate'],
    marker_color=['#78C6D6' if v >= 0 else '#D66565' for v in monthly['GrowthRate'].fillna(0)],
    text=[f"{v:.1f}%" for v in monthly['GrowthRate'].fillna(0)],
    textposition='outside'
))
fig2.update_layout(
    height=300, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#182232'),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#E5EDF2', title='Growth Rate (%)'),
    margin=dict(l=0, r=0, t=64, b=0)
)
with momentum_col2:
    st.plotly_chart(fig2, width='stretch')

st.markdown('<div class="executive-section-label">Order Quality</div>', unsafe_allow_html=True)
quality_col1, quality_col2 = st.columns([1, 1])
fig_aov = go.Figure(go.Scatter(
    x=monthly['Month'],
    y=monthly['AverageOrderValue'],
    mode='lines+markers',
    fill='tozeroy',
    line=dict(color=COLORS["navy"], width=2),
    fillcolor='rgba(120,198,214,0.22)',
    marker=dict(size=6, color=COLORS["teal"]),
    text=[f"£{value:,.0f}" for value in monthly['AverageOrderValue']],
))
apply_plotly_theme(fig_aov, height=300)
fig_aov.update_layout(title='Average Order Value Trend')
fig_aov.update_yaxes(title='Avg Order Value (£)')
with quality_col1:
    st.plotly_chart(fig_aov, width='stretch')

fig3 = go.Figure(go.Scatter(
    x=monthly['Month'], y=monthly['Orders'],
    mode='lines+markers', fill='tozeroy',
    line=dict(color='#1F3B60', width=2),
    fillcolor='rgba(120,198,214,0.22)'
))
fig3.update_layout(
    height=300, title='Monthly Orders',
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#182232'),
    yaxis=dict(title='Orders'), margin=dict(l=0,r=0,t=64,b=0)
)
with quality_col2:
    st.plotly_chart(fig3, width='stretch')

st.markdown('<div class="executive-section-label">Sales Timing</div>', unsafe_allow_html=True)
timing_col1, timing_col2 = st.columns([1, 1.25])
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
dow = filtered.groupby(filtered['InvoiceDate'].dt.day_name())['Revenue'].sum().reset_index()
dow['InvoiceDate'] = pd.Categorical(dow['InvoiceDate'], categories=day_order, ordered=True)
dow = dow.sort_values('InvoiceDate')
fig4 = go.Figure(go.Bar(
    x=dow['InvoiceDate'], y=dow['Revenue'],
    marker_color='#78C6D6'
))
fig4.update_layout(
    height=380, title='Revenue by Day of Week',
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#182232'),
    yaxis=dict(title='Revenue (£)'), margin=dict(l=0,r=0,t=64,b=0)
)
with timing_col1:
    st.plotly_chart(fig4, width='stretch')

heatmap = filtered.copy()
heatmap['MonthLabel'] = heatmap['InvoiceDate'].dt.strftime('%b %Y')
heatmap['Weekday'] = heatmap['InvoiceDate'].dt.day_name()
heatmap_data = heatmap.groupby(['Weekday', 'MonthLabel'])['Revenue'].sum().reset_index()
month_order = heatmap.drop_duplicates('Month')[['Month', 'MonthLabel']].sort_values('Month')['MonthLabel'].tolist()
heatmap_data['Weekday'] = pd.Categorical(heatmap_data['Weekday'], categories=day_order, ordered=True)
heatmap_pivot = heatmap_data.pivot(index='Weekday', columns='MonthLabel', values='Revenue').reindex(day_order)
heatmap_pivot = heatmap_pivot.reindex(columns=month_order).fillna(0)

fig_heatmap = go.Figure(go.Heatmap(
    z=heatmap_pivot.values,
    x=heatmap_pivot.columns,
    y=heatmap_pivot.index,
    colorscale=[[0, '#EEF3F6'], [0.5, COLORS["teal"]], [1, COLORS["navy"]]],
    colorbar=dict(title='Revenue (£)'),
    hovertemplate='Day: %{y}<br>Month: %{x}<br>Revenue: £%{z:,.0f}<extra></extra>',
))
apply_plotly_theme(fig_heatmap, height=380, top_margin=20)
fig_heatmap.update_layout(title='Revenue Timing Heatmap')
fig_heatmap.update_xaxes(tickangle=-35)
with timing_col2:
    st.plotly_chart(fig_heatmap, width='stretch')
