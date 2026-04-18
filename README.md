<p align="center">
  <img src="assets/logo.png" />
</p>

# MyProfile

A settings-driven Streamlit profile app with two pages: a landing page for your core profile and a dedicated projects page. The app keeps content in YAML, styling in a small theme file, and page behavior in a small set of Python files so it stays easy to deploy and maintain.

## Features

- YAML-driven content for profile details, work areas, projects, links, and scheduling
- A custom Streamlit UI with injected theme styles, expressive typography, gradients, and reusable tag components
- Two-page navigation with `Home` and `Projects`
- Support for either a hosted profile image (`photo_url`) or a local repo asset (`photo_path`)

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
|   |-- __init__.py
|   `-- projects_page.py
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

- `settings.yaml`: profile content, work areas, projects, scheduling info, and navigation labels
- `.streamlit/config.yaml`: fonts, colors, and radius values used by the injected theme

### Common content sections in `settings.yaml`

- `profile`: name, role, location, hero text, bio, social links, and photo source
- `work_areas`: cards shown on the landing page
- `projects`: project summaries and extended project descriptions
- `calendar`: booking link, provider text, topics, and privacy note
- `navigation`: labels used across the app

## Customizing the App

- Update text content in `settings.yaml`
- Place local images in `assets/` and reference them with `profile.photo_path`
- Use `profile.photo_url` if you want to load the image from the web instead
- Adjust fonts and colors in `.streamlit/config.yaml`
- Update the projects page logic in `pages/projects_page.py` and shared UI helpers in `app_helpers/ui.py`

## Deployment Notes

- Cloud environments are usually case-sensitive, so asset filenames must match exactly. For example, `profilepic.JPG` and `profilepic.jpg` are different files on Linux.
- Keep local assets committed to the repo if the deployed app depends on them.

## How It Works

- `application.py` loads the settings, injects the theme, builds the two-page Streamlit navigation, and renders the active page.
- `app_helpers/settings.py` loads and normalizes the YAML configuration.
- `app_helpers/ui.py` contains shared styling and small rendering helpers like section headers and tag clouds.
- `pages/projects_page.py` renders the dedicated projects view.

## Future Improvements

- Add automated tests for config loading and page rendering
- Add screenshots or a deployed demo link
- Expand content validation so invalid or missing settings fail more clearly
