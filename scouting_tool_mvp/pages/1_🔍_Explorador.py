import pandas as pd
import streamlit as st

from data_access import get_repository
from utils import calculate_age


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Explorador",
    page_icon="🔍",
    layout="wide",
)

repo = get_repository()

players = repo.read("jugadores")
reports = repo.read("reportes")
final_reports = repo.read("informes_finales")


st.title("🔍 Explorador de jugadores")


# ============================================================
# CONTROL DE BASE VACÍA
# ============================================================

if players.empty:
    st.info("Todavía no hay jugadores cargados.")
    st.stop()


# ============================================================
# CAMPGRAMA - SESSION STATE
# ============================================================

if "campograma_ids" not in st.session_state:
    st.session_state["campograma_ids"] = []


# ============================================================
# PREPARACIÓN DE JUGADORES
# ============================================================

players = players.copy()

players["edad"] = (
    players["fecha_nacimiento"]
    .apply(calculate_age)
)


# ------------------------------------------------------------
# Cantidad de reportes
# ------------------------------------------------------------

if not reports.empty:

    report_counts = (
        reports
        .groupby("player_id")
        .size()
        .reset_index(
            name="cantidad_reportes"
        )
    )

    players = players.merge(
        report_counts,
        on="player_id",
        how="left",
    )

else:

    players["cantidad_reportes"] = 0


players["cantidad_reportes"] = (
    players["cantidad_reportes"]
    .fillna(0)
    .astype(int)
)


# ============================================================
# FILTROS
# ============================================================

with st.expander(
    "Filtros",
    expanded=True,
):

    c1, c2, c3, c4 = st.columns(4)

    search = c1.text_input(
        "Nombre"
    )

    clubs = sorted(
        [
            x
            for x
            in players["club"].unique()
            if x
        ]
    )

    club = c2.selectbox(
        "Club",
        ["Todos"] + clubs,
    )

    positions = sorted(
        [
            x
            for x
            in players[
                "posicion_principal"
            ].unique()
            if x
        ]
    )

    position = c3.selectbox(
        "Posición",
        ["Todas"] + positions,
    )

    foot_options = sorted(
        [
            x
            for x
            in players["pie"].unique()
            if x
        ]
    )

    foot = c4.selectbox(
        "Pie",
        ["Todos"] + foot_options,
    )


    c5, c6, c7 = st.columns(3)

    competitions = sorted(
        [
            x
            for x
            in players[
                "competicion"
            ].unique()
            if x
        ]
    )

    competition = c5.selectbox(
        "Competición",
        ["Todas"] + competitions,
    )

    min_reports = c6.number_input(
        "Cantidad mínima de reportes",
        min_value=0,
        value=0,
    )

    status_options = sorted(
        [
            x
            for x
            in players[
                "estado"
            ].unique()
            if x
        ]
    )

    status = c7.selectbox(
        "Estado",
        ["Todos"] + status_options,
    )


# ============================================================
# APLICAR FILTROS
# ============================================================

filtered = players.copy()


if search:

    filtered = filtered[
        filtered["nombre"]
        .str.contains(
            search,
            case=False,
            na=False,
        )
    ]


if club != "Todos":

    filtered = filtered[
        filtered["club"] == club
    ]


if position != "Todas":

    filtered = filtered[
        filtered[
            "posicion_principal"
        ] == position
    ]


if foot != "Todos":

    filtered = filtered[
        filtered["pie"] == foot
    ]


if competition != "Todas":

    filtered = filtered[
        filtered[
            "competicion"
        ] == competition
    ]


if status != "Todos":

    filtered = filtered[
        filtered["estado"] == status
    ]


filtered = filtered[
    filtered[
        "cantidad_reportes"
    ] >= min_reports
]


st.caption(
    f"{len(filtered)} jugadores encontrados"
)


if filtered.empty:

    st.warning(
        "No se encontraron jugadores con esos filtros."
    )

    st.stop()


# ============================================================
# TABLA DE JUGADORES
# ============================================================

st.subheader(
    "Jugadores"
)


table_df = (
    filtered[
        [
            "player_id",
            "nombre",
            "club",
            "competicion",
            "edad",
            "posicion_principal",
            "pie",
            "cantidad_reportes",
        ]
    ]
    .copy()
)


# ------------------------------------------------------------
# Columnas interactivas
# ------------------------------------------------------------

table_df.insert(
    0,
    "Ver",
    False,
)


table_df["Agregar a campograma"] = (
    table_df["player_id"]
    .isin(
        st.session_state[
            "campograma_ids"
        ]
    )
)


edited_df = st.data_editor(
    table_df,
    hide_index=True,
    use_container_width=True,
    disabled=[
        "player_id",
        "nombre",
        "club",
        "competicion",
        "edad",
        "posicion_principal",
        "pie",
        "cantidad_reportes",
    ],
    column_config={

        "Ver":
            st.column_config.CheckboxColumn(
                "Ver",
                help=(
                    "Seleccioná el jugador "
                    "que querés consultar."
                ),
                default=False,
            ),

        "player_id":
            None,

        "nombre":
            st.column_config.TextColumn(
                "Jugador"
            ),

        "club":
            st.column_config.TextColumn(
                "Club"
            ),

        "competicion":
            st.column_config.TextColumn(
                "Categoría"
            ),

        "edad":
            st.column_config.NumberColumn(
                "Edad",
                format="%d",
            ),

        "posicion_principal":
            st.column_config.TextColumn(
                "Posición"
            ),

        "pie":
            st.column_config.TextColumn(
                "Pie"
            ),

        "cantidad_reportes":
            st.column_config.NumberColumn(
                "Reportes",
                format="%d",
            ),

        "Agregar a campograma":
            st.column_config.CheckboxColumn(
                "Agregar a campograma",
                default=False,
            ),
    },
    key="player_explorer_editor",
)


