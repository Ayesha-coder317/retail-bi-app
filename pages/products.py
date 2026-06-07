import streamlit as st
import sys
sys.path.append('.')
from data_loader import load_data
import plotly.graph_objects as go
import plotly.express as px
from theme import COLORS, TEAL_NAVY_SCALE, apply_plotly_theme, page_title

page_title("Product Performance")

with st.spinner("Loading data..."):
    df = load_data()

tab1, tab2 = st.tabs(["🛍️ Products", "🌍 Countries"])

with tab1:
    st.markdown("### Top 15 Products by Revenue")
    top_products = df.groupby('Description').agg(
        Revenue=('Revenue', 'sum'),
        Quantity=('Quantity', 'sum'),
        Orders=('InvoiceNo', 'nunique')
    ).reset_index().sort_values('Revenue', ascending=False).head(15)

    fig = go.Figure(go.Bar(
        y=top_products['Description'],
        x=top_products['Revenue'],
        orientation='h',
        marker=dict(color=top_products['Revenue'], colorscale=[[0, '#78C6D6'], [1, '#1F3B60']], showscale=False),
        text=[f"£{v:,.0f}" for v in top_products['Revenue']],
        textposition='outside'
    ))
    fig.update_layout(
        height=500, plot_bgcolor='white', paper_bgcolor='white',
        font=dict(color='#182232'),
        xaxis=dict(showgrid=True, gridcolor='#E5EDF2', title='Revenue (£)'),
        yaxis=dict(autorange='reversed'),
        margin=dict(l=0, r=80, t=10, b=0)
    )
    st.plotly_chart(fig, width='stretch')

    st.markdown("### Top Products by Quantity Sold")
    top_qty = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = go.Figure(go.Bar(
        x=top_qty['Description'],
        y=top_qty['Quantity'],
        marker_color='#78C6D6',
        text=top_qty['Quantity'],
        textposition='outside'
    ))
    fig2.update_layout(
        height=350, plot_bgcolor='white', paper_bgcolor='white',
        font=dict(color='#182232'),
        xaxis=dict(tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor='#E5EDF2', title='Units Sold'),
        margin=dict(l=0, r=0, t=10, b=80)
    )
    st.plotly_chart(fig2, width='stretch')

    st.markdown("### Product Portfolio Detail")
    portfolio = df.groupby('Description').agg(
        Revenue=('Revenue', 'sum'),
        Quantity=('Quantity', 'sum'),
        Orders=('InvoiceNo', 'nunique'),
        AvgPrice=('UnitPrice', 'mean'),
    ).reset_index().sort_values('Revenue', ascending=False).head(30)

    port_col1, port_col2 = st.columns([1, 1])
    with port_col1:
        fig_portfolio = px.scatter(
            portfolio,
            x='Quantity',
            y='Revenue',
            size='Orders',
            color='AvgPrice',
            color_continuous_scale=TEAL_NAVY_SCALE,
            hover_name='Description',
            labels={
                'Quantity': 'Units Sold',
                'Revenue': 'Revenue (£)',
                'AvgPrice': 'Avg Unit Price (£)',
                'Orders': 'Orders',
            },
        )
        apply_plotly_theme(fig_portfolio, height=360, top_margin=35)
        fig_portfolio.update_layout(title='Revenue vs Units Sold')
        st.plotly_chart(fig_portfolio, width='stretch')

    with port_col2:
        portfolio_pareto = portfolio.head(15).copy()
        portfolio_pareto['CumulativeShare'] = portfolio_pareto['Revenue'].cumsum() / portfolio['Revenue'].sum() * 100
        fig_conc = go.Figure()
        fig_conc.add_trace(go.Bar(
            x=portfolio_pareto['Description'],
            y=portfolio_pareto['Revenue'],
            marker_color=COLORS["teal"],
            name='Revenue',
        ))
        fig_conc.add_trace(go.Scatter(
            x=portfolio_pareto['Description'],
            y=portfolio_pareto['CumulativeShare'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(color=COLORS["navy"], width=2),
            name='Cumulative Share',
        ))
        apply_plotly_theme(fig_conc, height=360, top_margin=35)
        fig_conc.update_layout(
            title='Top Product Concentration',
            yaxis=dict(title='Revenue (£)', gridcolor=COLORS["grid"]),
            yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 100]),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
        )
        fig_conc.update_xaxes(tickangle=-35)
        st.plotly_chart(fig_conc, width='stretch')

    st.markdown("### Product Revenue Treemap")
    treemap_data = portfolio.head(20).copy()
    fig_tree = px.treemap(
        treemap_data,
        path=['Description'],
        values='Revenue',
        color='Orders',
        color_continuous_scale=TEAL_NAVY_SCALE,
        hover_data={'Quantity': ':,', 'AvgPrice': ':.2f'},
    )
    apply_plotly_theme(fig_tree, height=420, top_margin=35)
    fig_tree.update_layout(title='Top 20 Product Revenue Footprint')
    st.plotly_chart(fig_tree, width='stretch')

