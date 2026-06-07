import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_data
from html import escape
import plotly.graph_objects as go
from theme import COLORS, TEAL_NAVY_SCALE, apply_plotly_theme, page_title

page_title("Executive Overview")

with st.spinner("Loading data..."):
    df = load_data()

# Core KPIs
total_revenue    = df['Revenue'].sum()
total_orders     = df['InvoiceNo'].nunique()
total_customers  = df['CustomerID'].nunique()
total_products   = df['StockCode'].nunique()
avg_order_value  = total_revenue / total_orders
top_country      = df.groupby('Country')['Revenue'].sum().idxmax()
top_product      = df.groupby('Description')['Revenue'].sum().idxmax()
avg_items        = df.groupby('InvoiceNo')['Quantity'].sum().mean()

country_rev = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10).reset_index()

st.markdown(
    f"""
    <div class="executive-header">
        <div>
            <div class="eyebrow">Executive Command View</div>
            <h1>Performance at a glance</h1>
            <p>Track revenue, customer reach, order value, market concentration, and product contribution from the active retail dataset.</p>
        </div>
        <div class="executive-badge">{len(df):,} clean records</div>
    </div>
    <div class="kpi-grid">
        <div class="kpi-tile">
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-value">£{total_revenue:,.0f}</div>
            <div class="kpi-note">Across all completed transactions</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
            <div class="kpi-note">Unique invoices after cleaning</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Unique Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
            <div class="kpi-note">Known customers with valid IDs</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Unique Products</div>
            <div class="kpi-value">{total_products:,}</div>
            <div class="kpi-note">Distinct stock codes sold</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Avg Order Value</div>
            <div class="kpi-value">£{avg_order_value:,.2f}</div>
            <div class="kpi-note">Revenue divided by orders</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Top Country</div>
            <div class="kpi-value">{escape(str(top_country))}</div>
            <div class="kpi-note">Highest revenue market</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Top Product</div>
            <div class="kpi-value">{escape(top_product[:30] + "...")}</div>
            <div class="kpi-note">Highest revenue item</div>
        </div>
        <div class="kpi-tile">
            <div class="kpi-label">Avg Items / Order</div>
            <div class="kpi-value">{avg_items:.1f}</div>
            <div class="kpi-note">Average quantity per invoice</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_country_revenue = country_rev.iloc[0]['Revenue']
top_country_share = top_country_revenue / total_revenue * 100
top_product_revenue = df.groupby('Description')['Revenue'].sum().max()
top_product_share = top_product_revenue / total_revenue * 100

st.markdown(
    f"""
    <div class="insight-grid">
        <div class="exec-insight-card">
            <div class="eyebrow">Market Focus</div>
            <h3>{escape(str(top_country))} leads revenue</h3>
            <p>This market contributes {top_country_share:.1f}% of total revenue, making it the strongest executive priority.</p>
        </div>
        <div class="exec-insight-card pink">
            <div class="eyebrow">Product Focus</div>
            <h3>{escape(top_product[:42])}</h3>
            <p>The top product contributes {top_product_share:.1f}% of total revenue. Track concentration risk and stock availability.</p>
        </div>
        <div class="exec-insight-card green">
            <div class="eyebrow">Order Quality</div>
            <h3>£{avg_order_value:,.2f} average order</h3>
            <p>Average items per order is {avg_items:.1f}, connecting basket size with overall revenue quality.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="executive-section-label">Market Performance</div>', unsafe_allow_html=True)

fig = go.Figure(go.Bar(
    x=country_rev['Revenue'],
    y=country_rev['Country'],
    orientation='h',
    marker=dict(
        color=country_rev['Revenue'],
        colorscale=[[0, '#78C6D6'], [1, '#1F3B60']],
        showscale=False
    ),
    text=[f"£{v:,.0f}" for v in country_rev['Revenue']],
    textposition='outside'
))
fig.update_layout(
    height=360,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='#182232'),
    xaxis=dict(showgrid=True, gridcolor='#E5EDF2', title='Revenue (£)'),
    yaxis=dict(autorange='reversed'),
    margin=dict(l=0, r=80, t=20, b=20)
)
st.plotly_chart(fig, width='stretch')

