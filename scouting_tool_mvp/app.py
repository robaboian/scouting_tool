from pathlib import Path

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
# ESCUDO
# ============================================================

logo_path = (
    Path(__file__).resolve().parent
    / "assets"
    / "escudo_mitre.png"
)


# ============================================================
# ENCABEZADO
# ============================================================

col_logo, col_text = st.columns(
    [1, 5],
    vertical_alignment="center",
)


with col_logo:

    if logo_path.exists():
        st.image(
            str(logo_path),
            width=160,
        )


with col_text:

    st.title(
        "Club Atlético Mitre"
    )

    st.subheader(
        "Secretaría Técnica · Departamento de Scouting"
    )

    st.caption(
        "Herramienta interna de seguimiento, evaluación "
        "y gestión de jugadores."
    )


st.divider()


# ============================================================
# PRESENTACIÓN
# ============================================================

st.write(
    """
Esta plataforma centraliza el trabajo del área de scouting:
desde la creación y seguimiento de jugadores hasta la consulta
de reportes, conformación de campogramas y elaboración de
informes finales.
"""
)


# ============================================================
# MÓDULOS
# ============================================================

st.subheader(
    "Módulos de trabajo"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🔍 Explorador"
        )

        st.write(
            """
Buscá jugadores utilizando filtros por categoría,
club, posición y otros criterios.

Consultá sus reportes e informes.
"""
        )


with c2:

    with st.container(
        border=True
    ):

        st.markdown(
            "### ➕ Jugadores y reportes"
        )

        st.write(
            """
Creá nuevos jugadores y registrá observaciones
realizadas durante partidos o análisis de video.

También permite editar jugadores existentes.
"""
        )


with c3:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📋 Campograma"
        )

        st.write(
            """
Organizá los jugadores detectados por categoría
y posición.

Accedé directamente a sus reportes desde el
listado de mercado.
"""
        )


with c4:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📄 Informes"
        )

        st.write(
            """
Consolidá distintas observaciones en un informe
final del jugador.

Guardá conclusiones y generá documentos exportables.
"""
        )


# ============================================================
# FLUJO DE TRABAJO
# ============================================================

st.subheader(
    "Flujo de trabajo"
)

st.write(
    """
**1.** Crear o incorporar un jugador  
**2.** Registrar observaciones y reportes  
**3.** Consultar y comparar perfiles  
**4.** Incorporar candidatos al campograma  
**5.** Consolidar el informe final
"""
)


st.divider()


# ============================================================
# PIE
# ============================================================

st.caption(
    "Club Atlético Mitre · Secretaría Técnica · Departamento de Scouting"
)