with tab2:
    st.markdown("### Revenue by Country")
    country_rev = df.groupby('Country').agg(
        Revenue=('Revenue', 'sum'),
        Orders=('InvoiceNo', 'nunique'),
        Customers=('CustomerID', 'nunique')
    ).reset_index().sort_values('Revenue', ascending=False)

    col1, col2 = st.columns([2, 1])

    with col1:
        fig3 = px.choropleth(
            country_rev,
            locations='Country',
            locationmode='country names',
            color='Revenue',
            color_continuous_scale=[[0, '#D8F0F4'], [0.5, '#78C6D6'], [1, '#1F3B60']],
            labels={'Revenue': 'Revenue (£)'},
            title='Global Revenue Distribution'
        )
        fig3.update_layout(
            height=400,
            paper_bgcolor='white',
            font=dict(color='#182232'),
            geo=dict(showframe=False, showcoastlines=True),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig3, width='stretch')

    with col2:
        st.markdown("#### Country Breakdown")
        display = country_rev.head(10).copy()
        display['Revenue'] = display['Revenue'].apply(lambda x: f"£{x:,.0f}")
        display.columns = ['Country', 'Revenue', 'Orders', 'Customers']
        display.index = range(1, len(display) + 1)
        st.dataframe(display, width='stretch')

    st.markdown("### Top 10 Countries — Orders vs Revenue")
    top10 = country_rev.head(10)
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='Revenue (£)', x=top10['Country'], y=top10['Revenue'], marker_color='#78C6D6'))
    fig4.add_trace(go.Bar(name='Orders', x=top10['Country'], y=top10['Orders'], marker_color='#1F3B60'))
    fig4.update_layout(
        barmode='group', height=350,
        plot_bgcolor='white', paper_bgcolor='white',
        font=dict(color='#182232'),
        xaxis=dict(tickangle=-20),
        yaxis=dict(showgrid=True, gridcolor='#E5EDF2'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig4, width='stretch')

    st.markdown("### Country Efficiency Metrics")
    country_eff = country_rev.copy()
    country_eff['RevenuePerCustomer'] = country_eff['Revenue'] / country_eff['Customers']
    country_eff['RevenuePerOrder'] = country_eff['Revenue'] / country_eff['Orders']
    country_eff = country_eff.replace([float('inf'), -float('inf')], 0).fillna(0)

    eff_col1, eff_col2 = st.columns([1, 1])
    with eff_col1:
        top_eff = country_eff.sort_values('RevenuePerCustomer', ascending=False).head(12)
        fig_eff = go.Figure(go.Bar(
            x=top_eff['RevenuePerCustomer'],
            y=top_eff['Country'],
            orientation='h',
            marker=dict(color=top_eff['RevenuePerCustomer'], colorscale=TEAL_NAVY_SCALE, showscale=False),
            text=[f"£{value:,.0f}" for value in top_eff['RevenuePerCustomer']],
            textposition='outside',
        ))
        apply_plotly_theme(fig_eff, height=360, top_margin=30)
        fig_eff.update_layout(title='Revenue per Customer by Country')
        fig_eff.update_yaxes(autorange='reversed')
        fig_eff.update_xaxes(title='Revenue per Customer (£)')
        st.plotly_chart(fig_eff, width='stretch')

    with eff_col2:
        fig_country_bubble = px.scatter(
            country_eff.head(20),
            x='Orders',
            y='Revenue',
            size='Customers',
            color='RevenuePerOrder',
            color_continuous_scale=TEAL_NAVY_SCALE,
            hover_name='Country',
            labels={
                'Orders': 'Orders',
                'Revenue': 'Revenue (£)',
                'Customers': 'Customers',
                'RevenuePerOrder': 'Revenue per Order (£)',
            },
        )
        apply_plotly_theme(fig_country_bubble, height=360, top_margin=35)
        fig_country_bubble.update_layout(title='Country Scale vs Efficiency')
        st.plotly_chart(fig_country_bubble, width='stretch')
