import pandas as pd
import numpy as np
import streamlit as st

REQUIRED_COLS = {
    'invoice':     ['InvoiceNo', 'Invoice', 'OrderID', 'Order_ID', 'TransactionID'],
    'quantity':    ['Quantity', 'Qty', 'Units', 'Amount'],
    'price':       ['UnitPrice', 'Price', 'Unit_Price', 'SalePrice', 'Rate'],
    'customer':    ['CustomerID', 'Customer_ID', 'ClientID', 'CustomerCode'],
    'date':        ['InvoiceDate', 'Date', 'OrderDate', 'TransactionDate', 'SaleDate'],
    'country':     ['Country', 'Region', 'Location', 'Territory', 'Market'],
    'description': ['Description', 'Product', 'ProductName', 'Item', 'ItemName'],
    'stockcode':   ['StockCode', 'SKU', 'ProductCode', 'ItemCode'],
}

def detect_columns(df):
    mapping = {}
    cols_lower = {c.lower(): c for c in df.columns}
    for key, candidates in REQUIRED_COLS.items():
        for c in candidates:
            if c.lower() in cols_lower:
                mapping[key] = cols_lower[c.lower()]
                break
    return mapping

def standardise(df, mapping):
    rename = {}
    if 'invoice'     in mapping: rename[mapping['invoice']]     = 'InvoiceNo'
    if 'quantity'    in mapping: rename[mapping['quantity']]     = 'Quantity'
    if 'price'       in mapping: rename[mapping['price']]        = 'UnitPrice'
    if 'customer'    in mapping: rename[mapping['customer']]     = 'CustomerID'
    if 'date'        in mapping: rename[mapping['date']]         = 'InvoiceDate'
    if 'country'     in mapping: rename[mapping['country']]      = 'Country'
    if 'description' in mapping: rename[mapping['description']]  = 'Description'
    if 'stockcode'   in mapping: rename[mapping['stockcode']]    = 'StockCode'
    df = df.rename(columns=rename)
    if 'Country'     not in df.columns: df['Country']     = 'Unknown'
    if 'Description' not in df.columns: df['Description'] = 'Unknown'
    if 'StockCode'   not in df.columns: df['StockCode']   = df['InvoiceNo']
    if 'CustomerID'  not in df.columns: df['CustomerID']  = 'Unknown'
    return df

def clean_data(df):
    if 'InvoiceNo' in df.columns:
        df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity']  > 0]
    df = df[df['UnitPrice'] > 0]
    df = df.dropna(subset=['Quantity', 'UnitPrice'])
    df['InvoiceDate'] = pd.to_datetime(
        df['InvoiceDate'], infer_datetime_format=True, errors='coerce')
    df = df.dropna(subset=['InvoiceDate'])
    df['Revenue']  = df['Quantity'] * df['UnitPrice']
    df['Month']    = df['InvoiceDate'].dt.to_period('M')
    df['MonthStr'] = df['InvoiceDate'].dt.strftime('%b %Y')
    df['Year']     = df['InvoiceDate'].dt.year
    return df

def load_from_csv(file):
    try:
        try:
            df = pd.read_csv(file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(file, encoding='latin1')
        mapping = detect_columns(df)
        missing = [k for k in ['invoice','quantity','price','date']
                   if k not in mapping]
        if missing:
            return None, f"Could not detect columns: {', '.join(missing)}."
        df = standardise(df, mapping)
        df = clean_data(df)
        return df, None
    except Exception as e:
        return None, str(e)

def load_from_excel(file):
    try:
        df = pd.read_excel(file, engine='openpyxl')
        mapping = detect_columns(df)
        missing = [k for k in ['invoice','quantity','price','date']
                   if k not in mapping]
        if missing:
            return None, f"Could not detect columns: {', '.join(missing)}."
        df = standardise(df, mapping)
        df = clean_data(df)
        return df, None
    except Exception as e:
        return None, str(e)

def load_from_api(url):
    import requests
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            key = next(iter(data))
            df = pd.DataFrame(data[key])
        else:
            return None, "Unsupported API response format."
        mapping = detect_columns(df)
        missing = [k for k in ['invoice','quantity','price','date']
                   if k not in mapping]
        if missing:
            return None, f"Could not detect columns: {', '.join(missing)}."
        df = standardise(df, mapping)
        df = clean_data(df)
        return df, None
    except Exception as e:
        return None, str(e)

def generate_sample_data():
    np.random.seed(42)
    n = 10000
    countries = ['United Kingdom','Germany','France','Netherlands',
                 'Spain','Belgium','Switzerland','Portugal',
                 'Australia','Norway']
    products = [
        ('85123A','WHITE HANGING HEART T-LIGHT HOLDER'),
        ('71053', 'WHITE METAL LANTERN'),
        ('84406B','CREAM CUPID HEARTS COAT HANGER'),
        ('84029G','KNITTED UNION FLAG HOT WATER BOTTLE'),
        ('84029E','RED WOOLLY HOTTIE WHITE HEART'),
        ('22752', 'SET 7 BABUSHKA NESTING BOXES'),
        ('21730', 'GLASS STAR FROSTED T-LIGHT HOLDER'),
        ('22633', 'HAND WARMER UNION JACK'),
        ('22632', 'HAND WARMER RED POLKA DOT'),
        ('21080', 'SET OF 6 MUSHROOM MAGNETS'),
    ]
    stock_codes  = [p[0] for p in products]
    descriptions = [p[1] for p in products]
    dates = pd.date_range('2010-12-01', '2011-12-09', periods=n)
    idx   = np.random.randint(0, len(products), n)
    df = pd.DataFrame({
        'InvoiceNo':   [f'{500000+i//5}' for i in range(n)],
        'StockCode':   [stock_codes[i]  for i in idx],
        'Description': [descriptions[i] for i in idx],
        'Quantity':    np.random.randint(1, 50, n),
        'InvoiceDate': dates,
        'UnitPrice':   np.round(np.random.uniform(0.5, 15.0, n), 2),
        'CustomerID':  np.random.choice(
            [f'{i}' for i in range(12000,12500)] + [None]*200, n),
        'Country':     np.random.choice(
            countries, n,
            p=[0.85,0.04,0.03,0.02,0.02,0.01,0.01,0.01,0.005,0.005])
    })
    cancel_idx = np.random.choice(n, 300, replace=False)
    for i in cancel_idx:
        df.at[i,'InvoiceNo'] = 'C' + df.at[i,'InvoiceNo']
        df.at[i,'Quantity']  = -df.at[i,'Quantity']
    return df

@st.cache_data
def load_default():
    df = generate_sample_data()
    return clean_data(df)

def get_data():
    if 'uploaded_df' in st.session_state and \
       st.session_state.uploaded_df is not None:
        return st.session_state.uploaded_df
    return load_default()

def get_rfm(df):
    snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('CustomerID').agg(
        Recency   =('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
        Frequency =('InvoiceNo',   'nunique'),
        Monetary  =('Revenue',     'sum')
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