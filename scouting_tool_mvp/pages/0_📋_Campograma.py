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


# ============================================================
# LEER DATOS
# ============================================================

players = repo.read("jugadores")
reports = repo.read("reportes")
final_reports = repo.read("informes_finales")
campograma = repo.read("campograma")


st.title("📋 Campograma de mercado")


# ============================================================
# CONTROL
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
        for x in campograma["categoria"].unique()
        if x
    ]
)


categoria = st.selectbox(
    "Categoría",
    categorias,
    key="campograma_categoria",
)


# Si cambia la categoría, cerramos cualquier jugador abierto
if (
    "campograma_categoria_anterior"
    in st.session_state
    and st.session_state["campograma_categoria_anterior"] != categoria
):
    st.session_state.pop(
        "campograma_selected_player",
        None,
    )


st.session_state[
    "campograma_categoria_anterior"
] = categoria


campograma_categoria = (
    campograma[
        campograma["categoria"] == categoria
    ]
    .copy()
)


# ============================================================
# PREPARAR JUGADORES
# ============================================================

players = players.copy()

players["edad"] = (
    players["fecha_nacimiento"]
    .apply(calculate_age)
)


# ============================================================
# CANTIDAD DE REPORTES
# ============================================================

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


# ============================================================
# UNIR CAMPOGRAMA + JUGADORES
# ============================================================

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
# TARJETA
# ============================================================

