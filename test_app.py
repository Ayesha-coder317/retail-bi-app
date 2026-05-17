# test_app.py
# Automated Test Cases for Retail BI Web Application
# Run with: python -m pytest test_app.py -v

import pytest
import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from data_loader import generate_sample_data, clean_data, get_rfm

# ─── FIXTURES ────────────────────────────────────────────────────────────────

@pytest.fixture
def raw_df():
    """Generate raw sample dataset before cleaning"""
    return generate_sample_data()

@pytest.fixture
def clean_df():
    """Generate fully cleaned dataset"""
    df = generate_sample_data()
    return clean_data(df)

@pytest.fixture
def rfm_df(clean_df):
    """Generate RFM table from cleaned dataset"""
    return get_rfm(clean_df)

# ─── TEST 1: DATA GENERATION ─────────────────────────────────────────────────

class TestDataGeneration:

    def test_raw_data_has_records(self, raw_df):
        """TC01 — Raw dataset should contain records"""
        assert len(raw_df) > 0, "Dataset should not be empty"

    def test_raw_data_has_correct_columns(self, raw_df):
        """TC02 — Raw dataset should have all required columns"""
        required = ['InvoiceNo', 'StockCode', 'Description',
                    'Quantity', 'InvoiceDate', 'UnitPrice',
                    'CustomerID', 'Country']
        for col in required:
            assert col in raw_df.columns, f"Missing column: {col}"

    def test_raw_data_contains_cancellations(self, raw_df):
        """TC03 — Raw dataset should contain some cancelled invoices"""
        cancelled = raw_df['InvoiceNo'].astype(str).str.startswith('C')
        assert cancelled.sum() > 0, "Raw data should have cancellations"

    def test_raw_data_contains_negative_quantities(self, raw_df):
        """TC04 — Raw dataset should contain some negative quantities"""
        assert (raw_df['Quantity'] < 0).sum() > 0, \
            "Raw data should have negative quantities"

# ─── TEST 2: DATA CLEANING ────────────────────────────────────────────────────

class TestDataCleaning:

    def test_no_cancelled_invoices(self, clean_df):
        """TC05 — Cleaned data should have zero cancelled invoices"""
        cancelled = clean_df['InvoiceNo'].astype(str).str.startswith('C')
        assert cancelled.sum() == 0, "No cancelled invoices should remain"

    def test_no_negative_quantities(self, clean_df):
        """TC06 — All quantities should be positive after cleaning"""
        assert (clean_df['Quantity'] <= 0).sum() == 0, \
            "No negative or zero quantities should remain"

    def test_no_negative_prices(self, clean_df):
        """TC07 — All unit prices should be positive after cleaning"""
        assert (clean_df['UnitPrice'] <= 0).sum() == 0, \
            "No negative or zero prices should remain"

    def test_no_missing_customer_ids(self, clean_df):
        """TC08 — No missing CustomerIDs should remain after cleaning"""
        assert clean_df['CustomerID'].isnull().sum() == 0, \
            "No null CustomerIDs should remain"

    def test_revenue_column_exists(self, clean_df):
        """TC09 — Revenue column should be created during cleaning"""
        assert 'Revenue' in clean_df.columns, \
            "Revenue column should exist after cleaning"

    def test_revenue_calculation_correct(self, clean_df):
        """TC10 — Revenue should equal Quantity x UnitPrice"""
        expected = clean_df['Quantity'] * clean_df['UnitPrice']
        diff = (clean_df['Revenue'] - expected).abs()
        assert diff.max() < 0.01, "Revenue calculation is incorrect"

    def test_revenue_all_positive(self, clean_df):
        """TC11 — All revenue values should be positive"""
        assert (clean_df['Revenue'] <= 0).sum() == 0, \
            "All revenue values should be positive"

    def test_invoice_date_is_datetime(self, clean_df):
        """TC12 — InvoiceDate should be datetime type after cleaning"""
        assert pd.api.types.is_datetime64_any_dtype(clean_df['InvoiceDate']), \
            "InvoiceDate should be datetime"

    def test_month_column_exists(self, clean_df):
        """TC13 — Month column should be created during cleaning"""
        assert 'Month' in clean_df.columns, \
            "Month column should exist"

    def test_monthstr_column_exists(self, clean_df):
        """TC14 — MonthStr column should be created during cleaning"""
        assert 'MonthStr' in clean_df.columns, \
            "MonthStr column should exist"

    def test_year_column_exists(self, clean_df):
        """TC15 — Year column should be created during cleaning"""
        assert 'Year' in clean_df.columns, \
            "Year column should exist"

    def test_cleaning_reduces_records(self, raw_df, clean_df):
        """TC16 — Cleaning should reduce record count"""
        assert len(clean_df) < len(raw_df), \
            "Cleaned dataset should have fewer records than raw"

    def test_cleaned_data_not_empty(self, clean_df):
        """TC17 — Cleaned dataset should not be empty"""
        assert len(clean_df) > 0, \
            "Cleaned dataset should not be empty"

