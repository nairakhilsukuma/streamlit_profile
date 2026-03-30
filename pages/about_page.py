from __future__ import annotations
import streamlit as st
from app_helpers.ui import render_section_intro, render_tag_cloud


def render_about_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    profile = settings["profile"]

    render_section_intro(
        "Biography",
        settings["navigation"]["bio_label"],
        profile.get("bio_page_intro", profile.get("hero_summary", "")),
    )

    content_columns = st.columns([1.5, 1])
    with content_columns[0]:
        for paragraph in profile.get("bio", []):
            st.write(paragraph)

    with content_columns[1]:
        with st.container(border=True):
            st.caption("Snapshot")
            st.subheader(profile["name"])
            st.write(profile["role"])
            st.write(profile.get("location", "Remote friendly"))
            if profile.get("signature_points"):
                render_tag_cloud(profile["signature_points"])

    if profile.get("social_links"):
        render_section_intro("Links", "Where to find me", "The places where my work and writing are easiest to follow.")
        link_columns = st.columns(min(3, len(profile["social_links"])))
        for index, link in enumerate(profile["social_links"]):
            link_columns[index % len(link_columns)].link_button(
                link["label"], link["url"], use_container_width=True
            )

    nav_columns = st.columns(3)
    nav_columns[0].page_link(
        page_registry["work"],
        label=settings["navigation"]["work_label"],
        icon=":material/workspace_premium:",
        use_container_width=True,
    )
    nav_columns[1].page_link(
        page_registry["projects"],
        label=settings["navigation"]["projects_label"],
        icon=":material/rocket_launch:",
        use_container_width=True,
    )
    nav_columns[2].page_link(
        page_registry["schedule"],
        label=settings["navigation"]["schedule_label"],
        icon=":material/calendar_month:",
        use_container_width=True,
    )
