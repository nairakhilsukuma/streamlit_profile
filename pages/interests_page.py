from __future__ import annotations

import streamlit as st

from app_helpers.ui import render_section_intro


def render_interests_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    interests = settings["interests"]
    render_section_intro(
        "Interests",
        settings["navigation"]["interests_label"],
        interests.get("intro", ""),
    )

    columns = st.columns(2)
    for index, interest in enumerate(interests.get("items", [])):
        with columns[index % 2].container(border=True):
            st.subheader(interest["title"])
            st.write(interest["summary"])
            if interest.get("link_url"):
                st.link_button(
                    interest.get("link_label", "Explore"),
                    interest["link_url"],
                    use_container_width=True,
                )

    footer_columns = st.columns(2)
    footer_columns[0].page_link(
        page_registry["bio"],
        label=settings["navigation"]["bio_label"],
        icon=":material/person:",
        use_container_width=True,
    )
    footer_columns[1].page_link(
        page_registry["github"],
        label=settings["navigation"]["github_label"],
        icon=":material/code:",
        use_container_width=True,
    )
