from __future__ import annotations

import streamlit as st

from app_helpers.ui import render_section_intro, render_tag_cloud


def render_work_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    render_section_intro(
        "Work areas",
        settings["navigation"]["work_label"],
        settings["work_intro"],
    )

    work_areas = settings["work_areas"]
    columns = st.columns(2)
    for index, work_area in enumerate(work_areas):
        with columns[index % 2].container(border=True):
            st.caption(work_area.get("eyebrow", "Area"))
            st.subheader(work_area["title"])
            st.write(work_area["summary"])
            if work_area.get("highlight"):
                st.info(work_area["highlight"])
            if work_area.get("focus_tags"):
                render_tag_cloud(work_area["focus_tags"])

    call_to_action = st.columns(2)
    call_to_action[0].page_link(
        page_registry["projects"],
        label="Browse active projects",
        icon=":material/arrow_forward:",
        use_container_width=True,
    )
    call_to_action[1].page_link(
        page_registry["schedule"],
        label="Talk through an idea",
        icon=":material/event_available:",
        use_container_width=True,
    )
