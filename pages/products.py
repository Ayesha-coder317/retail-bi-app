import streamlit as st
import sys
sys.path.append('.')
from data_loader import get_data
import plotly.graph_objects as go
import plotly.express as px

st.markdown('<div class="section-title">Product & Country Analysis</div>',
            unsafe_allow_html=True)
st.markdown("##### Product Performance and Geographic Distribution")
st.markdown("---")

with st.spinner("Loading data..."):
    df = get_data()

total_products  = df['StockCode'].nunique()
top_product     = df.groupby('Description')['Revenue'].sum().idxmax()
top_product_rev = df.groupby('Description')['Revenue'].sum().max()
top_qty_product = df.groupby('Description')['Quantity'].sum().idxmax()
total_units     = df['Quantity'].sum()
avg_unit_price  = df['UnitPrice'].mean()
top_country     = df.groupby('Country')['Revenue'].sum().idxmax()
total_countries = df['Country'].nunique()

st.markdown("### Product KPIs")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Unique Products",  f"{total_products:,}")
c2.metric("Total Units Sold", f"{total_units:,}")
c3.metric("Avg Unit Price",   f"£{avg_unit_price:,.2f}")
c4.metric("Markets Served",   f"{total_countries:,}")

st.markdown("---")
c5, c6, c7, c8 = st.columns(4)
c5.metric("Top Product",     top_product[:25] + "...")
c6.metric("Top Product Rev", f"£{top_product_rev:,.0f}")
c7.metric("Top by Quantity", top_qty_product[:25] + "...")
c8.metric("Top Market",      top_country)

st.markdown("---")

tab1, tab2 = st.tabs(["Products", "Countries"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Top 15 Products by Revenue")
        top_products = (df.groupby('Description')
            .agg(Revenue =('Revenue','sum'),
                 Quantity=('Quantity','sum'))
            .reset_index()
            .sort_values('Revenue', ascending=False)
            .head(15))
        fig = go.Figure(go.Bar(
            y=top_products['Description'],
            x=top_products['Revenue'],
            orientation='h',
            marker=dict(color=top_products['Revenue'],
                        colorscale='Blues', showscale=False),
            text=[f"£{v:,.0f}" for v in top_products['Revenue']],
            textposition='outside'))
        fig.update_layout(
            height=500, plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                       title='Revenue (£)'),
            yaxis=dict(autorange='reversed'),
            margin=dict(l=0, r=80, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Top 15 Products by Quantity")
        top_qty = (df.groupby('Description')['Quantity']
                   .sum().sort_values(ascending=False)
                   .head(15).reset_index())
        fig2 = go.Figure(go.Bar(
            y=top_qty['Description'],
            x=top_qty['Quantity'],
            orientation='h',
            marker_color='#0A0F1E',
            text=top_qty['Quantity'],
            textposition='outside'))
        fig2.update_layout(
            height=500, plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=True, gridcolor='#f0f0f0',
                       title='Units Sold'),
            yaxis=dict(autorange='reversed'),
            margin=dict(l=0, r=80, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### Revenue vs Quantity — Top 10")
        top10 = (df.groupby('Description')
                 .agg(Revenue =('Revenue','sum'),
                      Quantity=('Quantity','sum'))
                 .reset_index()
                 .sort_values('Revenue', ascending=False)
                 .head(10))
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            name='Revenue (£)', x=top10['Description'],
            y=top10['Revenue'], marker_color='#2E86AB'))
        fig3.add_trace(go.Bar(
            name='Quantity', x=top10['Description'],
            y=top10['Quantity'], marker_color='#0A0F1E'))
        fig3.update_layout(
            barmode='group', height=320,
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(tickangle=-30, showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(l=0, r=0, t=10, b=80))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("### Product Revenue Distribution")
        product_rev = (df.groupby('Description')['Revenue']
                       .sum().reset_index())
        fig4 = go.Figure(go.Histogram(
            x=product_rev['Revenue'], nbinsx=30,
            marker_color='#2E86AB', opacity=0.85))
        fig4.update_layout(
            height=320, plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(title='Revenue (£)', showgrid=False),
            yaxis=dict(title='Number of Products',
                       showgrid=True, gridcolor='#f0f0f0'),
            margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.markdown("### Revenue by Country")
    country_rev = (df.groupby('Country')
        .agg(Revenue  =('Revenue',    'sum'),
             Orders   =('InvoiceNo',  'nunique'),
             Customers=('CustomerID', 'nunique'))
        .reset_index()
        .sort_values('Revenue', ascending=False))

    col5, col6 = st.columns([2, 1])
    with col5:
        fig5 = px.choropleth(
            country_rev, locations='Country',
            locationmode='country names', color='Revenue',
            color_continuous_scale='Blues',
            labels={'Revenue':'Revenue (£)'},
            title='Global Revenue Distribution')
        fig5.update_layout(
            height=400, paper_bgcolor='white',
            geo=dict(showframe=False, showcoastlines=True),
            margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        st.markdown("#### Top 10 Countries")
        display = country_rev.head(10).copy()
        display['Revenue'] = display['Revenue'].apply(
            lambda x: f"£{x:,.0f}")
        display.columns = ['Country','Revenue','Orders','Customers']
        display.index = range(1, len(display)+1)
        st.dataframe(display, use_container_width=True)

    st.markdown("---")
    col7, col8 = st.columns(2)
    with col7:
        st.markdown("### Orders vs Revenue by Country")
        top10c = country_rev.head(10)
        fig6 = go.Figure()
        fig6.add_trace(go.Bar(
            name='Revenue (£)', x=top10c['Country'],
            y=top10c['Revenue'], marker_color='#2E86AB'))
        fig6.add_trace(go.Bar(
            name='Orders', x=top10c['Country'],
            y=top10c['Orders'], marker_color='#0A0F1E'))
        fig6.update_layout(
            barmode='group', height=320,
            plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(tickangle=-20),
            yaxis=dict(showgrid=True, gridcolor='#f0f0f0'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig6, use_container_width=True)

    with col8:
        st.markdown("### Customers per Country")
        fig7 = go.Figure(go.Bar(
            x=country_rev.head(10)['Customers'],
            y=country_rev.head(10)['Country'],
            orientation='h',
            marker_color='#D4AF37',
            text=country_rev.head(10)['Customers'],
            textposition='outside'))
        fig7.update_layout(
            height=320, plot_bgcolor='white', paper_bgcolor='white',
            xaxis=dict(showgrid=False),
            yaxis=dict(autorange='reversed'),
            margin=dict(l=0, r=80, t=10, b=0))
        st.plotly_chart(fig7, use_container_width=True)