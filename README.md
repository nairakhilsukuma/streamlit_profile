<p align="center">
  <img src="assets/streamlit_logo.png" alt="Streamlit" />
</p>

# MyProfile

A settings-driven Streamlit profile app that turns a personal site into a polished, multi-page experience. The app keeps content in YAML, styling in a small theme file, and page behavior in modular Python files so you can update the site without constantly rewriting UI code.

## Features

- YAML-driven content for profile details, work areas, projects, links, and scheduling
- A custom Streamlit UI with injected theme styles, expressive typography, gradients, and reusable tag components
- Multi-page navigation with a landing page plus dedicated biography, work, GitHub, schedule, and project detail views
- Support for either a hosted profile image (`photo_url`) or a local repo asset (`photo_path`)
- Optional embedded calendar support through `calendar.embed_url`

## Project Structure

```text
.
|-- application.py
|-- settings.yaml
|-- pyproject.toml
|-- .streamlit/
|   `-- config.yaml
|-- app_helpers/
|   |-- settings.py
|   `-- ui.py
|-- pages/
|   |-- about_page.py
|   |-- github_page.py
|   |-- interests_page.py
|   |-- project_detail_page.py
|   |-- projects_page.py
|   |-- schedule_page.py
|   `-- work_page.py
`-- assets/
```

## Getting Started

### Requirements

- Python 3.12+
- `uv` recommended, or any Python environment with `streamlit`

### Install dependencies

```bash
uv sync
```

### Run the app

```bash
uv run streamlit run application.py
```

If you prefer not to use `uv`, install the package dependencies in a virtual environment and run:

```bash
streamlit run application.py
```

## Configuration

The app is configured through two main files:

- `settings.yaml`: profile content, work areas, projects, social links, GitHub links, scheduling info, and navigation labels
- `.streamlit/config.yaml`: fonts, colors, and radius values used by the injected theme

### Common content sections in `settings.yaml`

- `profile`: name, role, location, hero text, bio, social links, and photo source
- `work_areas`: cards shown on the landing and work pages
- `projects`: project summaries plus detail-page content
- `github`: profile link and repository list
- `calendar`: booking link, provider text, topics, privacy note, and optional embed URL
- `navigation`: labels used across the app

## Customizing the App

- Update text content in `settings.yaml`
- Place local images in `assets/` and reference them with `profile.photo_path`
- Use `profile.photo_url` if you want to load the image from the web instead
- Adjust fonts and colors in `.streamlit/config.yaml`
- Add or update page logic in `pages/` and shared UI helpers in `app_helpers/ui.py`

## Deployment Notes

- Cloud environments are usually case-sensitive, so asset filenames must match exactly. For example, `profilepic.JPG` and `profilepic.jpg` are different files on Linux.
- Keep local assets committed to the repo if the deployed app depends on them.
- If you use `calendar.embed_url`, make sure the source allows iframe embedding.

## How It Works

- `application.py` loads the settings, injects the theme, builds Streamlit navigation, and renders the active page.
- `app_helpers/settings.py` loads and normalizes the YAML configuration.
- `app_helpers/ui.py` contains shared styling and small rendering helpers like section headers and tag clouds.
- `pages/` contains focused render functions for each view, plus a project page factory for per-project detail pages.

## Future Improvements

- Add automated tests for config loading and page rendering
- Add screenshots or a deployed demo link
- Expand content validation so invalid or missing settings fail more clearly
