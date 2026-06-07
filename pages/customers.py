import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_data, get_rfm
import plotly.graph_objects as go
import plotly.express as px
from theme import COLORS, apply_plotly_theme, page_title

page_title("Customer Insights")

with st.spinner("Loading data..."):
    df = load_data()
    rfm = get_rfm(df)

st.markdown('<div class="executive-section-label">RFM Segmentation Overview</div>', unsafe_allow_html=True)
seg_counts = rfm['Segment'].value_counts().reset_index()
seg_counts.columns = ['Segment', 'Count']

colors = {
    'Champions': '#1F3B60',
    'Loyal Customers': '#78C6D6',
    'Potential Loyalists': '#A8DCE6',
    'At Risk': '#D9A441',
    'Lost': '#D66565'
}

col1, col2 = st.columns([1, 1])
with col1:
    fig = go.Figure(go.Pie(
        labels=seg_counts['Segment'],
        values=seg_counts['Count'],
        marker=dict(colors=[colors.get(s, '#999') for s in seg_counts['Segment']]),
        hole=0.45,
        textinfo='label+percent'
    ))
    fig.update_layout(
        height=320, showlegend=False,
        paper_bgcolor='white',
        font=dict(color='#182232'),
        margin=dict(l=0, r=0, t=64, b=0)
    )
    st.plotly_chart(fig, width='stretch')

with col2:
    st.markdown("#### Segment Summary")
    seg_summary = rfm.groupby('Segment').agg(
        Customers=('CustomerID', 'count'),
        Avg_Recency=('Recency', 'mean'),
        Avg_Frequency=('Frequency', 'mean'),
        Avg_Monetary=('Monetary', 'mean')
    ).reset_index().round(1)
    seg_summary.columns = ['Segment', 'Customers', 'Avg Recency (days)', 'Avg Orders', 'Avg Revenue (£)']
    st.dataframe(seg_summary, width='stretch', hide_index=True)

st.markdown('<div class="executive-section-label">Segment Value Contribution</div>', unsafe_allow_html=True)
segment_value = rfm.groupby('Segment').agg(
    Customers=('CustomerID', 'count'),
    Revenue=('Monetary', 'sum'),
    AvgRevenue=('Monetary', 'mean'),
    AvgFrequency=('Frequency', 'mean'),
).reset_index().sort_values('Revenue', ascending=False)

value_col1, value_col2 = st.columns([1, 1])
with value_col1:
    fig_value = go.Figure()
    fig_value.add_trace(go.Bar(
        x=segment_value['Segment'],
        y=segment_value['Revenue'],
        name='Revenue',
        marker_color=COLORS["teal"],
        text=[f"£{value:,.0f}" for value in segment_value['Revenue']],
        textposition='outside',
    ))
    fig_value.add_trace(go.Scatter(
        x=segment_value['Segment'],
        y=segment_value['Customers'],
        name='Customers',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color=COLORS["navy"], width=2),
    ))
    apply_plotly_theme(fig_value, height=320, top_margin=35)
    fig_value.update_layout(
        title='Revenue vs Customer Count by Segment',
        yaxis=dict(title='Revenue (£)', gridcolor=COLORS["grid"]),
        yaxis2=dict(title='Customers', overlaying='y', side='right'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
    )
    fig_value.update_xaxes(tickangle=-20)
    st.plotly_chart(fig_value, width='stretch')

with value_col2:
    fig_avg = go.Figure(go.Bar(
        x=segment_value['Segment'],
        y=segment_value['AvgRevenue'],
        marker_color=COLORS["navy"],
        text=[f"£{value:,.0f}" for value in segment_value['AvgRevenue']],
        textposition='outside',
    ))
    apply_plotly_theme(fig_avg, height=320, top_margin=35)
    fig_avg.update_layout(title='Average Customer Value by Segment')
    fig_avg.update_xaxes(tickangle=-20)
    fig_avg.update_yaxes(title='Avg Revenue per Customer (£)')
    st.plotly_chart(fig_avg, width='stretch')

st.markdown('<div class="executive-section-label">Customer Value Map</div>', unsafe_allow_html=True)
value_map_col1, value_map_col2 = st.columns([1.35, 1])
fig2 = px.scatter(
    rfm, x='Recency', y='Monetary',
    color='Segment', size='Frequency',
    color_discrete_map=colors,
    hover_data=['CustomerID', 'Frequency'],
    labels={'Recency': 'Recency (days)', 'Monetary': 'Total Revenue (£)'}
)
fig2.update_layout(
    height=330, plot_bgcolor='white', paper_bgcolor='white',
    title='Recency vs Monetary Value by Segment',
    font=dict(color='#182232'),
    xaxis=dict(showgrid=True, gridcolor='#E5EDF2'),
    yaxis=dict(showgrid=True, gridcolor='#E5EDF2'),
    margin=dict(l=0, r=0, t=64, b=0)
)
with value_map_col1:
    st.plotly_chart(fig2, width='stretch')

score_counts = rfm['RFM_Score'].value_counts().sort_index().reset_index()
score_counts.columns = ['RFM Score', 'Customers']
fig_score = go.Figure(go.Bar(
    x=score_counts['RFM Score'],
    y=score_counts['Customers'],
    marker_color=COLORS["teal"],
    text=score_counts['Customers'],
    textposition='outside',
))
apply_plotly_theme(fig_score, height=330, top_margin=30)
fig_score.update_layout(title='Customers by RFM Score')
fig_score.update_xaxes(title='RFM Score')
fig_score.update_yaxes(title='Customers')
with value_map_col2:
    st.plotly_chart(fig_score, width='stretch')

st.markdown('<div class="executive-section-label">Behavioral Spread</div>', unsafe_allow_html=True)
behavior_col1, behavior_col2 = st.columns([1, 1])
fig_freq = px.box(
    rfm,
    x='Segment',
    y='Frequency',
    color='Segment',
    color_discrete_map=colors,
    points='outliers',
    labels={'Frequency': 'Orders per Customer'},
)
apply_plotly_theme(fig_freq, height=330, top_margin=30)
fig_freq.update_layout(title='Order Frequency Spread by Segment', showlegend=False)
fig_freq.update_xaxes(tickangle=-20)
with behavior_col1:
    st.plotly_chart(fig_freq, width='stretch')

fig_recency = px.histogram(
    rfm,
    x='Recency',
    color='Segment',
    color_discrete_map=colors,
    nbins=28,
    barmode='overlay',
    opacity=0.78,
    labels={'Recency': 'Days Since Last Purchase'},
)
apply_plotly_theme(fig_recency, height=330, top_margin=30)
fig_recency.update_layout(title='Customer Recency Distribution', legend=dict(orientation='h', yanchor='bottom', y=1.02))
fig_recency.update_yaxes(title='Customers')
with behavior_col2:
    st.plotly_chart(fig_recency, width='stretch')

st.markdown('<div class="executive-section-label">Top Customers</div>', unsafe_allow_html=True)
top_customers = df.groupby('CustomerID').agg(
    Total_Revenue=('Revenue', 'sum'),
    Total_Orders=('InvoiceNo', 'nunique'),
    Total_Items=('Quantity', 'sum')
).reset_index().sort_values('Total_Revenue', ascending=False).head(15)

top_customers['Total_Revenue'] = top_customers['Total_Revenue'].round(2)
top_customers.columns = ['Customer ID', 'Total Revenue (£)', 'Total Orders', 'Total Items']
top_customers.index = range(1, len(top_customers) + 1)
st.dataframe(top_customers, width='stretch')
