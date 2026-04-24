from __future__ import annotations

from pathlib import Path

import streamlit as st
from PIL import Image

from app_helpers.settings import load_settings_file
from app_helpers.ui import inject_theme

APP_ROOT = Path(__file__).resolve().parents[1]


def render_bio_page(settings: dict, page_registry: dict[str, st.Page] | None = None) -> None:
    page_registry = page_registry or {}
    profile = settings["profile"]
    navigation = settings["navigation"]

    st.markdown(f"## {navigation['bio_label']}")
    st.markdown(profile.get("bio_page_intro", "A little more context on how I work and what I care about."))

    st.title("Advanced Process Controls & Optimization Portfolio")
    st.divider()

    st.header("MPC • Scheduling • AI-driven Industrial Systems")


    top_columns = st.columns([1, 1.5], gap="large")
    with top_columns[0]:
        image_path = APP_ROOT / "assets" / "controlstack.png"
        if image_path.exists():
            image = Image.open(image_path)
            st.image(image, caption="Process Controls Hierarchy & Project Stack", width=500)
        st.divider()

    with top_columns[1]:
        st.header("Process Automation Stack Breakdown")
        stack_columns = st.columns(2)

        with stack_columns[0]:
            st.subheader("Scheduling & Optimization")
            st.markdown(
                """
                - Time scale: **days to weeks**
                - Production planning and capacity optimization
                - Resource allocation using **LP / NLP / ML models**
                - Job shop scheduling using **constraint programming**
                - Tools used: Aspen PIMS, Pyomo, Gurobi, AMPL, CVXPY
                """
            )

            st.subheader("Real-Time Optimization")
            st.markdown(
                """
                - Time scale: **hours to days**
                - Setpoint optimization for MPC layer
                - Economic optimization under constraints
                - Model-based decision tuning
                - Tools used: Matlab, Python (SciPy, Pyomo), PyTorch
                """
            )

        with stack_columns[1]:
            st.subheader("Process Control (MPC)")
            st.markdown(
                """
                - Time scale: **seconds to minutes**
                - Multivariable constrained control
                - Step-response / state-space based prediction
                - Handles interaction between variables
                - Tools used: Aspen DMC3, Matlab MPC, Python (custom)
                """
            )

            st.subheader("Regulatory Control (PLC)")
            st.markdown(
                """
                - Time scale: **milliseconds to seconds**
                - PID loops, servo control, safety logic
                - PLC integration (Allen Bradley, Siemens, Omron)
                - SCADA systems (WinCC, FactoryTalk)
                """
            )

        st.subheader("Work Experience")
        st.markdown(
            """
            - Manufacturing Controls: Bharat Petroleum (2017-2019)
            - Scheduling and Optimization: Bharat Petroleum (2019-2021)
            - Research (Superstructure optimization): Carnegie Mellon University (2021-2022)
            - Advanced Controls and Optimization: Corning Incorporated (2022-Present)
            """
        )

    st.divider()

    st.header("Technology Stack")
    lower_columns = st.columns(3, gap="large")

    st.divider()
    with lower_columns[0]:
        st.subheader("Modeling & Simulation")
        st.markdown(
            """
            **Simulation & Modeling**
            - Python (NumPy, SciPy, PyTorch)
            - MATLAB / Simulink
            - First-principles plus data-driven modeling

            **Industrial Systems**
            - Aspen PIMS (planning concepts)
            - DMC-style MPC (step-response models)
            - PLC / SCADA systems (WinCC, Studio 5000)

            **AI / Advanced Analytics**
            - Fault detection using grey-box models
            - Machine learning for anomaly detection
            - Computer vision for defect detection
            """
        )

    with lower_columns[1]:
        st.subheader("Major Projects Led")
        st.markdown(
            """
            **Scheduling & Optimization Systems**
            - Refinery production planning models (PIMS-style)
            - Resource optimization using LP/MILP
            - Superstructure optimization for process selection

            **Model Predictive Control Systems**
            - Multivariable MPC for interacting processes
            - Step-response model development (DMC-like structure)
            - Constraint handling and economic optimization

            **AI + Process Engineering**
            - Fault detection using grey-box models
            - Deep learning models for defect detection (glass manufacturing)
            - Predictive maintenance systems

            **Industrial Automation**
            - PLC logic development (Allen Bradley, Siemens)
            - SCADA integration (WinCC, Sysmac Studio)
            - PID tuning and control architecture design
            """
        )

    with lower_columns[2]:
        st.subheader("Philosophy")
        st.markdown(
            """
            I focus on **bridging three layers of industrial intelligence**:

            1. **Planning (PIMS)**: What should we produce?
            2. **Control (MPC/DMC3)**: How do we achieve it optimally?
            3. **Automation (PLC/SCADA)**: How do we execute it reliably?

            My strength lies in connecting **economic decisions, dynamic constraints, and physical execution**
            into one coherent system.
            """
        )

    st.success("Open to roles in Advanced Controls, Optimization, and Industrial AI Systems")

    footer_columns = st.columns(1)
    footer_columns[0].page_link(
        page_registry.get("home", "application.py"),
        label=navigation["home_label"],
        icon=":material/home:",
        use_container_width=True,
    )


def main() -> None:
    settings = load_settings_file("settings.yaml")
    theme = load_settings_file(".streamlit/config.yaml")

    st.set_page_config(
        page_title=f"{settings['profile']['name']} | {settings['navigation']['bio_label']}",
        page_icon=":material/person:",
        layout="wide",
    )
    inject_theme(theme)
    render_bio_page(settings)


if __name__ == "__main__":
    main()
