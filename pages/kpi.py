import streamlit as st
import sys
sys.path.append('.')
from data_loader import get_data
import plotly.graph_objects as go
import pandas as pd

st.markdown('<div class="section-title">Sales Performance</div>',
            unsafe_allow_html=True)
st.markdown("##### Revenue, Orders and Growth Analysis")
st.markdown("---")

with st.spinner("Loading data..."):
    df = get_data()

total_revenue   = df['Revenue'].sum()
total_orders    = df['InvoiceNo'].nunique()
avg_order_value = total_revenue / total_orders
top_country     = df.groupby('Country')['Revenue'].sum().idxmax()
top_product     = df.groupby('Description')['Revenue'].sum().idxmax()
avg_items       = df.groupby('InvoiceNo')['Quantity'].sum().mean()
best_month      = df.groupby('MonthStr')['Revenue'].sum().idxmax()
best_day        = df.groupby(
    df['InvoiceDate'].dt.day_name())['Revenue'].sum().idxmax()

st.markdown("### Sales KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue",   f"£{total_revenue:,.0f}")
c2.metric("Total Orders",    f"{total_orders:,}")
c3.metric("Avg Order Value", f"£{avg_order_value:,.2f}")
c4.metric("Avg Items/Order", f"{avg_items:.1f}")

st.markdown("---")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Top Country",  top_country)
c6.metric("Top Product",  top_product[:25] + "...")
c7.metric("Peak Month",   best_month)
c8.metric("Best Day",     best_day)

st.markdown("---")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("### Revenue by Country — Top 10")
    country_rev = (df.groupby('Country')['Revenue']
                   .sum().sort_values(ascending=False)
                   .head(10).reset_index())
    fig = go.Figure(go.Bar(
        x=country_rev['Revenue'],
        y=country_rev['Country'],
        orientation='h',
        marker=dict(color=country_rev['Revenue'],
                    colorscale='Blues', showscale=False),
        text=[f"£{v:,.0f}" for v in country_rev['Revenue']],
        textposition='outside'))
    fig.update_layout(
        height=380, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                   title='Revenue (£)'),
        yaxis=dict(autorange='reversed'),
        margin=dict(l=0, r=80, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Revenue Share")
    top5   = (df.groupby('Country')['Revenue']
              .sum().sort_values(ascending=False)
              .head(5).reset_index())
    others = total_revenue - top5['Revenue'].sum()
    top5.loc[len(top5)] = ['Others', others]
    fig2 = go.Figure(go.Pie(
        labels=top5['Country'],
        values=top5['Revenue'],
        hole=0.45,
        textinfo='label+percent',
        marker=dict(colors=[
            '#0A0F1E', '#D4AF37', '#2E86AB',
            '#E84855', '#3BB273', '#AAAAAA'
        ])))
    fig2.update_layout(
        height=380, showlegend=False,
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Revenue by Day of Week")
    dow = (df.groupby(df['InvoiceDate'].dt.day_name())
           ['Revenue'].sum().reset_index())
    day_order = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday','Sunday']
    dow['InvoiceDate'] = pd.Categorical(
        dow['InvoiceDate'], categories=day_order, ordered=True)
    dow = dow.sort_values('InvoiceDate')
    fig3 = go.Figure(go.Bar(
        x=dow['InvoiceDate'],
        y=dow['Revenue'],
        marker_color='#D4AF37',
        text=[f"£{v:,.0f}" for v in dow['Revenue']],
        textposition='outside'))
    fig3.update_layout(
        height=300, plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                   title='Revenue (£)'),
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("### Top 10 Products by Revenue")
    top_p = (df.groupby('Description')['Revenue']
             .sum().sort_values(ascending=False)
             .head(10).reset_index())
    fig4 = go.Figure(go.Bar(
        x=top_p['Revenue'],
        y=top_p['Description'],
        orientation='h',
        marker_color='#0A0F1E',
        text=[f"£{v:,.0f}" for v in top_p['Revenue']],
        textposition='outside'))
    fig4.update_layout(
        height=300, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(autorange='reversed'),
        margin=dict(l=0, r=80, t=10, b=0))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("### Monthly Revenue Overview")
monthly = (df.groupby('MonthStr')['Revenue']
           .sum().reset_index().sort_values('MonthStr'))
fig5 = go.Figure()
fig5.add_trace(go.Scatter(
    x=monthly['MonthStr'], y=monthly['Revenue'],
    fill='tozeroy', mode='lines+markers',
    line=dict(color='#2E86AB', width=2),
    fillcolor='rgba(46,134,171,0.1)',
    marker=dict(size=6, color='#D4AF37')))
fig5.update_layout(
    height=280, plot_bgcolor='white', paper_bgcolor='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#f0f0f0',
               title='Revenue (£)'),
    margin=dict(l=0, r=0, t=10, b=0))
st.plotly_chart(fig5, use_container_width=True)