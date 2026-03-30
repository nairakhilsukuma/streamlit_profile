from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from app_helpers.ui import render_section_intro


def render_schedule_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    calendar = settings["calendar"]
    render_section_intro(
        "Availability",
        settings["navigation"]["schedule_label"],
        calendar.get("description", "Book a conversation directly through my calendar."),
    )

    schedule_columns = st.columns([1.05, 1.35])
    with schedule_columns[0]:
        with st.container(border=True):
            st.subheader(calendar.get("title", "Reserve a meeting"))
            st.write(calendar.get("provider", "Google Calendar"))
            for topic in calendar.get("meeting_topics", []):
                st.write(f"- {topic}")
            st.write(
                calendar.get(
                    "privacy_note",
                    "Your booking is handled by the calendar provider, not stored in this app.",
                )
            )
            if calendar.get("booking_url"):
                st.link_button(
                    calendar.get("booking_label", "Open booking page"),
                    calendar["booking_url"],
                    use_container_width=True,
                )

    with schedule_columns[1]:
        embed_url = calendar.get("embed_url")
        if embed_url:
            components.iframe(embed_url, height=720, scrolling=True)
        else:
            with st.container(border=True):
                st.caption("Embed not configured")
                st.write("Add `calendar.embed_url` to `settings.yaml` if you want an inline calendar frame here.")

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
