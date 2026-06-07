from pathlib import Path
from textwrap import dedent

import streamlit as st


THEME_DIR = Path(__file__).parent / "assets"
THEME_CSS = THEME_DIR / "theme.css"
COLORS = {
    "navy": "#1F3B60",
    "navy_dark": "#183152",
    "teal": "#78C6D6",
    "background": "#EEF3F6",
    "card": "#FFFFFF",
    "text": "#182232",
    "muted": "#667085",
    "grid": "#E5EDF2",
    "pink": "#D84B83",
    "green": "#22B573",
    "red": "#D66565",
    "amber": "#D9A441",
}
TEAL_NAVY_SCALE = [[0, COLORS["teal"]], [1, COLORS["navy"]]]


def apply_plotly_theme(fig, height=None, top_margin=56):
    top_margin = max(top_margin, 56)
    layout = {
        "plot_bgcolor": COLORS["card"],
        "paper_bgcolor": COLORS["card"],
        "font": {"color": COLORS["text"]},
        "title": {
            "font": {"color": COLORS["text"], "size": 16},
            "x": 0,
            "xanchor": "left",
            "y": 0.96,
            "yanchor": "top",
            "pad": {"t": 12, "b": 18},
        },
        "margin": {"l": 0, "r": 0, "t": top_margin, "b": 0},
        "modebar": {"orientation": "h"},
    }
    if height:
        layout["height"] = height
    fig.update_layout(**layout)
    fig.update_xaxes(gridcolor=COLORS["grid"], automargin=True, tickfont={"size": 11})
    fig.update_yaxes(gridcolor=COLORS["grid"], automargin=True, tickfont={"size": 11})
    return fig


def apply_theme():
    css = THEME_CSS.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_navbar():
    st.markdown(
        """
        <div class="top-nav">
            <div class="brand-row">
                <a class="brand-link" href="?page=Home" target="_self" aria-label="Go to Lumiq home">
                    <div class="logo-mark"></div>
                    <div>
                        <div class="brand-title">LUMIQ</div>
                        <div class="brand-subtitle">Retail BI Command Center</div>
                    </div>
                </a>
                <div class="brand-meta">AJ</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_title(title, subtitle=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-kicker">{subtitle}</div>', unsafe_allow_html=True)


def content_card(body):
    st.markdown(
        f"""
        <div class="content-card">
            {dedent(body).strip()}
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_grid_markup(items):
    cards = "\n".join(
        f'<div class="feature-pill">{title}<br><span>{description}</span></div>'
        for title, description in items
    )
    return f'<div class="feature-grid">{cards}</div>'


def feature_grid(items):
    st.markdown(feature_grid_markup(items), unsafe_allow_html=True)


def pipeline_card(number, label):
    st.markdown(
        f"""
        <div class="pipeline-card">
            <div class="pipeline-num">{number}</div>
            <div class="pipeline-label">{label.replace(chr(10), '<br>')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
