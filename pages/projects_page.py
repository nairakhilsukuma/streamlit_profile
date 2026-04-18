from __future__ import annotations

import streamlit as st

from app_helpers.ui import render_section_intro, render_tag_cloud


def render_projects_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    render_section_intro(
        "Projects",
        settings["navigation"]["projects_label"],
        settings.get("projects_intro", ""),
    )

    projects = settings["projects"]
    columns = st.columns(2)
    for index, project in enumerate(projects):
        with columns[index % 2].container(border=True):
            st.caption(project.get("status", "In progress"))
            st.subheader(project["name"])
            st.write(project["summary"])
            for paragraph in project.get("description", []):
                st.write(paragraph)
            if project.get("outcomes"):
                st.caption("Outcomes")
                for outcome in project["outcomes"]:
                    st.write(f"- {outcome}")
            if project.get("stack"):
                render_tag_cloud(project["stack"])
            if project.get("github_url"):
                st.link_button("GitHub", project["github_url"], use_container_width=True)
            if project.get("demo_url"):
                st.link_button("Demo", project["demo_url"], use_container_width=True)

    st.page_link(
        page_registry["home"],
        label=f"Back to {settings['navigation']['home_label']}",
        icon=":material/arrow_back:",
        use_container_width=True,
    )
