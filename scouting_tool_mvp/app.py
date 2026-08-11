from pathlib import Path
from textwrap import dedent

import streamlit as st


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Scouting | Club Atlético Mitre",
    page_icon="⚽",
    layout="wide",
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    dedent(
        """
        <style>

        .stApp {
            background-color: #F7F7F7;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        /* =========================
           ENCABEZADO
        ========================= */

        .mitre-header {
            background: linear-gradient(
                135deg,
                #111111 0%,
                #1b1b1b 100%
            );
            border-left: 8px solid #F2C300;
            border-radius: 12px;
            padding: 30px 34px;
            margin-bottom: 28px;
        }

        .mitre-club {
            color: #F2C300;
            font-size: 15px;
            font-weight: 700;
            letter-spacing: 1.8px;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .mitre-title {
            color: #FFFFFF;
            font-size: 36px;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 7px;
        }

        .mitre-subtitle {
            color: #D5D5D5;
            font-size: 18px;
            font-weight: 400;
        }

        /* =========================
           SECCIONES
        ========================= */

        .section-title {
            font-size: 24px;
            font-weight: 750;
            color: #171717;
            margin-top: 30px;
            margin-bottom: 16px;
        }

        /* =========================
           TARJETAS
        ========================= */

        .home-card {
            background-color: #FFFFFF;
            border: 1px solid #E1E1E1;
            border-top: 5px solid #F2C300;
            border-radius: 11px;
            padding: 22px;
            min-height: 215px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }

        .home-card-title {
            font-size: 19px;
            font-weight: 750;
            color: #111111;
            margin-bottom: 13px;
        }

        .home-card-text {
            color: #555555;
            font-size: 15px;
            line-height: 1.55;
        }

        /* =========================
           FLUJO
        ========================= */

        .workflow-box {
            background-color: #111111;
            color: #FFFFFF;
            border-radius: 11px;
            padding: 22px 26px;
            margin-top: 10px;
            line-height: 2;
        }

        .workflow-number {
            color: #F2C300;
            font-weight: 800;
        }

        /* =========================
           SIDEBAR
        ========================= */

        [data-testid="stSidebar"] {
            background-color: #111111;
        }

        [data-testid="stSidebar"] * {
            color: #F4F4F4;
        }

        [data-testid="stSidebarNav"] a:hover {
            background-color: rgba(242, 195, 0, 0.15);
        }

        </style>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# ENCABEZADO
# ============================================================

logo_path = Path(__file__).resolve().parent / "assets" / "escudo_mitre.png"

col_logo, col_header = st.columns(
    [1, 8],
    vertical_alignment="center",
)


with col_logo:

    if logo_path.exists():

        st.image(
            str(logo_path),
            width=115,
        )

    else:

        st.markdown(
            dedent(
                """
                <div style="
                    width:110px;
                    height:110px;
                    border-radius:14px;
                    background:#111111;
                    color:#F2C300;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:30px;
                    font-weight:800;
                ">
                    CAM
                </div>
                """
            ),
            unsafe_allow_html=True,
        )


with col_header:

    st.markdown(
        dedent(
            """
            <div class="mitre-header">

                <div class="mitre-club">
                    Club Atlético Mitre
                </div>

                <div class="mitre-title">
                    Secretaría Técnica
                </div>

                <div class="mitre-subtitle">
                    Departamento de Scouting
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# DESCRIPCIÓN
# ============================================================

st.markdown(
    """
Herramienta interna para la **gestión, seguimiento y evaluación de jugadores**.

Centraliza el proceso de scouting desde la detección inicial y la carga de
observaciones hasta la elaboración de informes y la conformación de
campogramas de mercado.
"""
)


# ============================================================
# MÓDULOS
# ============================================================

st.markdown(
    dedent(
        """
        <div class="section-title">
            Módulos de trabajo
        </div>
        """
    ),
    unsafe_allow_html=True,
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        dedent(
            """
            <div class="home-card">

                <div class="home-card-title">
                    🔍 Explorador
                </div>

                <div class="home-card-text">
                    Consultá la base de jugadores utilizando filtros
                    por categoría, club, posición y otros criterios.
                    <br><br>
                    Accedé a los reportes e informes realizados
                    sobre cada jugador.
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


with c2:

    st.markdown(
        dedent(
            """
            <div class="home-card">

                <div class="home-card-title">
                    ➕ Jugadores y reportes
                </div>

                <div class="home-card-text">
                    Incorporá nuevos jugadores a la base y registrá
                    observaciones realizadas durante partidos o
                    análisis de video.
                    <br><br>
                    Editá y administrá jugadores existentes.
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


with c3:

    st.markdown(
        dedent(
            """
            <div class="home-card">

                <div class="home-card-title">
                    📋 Campograma
                </div>

                <div class="home-card-text">
                    Organizá los jugadores detectados por categoría
                    y posición.
                    <br><br>
                    Compará candidatos y accedé directamente a sus
                    reportes desde el tablero de mercado.
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


with c4:

    st.markdown(
        dedent(
            """
            <div class="home-card">

                <div class="home-card-title">
                    📄 Informes
                </div>

                <div class="home-card-text">
                    Consolidá las distintas observaciones de un
                    jugador en un informe final.
                    <br><br>
                    Guardá conclusiones y generá documentos
                    exportables.
                </div>

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# FLUJO DE TRABAJO
# ============================================================

st.markdown(
    dedent(
        """
        <div class="section-title">
            Flujo de trabajo
        </div>
        """
    ),
    unsafe_allow_html=True,
)


st.markdown(
    dedent(
        """
        <div class="workflow-box">

            <span class="workflow-number">01</span>
            &nbsp; Detectar y crear jugador

            &nbsp;&nbsp;→&nbsp;&nbsp;

            <span class="workflow-number">02</span>
            &nbsp; Cargar observaciones

            &nbsp;&nbsp;→&nbsp;&nbsp;

            <span class="workflow-number">03</span>
            &nbsp; Consultar y comparar

            &nbsp;&nbsp;→&nbsp;&nbsp;

            <span class="workflow-number">04</span>
            &nbsp; Incorporar al campograma

            &nbsp;&nbsp;→&nbsp;&nbsp;

            <span class="workflow-number">05</span>
            &nbsp; Consolidar informe final

        </div>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# PIE
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.caption(
    "Club Atlético Mitre · Secretaría Técnica · Departamento de Scouting"
)
