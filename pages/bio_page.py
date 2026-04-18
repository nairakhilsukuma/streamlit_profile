from __future__ import annotations

import streamlit as st

from app_helpers.ui import render_section_intro, render_tag_cloud


def render_bio_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    profile = settings["profile"]

    render_section_intro(
        "Bio",
        settings["navigation"]["bio_label"],
        profile.get("bio_page_intro", "A little more context on how I work and what I care about."),
    )

    content_columns = st.columns([1.3, 0.9])

    with content_columns[0]:
        with st.container(border=True):
            st.subheader("A bit more about me")
            for paragraph in profile.get("bio", []):
                st.write(paragraph)

    with content_columns[1]:
        with st.container(border=True):
            st.caption("Snapshot")
            st.markdown(f"### {profile.get('name', 'Your Name')}")
            st.write(profile.get("role", "Builder"))
            st.write(profile.get("location", "Remote friendly"))
            if profile.get("company"):
                st.write(profile["company"])
            if profile.get("signature_points"):
                st.caption("What I optimize for")
                render_tag_cloud(profile["signature_points"])

    footer_columns = st.columns(2)
    footer_columns[0].page_link(
        page_registry["home"],
        label=settings["navigation"]["home_label"],
        icon=":material/home:",
        use_container_width=True,
    )
    footer_columns[1].page_link(
        page_registry["projects"],
        label=settings["navigation"]["projects_label"],
        icon=":material/rocket_launch:",
        use_container_width=True,
    )