st.markdown('<div class="executive-section-label">Revenue Mix & Concentration</div>', unsafe_allow_html=True)
mix_col1, mix_col2 = st.columns([1, 1])

with mix_col1:
    country_mix = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False)
    country_mix_display = country_mix.head(5).reset_index()
    other_revenue = country_mix.iloc[5:].sum()
    if other_revenue > 0:
        country_mix_display.loc[len(country_mix_display)] = ['Other', other_revenue]

    fig_mix = go.Figure(go.Pie(
        labels=country_mix_display['Country'],
        values=country_mix_display['Revenue'],
        hole=0.52,
        marker=dict(colors=[COLORS["navy"], COLORS["teal"], '#A8DCE6', COLORS["amber"], COLORS["pink"], '#D8E6EE']),
        textinfo='label+percent',
    ))
    apply_plotly_theme(fig_mix, height=320, top_margin=30)
    fig_mix.update_layout(title='Country Revenue Share', showlegend=False)
    st.plotly_chart(fig_mix, width='stretch')

with mix_col2:
    product_rev = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(12).reset_index()
    product_rev['CumulativeShare'] = product_rev['Revenue'].cumsum() / df['Revenue'].sum() * 100
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(
        x=product_rev['Description'],
        y=product_rev['Revenue'],
        name='Revenue',
        marker_color=COLORS["teal"],
    ))
    fig_pareto.add_trace(go.Scatter(
        x=product_rev['Description'],
        y=product_rev['CumulativeShare'],
        name='Cumulative Share',
        yaxis='y2',
        mode='lines+markers',
        line=dict(color=COLORS["navy"], width=2),
    ))
    apply_plotly_theme(fig_pareto, height=320, top_margin=35)
    fig_pareto.update_layout(
        title='Top Product Revenue Concentration',
        yaxis=dict(title='Revenue (£)', gridcolor=COLORS["grid"]),
        yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100]),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
    )
    fig_pareto.update_xaxes(tickangle=-35)
    st.plotly_chart(fig_pareto, width='stretch')

st.markdown('<div class="executive-section-label">Revenue Trend</div>', unsafe_allow_html=True)
monthly = df.groupby('MonthStr')['Revenue'].sum().reset_index()
monthly = monthly.sort_values('MonthStr')

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=monthly['MonthStr'], y=monthly['Revenue'],
    fill='tozeroy', mode='lines+markers',
    line=dict(color='#1F3B60', width=2),
    fillcolor='rgba(120,198,214,0.22)',
    marker=dict(size=6, color='#78C6D6')
))
fig2.update_layout(
    height=300,
    plot_bgcolor='white', paper_bgcolor='white',
    font=dict(color='#182232'),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#E5EDF2', title='Revenue (£)'),
    margin=dict(l=0, r=0, t=10, b=10)
)
st.plotly_chart(fig2, width='stretch')

st.markdown('<div class="executive-section-label">Order Economics</div>', unsafe_allow_html=True)
monthly_detail = df.groupby('Month').agg(
    Revenue=('Revenue', 'sum'),
    Orders=('InvoiceNo', 'nunique'),
).reset_index()
monthly_detail['Month'] = monthly_detail['Month'].dt.strftime('%b %Y')
monthly_detail['AverageOrderValue'] = monthly_detail['Revenue'] / monthly_detail['Orders']

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=monthly_detail['Month'],
    y=monthly_detail['Orders'],
    name='Orders',
    marker_color=COLORS["teal"],
))
fig3.add_trace(go.Scatter(
    x=monthly_detail['Month'],
    y=monthly_detail['AverageOrderValue'],
    name='Avg Order Value',
    yaxis='y2',
    mode='lines+markers',
    line=dict(color=COLORS["navy"], width=2),
))
apply_plotly_theme(fig3, height=320, top_margin=35)
fig3.update_layout(
    yaxis=dict(title='Orders', gridcolor=COLORS["grid"]),
    yaxis2=dict(title='Avg Order Value (£)', overlaying='y', side='right'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02),
)
st.plotly_chart(fig3, width='stretch')
