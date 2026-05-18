import streamlit as st
import sys
sys.path.append('.')
from data_loader import get_data, get_rfm
import plotly.graph_objects as go
import plotly.express as px

st.markdown('<div class="section-title">Customer Insights</div>',
            unsafe_allow_html=True)
st.markdown("##### RFM Segmentation and Customer Behaviour Analysis")
st.markdown("---")

with st.spinner("Loading data..."):
    df  = get_data()
    rfm = get_rfm(df)

total_customers  = df['CustomerID'].nunique()
avg_order_value  = df['Revenue'].sum() / df['InvoiceNo'].nunique()
top_customer_rev = df.groupby('CustomerID')['Revenue'].sum().max()
avg_frequency    = rfm['Frequency'].mean()
avg_recency      = rfm['Recency'].mean()
avg_monetary     = rfm['Monetary'].mean()
champions_count  = len(rfm[rfm['Segment'] == 'Champions'])

st.markdown("### Customer KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers",    f"{total_customers:,}")
c2.metric("Champions",          f"{champions_count:,}")
c3.metric("Avg Order Value",    f"£{avg_order_value:,.2f}")
c4.metric("Top Customer Rev",   f"£{top_customer_rev:,.0f}")

st.markdown("---")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Avg Recency (days)", f"{avg_recency:.0f}")
c6.metric("Avg Order Freq",     f"{avg_frequency:.1f}")
c7.metric("Avg Spend/Customer", f"£{avg_monetary:,.0f}")
c8.metric("Total Segments",     "5")

st.markdown("---")

colors = {
    'Champions':           '#0A0F1E',
    'Loyal Customers':     '#D4AF37',
    'Potential Loyalists': '#2E86AB',
    'At Risk':             '#E84855',
    'Lost':                '#AAAAAA'
}

col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### Customer Segments")
    seg_counts = rfm['Segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    fig = go.Figure(go.Pie(
        labels=seg_counts['Segment'],
        values=seg_counts['Count'],
        marker=dict(colors=[colors.get(s,'#999')
                             for s in seg_counts['Segment']]),
        hole=0.45, textinfo='label+percent'))
    fig.update_layout(
        height=320, showlegend=False,
        paper_bgcolor='white',
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### Segment Summary")
    seg_summary = rfm.groupby('Segment').agg(
        Customers   =('CustomerID','count'),
        Avg_Recency =('Recency',   'mean'),
        Avg_Freq    =('Frequency', 'mean'),
        Avg_Revenue =('Monetary',  'mean')
    ).reset_index().round(1)
    seg_summary.columns = ['Segment','Customers',
                            'Avg Recency','Avg Orders',
                            'Avg Revenue (£)']
    st.dataframe(seg_summary, use_container_width=True,
                 hide_index=True)

    st.markdown("### Revenue by Segment")
    seg_rev = rfm.groupby('Segment')['Monetary'].sum().reset_index()
    fig2 = go.Figure(go.Bar(
        x=seg_rev['Monetary'],
        y=seg_rev['Segment'],
        orientation='h',
        marker=dict(color=[colors.get(s,'#999')
                           for s in seg_rev['Segment']]),
        text=[f"£{v:,.0f}" for v in seg_rev['Monetary']],
        textposition='outside'))
    fig2.update_layout(
        height=220, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=False),
        yaxis=dict(autorange='reversed'),
        margin=dict(l=0, r=80, t=10, b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)
with col3:
    st.markdown("### Recency vs Revenue")
    fig3 = px.scatter(
        rfm, x='Recency', y='Monetary',
        color='Segment', size='Frequency',
        color_discrete_map=colors,
        labels={'Recency':'Recency (days)',
                'Monetary':'Revenue (£)'})
    fig3.update_layout(
        height=320, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown("### Frequency Distribution")
    fig4 = go.Figure(go.Histogram(
        x=rfm['Frequency'], nbinsx=20,
        marker_color='#2E86AB', opacity=0.85))
    fig4.update_layout(
        height=320, plot_bgcolor='white', paper_bgcolor='white',
        xaxis=dict(title='Number of Orders', showgrid=False),
        yaxis=dict(title='Customers',
                   showgrid=True, gridcolor='#f0f0f0'),
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("### Top 15 Customers by Revenue")
top_customers = (df.groupby('CustomerID')
    .agg(Total_Revenue=('Revenue', 'sum'),
         Total_Orders =('InvoiceNo','nunique'),
         Total_Items  =('Quantity', 'sum'))
    .reset_index()
    .sort_values('Total_Revenue', ascending=False)
    .head(15))
top_customers['Total_Revenue'] = top_customers['Total_Revenue'].round(2)
top_customers.columns = ['Customer ID','Total Revenue (£)',
                          'Total Orders','Total Items']
top_customers.index = range(1, len(top_customers)+1)
st.dataframe(top_customers, use_container_width=True)