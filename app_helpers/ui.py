from __future__ import annotations

from html import escape
from typing import Iterable

import streamlit as st


def inject_theme(theme: dict) -> None:
    theme_root = theme.get("theme", {})
    colors = theme_root.get("colors", {})
    fonts = theme_root.get("fonts", {})
    radii = theme_root.get("radii", {})

    display_font = fonts.get("display", "Fraunces")
    body_font = fonts.get("body", "Space Grotesk")

    st.markdown(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

            :root {{
                --app-bg: {colors.get("background", "#F7F3EA")};
                --surface: {colors.get("surface", "#FFFDF8")};
                --surface-alt: {colors.get("surface_alt", "#F3EEE2")};
                --text: {colors.get("text", "#14213D")};
                --muted: {colors.get("muted", "#52616B")};
                --border: {colors.get("border", "#D9CDBA")};
                --primary: {colors.get("primary", "#0F766E")};
                --primary-soft: {colors.get("primary_soft", "#D9F2EE")};
                --accent: {colors.get("accent", "#D97706")};
                --hero-from: {colors.get("hero_from", "#0F766E")};
                --hero-to: {colors.get("hero_to", "#D97706")};
                --radius-xl: {radii.get("xl", "28px")};
                --radius-lg: {radii.get("lg", "22px")};
                --radius-md: {radii.get("md", "16px")};
            }}

            .stApp {{
                background:
                    radial-gradient(circle at top left, rgba(217, 119, 6, 0.14), transparent 28%),
                    radial-gradient(circle at top right, rgba(15, 118, 110, 0.18), transparent 26%),
                    var(--app-bg);
                color: var(--text);
            }}

            [data-testid="stAppViewContainer"] {{
                background: transparent;
            }}

            [data-testid="stHeader"] {{
                background: rgba(247, 243, 234, 0.72);
                backdrop-filter: blur(14px);
            }}

            html, body, [class*="css"] {{
                font-family: '{body_font}', sans-serif;
            }}

            h1, h2, h3 {{
                font-family: '{display_font}', serif;
                letter-spacing: -0.03em;
            }}

            .hero-panel {{
                display: grid;
                grid-template-columns: minmax(0, 1.8fr) minmax(280px, 1fr);
                gap: 1.25rem;
                padding: 2rem;
                border-radius: var(--radius-xl);
                color: white;
                background:
                    linear-gradient(135deg, rgba(255,255,255,0.16), rgba(255,255,255,0.02)),
                    linear-gradient(135deg, var(--hero-from), var(--hero-to));
                box-shadow: 0 28px 80px rgba(20, 33, 61, 0.18);
                margin: 0.4rem 0 1.4rem 0;
            }}

            .hero-panel h1 {{
                margin: 0.35rem 0 0;
                font-size: clamp(2.3rem, 5vw, 4.6rem);
                line-height: 0.96;
            }}

            .hero-summary {{
                max-width: 42rem;
                font-size: 1.05rem;
                line-height: 1.7;
                color: rgba(255, 255, 255, 0.92);
                margin-top: 1rem;
            }}

            .eyebrow {{
                margin: 0;
                text-transform: uppercase;
                letter-spacing: 0.18em;
                font-size: 0.78rem;
                font-weight: 700;
                opacity: 0.8;
            }}

            .hero-meta {{
                display: grid;
                gap: 0.85rem;
            }}

            .meta-card {{
                background: rgba(255,255,255,0.12);
                border: 1px solid rgba(255,255,255,0.16);
                border-radius: var(--radius-lg);
                padding: 1rem 1.1rem;
                backdrop-filter: blur(8px);
            }}

            .meta-label {{
                display: block;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.14em;
                opacity: 0.72;
                margin-bottom: 0.35rem;
            }}

            .section-intro {{
                margin: 1.6rem 0 0.65rem 0;
            }}

            .section-intro h2 {{
                margin: 0.2rem 0 0;
                font-size: clamp(1.7rem, 3vw, 2.6rem);
            }}

            .section-intro p {{
                max-width: 42rem;
                color: var(--muted);
                margin: 0.55rem 0 0;
                line-height: 1.7;
            }}

            .tag-cloud {{
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                margin-top: 0.45rem;
            }}

            .tag-pill {{
                display: inline-flex;
                align-items: center;
                gap: 0.25rem;
                padding: 0.42rem 0.8rem;
                border-radius: 999px;
                background: var(--primary-soft);
                border: 1px solid rgba(15, 118, 110, 0.12);
                color: var(--primary);
                font-size: 0.87rem;
                font-weight: 700;
            }}

            div[data-testid="stMetric"] {{
                background: rgba(255, 253, 248, 0.86);
                border: 1px solid var(--border);
                border-radius: var(--radius-lg);
                padding: 0.4rem 0.75rem;
            }}

            @media (max-width: 900px) {{
                .hero-panel {{
                    grid-template-columns: 1fr;
                    padding: 1.4rem;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_section_intro(eyebrow: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="section-intro">
            <p class="eyebrow">{escape(eyebrow)}</p>
            <h2>{escape(title)}</h2>
            <p>{escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_tag_cloud(items: Iterable[str]) -> None:
    tags = "".join(f'<span class="tag-pill">{escape(item)}</span>' for item in items)
    st.markdown(f'<div class="tag-cloud">{tags}</div>', unsafe_allow_html=True)
