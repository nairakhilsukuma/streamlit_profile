from __future__ import annotations

import streamlit as st

from app_helpers.settings import load_settings_file
from app_helpers.ui import inject_theme


def render_projects_page(settings: dict, page_registry: dict[str, st.Page] | None = None) -> None:
    st.warning("The projects page is currently disabled.")
    st.stop()


def main() -> None:
    settings = load_settings_file("settings.yaml")
    theme = load_settings_file(".streamlit/config.yaml")

    st.set_page_config(
        page_title=f"{settings['profile']['name']} | {settings['navigation']['projects_label']}",
        page_icon=":material/rocket_launch:",
        layout="wide",
    )
    inject_theme(theme)
    render_projects_page(settings)


if __name__ == "__main__":
    main()
