import pandas as pd
import streamlit as st

from data_access import get_repository
from utils import calculate_age


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Campograma",
    page_icon="📋",
    layout="wide",
)

repo = get_repository()


players = repo.read("jugadores")
reports = repo.read("reportes")
final_reports = repo.read("informes_finales")
campograma = repo.read("campograma")


st.title("📋 Campograma de mercado")


# ============================================================
# CONTROL DE DATOS
# ============================================================

if campograma.empty:

    st.info(
        "Todavía no hay jugadores agregados al campograma."
    )

    st.stop()


# ============================================================
# CATEGORÍA
# ============================================================

categorias = sorted(
    [
        x
        for x
        in campograma["categoria"].unique()
        if x
    ]
)


categoria = st.selectbox(
    "Categoría",
    categorias,
)


campograma_categoria = campograma[
    campograma["categoria"] == categoria
].copy()


# ============================================================
# DATOS DE JUGADORES
# ============================================================

players = players.copy()

players["edad"] = (
    players["fecha_nacimiento"]
    .apply(calculate_age)
)


if not reports.empty:

    report_counts = (
        reports
        .groupby("player_id")
        .size()
        .reset_index(
            name="cantidad_reportes"
        )
    )

else:

    report_counts = pd.DataFrame(
        columns=[
            "player_id",
            "cantidad_reportes",
        ]
    )


campograma_categoria = (
    campograma_categoria
    .merge(
        players,
        on="player_id",
        how="left",
    )
    .merge(
        report_counts,
        on="player_id",
        how="left",
    )
)


campograma_categoria[
    "cantidad_reportes"
] = (
    campograma_categoria[
        "cantidad_reportes"
    ]
    .fillna(0)
    .astype(int)
)


# ============================================================
# HELPERS
# ============================================================

def mostrar_jugador_card(
    player_row,
    key_suffix,
):

    nombre = (
        player_row["nombre"]
        if player_row["nombre"]
        else "Jugador"
    )

    club = (
        player_row["club"]
        if player_row["club"]
        else "Sin club"
    )

    edad = (
        player_row["edad"]
        if player_row["edad"]
        else "—"
    )

    cantidad_reportes = (
        int(
            player_row[
                "cantidad_reportes"
            ]
        )
    )


    with st.container(
        border=True
    ):

        st.markdown(
            f"**{nombre}**"
        )

        st.caption(
            f"{club} · {edad} años"
        )

        st.caption(
            f"{cantidad_reportes} reportes"
        )

        if st.button(
            "Ver",
            key=(
                f"ver_"
                f"{key_suffix}_"
                f"{player_row['player_id']}"
            ),
            use_container_width=True,
        ):

            st.session_state[
                "campograma_selected_player"
            ] = player_row[
                "player_id"
            ]


        if st.button(
            "Quitar",
            key=(
                f"quitar_"
                f"{key_suffix}_"
                f"{player_row['player_id']}"
            ),
            use_container_width=True,
        ):

            repo.delete_where(
                "campograma",
                "campograma_id",
                player_row[
                    "campograma_id"
                ],
            )

            st.rerun()


def mostrar_zona(
    titulo,
    posicion,
    columnas=3,
):

    st.markdown(
        f"### {titulo}"
    )

    zone_players = (
        campograma_categoria[
            campograma_categoria[
                "posicion_campograma"
            ] == posicion
        ]
    )


    if zone_players.empty:

        st.caption(
            "Sin jugadores"
        )

        return


    cols = st.columns(
        columnas
    )


    for index, (_, row) in enumerate(
        zone_players.iterrows()
    ):

        with cols[
            index % columnas
        ]:

            mostrar_jugador_card(
                row,
                posicion,
            )


# ============================================================
# CAMPOGRAMA
# ============================================================

st.divider()


# ------------------------------------------------------------
# ARQUEROS
# ------------------------------------------------------------

c1, c2, c3 = st.columns(
    [1, 2, 1]
)

with c2:

    mostrar_zona(
        "ARQUEROS",
        "ARQUEROS",
        columnas=2,
    )


st.divider()


# ------------------------------------------------------------
# CENTRALES
# ------------------------------------------------------------

c1, c2 = st.columns(2)

with c1:

    mostrar_zona(
        "DEF. CEN. DER.",
        "DEF.CEN.DER",
    )


with c2:

    mostrar_zona(
        "DEF. CEN. IZQ.",
        "DEF.CEN.IZQ",
    )


st.divider()


# ------------------------------------------------------------
# LATERALES + POSICIONAL
# ------------------------------------------------------------

c1, c2, c3 = st.columns(3)


with c1:

    mostrar_zona(
        "LAT. DER.",
        "LAT.DER",
        columnas=2,
    )


with c2:

    mostrar_zona(
        "VOL. POSICIONAL",
        "VOL.POSICIONAL",
        columnas=2,
    )


with c3:

    mostrar_zona(
        "LAT. IZQ.",
        "LAT.IZQ",
        columnas=2,
    )


st.divider()


# ------------------------------------------------------------
# INTERNOS
# ------------------------------------------------------------

c1, c2 = st.columns(2)


with c1:

    mostrar_zona(
        "INT. CONTENCIÓN",
        "INT.CONTENCION",
    )


with c2:

    mostrar_zona(
        "INT. OFENSIVO",
        "INT.OFENSIVO",
    )