# ─── TEST 3: KPI CALCULATIONS ────────────────────────────────────────────────

class TestKPICalculations:

    def test_total_revenue_positive(self, clean_df):
        """TC18 — Total revenue should be positive"""
        total = clean_df['Revenue'].sum()
        assert total > 0, "Total revenue should be positive"

    def test_total_orders_positive(self, clean_df):
        """TC19 — Total orders count should be positive"""
        orders = clean_df['InvoiceNo'].nunique()
        assert orders > 0, "Total orders should be positive"

    def test_total_customers_positive(self, clean_df):
        """TC20 — Total customers count should be positive"""
        customers = clean_df['CustomerID'].nunique()
        assert customers > 0, "Total customers should be positive"

    def test_avg_order_value_positive(self, clean_df):
        """TC21 — Average order value should be positive"""
        aov = clean_df['Revenue'].sum() / clean_df['InvoiceNo'].nunique()
        assert aov > 0, "Average order value should be positive"

    def test_top_country_exists(self, clean_df):
        """TC22 — Top country by revenue should be identifiable"""
        top = clean_df.groupby('Country')['Revenue'].sum().idxmax()
        assert isinstance(top, str), "Top country should be a string"
        assert len(top) > 0, "Top country should not be empty"

    def test_top_product_exists(self, clean_df):
        """TC23 — Top product by revenue should be identifiable"""
        top = clean_df.groupby('Description')['Revenue'].sum().idxmax()
        assert isinstance(top, str), "Top product should be a string"
        assert len(top) > 0, "Top product should not be empty"

    def test_monthly_revenue_grouping(self, clean_df):
        """TC24 — Monthly revenue grouping should produce results"""
        monthly = clean_df.groupby('MonthStr')['Revenue'].sum()
        assert len(monthly) > 0, "Monthly grouping should have results"
        assert (monthly > 0).all(), "All monthly revenues should be positive"

    def test_country_revenue_grouping(self, clean_df):
        """TC25 — Country revenue grouping should produce results"""
        country = clean_df.groupby('Country')['Revenue'].sum()
        assert len(country) > 0, "Country grouping should have results"

    def test_product_revenue_grouping(self, clean_df):
        """TC26 — Product revenue grouping should produce results"""
        products = clean_df.groupby('Description')['Revenue'].sum()
        assert len(products) > 0, "Product grouping should have results"

# ─── TEST 4: RFM SEGMENTATION ────────────────────────────────────────────────