def mostrar_jugador_card(
    player_row,
    key_suffix,
):

    nombre = (
        player_row["nombre"]
        or "Jugador"
    )

    club = (
        player_row["club"]
        or "Sin club"
    )

    edad = (
        player_row["edad"]
        or "—"
    )

    cantidad_reportes = int(
        player_row[
            "cantidad_reportes"
        ]
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

        if cantidad_reportes == 1:
            st.caption(
                "1 reporte"
            )
        else:
            st.caption(
                f"{cantidad_reportes} reportes"
            )


        c1, c2 = st.columns(2)


        with c1:

            if st.button(
                "Ver",
                key=(
                    f"ver_"
                    f"{key_suffix}_"
                    f"{player_row['campograma_id']}"
                ),
                use_container_width=True,
            ):

                st.session_state[
                    "campograma_selected_player"
                ] = player_row[
                    "player_id"
                ]

                st.rerun()


        with c2:

            if st.button(
                "Quitar",
                key=(
                    f"quitar_"
                    f"{key_suffix}_"
                    f"{player_row['campograma_id']}"
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

                if (
                    st.session_state.get(
                        "campograma_selected_player"
                    )
                    == player_row[
                        "player_id"
                    ]
                ):

                    st.session_state.pop(
                        "campograma_selected_player",
                        None,
                    )

                st.rerun()


# ============================================================
# DETALLE DEL JUGADOR
# ============================================================

def mostrar_detalle_jugador(
    player_id,
):

    selected_player = (
        players[
            players[
                "player_id"
            ] == player_id
        ]
    )


    if selected_player.empty:
        return


    player = (
        selected_player
        .iloc[0]
    )


    with st.container(
        border=True
    ):

        header_left, header_right = (
            st.columns(
                [6, 1]
            )
        )


        with header_left:

            st.subheader(
                f'🔎 {player["nombre"]}'
            )


        with header_right:

            if st.button(
                "Cerrar",
                key=(
                    f"cerrar_"
                    f"{player_id}"
                ),
                use_container_width=True,
            ):

                st.session_state.pop(
                    "campograma_selected_player",
                    None,
                )

                st.rerun()


        c1, c2, c3, c4, c5 = (
            st.columns(5)
        )


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


        c5.metric(
            "Altura",
            (
                f'{player["altura"]} cm'
                if player["altura"]
                else "—"
            ),
        )


        # ====================================================
        # DOCUMENTOS
        # ====================================================

        player_reports = (
            reports[
                reports[
                    "player_id"
                ] == player_id
            ]
            .copy()
        )


        player_final = (
            final_reports[
                final_reports[
                    "player_id"
                ] == player_id
            ]
            .copy()
        )


        document_options = {}


        # ----------------------------------------------------
        # REPORTES
        # ----------------------------------------------------

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

                fecha = (
                    report[
                        "fecha_observacion"
                    ]
                    or "Sin fecha"
                )

                rival = (
                    report[
                        "rival"
                    ]
                    or "Sin rival"
                )


                label = (
                    f"Reporte | "
                    f"{fecha} | "
                    f"vs. {rival}"
                )


                document_options[
                    label
                ] = {
                    "tipo":
                        "reporte",

                    "data":
                        report,
                }


        # ----------------------------------------------------
        # INFORME FINAL
        # ----------------------------------------------------

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
                "tipo":
                    "informe",

                "data":
                    final,
            }


        # ----------------------------------------------------
        # SIN DOCUMENTOS
        # ----------------------------------------------------

        if not document_options:

            st.info(
                "Este jugador todavía no tiene "
                "reportes ni informe final."
            )

            return


        # ----------------------------------------------------
        # SELECTOR
        # ----------------------------------------------------

        selected_document_label = (
            st.selectbox(
                "Documento",
                list(
                    document_options.keys()
                ),
                key=(
                    f"document_"
                    f"{player_id}"
                ),
            )
        )


        document = (
            document_options[
                selected_document_label
            ]
        )


        # ====================================================
        # REPORTE
        # ====================================================

        if (
            document[
                "tipo"
            ] == "reporte"
        ):

            report = (
                document[
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


            for title, field in sections:

                value = (
                    report[
                        field
                    ]
                )

                if value:

                    st.markdown(
                        f"#### {title}"
                    )

                    st.write(
                        value
                    )


            if report[
                "video_url"
            ]:

                st.link_button(
                    "Abrir video",
                    report[
                        "video_url"
                    ],
                )


        # ====================================================
        # INFORME FINAL
        # ====================================================

        else:

            final = (
                document[
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

                value = (
                    final[
                        field
                    ]
                )

                if value:

                    st.markdown(
                        f"#### {title}"
                    )

                    st.write(
                        value
                    )


# ============================================================
# LISTADO DE UNA POSICIÓN
# ============================================================

def mostrar_posicion(
    titulo,
    posicion,
    tarjetas_por_fila=4,
):

    st.subheader(
        titulo
    )


    zone_players = (
        campograma_categoria[
            campograma_categoria[
                "posicion_campograma"
            ] == posicion
        ]
        .copy()
    )


    if zone_players.empty:

        st.caption(
            "Sin jugadores"
        )

        st.divider()

        return


    zone_players[
        "_orden"
    ] = pd.to_numeric(
        zone_players[
            "orden"
        ],
        errors="coerce",
    )


    zone_players = (
        zone_players
        .sort_values(
            [
                "_orden",
                "nombre",
            ],
            na_position="last",
        )
    )


    rows = list(
        zone_players.iterrows()
    )


    # ========================================================
    # TARJETAS EN FILAS
    # ========================================================

    for start in range(
        0,
        len(rows),
        tarjetas_por_fila,
    ):

        bloque = rows[
            start:
            start + tarjetas_por_fila
        ]


        columnas = st.columns(
            tarjetas_por_fila
        )


        for index, (_, row) in enumerate(
            bloque
        ):

            with columnas[
                index
            ]:

                mostrar_jugador_card(
                    row,
                    posicion,
                )


    # ========================================================
    # DETALLE JUSTO DEBAJO DEL PUESTO
    # ========================================================

    selected_id = (
        st.session_state.get(
            "campograma_selected_player"
        )
    )


    if selected_id:

        ids_de_esta_posicion = (
            zone_players[
                "player_id"
            ]
            .astype(str)
            .tolist()
        )


        if str(
            selected_id
        ) in ids_de_esta_posicion:

            st.markdown(
                "---"
            )

            mostrar_detalle_jugador(
                selected_id
            )


    st.divider()


# ============================================================
# RESUMEN
# ============================================================

total_jugadores = len(
    campograma_categoria
)


posiciones_cubiertas = (
    campograma_categoria[
        "posicion_campograma"
    ]
    .nunique()
)


c1, c2 = st.columns(2)


c1.metric(
    "Jugadores en campograma",
    total_jugadores,
)


c2.metric(
    "Puestos con candidatos",
    posiciones_cubiertas,
)


st.divider()


# ============================================================
# PUESTOS
# ============================================================

mostrar_posicion(
    "ARQUEROS",
    "ARQUEROS",
)


mostrar_posicion(
    "DEF. CEN. DER.",
    "DEF.CEN.DER",
)


mostrar_posicion(
    "DEF. CEN. IZQ.",
    "DEF.CEN.IZQ",
)


mostrar_posicion(
    "LAT. DER.",
    "LAT.DER",
)


mostrar_posicion(
    "LAT. IZQ.",
    "LAT.IZQ",
)


mostrar_posicion(
    "VOL. POSICIONAL",
    "VOL.POSICIONAL",
)


mostrar_posicion(
    "INT. CONTENCIÓN",
    "INT.CONTENCION",
)


mostrar_posicion(
    "INT. OFENSIVO",
    "INT.OFENSIVO",
)


mostrar_posicion(
    "VOL. OFENSIVO",
    "VOL.OFENSIVO",
)


mostrar_posicion(
    "EXTREMOS DER.",
    "EXTREMOS DER",
)


mostrar_posicion(
    "EXTREMOS IZQ.",
    "EXTREMOS IZQ",
)


mostrar_posicion(
    "MEDIA PUNTA",
    "MEDIA PUNTA",
)


mostrar_posicion(
    "DEL. CENTRO",
    "DEL.CENTRO",
)
