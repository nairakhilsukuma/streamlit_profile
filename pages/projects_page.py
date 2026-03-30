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
            if project.get("stack"):
                render_tag_cloud(project["stack"])
            st.page_link(
                page_registry[f"project:{project['slug']}"],
                label=project.get("detail_label", "Open project page"),
                icon=":material/open_in_new:",
                use_container_width=True,
            )
            if project.get("github_url"):
                st.link_button("GitHub", project["github_url"], use_container_width=True)
            if project.get("demo_url"):
                st.link_button("Demo", project["demo_url"], use_container_width=True)

    st.page_link(
        page_registry["schedule"],
        label="Discuss a project or collaboration",
        icon=":material/event_available:",
        use_container_width=True,
    )
