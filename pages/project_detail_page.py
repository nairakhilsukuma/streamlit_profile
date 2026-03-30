from __future__ import annotations

from functools import partial

import streamlit as st

from app_helpers.ui import render_section_intro, render_tag_cloud


def make_project_page(settings: dict, project: dict, page_registry: dict[str, st.Page]):
    return partial(render_project_page, settings, project, page_registry)


def render_project_page(settings: dict, project: dict, page_registry: dict[str, st.Page]) -> None:
    render_section_intro(
        project.get("status", "Project"),
        project["name"],
        project["summary"],
    )

    overview_columns = st.columns([1.3, 1])
    with overview_columns[0]:
        for paragraph in project.get("description", []):
            st.write(paragraph)
        if project.get("outcomes"):
            st.caption("What this project is aiming for")
            for outcome in project["outcomes"]:
                st.write(f"- {outcome}")

    with overview_columns[1]:
        with st.container(border=True):
            st.caption("Project details")
            if project.get("stack"):
                render_tag_cloud(project["stack"])
            if project.get("github_url"):
                st.link_button("GitHub repository", project["github_url"], use_container_width=True)
            if project.get("demo_url"):
                st.link_button("Live demo", project["demo_url"], use_container_width=True)

    footer_columns = st.columns(3)
    footer_columns[0].page_link(
        page_registry["projects"],
        label=settings["navigation"]["projects_label"],
        icon=":material/arrow_back:",
        use_container_width=True,
    )
    footer_columns[1].page_link(
        page_registry["github"],
        label=settings["navigation"]["github_label"],
        icon=":material/code:",
        use_container_width=True,
    )
    footer_columns[2].page_link(
        page_registry["schedule"],
        label="Schedule a conversation",
        icon=":material/calendar_month:",
        use_container_width=True,
    )