# ============================================================
# ACTUALIZAR CAMPGRAMA
# ============================================================

campograma_ids = (
    edited_df.loc[
        edited_df[
            "Agregar a campograma"
        ],
        "player_id",
    ]
    .astype(str)
    .tolist()
)


st.session_state[
    "campograma_ids"
] = campograma_ids


if campograma_ids:

    st.caption(
        f"{len(campograma_ids)} "
        f"jugadores agregados al campograma."
    )


# ============================================================
# SELECCIONAR JUGADOR
# ============================================================

selected_rows = edited_df[
    edited_df["Ver"]
]


if selected_rows.empty:

    st.info(
        "Seleccioná un jugador en la columna "
        "'Ver' para consultar su información."
    )

    st.stop()


# Si por accidente se seleccionan varios,
# tomamos el primero.

selected_id = (
    selected_rows.iloc[0][
        "player_id"
    ]
)


player = (
    filtered.loc[
        filtered[
            "player_id"
        ] == selected_id
    ]
    .iloc[0]
)


# ============================================================
# FICHA DEL JUGADOR
# ============================================================

st.divider()

st.subheader(
    player["nombre"]
)


m1, m2, m3, m4, m5, m6 = (
    st.columns(6)
)


m1.metric(
    "Club",
    player["club"]
    or "—",
)


m2.metric(
    "Edad",
    player["edad"]
    or "—",
)


m3.metric(
    "Posición",
    player[
        "posicion_principal"
    ]
    or "—",
)


m4.metric(
    "Pie",
    player["pie"]
    or "—",
)


m5.metric(
    "Altura",
    (
        f'{player["altura"]} cm'
        if player["altura"]
        else "—"
    ),
)


m6.metric(
    "Reportes",
    int(
        player[
            "cantidad_reportes"
        ]
    ),
)


# ============================================================
# DOCUMENTOS DISPONIBLES
# ============================================================

st.subheader(
    "Reportes e informe"
)


player_reports = (
    reports[
        reports[
            "player_id"
        ] == selected_id
    ]
    .copy()
)


player_final_reports = (
    final_reports[
        final_reports[
            "player_id"
        ] == selected_id
    ]
    .copy()
)


document_options = {}


# ------------------------------------------------------------
# Reportes por partido
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

        fecha_display = (
            report[
                "fecha_observacion"
            ]
        )

        rival_display = (
            report["rival"]
            or "Rival sin definir"
        )

        label = (
            f"Reporte | "
            f"{fecha_display} | "
            f"vs. {rival_display}"
        )

        document_options[
            label
        ] = {
            "tipo": "reporte",
            "data": report,
        }


# ------------------------------------------------------------
# Informe final
# ------------------------------------------------------------

if not player_final_reports.empty:

    final_report = (
        player_final_reports
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


# ============================================================
# SIN DOCUMENTOS
# ============================================================

if not document_options:

    st.info(
        "Este jugador todavía no tiene "
        "reportes ni informe final."
    )

    st.stop()


# ============================================================
# SELECTOR DE DOCUMENTO
# ============================================================

selected_document_label = (
    st.selectbox(
        "Seleccionar documento",
        options=list(
            document_options.keys()
        ),
    )
)


selected_document = (
    document_options[
        selected_document_label
    ]
)


st.divider()


# ============================================================
# MOSTRAR REPORTE
# ============================================================

if (
    selected_document[
        "tipo"
    ] == "reporte"
):

    report = (
        selected_document[
            "data"
        ]
    )

    c1, c2, c3, c4 = (
        st.columns(4)
    )

    c1.write(
        f'**Scout:** '
        f'{report["scout"] or "—"}'
    )

    c2.write(
        f'**Posición:** '
        f'{report["posicion_observada"] or "—"}'
    )

    c3.write(
        f'**Valoración:** '
        f'{report["valoracion_general"] or "—"}/5'
    )

    c4.write(
        f'**Recomendación:** '
        f'{report["recomendacion"] or "—"}'
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


    for label, field in sections:

        value = report[field]

        if value:

            st.markdown(
                f"### {label}"
            )

            st.write(
                value
            )


    if report["video_url"]:

        st.link_button(
            "Abrir video",
            report[
                "video_url"
            ],
        )


# ============================================================
# MOSTRAR INFORME FINAL
# ============================================================

elif (
    selected_document[
        "tipo"
    ] == "informe"
):

    final = (
        selected_document[
            "data"
        ]
    )


    c1, c2, c3 = (
        st.columns(3)
    )


    c1.write(
        f'**Estado:** '
        f'{final["estado"] or "—"}'
    )


    c2.write(
        f'**Autor:** '
        f'{final["autor"] or "—"}'
    )


    c3.write(
        f'**Última modificación:** '
        f'{final["fecha_modificacion"] or "—"}'
    )


    final_sections = [
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
        (
            "Características determinantes",
            "caracteristicas_determinantes",
        ),
        (
            "Enlaces de video",
            "enlaces_video",
        ),
    ]


    for label, field in final_sections:

        value = final[field]

        if value:

            st.markdown(
                f"### {label}"
            )

            st.write(
                value
            )
