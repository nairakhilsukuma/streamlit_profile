
from __future__ import annotations
from functools import partial
from pathlib import Path
import streamlit as st
from app_helpers.settings import load_settings_file
from app_helpers.ui import inject_theme, render_icon_links, render_section_intro, render_tag_cloud

APP_ROOT = Path(__file__).resolve().parent
TOP_CARD_HEIGHT = 250
WORK_CARD_HEIGHT = 230
SCHEDULE_CARD_HEIGHT = 220


def resolve_photo_source(profile: dict) -> str | None:
    photo_url = profile.get("photo_url")
    if photo_url:
        return photo_url

    photo_path = profile.get("photo_path")
    if not photo_path:
        return None

    candidate = Path(photo_path)
    if not candidate.is_absolute():
        candidate = APP_ROOT / candidate

    if candidate.exists():
        return str(candidate)

    parent = candidate.parent
    if not parent.exists():
        return None

    normalized_name = candidate.name.casefold()
    for sibling in parent.iterdir():
        if sibling.name.casefold() == normalized_name:
            return str(sibling)

    return None


def render_landing_page(settings: dict, page_registry: dict[str, st.Page]) -> None:
    profile = settings["profile"]
    work_areas = settings["work_areas"]
    projects = settings["projects"]
    calendar = settings["calendar"]
    support = settings.get("support", {})

    photo_source = resolve_photo_source(profile)
    if photo_source:
        profile_columns = st.columns([1.1, 0.9, 0.28])

        with profile_columns[0]:
            with st.container(border=True, height=TOP_CARD_HEIGHT, key="profile_intro_card"):
                st.markdown("### Hi, I'm Akhil")
                st.markdown("Welcome to my profile!")
                if profile.get("landing_bio_intro"):
                    st.write(profile["landing_bio_intro"])
                if profile.get("favorite_quote"):
                    st.markdown(f"##### {profile['favorite_quote']}")


        with profile_columns[1]:
            with st.container(border=True, height=TOP_CARD_HEIGHT, key="profile_links_card"):
                st.caption("Quick links")
                render_icon_links(profile.get("social_links", []))
                if profile.get("signature_points"):
                    st.caption("What I optimize for")
                    render_tag_cloud(profile["signature_points"])

        with profile_columns[2]:
            with st.container(border=True, height=TOP_CARD_HEIGHT, key="profile_image_card"):
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
    metric_columns[2].metric("Bio", len(profile.get("bio", [])), "Experience snapshot")

    action_columns = st.columns(2)
    action_columns[0].page_link(
        page_registry["home"],
        label=settings["navigation"]["home_label"],
        icon=":material/home:",
        use_container_width=True,
    )
    if calendar.get("booking_url"):
        action_columns[1].link_button(
            calendar.get("booking_label", "Book on Google Calendar"),
            calendar["booking_url"],
            icon=":material/calendar_month:",
            use_container_width=True,
        )


    render_section_intro(
        "What I do",
        "Areas of Work",
        settings["work_intro"],
    )
    work_columns = st.columns(3)
    for index, work_area in enumerate(work_areas[:3]):
        with work_columns[index % 3].container(
            border=True,
            height=WORK_CARD_HEIGHT,
            key=f"work_card_{index}",
        ):
            st.caption(work_area.get("eyebrow", "Area of work"))
            st.subheader(work_area["title"])
            st.write(work_area["summary"])
            if work_area.get("highlight"):
                st.info(work_area["highlight"])

    render_section_intro(
        "Schedule time",
        "Schedule",
        calendar.get("description", ""),
    )
    schedule_columns = st.columns([1.1, 1])
    with schedule_columns[0]:
        with st.container(
            border=True,
            height=SCHEDULE_CARD_HEIGHT,
            key="schedule_topics_card",
        ):
            st.subheader(calendar.get("title", "Reserve a meeting"))
            for topic in calendar.get("meeting_topics", []):
                st.write(f"- {topic}")

    with schedule_columns[1]:
        with st.container(
            border=True,
            height=SCHEDULE_CARD_HEIGHT,
            key="schedule_provider_card",
        ):
            st.caption("Booking provider")
            st.markdown(f"### **{calendar.get('provider', 'Google Calendar')}**")
            st.write(calendar.get("privacy_note", "Booking data stays with your calendar provider."))
            if calendar.get("booking_url"):
                st.link_button(
                    calendar.get("booking_label", "Book a meeting"),
                    calendar["booking_url"],
                    icon=":material/calendar_month:",
                    use_container_width=True,
                )

    # if support.get("url"):
    #     render_section_intro(
    #         "Support",
    #         support.get("title", "Support My Projects"),
    #         support.get(
    #             "description",
    #             "If you are interested in supporting my projects, want to know more, or would like to collaborate, feel free to buy me a coffee.",
    #         ),
    #     )
    #     with st.container(border=True):
    #         support_columns = st.columns([1.4, 0.6])
    #         with support_columns[0]:
    #             st.write(
    #                 support.get(
    #                     "description",
    #                     "If you are interested in supporting my projects, want to know more, or would like to collaborate, feel free to buy me a coffee.",
    #                 )
    #             )
    #         with support_columns[1]:
    #             st.link_button(
    #                 support.get("button_label", "Buy Me a Coffee"),
    #                 support["url"],
    #                 icon=":material/coffee:",
    #                 use_container_width=True,
    #             )


def build_navigation(settings: dict) -> st.navigation:
    page_registry: dict[str, st.Page] = {}

    landing_page = st.Page(
        partial(render_landing_page, settings, page_registry),
        title=settings["navigation"]["home_label"],
        icon=":material/home:",
        default=True,
        url_path="home",
    )

    page_registry.update(
        {
            "home": landing_page,
        }
    )

    navigation = st.navigation(
        {
            settings["navigation"]["primary_section_label"]: [
                landing_page,
            ]
        },
        position="top",
        expanded=False,
    )
    return navigation



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
