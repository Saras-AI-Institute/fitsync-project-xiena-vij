import streamlit as st

def apply_theme(page_key="default"):
    if "theme" not in st.session_state:
        st.session_state["theme"] = "dark"

    is_dark = st.session_state["theme"] == "dark"

    # Colors
    bg         = "#0d1117" if is_dark else "#f0f2f6"
    card_bg    = "#161b22" if is_dark else "#ffffff"
    sidebar_bg = "#161b22" if is_dark else "#ffffff"
    text       = "#e6edf3" if is_dark else "#1a1a2e"
    subtext    = "#8b949e" if is_dark else "#6b7280"
    accent     = "#58a6ff" if is_dark else "#1f6feb"
    border     = "#30363d" if is_dark else "#e5e7eb"
    plot_bg    = "#161b22" if is_dark else "#ffffff"
    plot_paper = "#0d1117" if is_dark else "#f0f2f6"
    plot_font  = "#e6edf3" if is_dark else "#1a1a2e"
    grid_color = "#21262d" if is_dark else "#f3f4f6"
    shadow     = "0 4px 24px rgba(0,0,0,0.4)" if is_dark else "0 4px 24px rgba(0,0,0,0.08)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    *, html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif !important;
        box-sizing: border-box;
    }}

    /* Main background */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: {bg} !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background-color: {bg} !important;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {border} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {text} !important;
    }}
    [data-testid="stSidebar"] .stSelectbox > div > div {{
        background-color: {bg} !important;
        border: 1px solid {border} !important;
        color: {text} !important;
        border-radius: 8px !important;
    }}

    /* All text */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li {{
        color: {text} !important;
    }}

    /* Remove default padding */
    .block-container {{
        padding: 2rem 2rem 2rem 2rem !important;
        max-width: 1300px !important;
    }}

    /* Toggle button — fixed top right */
    [data-testid="stAppViewContainer"] > .main > div > div:first-child {{
        position: sticky;
        top: 0;
        z-index: 999;
    }}
    .stButton > button {{
        border-radius: 50px !important;
        border: 1.5px solid {border} !important;
        background: {card_bg} !important;
        color: {text} !important;
        font-size: 20px !important;
        width: 48px !important;
        height: 48px !important;
        padding: 0 !important;
        box-shadow: {shadow} !important;
        transition: all 0.2s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .stButton > button:hover {{
        border-color: {accent} !important;
        transform: scale(1.1) !important;
        background: {accent}22 !important;
    }}

    /* Selectbox */
    .stSelectbox > div > div {{
        background-color: {card_bg} !important;
        border: 1px solid {border} !important;
        color: {text} !important;
        border-radius: 10px !important;
    }}

    /* Dataframe */
    [data-testid="stDataFrame"] > div {{
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid {border} !important;
    }}

    /* Divider */
    hr {{
        border-color: {border} !important;
        margin: 1.5rem 0 !important;
    }}

    /* Plotly charts */
    .js-plotly-plot {{
        border-radius: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Theme toggle — always top right
    col_spacer, col_btn = st.columns([11, 1])
    with col_btn:
        label = "☀️" if is_dark else "🌙"
        if st.button(label, key=f"theme_btn_{page_key}"):
            st.session_state["theme"] = "light" if is_dark else "dark"
            st.rerun()

    return {
        "is_dark": is_dark, "bg": bg, "card_bg": card_bg,
        "text": text, "subtext": subtext, "accent": accent,
        "border": border, "shadow": shadow,
        "plot_bg": plot_bg, "plot_paper": plot_paper,
        "plot_font": plot_font, "grid_color": grid_color
    }


def style_fig(fig, theme):
    fig.update_layout(
        plot_bgcolor=theme["plot_bg"],
        paper_bgcolor=theme["plot_bg"],
        font=dict(color=theme["plot_font"], family="Inter", size=12),
        title_font=dict(size=14, color=theme["plot_font"], family="Inter"),
        margin=dict(l=16, r=16, t=48, b=16),
        legend=dict(
            bgcolor=theme["card_bg"],
            bordercolor=theme["border"],
            borderwidth=1,
            font=dict(color=theme["plot_font"])
        ),
        xaxis=dict(
            gridcolor=theme["grid_color"],
            linecolor=theme["border"],
            zerolinecolor=theme["grid_color"],
            tickfont=dict(color=theme["plot_font"]),
            title_font=dict(color=theme["plot_font"])
        ),
        yaxis=dict(
            gridcolor=theme["grid_color"],
            linecolor=theme["border"],
            zerolinecolor=theme["grid_color"],
            tickfont=dict(color=theme["plot_font"]),
            title_font=dict(color=theme["plot_font"])
        )
    )
    return fig


def metric_card(label, value, emoji, accent_color, theme, delta=None):
    delta_html = ""
    if delta:
        color = "#3fb950" if delta.startswith("+") else "#f78166"
        delta_html = f'<div style="font-size:12px; color:{color}; font-weight:600; margin-top:4px;">{delta}</div>'

    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, {theme['card_bg']}, {theme['card_bg']}ee);
        border: 1px solid {theme['border']};
        border-radius: 16px;
        padding: 20px 16px;
        text-align: center;
        box-shadow: {theme['shadow']};
        border-top: 3px solid {accent_color};
        min-height: 130px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 4px;
    ">
        <div style="font-size: 30px; line-height: 1;">{emoji}</div>
        <div style="font-size: 24px; font-weight: 800; color: {accent_color} !important; line-height: 1.2; margin-top: 6px;">{value}</div>
        <div style="font-size: 12px; color: {theme['subtext']} !important; font-weight: 500; margin-top: 2px;">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def section_header(title, theme):
    st.markdown(f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 28px 0 16px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid {theme['border']};
    ">
        <span style="font-size: 22px; font-weight: 700; color: {theme['text']} !important;">{title}</span>
    </div>
    """, unsafe_allow_html=True)


def page_banner(title, subtitle, gradient, theme):
    st.markdown(f"""
    <div style="
        background: {gradient};
        border: 1px solid {theme['border']};
        border-radius: 20px;
        padding: 32px 40px;
        margin-bottom: 28px;
        box-shadow: {theme['shadow']};
    ">
        <div style="font-size: 30px; font-weight: 800; color: {theme['text']} !important; margin: 0; line-height: 1.2;">{title}</div>
        <div style="font-size: 15px; color: {theme['subtext']} !important; margin-top: 8px; font-weight: 400;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)