import pandas as pd
import streamlit as st

from data_access import (
    get_repository,
    make_id,
    now_iso,
)

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
campograma = repo.read("campograma")


st.title("🔍 Explorador de jugadores")


# ============================================================
# CONTROL
# ============================================================

if players.empty:

    st.info(
        "Todavía no hay jugadores cargados."
    )

    st.stop()


# ============================================================
# PREPARAR JUGADORES
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

    players = players.merge(
        report_counts,
        on="player_id",
        how="left",
    )

else:

    players[
        "cantidad_reportes"
    ] = 0


players[
    "cantidad_reportes"
] = (
    players[
        "cantidad_reportes"
    ]
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

    c1, c2, c3, c4 = (
        st.columns(4)
    )

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

    feet = sorted(
        [
            x
            for x
            in players["pie"].unique()
            if x
        ]
    )

    foot = c4.selectbox(
        "Pie",
        ["Todos"] + feet,
    )

    c5, c6, c7 = (
        st.columns(3)
    )

    categories = sorted(
        [
            x
            for x
            in players[
                "competicion"
            ].unique()
            if x
        ]
    )

    category = c5.selectbox(
        "Categoría",
        ["Todas"] + categories,
    )

    min_reports = (
        c6.number_input(
            "Cantidad mínima de reportes",
            min_value=0,
            value=0,
        )
    )

    statuses = sorted(
        [
            x
            for x
            in players["estado"].unique()
            if x
        ]
    )

    status = c7.selectbox(
        "Estado",
        ["Todos"] + statuses,
    )


# ============================================================
# FILTRAR
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


if category != "Todas":

    filtered = filtered[
        filtered[
            "competicion"
        ] == category
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
# JUGADORES YA EN CAMPOGRAMA
# ============================================================

campograma_player_ids = (
    campograma[
        "player_id"
    ]
    .astype(str)
    .tolist()
    if not campograma.empty
    else []
)


# ============================================================
# DATAFRAME
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


table_df.insert(
    0,
    "Ver",
    False,
)


table_df[
    "Agregar a campograma"
] = (
    table_df[
        "player_id"
    ]
    .isin(
        campograma_player_ids
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
# QUITAR DEL CAMPOGRAMA AL DESMARCAR
# ============================================================

visible_player_ids = set(
    edited_df[
        "player_id"
    ]
    .astype(str)
    .tolist()
)


checked_campograma_ids = set(
    edited_df.loc[
        edited_df[
            "Agregar a campograma"
        ],
        "player_id",
    ]
    .astype(str)
    .tolist()
)


existing_visible_campograma_ids = (
    set(
        str(player_id)
        for player_id
        in campograma_player_ids
    )
    &
    visible_player_ids
)


removed_from_campograma = (
    existing_visible_campograma_ids
    -
    checked_campograma_ids
)


if removed_from_campograma:

    repo.delete_where(
        "campograma",
        "player_id",
        list(
            removed_from_campograma
        ),
    )

    st.rerun()


# ============================================================
# AGREGAR AL CAMPOGRAMA
# ============================================================

USUARIOS_APP = [
    "Juan Pablo Bouzas",
    "Kevin Quisbert",
    "Roberto Aboian",
]


POSICIONES_LATERALES = {

    "Defensor central": [
        "DEF.CEN.DER",
        "DEF.CEN.IZQ",
    ],

    "Lateral": [
        "LAT.DER",
        "LAT.IZQ",
    ],

    "Extremo": [
        "EXTREMOS DER",
        "EXTREMOS IZQ",
    ],
}


POSICIONES_AUTOMATICAS = {

    "Arquero":
        "ARQUEROS",

    "Volante posicional":
        "VOL.POSICIONAL",

    "Volante interno/contención":
        "INT.CONTENCION",

    "Volante interno/ofensivo":
        "INT.OFENSIVO",

    "Volante ofensivo":
        "VOL.OFENSIVO",

    "Mediapunta":
        "MEDIA PUNTA",

    "Delantero centro":
        "DEL.CENTRO",
}


selected_for_campograma = (
    edited_df[
        edited_df[
            "Agregar a campograma"
        ]
    ]
    .copy()
)


new_for_campograma = (
    selected_for_campograma[
        ~selected_for_campograma[
            "player_id"
        ]
        .isin(
            campograma_player_ids
        )
    ]
)


if not new_for_campograma.empty:

    st.markdown(
        "### Agregar al campograma"
    )

    agregado_por = st.selectbox(
        "Agregado por",
        USUARIOS_APP,
        key="campograma_agregado_por",
    )

    pending_rows = []

    for _, row in (
        new_for_campograma
        .iterrows()
    ):

        posicion_principal = (
            row[
                "posicion_principal"
            ]
        )

        st.markdown(
            f'**{row["nombre"]} — {row["club"]}**'
        )

        if (
            posicion_principal
            in POSICIONES_LATERALES
        ):

            posicion_campograma = (
                st.selectbox(
                    "Ubicación",
                    POSICIONES_LATERALES[
                        posicion_principal
                    ],
                    key=(
                        f'camp_pos_'
                        f'{row["player_id"]}'
                    ),
                )
            )

        elif (
            posicion_principal
            in POSICIONES_AUTOMATICAS
        ):

            posicion_campograma = (
                POSICIONES_AUTOMATICAS[
                    posicion_principal
                ]
            )

            st.caption(
                f"Ubicación: "
                f"{posicion_campograma}"
            )

        else:

            posicion_campograma = None

            st.warning(
                "No hay ubicación configurada."
            )

        if posicion_campograma:

            pending_rows.append(
                {
                    "campograma_id":
                        make_id("CMP"),

                    "player_id":
                        row["player_id"],

                    "categoria":
                        row["competicion"],

                    "posicion_campograma":
                        posicion_campograma,

                    "orden":
                        "",

                    "fecha_agregado":
                        now_iso(),

                    "agregado_por":
                        agregado_por,
                }
            )


    if st.button(
        "Guardar en campograma",
        type="primary",
    ):

        repo.append(
            "campograma",
            pending_rows,
        )

        st.success(
            "Jugador/es agregados al campograma."
        )

        st.rerun()


# ============================================================
# VER JUGADOR
# ============================================================

selected_rows = (
    edited_df[
        edited_df["Ver"]
    ]
)


if selected_rows.empty:

    st.info(
        "Seleccioná un jugador en la columna "
        "'Ver' para consultar su información."
    )

    st.stop()


selected_id = (
    selected_rows
    .iloc[0][
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
# FICHA
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
# DOCUMENTOS
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


player_final = (
    final_reports[
        final_reports[
            "player_id"
        ] == selected_id
    ]
    .copy()
)


document_options = {}


if not player_reports.empty:

    player_reports = (
        player_reports
        .sort_values(
            "fecha_observacion",
            ascending=False,
        )
    )

    for _, report in (
        player_reports
        .iterrows()
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


if not player_final.empty:

    final = (
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
        "data": final,
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


st.divider()


# ============================================================
# REPORTE
# ============================================================

if document["tipo"] == "reporte":

    report = document["data"]

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
        ("Observaciones", "observaciones"),
        ("Perfil físico", "perfil_fisico"),
        ("Perfil táctico", "perfil_tactico"),
        ("Perfil técnico", "perfil_tecnico"),
        ("Perfil mental", "perfil_mental"),
        ("Fases del juego", "fases_juego"),
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


    if report["video_url"]:

        st.link_button(
            "Abrir video",
            report[
                "video_url"
            ],
        )


# ============================================================
# INFORME FINAL
# ============================================================

else:

    final = document["data"]

    sections = [
        ("Observaciones generales", "observaciones"),
        ("Perfil físico", "perfil_fisico"),
        ("Perfil táctico", "perfil_tactico"),
        ("Perfil técnico", "perfil_tecnico"),
        ("Perfil mental", "perfil_mental"),
        ("Fases del juego", "fases_juego"),
        ("Áreas consolidadas", "areas_consolidadas"),
        ("Áreas de mejora", "areas_mejora"),
        ("Conclusión", "conclusion"),
        (
            "Características determinantes",
            "caracteristicas_determinantes",
        ),
        (
            "Enlaces de video",
            "enlaces_video",
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
