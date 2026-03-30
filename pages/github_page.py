from __future__ import annotations

import streamlit as st

from app_helpers.ui import render_section_intro


def render_github_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    github = settings["github"]
    render_section_intro(
        "Code",
        settings["navigation"]["github_label"],
        github.get(
            "headline",
            "A quick gateway into the repositories, experiments, and shipping work behind this profile.",
        ),
    )

    if github.get("profile_url"):
        st.link_button(
            github.get("profile_label", "Open GitHub profile"),
            github["profile_url"],
            use_container_width=True,
        )

    repositories = github.get("repositories", [])
    columns = st.columns(2)
    for index, repository in enumerate(repositories):
        with columns[index % 2].container(border=True):
            st.subheader(repository["name"])
            st.write(repository["description"])
            st.link_button(
                repository.get("button_label", "Visit repository"),
                repository["url"],
                use_container_width=True,
            )

    action_columns = st.columns(2)
    action_columns[0].page_link(
        page_registry["projects"],
        label=settings["navigation"]["projects_label"],
        icon=":material/rocket_launch:",
        use_container_width=True,
    )
    action_columns[1].page_link(
        page_registry["schedule"],
        label="Book time to talk code",
        icon=":material/event_available:",
        use_container_width=True,
    )