st.divider()


# ------------------------------------------------------------
# VOLANTE OFENSIVO
# ------------------------------------------------------------

c1, c2, c3 = st.columns(
    [1, 2, 1]
)


with c2:

    mostrar_zona(
        "VOL. OFENSIVO",
        "VOL.OFENSIVO",
    )


st.divider()


# ------------------------------------------------------------
# EXTREMOS
# ------------------------------------------------------------

c1, c2 = st.columns(2)


with c1:

    mostrar_zona(
        "EXTREMOS DER.",
        "EXTREMOS DER",
    )


with c2:

    mostrar_zona(
        "EXTREMOS IZQ.",
        "EXTREMOS IZQ",
    )


st.divider()


# ------------------------------------------------------------
# MEDIA PUNTA / DELANTERO
# ------------------------------------------------------------

c1, c2 = st.columns(2)


with c1:

    mostrar_zona(
        "MEDIA PUNTA",
        "MEDIA PUNTA",
    )


with c2:

    mostrar_zona(
        "DEL. CENTRO",
        "DEL.CENTRO",
    )


# ============================================================
# JUGADOR SELECCIONADO
# ============================================================

if (
    "campograma_selected_player"
    not in st.session_state
):

    st.stop()


selected_id = (
    st.session_state[
        "campograma_selected_player"
    ]
)


selected_player = players[
    players["player_id"]
    == selected_id
]


if selected_player.empty:

    st.stop()


player = (
    selected_player.iloc[0]
)


st.divider()

st.header(
    player["nombre"]
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "Club",
    player["club"]
    or "—",
)


c2.metric(
    "Edad",
    player["edad"]
    or "—",
)


c3.metric(
    "Posición",
    player[
        "posicion_principal"
    ]
    or "—",
)


c4.metric(
    "Pie",
    player["pie"]
    or "—",
)


# ============================================================
# DOCUMENTOS
# ============================================================

player_reports = reports[
    reports["player_id"]
    == selected_id
].copy()


player_final = final_reports[
    final_reports["player_id"]
    == selected_id
].copy()


document_options = {}


# ------------------------------------------------------------
# REPORTES
# ------------------------------------------------------------

if not player_reports.empty:

    player_reports = (
        player_reports
        .sort_values(
            "fecha_observacion",
            ascending=False,
        )
    )


    for _, report in (
        player_reports.iterrows()
    ):

        label = (
            f'Reporte | '
            f'{report["fecha_observacion"]} | '
            f'vs. {report["rival"]}'
        )

        document_options[
            label
        ] = {
            "tipo": "reporte",
            "data": report,
        }


# ------------------------------------------------------------
# INFORME FINAL
# ------------------------------------------------------------

if not player_final.empty:

    final_report = (
        player_final
        .sort_values(
            "fecha_modificacion",
            ascending=False,
        )
        .iloc[0]
    )

    document_options[
        "Informe final"
    ] = {
        "tipo": "informe",
        "data": final_report,
    }


if not document_options:

    st.info(
        "Este jugador todavía no tiene documentos."
    )

    st.stop()


selected_document_label = (
    st.selectbox(
        "Ver documento",
        list(
            document_options.keys()
        ),
    )
)


document = (
    document_options[
        selected_document_label
    ]
)


# ============================================================
# REPORTE
# ============================================================

if document["tipo"] == "reporte":

    report = document["data"]

    st.subheader(
        selected_document_label
    )

    c1, c2, c3 = (
        st.columns(3)
    )


    c1.write(
        f'**Scout:** '
        f'{report["scout"]}'
    )


    c2.write(
        f'**Valoración:** '
        f'{report["valoracion_general"]}/5'
    )


    c3.write(
        f'**Recomendación:** '
        f'{report["recomendacion"]}'
    )


    sections = [
        (
            "Observaciones",
            "observaciones",
        ),
        (
            "Perfil físico",
            "perfil_fisico",
        ),
        (
            "Perfil táctico",
            "perfil_tactico",
        ),
        (
            "Perfil técnico",
            "perfil_tecnico",
        ),
        (
            "Perfil mental",
            "perfil_mental",
        ),
        (
            "Fases del juego",
            "fases_juego",
        ),
    ]


    for title, field in sections:

        value = report[field]

        if value:

            st.markdown(
                f"### {title}"
            )

            st.write(
                value
            )


# ============================================================
# INFORME FINAL
# ============================================================

else:

    final = document["data"]

    st.subheader(
        "Informe final"
    )


    sections = [
        (
            "Observaciones generales",
            "observaciones",
        ),
        (
            "Perfil físico",
            "perfil_fisico",
        ),
        (
            "Perfil táctico",
            "perfil_tactico",
        ),
        (
            "Perfil técnico",
            "perfil_tecnico",
        ),
        (
            "Perfil mental",
            "perfil_mental",
        ),
        (
            "Fases del juego",
            "fases_juego",
        ),
        (
            "Áreas consolidadas",
            "areas_consolidadas",
        ),
        (
            "Áreas de mejora",
            "areas_mejora",
        ),
        (
            "Conclusión",
            "conclusion",
        ),
    ]


    for title, field in sections:

        value = final[field]

        if value:

            st.markdown(
                f"### {title}"
            )

            st.write(
                value
            )
