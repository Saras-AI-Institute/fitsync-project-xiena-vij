import streamlit as st
from modules.theme import apply_theme, page_banner

st.set_page_config(layout="wide", page_title="FitSync", page_icon="💪")

theme = apply_theme("main")
T = theme

gradient = "linear-gradient(135deg, #1f3a5f 0%, #0d2137 60%, #0d1117 100%)" if T["is_dark"] else "linear-gradient(135deg, #dbeafe 0%, #eff6ff 60%, #f0f2f6 100%)"

page_banner(
    "💪 Welcome to FitSync",
    "Your personal health analytics dashboard — track, analyze, and improve.",
    gradient, T
)

# Feature cards
cards = [
    ("📊", "Dashboard", "Daily steps, sleep, recovery & calories in one place.", "#58a6ff", "/Dashboard"),
    ("📈", "Trends", "Monthly patterns and distribution of your health metrics.", "#3fb950", "/Trends"),
    ("🎯", "Goal Tracking", "Monitor progress and stay on top of your fitness goals.", "#d2a8ff", None),
]

cols = st.columns(3)
for col, (emoji, title, desc, color, _) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div style="
            background-color: {T['card_bg']};
            border: 1px solid {T['border']};
            border-radius: 16px;
            padding: 28px 24px;
            box-shadow: {T['shadow']};
            border-top: 4px solid {color};
            min-height: 180px;
            transition: transform 0.2s;
        ">
            <div style="font-size: 38px; margin-bottom: 12px;">{emoji}</div>
            <div style="font-size: 18px; font-weight: 700; color: {color} !important; margin-bottom: 8px;">{title}</div>
            <div style="font-size: 13px; color: {T['subtext']} !important; line-height: 1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# How to use
st.markdown(f"""
<div style="
    background-color: {T['card_bg']};
    border: 1px solid {T['border']};
    border-radius: 16px;
    padding: 28px 32px;
    box-shadow: {T['shadow']};
">
    <div style="font-size: 20px; font-weight: 700; margin-bottom: 20px;">🧭 How to use FitSync</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
        <div style="
            background: {T['bg']};
            border-radius: 10px;
            padding: 14px 18px;
            border: 1px solid {T['border']};
            font-size: 14px;
            color: {T['subtext']} !important;
        ">👈 Use the <b style="color:{T['text']} !important;">sidebar</b> to navigate between pages</div>
        <div style="
            background: {T['bg']};
            border-radius: 10px;
            padding: 14px 18px;
            border: 1px solid {T['border']};
            font-size: 14px;
            color: {T['subtext']} !important;
        ">🔍 <b style="color:{T['text']} !important;">Filter</b> data by time range on each page</div>
        <div style="
            background: {T['bg']};
            border-radius: 10px;
            padding: 14px 18px;
            border: 1px solid {T['border']};
            font-size: 14px;
            color: {T['subtext']} !important;
        ">☀️🌙 <b style="color:{T['text']} !important;">Toggle</b> light/dark mode via top-right button</div>
        <div style="
            background: {T['bg']};
            border-radius: 10px;
            padding: 14px 18px;
            border: 1px solid {T['border']};
            font-size: 14px;
            color: {T['subtext']} !important;
        ">📊 <b style="color:{T['text']} !important;">Hover</b> over charts for detailed values</div>
    </div>
</div>
""", unsafe_allow_html=True)