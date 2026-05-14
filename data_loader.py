import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx"
    try:
        df = pd.read_excel(url, engine='openpyxl')
        df = clean_data(df)
    except Exception:
        df = generate_sample_data()
        df = clean_data(df)
    return df

def generate_sample_data():
    np.random.seed(42)
    n = 10000
    countries = ['United Kingdom', 'Germany', 'France', 'Netherlands',
                 'Spain', 'Belgium', 'Switzerland', 'Portugal',
                 'Australia', 'Norway']
    products = [
        ('85123A', 'WHITE HANGING HEART T-LIGHT HOLDER'),
        ('71053',  'WHITE METAL LANTERN'),
        ('84406B', 'CREAM CUPID HEARTS COAT HANGER'),
        ('84029G', 'KNITTED UNION FLAG HOT WATER BOTTLE'),
        ('84029E', 'RED WOOLLY HOTTIE WHITE HEART'),
        ('22752',  'SET 7 BABUSHKA NESTING BOXES'),
        ('21730',  'GLASS STAR FROSTED T-LIGHT HOLDER'),
        ('22633',  'HAND WARMER UNION JACK'),
        ('22632',  'HAND WARMER RED POLKA DOT'),
        ('21080',  'SET OF 6 MUSHROOM MAGNETS'),
    ]
    stock_codes  = [p[0] for p in products]
    descriptions = [p[1] for p in products]
    dates = pd.date_range('2010-12-01', '2011-12-09', periods=n)
    idx   = np.random.randint(0, len(products), n)

    df = pd.DataFrame({
        'InvoiceNo':   [f'{500000 + i//5}' for i in range(n)],
        'StockCode':   [stock_codes[i]  for i in idx],
        'Description': [descriptions[i] for i in idx],
        'Quantity':    np.random.randint(1, 50, n),
        'InvoiceDate': dates,
        'UnitPrice':   np.round(np.random.uniform(0.5, 15.0, n), 2),
        'CustomerID':  np.random.choice(
            [f'{i}' for i in range(12000, 12500)] + [None]*200, n),
        'Country':     np.random.choice(
            countries, n,
            p=[0.85,0.04,0.03,0.02,0.02,0.01,0.01,0.01,0.005,0.005])
    })
    cancel_idx = np.random.choice(n, 300, replace=False)
    for i in cancel_idx:
        df.at[i, 'InvoiceNo'] = 'C' + df.at[i, 'InvoiceNo']
        df.at[i, 'Quantity']  = -df.at[i, 'Quantity']
    return df

def clean_data(df):
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity']  > 0]
    df = df[df['UnitPrice'] > 0]
    df = df.dropna(subset=['CustomerID'])
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Revenue']     = df['Quantity'] * df['UnitPrice']
    df['Month']       = df['InvoiceDate'].dt.to_period('M')
    df['MonthStr']    = df['InvoiceDate'].dt.strftime('%b %Y')
    df['Year']        = df['InvoiceDate'].dt.year
    return df

def get_rfm(df):
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg(
        Recency   = ('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
        Frequency = ('InvoiceNo',   'nunique'),
        Monetary  = ('Revenue',     'sum')
    ).reset_index()

    rfm['R_Score'] = pd.qcut(
        rfm['Recency'], 4, labels=[4,3,2,1]).astype(int)
    rfm['F_Score'] = pd.qcut(
        rfm['Frequency'].rank(method='first'), 4,
        labels=[1,2,3,4]).astype(int)
    rfm['M_Score'] = pd.qcut(
        rfm['Monetary'].rank(method='first'), 4,
        labels=[1,2,3,4]).astype(int)
    rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

    def segment(score):
        if score >= 10: return 'Champions'
        elif score >= 7: return 'Loyal Customers'
        elif score >= 5: return 'Potential Loyalists'
        elif score >= 3: return 'At Risk'
        else:            return 'Lost'

    rfm['Segment'] = rfm['RFM_Score'].apply(segment)
    return rfm
