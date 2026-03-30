
from __future__ import annotations
from functools import partial
from pathlib import Path
import streamlit as st
from app_helpers.settings import load_settings_file
from app_helpers.ui import inject_theme, render_section_intro, render_tag_cloud
from pages.about_page import render_about_page
from pages.github_page import render_github_page
from pages.interests_page import render_interests_page
from pages.project_detail_page import make_project_page
from pages.projects_page import render_projects_page
from pages.schedule_page import render_schedule_page
from pages.work_page import render_work_page


def render_landing_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    profile = settings["profile"]
    work_areas = settings["work_areas"]
    interests = settings["interests"].get("items", [])
    projects = settings["projects"]
    calendar = settings["calendar"]

    photo_source = resolve_photo_source(profile)
    if photo_source:
        profile_columns = st.columns([1.4, 0.7, 0.35])

        with profile_columns[0]:
            with st.container(border=True):
                st.markdown("### Hi, I'm Akhil")
                st.markdown("Welcome to my profile")
                if profile.get("landing_bio_intro"):
                    st.write(profile["landing_bio_intro"])
                    st.markdown(f"##### {profile["favorite_quote"]}")


        with profile_columns[1]:
            with st.container(border=True):
                st.caption("Quick links")
                for link in profile.get("social_links", []):
                    st.link_button(link["label"], link["url"], use_container_width=True)
                if profile.get("signature_points"):
                    st.caption("What I optimize for")
                    render_tag_cloud(profile["signature_points"])

        with profile_columns[2]:
            with st.container(border=True):
                st.image(photo_source, use_container_width=True)
                # if profile.get("photo_caption"):
                #     st.caption(profile["photo_caption"])



    st.markdown(
        f"""
        <section class="hero-panel">
            <div class="hero-copy">
                <p class="eyebrow">{profile.get("hero_eyebrow", profile["role"])}</p>
                <h1>{profile.get("hero_title", profile["name"])}</h1>
                <p class="hero-summary">{profile.get("hero_summary", "")}</p>
            </div>
            <div class="hero-meta">
                <div class="meta-card">
                    <span class="meta-label">Role</span>
                    <strong>{profile["role"]}</strong>
                </div>
                <div class="meta-card">
                    <span class="meta-label">Company</span>
                    <strong>{profile.get("company", "Remote friendly")}</strong>
                </div>
                <div class="meta-card">
                    <span class="meta-label">Location</span>
                    <strong>{profile.get("location", "Remote friendly")}</strong>
                </div>
                <div class="meta-card">
                    <span class="meta-label">Availability</span>
                    <strong>{profile.get("availability_badge", "Open for collaborations")}</strong>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(3)
    metric_columns[0].metric("Work areas", len(work_areas), profile.get("focus_note", "Active focus"))
    metric_columns[1].metric("Projects", len(projects), profile.get("projects_note", "Current builds"))
    metric_columns[2].metric("Interests", len(interests), profile.get("interests_note", "Ideas in motion"))

    action_columns = st.columns(4)
    action_columns[0].page_link(
        page_registry["bio"],
        label=settings["navigation"]["bio_label"],
        icon=":material/person:",
        use_container_width=True,
    )
    action_columns[1].page_link(
        page_registry["work"],
        label=settings["navigation"]["work_label"],
        icon=":material/workspace_premium:",
        use_container_width=True,
    )
    action_columns[2].page_link(
        page_registry["github"],
        label=settings["navigation"]["github_label"],
        icon=":material/rocket_launch:",
        use_container_width=True,
    )
    action_columns[3].page_link(
        page_registry["schedule"],
        label=settings["navigation"]["schedule_label"],
        icon=":material/calendar_month:",
        use_container_width=True,
    )


    render_section_intro(
        "What I do",
        settings["navigation"]["work_label"],
        settings["work_intro"],
    )
    work_columns = st.columns(3)
    for index, work_area in enumerate(work_areas[:3]):
        with work_columns[index % 3].container(border=True):
            st.caption(work_area.get("eyebrow", "Area of work"))
            st.subheader(work_area["title"])
            st.write(work_area["summary"])
            if work_area.get("highlight"):
                st.info(work_area["highlight"])

    # render_section_intro(
    #     "What I am exploring",
    #     settings["navigation"]["interests_label"],
    #     settings["interests"].get("intro", ""),
    # )
    # interest_columns = st.columns(2)
    # for index, interest in enumerate(interests[:4]):
    #     with interest_columns[index % 2].container(border=True):
    #         st.subheader(interest["title"])
    #         st.write(interest["summary"])
    #         if interest.get("link_url"):
    #             st.link_button(
    #                 interest.get("link_label", "Learn more"),
    #                 interest["link_url"],
    #                 use_container_width=True,
    #             )

    # render_section_intro(
    #     "Current builds",
    #     settings["navigation"]["projects_label"],
    #     settings.get("projects_intro", ""),
    # )
    # project_columns = st.columns(2)
    # for index, project in enumerate(projects[:4]):
    #     with project_columns[index % 2].container(border=True):
    #         st.caption(project.get("status", "In progress"))
    #         st.subheader(project["name"])
    #         st.write(project["summary"])
    #         if project.get("stack"):
    #             render_tag_cloud(project["stack"])
    #         st.page_link(
    #             page_registry[f"project:{project['slug']}"],
    #             label=project.get("detail_label", "Open project page"),
    #             icon=":material/open_in_new:",
    #             use_container_width=True,
    #         )
    #         if project.get("github_url"):
    #             st.link_button("GitHub", project["github_url"], use_container_width=True)

    render_section_intro(
        "Schedule time",
        settings["navigation"]["schedule_label"],
        calendar.get("description", ""),
    )
    schedule_columns = st.columns([1.1, 1])
    with schedule_columns[0]:
        with st.container(border=True):
            st.subheader(calendar.get("title", "Reserve a meeting"))
            for topic in calendar.get("meeting_topics", []):
                st.write(f"- {topic}")

    with schedule_columns[1]:
        with st.container(border=True):
            st.caption("Booking provider")
            st.markdown(f"### **{calendar.get('provider', 'Google Calendar')}**")
            st.write(calendar.get("privacy_note", "Booking data stays with your calendar provider."))
            if calendar.get("booking_url"):
                st.link_button(
                    calendar.get("booking_label", "Book on Google Calendar"),
                    calendar["booking_url"],
                    use_container_width=True,
                )


def build_navigation(settings: dict) -> st.navigation:
    page_registry: dict[str, st.Page] = {}

    landing_page = st.Page(
        partial(render_landing_page, settings, page_registry),
        title=settings["navigation"]["home_label"],
        icon=":material/home:",
        default=True,
        url_path="home",
    )
    bio_page = st.Page(
        partial(render_about_page, settings, page_registry),
        title=settings["navigation"]["bio_label"],
        icon=":material/person:",
        url_path="bio",
    )
    work_page = st.Page(
        partial(render_work_page, settings, page_registry),
        title=settings["navigation"]["work_label"],
        icon=":material/workspace_premium:",
        url_path="work",
    )
    # interests_page = st.Page(
    #     partial(render_interests_page, settings, page_registry),
    #     title=settings["navigation"]["interests_label"],
    #     icon=":material/interests:",
    #     url_path="interests",
    # )
    # projects_page = st.Page(
    #     partial(render_projects_page, settings, page_registry),
    #     title=settings["navigation"]["projects_label"],
    #     icon=":material/rocket_launch:",
    #     url_path="projects",
    # )
    github_page = st.Page(
        partial(render_github_page, settings, page_registry),
        title=settings["navigation"]["github_label"],
        icon=":material/code:",
        url_path="github",
    )
    schedule_page = st.Page(
        partial(render_schedule_page, settings, page_registry),
        title=settings["navigation"]["schedule_label"],
        icon=":material/calendar_month:",
        url_path="schedule",
    )

    page_registry.update(
        {
            "home": landing_page,
            "bio": bio_page,
            "work": work_page,
            # "interests": interests_page,
            # "projects": projects_page,
            "github": github_page,
            "schedule": schedule_page,
        }
    )

    project_pages: list[st.Page] = []
    for project in settings["projects"]:
        page = st.Page(
            make_project_page(settings, project, page_registry),
            title=project["name"],
            icon=":material/description:",
            url_path=f"project-{project['slug']}",
            visibility="hidden",
        )
        page_registry[f"project:{project['slug']}"] = page
        project_pages.append(page)

    navigation = st.navigation(
        {
            settings["navigation"]["primary_section_label"]: [
                landing_page,
                bio_page,
                work_page,
                # interests_page,
                # projects_page,
                github_page,
                schedule_page,
                *project_pages,
            ]
        },
        position="top",
        expanded=False,
    )
    return navigation


def resolve_photo_source(profile: dict) -> str | None:
    photo_url = profile.get("photo_url")
    if photo_url:
        return photo_url

    photo_path = profile.get("photo_path")
    if not photo_path:
        return None

    candidate = Path(photo_path)
    if candidate.exists():
        return str(candidate)

    return None


def main() -> None:
    settings = load_settings_file("settings.yaml")
    theme = load_settings_file(".streamlit/config.yaml")

    st.set_page_config(
        page_title=settings["profile"]["name"],
        page_icon=":material/space_dashboard:",
        layout="wide",
    )
    inject_theme(theme)

    navigation = build_navigation(settings)
    navigation.run()


if __name__ == "__main__":
    main()
