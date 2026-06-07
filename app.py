import streamlit as st

from theme import apply_theme, render_navbar


st.set_page_config(
    page_title="Lumiq",
    page_icon="△",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_theme()

pages = {
    "Home": "pages/home.py",
    "Executive": "pages/kpi.py",
    "Sales": "pages/sales.py",
    "Customer Insights": "pages/customers.py",
    "Products": "pages/products.py",
}


page_names = list(pages.keys())
requested_page = st.query_params.get("page", "Home")
if requested_page not in pages:
    requested_page = "Home"

if st.session_state.get("selected_page") != requested_page:
    st.session_state["selected_page"] = requested_page


def update_page_query():
    st.query_params["page"] = st.session_state["selected_page"]


render_navbar()
selection = st.radio(
    "Navigation",
    page_names,
    index=page_names.index(requested_page),
    horizontal=True,
    label_visibility="collapsed",
    key="selected_page",
    on_change=update_page_query,
)

with open(pages[selection], encoding="utf-8") as page:
    exec(page.read())
