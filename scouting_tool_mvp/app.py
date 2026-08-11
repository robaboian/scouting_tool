import streamlit as st
from pathlib import Path


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
    """
    <style>

    /* Fondo general */
    .stApp {
        background-color: #F7F7F7;
    }

    /* Ocultar padding exagerado superior */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Header principal */
    .mitre-header {
        background: linear-gradient(
            135deg,
            #111111 0%,
            #1b1b1b 100%
        );
        border-left: 8px solid #F2C300;
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 28px;
    }

    .mitre-club {
        color: #F2C300;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .mitre-title {
        color: white;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 4px;
        line-height: 1.1;
    }

    .mitre-subtitle {
        color: #D8D8D8;
        font-size: 17px;
        font-weight: 400;
        margin-top: 8px;
    }

    /* Títulos de sección */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #171717;
        margin-top: 14px;
        margin-bottom: 16px;
    }

    /* Tarjetas */
    .home-card {
        background-color: white;
        border: 1px solid #E3E3E3;
        border-top: 4px solid #F2C300;
        border-radius: 10px;
        padding: 22px;
        min-height: 180px;
        box-shadow: 0px 2px 7px rgba(0, 0, 0, 0.04);
    }

    .home-card-title {
        font-size: 20px;
        font-weight: 700;
        color: #151515;
        margin-bottom: 10px;
    }

    .home-card-text {
        color: #555555;
        font-size: 15px;
        line-height: 1.5;
    }

    /* Flujo inferior */
    .workflow-box {
        background-color: #111111;
        color: white;
        border-radius: 10px;
        padding: 20px 24px;
        margin-top: 10px;
    }

    .workflow-number {
        color: #F2C300;
        font-weight: 800;
    }

    /* Sidebar */
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
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ENCABEZADO
# ============================================================

logo_path = Path("assets/escudo_mitre.png")


col_logo, col_header = st.columns(
    [1, 8],
    vertical_alignment="center",
)


with col_logo:

    if logo_path.exists():

        st.image(
            str(logo_path),
            width=110,
        )

    else:

        # Mientras no esté cargado el escudo
        st.markdown(
            """
            <div style="
                width:100px;
                height:100px;
                border-radius:12px;
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
            """,
            unsafe_allow_html=True,
        )


with col_header:

    st.markdown(
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
        """,
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
    '<div class="section-title">Módulos de trabajo</div>',
    unsafe_allow_html=True,
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(
        """
        <div class="home-card">

            <div class="home-card-title">
                🔍 Explorador
            </div>

            <div class="home-card-text">
                Consultá la base de jugadores utilizando filtros por categoría,
                club, posición y otros criterios.
                <br><br>
                Accedé a los reportes e informes realizados sobre cada jugador.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with c2:

    st.markdown(
        """
        <div class="home-card">

            <div class="home-card-title">
                ➕ Jugadores y reportes
            </div>

            <div class="home-card-text">
                Incorporá nuevos jugadores a la base y registrá observaciones
                realizadas durante partidos o análisis de video.
                <br><br>
                También permite editar y administrar jugadores existentes.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:

    st.markdown(
        """
        <div class="home-card">

            <div class="home-card-title">
                📋 Campograma
            </div>

            <div class="home-card-text">
                Organizá los jugadores detectados por categoría y posición.
                <br><br>
                Compará candidatos y accedé directamente a sus reportes
                desde el tablero de mercado.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


with c4:

    st.markdown(
        """
        <div class="home-card">

            <div class="home-card-title">
                📄 Informes
            </div>

            <div class="home-card-text">
                Consolidá las distintas observaciones de un jugador en un
                informe final.
                <br><br>
                Guardá conclusiones y generá documentos exportables.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# FLUJO DE TRABAJO
# ============================================================

st.markdown(
    '<div class="section-title">Flujo de trabajo</div>',
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="workflow-box">

        <span class="workflow-number">01</span>
        &nbsp; Detectar y crear el jugador
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
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PIE
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.caption(
    "Club Atlético Mitre · Secretaría Técnica · Departamento de Scouting"
)