class TestRFMSegmentation:

    def test_rfm_has_correct_columns(self, rfm_df):
        """TC27 — RFM table should have all required columns"""
        required = ['CustomerID', 'Recency', 'Frequency',
                    'Monetary', 'R_Score', 'F_Score',
                    'M_Score', 'RFM_Score', 'Segment']
        for col in required:
            assert col in rfm_df.columns, f"Missing RFM column: {col}"

    def test_rfm_no_duplicate_customers(self, rfm_df):
        """TC28 — Each customer should appear once in RFM table"""
        assert rfm_df['CustomerID'].nunique() == len(rfm_df), \
            "Duplicate customers found in RFM table"

    def test_rfm_recency_positive(self, rfm_df):
        """TC29 — All recency values should be positive"""
        assert (rfm_df['Recency'] >= 0).all(), \
            "All recency values should be non-negative"

    def test_rfm_frequency_positive(self, rfm_df):
        """TC30 — All frequency values should be positive"""
        assert (rfm_df['Frequency'] > 0).all(), \
            "All frequency values should be positive"

    def test_rfm_monetary_positive(self, rfm_df):
        """TC31 — All monetary values should be positive"""
        assert (rfm_df['Monetary'] > 0).all(), \
            "All monetary values should be positive"

    def test_rfm_scores_in_range(self, rfm_df):
        """TC32 — RFM scores should be between 1 and 4"""
        for col in ['R_Score', 'F_Score', 'M_Score']:
            assert rfm_df[col].between(1, 4).all(), \
                f"{col} values should be between 1 and 4"

    def test_rfm_total_score_in_range(self, rfm_df):
        """TC33 — Total RFM score should be between 3 and 12"""
        assert rfm_df['RFM_Score'].between(3, 12).all(), \
            "RFM total score should be between 3 and 12"

    def test_rfm_segments_valid(self, rfm_df):
        """TC34 — All segments should be valid labels"""
        valid = {'Champions', 'Loyal Customers',
                 'Potential Loyalists', 'At Risk', 'Lost'}
        actual = set(rfm_df['Segment'].unique())
        assert actual.issubset(valid), \
            f"Invalid segments found: {actual - valid}"

    def test_champions_have_high_scores(self, rfm_df):
        """TC35 — Champions should all have RFM score >= 10"""
        champions = rfm_df[rfm_df['Segment'] == 'Champions']
        if len(champions) > 0:
            assert (champions['RFM_Score'] >= 10).all(), \
                "All Champions should have score >= 10"

    def test_at_risk_have_low_scores(self, rfm_df):
        """TC36 — At Risk customers should have RFM score <= 4"""
        at_risk = rfm_df[rfm_df['Segment'] == 'At Risk']
        if len(at_risk) > 0:
            assert (at_risk['RFM_Score'] <= 4).all(), \
                "At Risk customers should have score <= 4"

    def test_rfm_not_empty(self, rfm_df):
        """TC37 — RFM table should not be empty"""
        assert len(rfm_df) > 0, "RFM table should not be empty"

# ─── TEST 5: DATA INTEGRITY ───────────────────────────────────────────────────

class TestDataIntegrity:

    def test_year_values_valid(self, clean_df):
        """TC38 — Year values should be within dataset period"""
        assert clean_df['Year'].between(2010, 2011).all(), \
            "Year values should be 2010 or 2011"

    def test_countries_not_empty(self, clean_df):
        """TC39 — Country field should not have empty values"""
        assert clean_df['Country'].isnull().sum() == 0, \
            "Country field should have no null values"

    def test_multiple_countries_exist(self, clean_df):
        """TC40 — Dataset should contain multiple countries"""
        assert clean_df['Country'].nunique() > 1, \
            "Dataset should have more than one country"

    def test_multiple_products_exist(self, clean_df):
        """TC41 — Dataset should contain multiple products"""
        assert clean_df['StockCode'].nunique() > 1, \
            "Dataset should have more than one product"

    def test_revenue_sum_matches_components(self, clean_df):
        """TC42 — Total revenue should match sum of all line revenues"""
        total = clean_df['Revenue'].sum()
        components = (clean_df['Quantity'] * clean_df['UnitPrice']).sum()
        assert abs(total - components) < 0.01, \
            "Total revenue should match sum of components"

    def test_no_future_dates(self, clean_df):
        """TC43 — No invoice dates should be in the future"""
        max_date = pd.Timestamp('2012-01-01')
        assert (clean_df['InvoiceDate'] < max_date).all(), \
            "No dates should be after 2012"

    def test_monthstr_format(self, clean_df):
        """TC44 — MonthStr should follow MMM YYYY format"""
        import re
        pattern = r'^[A-Z][a-z]{2} \d{4}$'
        sample = clean_df['MonthStr'].iloc[0]
        assert re.match(pattern, sample), \
            f"MonthStr format incorrect: {sample}"