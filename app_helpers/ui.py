from __future__ import annotations

from html import escape
from typing import Iterable

import streamlit as st


SOCIAL_ICONS = {
    "email": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M3 6.75A1.75 1.75 0 0 1 4.75 5h14.5A1.75 1.75 0 0 1 21 6.75v10.5A1.75 1.75 0 0 1 19.25 19H4.75A1.75 1.75 0 0 1 3 17.25V6.75Zm1.8.17 7.2 5.4 7.2-5.4a.75.75 0 0 0-.45-.17H5.25a.75.75 0 0 0-.45.17Zm14.7 1.88-6.9 5.17a1 1 0 0 1-1.2 0L4.5 8.8v8.45c0 .41.34.75.75.75h13.5c.41 0 .75-.34.75-.75V8.8Z"/>
        </svg>
    """,
    "gmail": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M3 7.5 12 14l9-6.5v9.75A1.75 1.75 0 0 1 19.25 19h-2.5v-7.1L12 15.2 7.25 11.9V19h-2.5A1.75 1.75 0 0 1 3 17.25V7.5Z"/>
            <path d="M3.65 6.1A1.74 1.74 0 0 1 4.75 5h14.5c.45 0 .86.17 1.17.45L12 11.5 3.65 6.1Z"/>
        </svg>
    """,
    "github": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 .75a11.25 11.25 0 0 0-3.56 21.92c.56.1.77-.24.77-.54v-2.08c-3.14.68-3.8-1.33-3.8-1.33-.5-1.27-1.22-1.6-1.22-1.6-1-.68.07-.67.07-.67 1.11.08 1.69 1.13 1.69 1.13.98 1.68 2.58 1.2 3.21.91.1-.72.39-1.2.7-1.47-2.5-.29-5.12-1.25-5.12-5.56 0-1.23.44-2.24 1.16-3.03-.11-.29-.5-1.47.11-3.05 0 0 .95-.3 3.11 1.16a10.7 10.7 0 0 1 5.66 0c2.16-1.46 3.11-1.16 3.11-1.16.61 1.58.22 2.76.11 3.05.72.79 1.16 1.8 1.16 3.03 0 4.32-2.63 5.27-5.14 5.55.4.35.76 1.04.76 2.1v3.11c0 .3.2.65.78.54A11.25 11.25 0 0 0 12 .75Z"/>
        </svg>
    """,
    "linkedin": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M5.5 8.5A1.5 1.5 0 1 0 5.5 5.5a1.5 1.5 0 0 0 0 3ZM4.25 9.75h2.5V19h-2.5V9.75Zm4 0h2.4V11h.03c.33-.63 1.15-1.3 2.37-1.3 2.53 0 3 1.67 3 3.85V19h-2.5v-4.8c0-1.14-.02-2.6-1.58-2.6-1.58 0-1.82 1.23-1.82 2.52V19h-2.5V9.75Z"/>
        </svg>
    """,
    "calendar": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M7 2.75a.75.75 0 0 1 .75.75V5h8.5V3.5a.75.75 0 0 1 1.5 0V5h.5A2.75 2.75 0 0 1 21 7.75v11.5A2.75 2.75 0 0 1 18.25 22H5.75A2.75 2.75 0 0 1 3 19.25V7.75A2.75 2.75 0 0 1 5.75 5h.5V3.5A.75.75 0 0 1 7 2.75ZM4.5 9.5v9.75c0 .69.56 1.25 1.25 1.25h12.5c.69 0 1.25-.56 1.25-1.25V9.5h-15Zm1.25-3A1.25 1.25 0 0 0 4.5 7.75V8h15v-.25a1.25 1.25 0 0 0-1.25-1.25H5.75Z"/>
        </svg>
    """,
    "coffee": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M4 7.75A1.75 1.75 0 0 1 5.75 6h8.5A1.75 1.75 0 0 1 16 7.75v.25h1.25A2.75 2.75 0 0 1 20 10.75v.5A4.75 4.75 0 0 1 15.25 16H15A4 4 0 0 1 11 20H8a4 4 0 0 1-4-4V7.75Zm12 1.75v2.75c0 .78-.17 1.53-.48 2.2a3.25 3.25 0 0 0 2.98-3.2v-.5c0-.69-.56-1.25-1.25-1.25H16ZM5.5 16A2.5 2.5 0 0 0 8 18.5h3A2.5 2.5 0 0 0 13.5 16V7.75a.25.25 0 0 0-.25-.25h-7.5a.25.25 0 0 0-.25.25V16Zm5.8-13.54c.3-.4.87-.49 1.27-.19.4.3.49.87.19 1.27-.49.65-.55 1-.22 1.54.74 1.2.6 2.34-.31 3.41a.9.9 0 0 1-1.37-1.17c.42-.49.5-.87.15-1.45-.8-1.3-.65-2.51.29-3.41Zm-3 0c.3-.4.87-.49 1.27-.19.4.3.49.87.19 1.27-.49.65-.55 1-.22 1.54.74 1.2.6 2.34-.31 3.41A.9.9 0 0 1 7.86 7.3c.42-.49.5-.87.15-1.45-.8-1.3-.65-2.51.29-3.41Z"/>
        </svg>
    """,
}


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

            .icon-links {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                grid-auto-rows: 1fr;
                align-items: stretch;
                gap: 0.65rem;
                margin-top: 0.35rem;
                height: 100%;
            }}

            .icon-link {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.55rem;
                width: 100%;
                height: 100%;
                min-height: 4.4rem;
                padding: 0.9rem 1.2rem;
                border-radius: var(--radius-md);
                text-decoration: none;
                color: var(--text);
                background: rgba(255, 253, 248, 0.92);
                border: 1px solid var(--border);
                transition: transform 0.18s ease, border-color 0.18s ease, box-shadow 0.18s ease;
                font-weight: 600;
                box-sizing: border-box;
            }}

            .icon-link:hover {{
                transform: translateY(-1px);
                border-color: var(--primary);
                box-shadow: 0 16px 30px rgba(15, 118, 110, 0.12);
            }}

            .icon-link svg {{
                width: 1rem;
                height: 1rem;
                fill: currentColor;
                flex: 0 0 auto;
            }}

            .st-key-profile_intro_card,
            .st-key-profile_links_card,
            .st-key-profile_image_card {{
                height: 100%;
            }}

            .st-key-profile_intro_card [data-testid="stVerticalBlockBorderWrapper"],
            .st-key-profile_links_card [data-testid="stVerticalBlockBorderWrapper"],
            .st-key-profile_image_card [data-testid="stVerticalBlockBorderWrapper"] {{
                height: 100%;
            }}

            .st-key-profile_intro_card [data-testid="stVerticalBlock"],
            .st-key-profile_links_card [data-testid="stVerticalBlock"],
            .st-key-profile_image_card [data-testid="stVerticalBlock"] {{
                height: 100%;
            }}

            .st-key-profile_links_card [data-testid="stVerticalBlock"] {{
                justify-content: space-between;
            }}

            .st-key-profile_image_card [data-testid="stImage"] {{
                height: 100%;
            }}

            .st-key-profile_image_card img {{
                height: 100%;
                object-fit: cover;
                border-radius: calc(var(--radius-lg) - 4px);
            }}

            [class*="st-key-work_card_"] {{
                height: 100%;
            }}

            [class*="st-key-work_card_"] [data-testid="stVerticalBlockBorderWrapper"] {{
                height: 100%;
            }}

            [class*="st-key-work_card_"] [data-testid="stVerticalBlock"] {{
                height: 100%;
            }}

            .st-key-schedule_topics_card,
            .st-key-schedule_provider_card {{
                height: 100%;
            }}

            .st-key-schedule_topics_card [data-testid="stVerticalBlockBorderWrapper"],
            .st-key-schedule_provider_card [data-testid="stVerticalBlockBorderWrapper"] {{
                height: 100%;
            }}

            .st-key-schedule_topics_card [data-testid="stVerticalBlock"],
            .st-key-schedule_provider_card [data-testid="stVerticalBlock"] {{
                height: 100%;
            }}

            .st-key-schedule_provider_card [data-testid="stVerticalBlock"] {{
                justify-content: space-between;
            }}

            @media (max-width: 900px) {{
                .hero-panel {{
                    grid-template-columns: 1fr;
                    padding: 1.4rem;
                }}

                .icon-links {{
                    grid-template-columns: 1fr;
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


def render_icon_links(items: Iterable[dict[str, str]]) -> None:
    links = []
    for item in items:
        label = item.get("label", "").strip()
        url = item.get("url", "").strip()
        icon = SOCIAL_ICONS.get(item.get("icon", "").strip().lower(), SOCIAL_ICONS["email"])
        if not label or not url:
            continue
        links.append(
            f'<a class="icon-link" href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">'
            f"{icon}<span>{escape(label)}</span></a>"
        )

    if links:
        st.markdown(f'<div class="icon-links">{"".join(links)}</div>', unsafe_allow_html=True)
