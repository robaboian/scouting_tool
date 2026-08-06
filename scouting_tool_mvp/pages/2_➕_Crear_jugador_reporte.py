from datetime import date

import pandas as pd
import streamlit as st

from config import (
    FEET,
    REPORT_RECOMMENDATIONS,
    REPORT_TYPES,
    CHARACTERISTIC_CATEGORIES,
    CHARACTERISTIC_RATINGS,
)

from data_access import (
    get_repository,
    make_id,
    now_iso,
)

from utils import player_label


# ============================================================
# OPCIONES
# ============================================================

NACIONALIDADES = [
    "Argentina",
    "Bolivia",
    "Brasil",
    "Chile",
    "Colombia",
    "Costa Rica",
    "Cuba",
    "Ecuador",
    "El Salvador",
    "España",
    "Estados Unidos",
    "Guatemala",
    "Haití",
    "Honduras",
    "Italia",
    "México",
    "Nicaragua",
    "Panamá",
    "Paraguay",
    "Perú",
    "Portugal",
    "República Dominicana",
    "Uruguay",
    "Venezuela",
    "Otra",
]


POSICIONES_PRINCIPALES = [
    "Arquero",
    "Defensor central",
    "Lateral",
    "Volante posicional",
    "Volante interno/contención",
    "Volante interno/ofensivo",
    "Volante ofensivo",
    "Extremo",
    "Mediapunta",
    "Delantero centro",
]


POSICIONES_SECUNDARIAS = [
    "Stopper",
    "Líbero",
    "Lateral volante",
    "Volante central",
    "Volante carrilero",
]


USUARIOS_APP = [
    "Juan Pablo Bouzas",
    "Kevin Quisbert",
    "Roberto Aboian",
]


CLUBES_POR_CATEGORIA = {

    "Primera B Metropolitana": [
        "Arsenal",
        "Argentino de Merlo",
        "Argentino de Quilmes",
        "Brown de Adrogué",
        "Camioneros",
        "Comunicaciones",
        "Defensores Unidos",
        "Deportivo Armenio",
        "Deportivo Laferrere",
        "Deportivo Merlo",
        "Dock Sud",
        "Excursionistas",
        "Flandria",
        "Ituzaingó",
        "Liniers",
        "Real Pilar",
        "San Martín de Burzaco",
        "Sportivo Italiano",
        "Talleres de Remedios de Escalada",
        "UAI Urquiza",
        "Villa Dálmine",
        "Villa San Carlos",
    ],

    "Primera Nacional": [
        "Acassuso",
        "Agropecuario Argentino",
        "All Boys",
        "Almagro",
        "Almirante Brown",
        "Atlanta",
        "Atlético de Rafaela",
        "Chacarita Juniors",
        "Chaco For Ever",
        "Ciudad de Bolívar",
        "Colegiales",
        "Colón",
        "Defensores de Belgrano",
        "Deportivo Maipú",
        "Deportivo Madryn",
        "Deportivo Morón",
        "Estudiantes de Buenos Aires",
        "Ferro Carril Oeste",
        "Gimnasia y Esgrima de Jujuy",
        "Gimnasia y Tiro de Salta",
        "Godoy Cruz",
        "Güemes de Santiago del Estero",
        "Los Andes",
        "Midland",
        "Mitre de Santiago del Estero",
        "Nueva Chicago",
        "Patronato",
        "Quilmes",
        "Racing de Córdoba",
        "San Martín de San Juan",
        "San Martín de Tucumán",
        "San Miguel",
        "San Telmo",
        "Temperley",
        "Tristán Suárez",
        "Central Norte de Salta",
    ],

    "Torneo Federal A": [
        "9 de Julio de Rafaela",
        "Alvarado",
        "Argentino de Monte Maíz",
        "Atenas de Río Cuarto",
        "Boca Unidos",
        "Cipolletti",
        "Costa Brava",
        "Círculo Deportivo",
        "Defensores de Belgrano de Villa Ramallo",
        "Defensores de Puerto Vilelas",
        "Deportivo Rincón",
        "Douglas Haig",
        "El Linqueño",
        "Escobar FC",
        "FADEP",
        "Germinal",
        "Gimnasia y Esgrima de Chivilcoy",
        "Gimnasia y Esgrima de Concepción del Uruguay",
        "Guillermo Brown",
        "Huracán Las Heras",
        "Independiente de Chivilcoy",
        "Juventud Antoniana",
        "Juventud Unida Universitario",
        "Kimberley",
        "Mitre de Posadas",
        "Olimpo",
        "San Martín de Formosa",
        "San Martín de Mendoza",
        "Sarmiento de La Banda",
        "Sarmiento de Resistencia",
        "Sol de América",
        "Sol de Mayo",
        "Sportivo Atlético Club",
        "Sportivo Belgrano",
        "Santamarina",
        "Tucumán Central",
        "Villa Mitre",
    ],

    "Primera C Metropolitana": [
        "Argentino de Rosario",
        "Atlas",
        "Berazategui",
        "Cañuelas",
        "Central Ballester",
        "Central Córdoba de Rosario",
        "Centro Español",
        "Claypole",
        "Defensores de Cambaceres",
        "Deportivo Español",
        "Deportivo Paraguayo",
        "El Porvenir",
        "Estrella del Sur",
        "Fénix",
        "General Lamadrid",
        "Juventud Unida",
        "Leandro N. Alem",
        "Leones FC",
        "Lugano",
        "Luján",
        "Mercedes",
        "Muñiz",
        "Puerto Nuevo",
        "J. J. Urquiza",
        "Sacachispas",
        "Sportivo Barracas",
        "Victoriano Arenas",
        "Yupanqui",
    ],
}


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Crear jugador / reporte",
    page_icon="➕",
    layout="wide",
)

repo = get_repository()

st.title("➕ Crear jugador / reporte")

players = repo.read(
    "jugadores"
)


tab_new, tab_existing, tab_manage = st.tabs(
    [
        "Crear jugador nuevo",
        "Agregar reporte a jugador existente",
        "Editar / eliminar jugador",
    ]
)


# ============================================================
# CREAR JUGADOR
# ============================================================

with tab_new:

    st.subheader(
        "Datos del jugador"
    )

    categoria = st.selectbox(
        "Categoría *",
        options=list(
            CLUBES_POR_CATEGORIA.keys()
        ),
        key="categoria_nuevo_jugador",
    )

    club = st.selectbox(
        "Club actual *",
        options=CLUBES_POR_CATEGORIA[
            categoria
        ],
        key="club_nuevo_jugador",
    )

    with st.form(
        "new_player_form",
        clear_on_submit=False,
    ):

        c1, c2, c3 = st.columns(3)

        nombre = c1.text_input(
            "Nombre completo *"
        )

        fecha_nacimiento = (
            c2.date_input(
                "Fecha de nacimiento",
                value=None,
                min_value=date(
                    1970,
                    1,
                    1,
                ),
                max_value=date.today(),
                format="DD/MM/YYYY",
            )
        )

        nacionalidad = c3.selectbox(
            "Nacionalidad",
            options=NACIONALIDADES,
            index=0,
        )

        c4, c5, c6 = st.columns(3)

        posicion_principal = (
            c4.selectbox(
                "Posición principal *",
                options=POSICIONES_PRINCIPALES,
            )
        )

        posicion_secundaria = (
            c5.selectbox(
                "Posición secundaria",
                options=[
                    "Sin posición secundaria",
                    *POSICIONES_SECUNDARIAS,
                ],
            )
        )

        pie = c6.selectbox(
            "Pie hábil",
            options=FEET,
        )

        c7, c8, c9 = st.columns(3)

        altura = c7.number_input(
            "Altura (cm)",
            min_value=0,
            max_value=230,
            value=0,
        )

        peso = c8.number_input(
            "Peso (kg)",
            min_value=0,
            max_value=180,
            value=0,
        )

        fin_contrato = (
            c9.date_input(
                "Fin de contrato",
                value=None,
                format="DD/MM/YYYY",
            )
        )

        c10, c11 = st.columns(2)

        estado = c10.selectbox(
            "Estado",
            options=[
                "Seguimiento activo",
                "Pendiente",
                "Cerrado",
            ],
        )

        creado_por = c11.selectbox(
            "Creado por *",
            options=USUARIOS_APP,
        )

        enlace_externo = (
            st.text_input(
                "Enlace externo"
            )
        )

        submitted = (
            st.form_submit_button(
                "Crear jugador",
                type="primary",
            )
        )


    if submitted:

        if not nombre.strip():

            st.error(
                "El nombre del jugador es obligatorio."
            )

        else:

            possible = (
                players[
                    players[
                        "nombre"
                    ]
                    .str.lower()
                    .str.strip()
                    .eq(
                        nombre
                        .lower()
                        .strip()
                    )
                ]

                if not players.empty

                else pd.DataFrame()
            )

            if not possible.empty:

                st.warning(
                    "Ya existe un jugador con el mismo nombre."
                )

            else:

                player_id = make_id(
                    "PLY"
                )

                repo.append(
                    "jugadores",
                    [
                        {
                            "player_id": player_id,
                            "nombre": nombre.strip(),
                            "fecha_nacimiento": (
                                fecha_nacimiento.isoformat()
                                if fecha_nacimiento
                                else ""
                            ),
                            "nacionalidad": nacionalidad,
                            "club": club,
                            "competicion": categoria,
                            "posicion_principal": posicion_principal,
                            "posicion_secundaria": (
                                ""
                                if posicion_secundaria
                                == "Sin posición secundaria"
                                else posicion_secundaria
                            ),
                            "pie": pie,
                            "altura": altura or "",
                            "peso": peso or "",
                            "fin_contrato": (
                                fin_contrato.isoformat()
                                if fin_contrato
                                else ""
                            ),
                            "enlace_externo": enlace_externo.strip(),
                            "estado": estado,
                            "fecha_creacion": now_iso(),
                            "creado_por": creado_por,
                        }
                    ],
                )

                st.success(
                    f"Jugador creado correctamente: {nombre}"
                )

                st.cache_data.clear()


# ============================================================
# AGREGAR REPORTE
# ============================================================

with tab_existing:

    players = repo.read(
        "jugadores"
    )

    if players.empty:

        st.info(
            "Primero tenés que crear un jugador."
        )

    else:

        selected_id = (
            st.selectbox(
                "Buscar jugador",
                players[
                    "player_id"
                ].tolist(),
                format_func=lambda pid:
                    player_label(
                        players.loc[
                            players[
                                "player_id"
                            ] == pid
                        ].iloc[0]
                    ),
            )
        )

        player = players.loc[
            players[
                "player_id"
            ] == selected_id
        ].iloc[0]

        st.caption(
            f'{player["nombre"]} | '
            f'{player["club"]} | '
            f'{player["posicion_principal"]}'
        )

        st.subheader(
            "Nueva observación"
        )

        with st.form(
            "new_report_form",
            clear_on_submit=True,
        ):

            c1, c2, c3 = (
                st.columns(3)
            )

            fecha = c1.date_input(
                "Fecha de observación",
                value=date.today(),
                max_value=date.today(),
                format="DD/MM/YYYY",
            )

            equipo = c2.text_input(
                "Equipo",
                value=player[
                    "club"
                ],
            )

            rival = c3.text_input(
                "Rival *"
            )

            c4, c5, c6 = (
                st.columns(3)
            )

            competicion = (
                c4.text_input(
                    "Competición",
                    value=player[
                        "competicion"
                    ],
                )
            )

            tipo = c5.selectbox(
                "Tipo de observación",
                REPORT_TYPES,
            )

            minutos = (
                c6.number_input(
                    "Minutos observados",
                    min_value=0,
                    max_value=130,
                    value=90,
                )
            )

            c7, c8 = (
                st.columns(2)
            )

            posicion_actual = (
                player[
                    "posicion_principal"
                ]
            )

            posicion = (
                c7.selectbox(
                    "Posición observada",
                    POSICIONES_PRINCIPALES,
                    index=(
                        POSICIONES_PRINCIPALES.index(
                            posicion_actual
                        )
                        if posicion_actual
                        in POSICIONES_PRINCIPALES
                        else 0
                    ),
                )
            )

            scout = (
                c8.selectbox(
                    "Scout *",
                    options=USUARIOS_APP,
                )
            )

            observaciones = (
                st.text_area(
                    "Observaciones generales",
                    height=100,
                )
            )

            perfil_fisico = (
                st.text_area(
                    "Perfil físico",
                    height=100,
                )
            )

            perfil_tactico = (
                st.text_area(
                    "Perfil táctico",
                    height=100,
                )
            )

            perfil_tecnico = (
                st.text_area(
                    "Perfil técnico",
                    height=100,
                )
            )

            perfil_mental = (
                st.text_area(
                    "Perfil mental",
                    height=100,
                )
            )

            fases_juego = (
                st.text_area(
                    "Fases del juego",
                    height=100,
                )
            )

            st.markdown(
                "#### Áreas consolidadas y de mejora"
            )

            fortalezas = (
                st.text_area(
                    "Áreas consolidadas",
                    placeholder="Una por línea",
                    height=100,
                )
            )

            mejoras = (
                st.text_area(
                    "Áreas de mejora",
                    placeholder="Una por línea",
                    height=100,
                )
            )

            st.markdown(
                "#### Características determinantes"
            )

            characteristics = (
                st.data_editor(
                    pd.DataFrame(
                        [
                            {
                                "categoria": "",
                                "caracteristica": "",
                                "valoracion": "",
                            }
                        ]
                    ),
                    column_config={
                        "categoria":
                            st.column_config.SelectboxColumn(
                                "Categoría",
                                options=CHARACTERISTIC_CATEGORIES,
                            ),

                        "caracteristica":
                            st.column_config.TextColumn(
                                "Característica"
                            ),

                        "valoracion":
                            st.column_config.SelectboxColumn(
                                "Valoración",
                                options=CHARACTERISTIC_RATINGS,
                            ),
                    },
                    num_rows="dynamic",
                    use_container_width=True,
                )
            )

            c9, c10 = (
                st.columns(2)
            )

            valoracion = (
                c9.slider(
                    "Valoración general",
                    1,
                    5,
                    3,
                )
            )

            recomendacion = (
                c10.selectbox(
                    "Recomendación",
                    REPORT_RECOMMENDATIONS,
                )
            )

            video_url = (
                st.text_input(
                    "Enlace de video"
                )
            )

            save_report = (
                st.form_submit_button(
                    "Guardar reporte",
                    type="primary",
                )
            )


        if save_report:

            if not rival.strip():

                st.error(
                    "El rival es obligatorio."
                )

            else:

                report_id = make_id(
                    "REP"
                )

                repo.append(
                    "reportes",
                    [
                        {
                            "report_id": report_id,
                            "player_id": selected_id,
                            "fecha_observacion": fecha.isoformat(),
                            "equipo": equipo.strip(),
                            "rival": rival.strip(),
                            "competicion": competicion.strip(),
                            "tipo_observacion": tipo,
                            "minutos_observados": minutos,
                            "posicion_observada": posicion,
                            "scout": scout,
                            "observaciones": observaciones.strip(),
                            "perfil_fisico": perfil_fisico.strip(),
                            "perfil_tactico": perfil_tactico.strip(),
                            "perfil_tecnico": perfil_tecnico.strip(),
                            "perfil_mental": perfil_mental.strip(),
                            "fases_juego": fases_juego.strip(),
                            "valoracion_general": valoracion,
                            "recomendacion": recomendacion,
                            "video_url": video_url.strip(),
                            "fecha_carga": now_iso(),
                        }
                    ],
                )

                area_rows = []

                for line in fortalezas.splitlines():

                    if line.strip():

                        area_rows.append(
                            {
                                "area_id": make_id("ARE"),
                                "report_id": report_id,
                                "tipo": "Área consolidada",
                                "descripcion": line.strip(),
                            }
                        )

                for line in mejoras.splitlines():

                    if line.strip():

                        area_rows.append(
                            {
                                "area_id": make_id("ARE"),
                                "report_id": report_id,
                                "tipo": "Área de mejora",
                                "descripcion": line.strip(),
                            }
                        )

                repo.append(
                    "areas_reporte",
                    area_rows,
                )

                characteristic_rows = []

                for _, row in (
                    characteristics
                    .fillna("")
                    .iterrows()
                ):

                    if (
                        row[
                            "caracteristica"
                        ]
                        .strip()
                    ):

                        characteristic_rows.append(
                            {
                                "characteristic_id":
                                    make_id("CHR"),

                                "report_id":
                                    report_id,

                                "categoria":
                                    row[
                                        "categoria"
                                    ],

                                "caracteristica":
                                    row[
                                        "caracteristica"
                                    ].strip(),

                                "valoracion":
                                    row[
                                        "valoracion"
                                    ],
                            }
                        )

                repo.append(
                    "caracteristicas",
                    characteristic_rows,
                )

                st.success(
                    f"Reporte guardado para {player['nombre']}."
                )

                st.cache_data.clear()


# ============================================================
# EDITAR / ELIMINAR
# ============================================================

with tab_manage:

    st.subheader(
        "Editar o eliminar jugador"
    )

    players = repo.read(
        "jugadores"
    )

    if players.empty:

        st.info(
            "Todavía no hay jugadores cargados."
        )

    else:

        selected_manage_id = (
            st.selectbox(
                "Seleccionar jugador",
                players[
                    "player_id"
                ].tolist(),
                format_func=lambda pid:
                    player_label(
                        players.loc[
                            players[
                                "player_id"
                            ] == pid
                        ].iloc[0]
                    ),
                key="manage_player_selector",
            )
        )

        selected_player = (
            players.loc[
                players[
                    "player_id"
                ]
                == selected_manage_id
            ].iloc[0]
        )


        edit_tab, delete_tab = (
            st.tabs(
                [
                    "Editar datos",
                    "Eliminar jugador",
                ]
            )
        )


        # ====================================================
        # EDITAR
        # ====================================================

        with edit_tab:

            current_category = (
                selected_player[
                    "competicion"
                ]
            )

            if (
                current_category
                not in CLUBES_POR_CATEGORIA
            ):

                current_category = (
                    list(
                        CLUBES_POR_CATEGORIA.keys()
                    )[0]
                )

            category_index = (
                list(
                    CLUBES_POR_CATEGORIA.keys()
                ).index(
                    current_category
                )
            )

            edited_category = (
                st.selectbox(
                    "Categoría",
                    options=list(
                        CLUBES_POR_CATEGORIA.keys()
                    ),
                    index=category_index,
                    key=f"edit_category_{selected_manage_id}",
                )
            )

            available_clubs = (
                CLUBES_POR_CATEGORIA[
                    edited_category
                ]
            )

            current_club = (
                selected_player[
                    "club"
                ]
            )

            club_index = (
                available_clubs.index(
                    current_club
                )

                if current_club
                in available_clubs

                else 0
            )

            edited_club = (
                st.selectbox(
                    "Club actual",
                    options=available_clubs,
                    index=club_index,
                    key=f"edit_club_{selected_manage_id}",
                )
            )


            with st.form(
                f"edit_player_form_{selected_manage_id}"
            ):

                c1, c2, c3 = (
                    st.columns(3)
                )

                edited_name = (
                    c1.text_input(
                        "Nombre completo *",
                        value=selected_player[
                            "nombre"
                        ],
                    )
                )

                try:

                    current_birth_date = (
                        pd.to_datetime(
                            selected_player[
                                "fecha_nacimiento"
                            ]
                        ).date()
                    )

                except Exception:

                    current_birth_date = None


                edited_birth_date = (
                    c2.date_input(
                        "Fecha de nacimiento",
                        value=current_birth_date,
                        min_value=date(
                            1970,
                            1,
                            1,
                        ),
                        max_value=date.today(),
                        format="DD/MM/YYYY",
                    )
                )


                nationality_index = (

                    NACIONALIDADES.index(
                        selected_player[
                            "nacionalidad"
                        ]
                    )

                    if selected_player[
                        "nacionalidad"
                    ] in NACIONALIDADES

                    else 0
                )


                edited_nationality = (
                    c3.selectbox(
                        "Nacionalidad",
                        options=NACIONALIDADES,
                        index=nationality_index,
                    )
                )


                c4, c5, c6 = (
                    st.columns(3)
                )


                principal_index = (

                    POSICIONES_PRINCIPALES.index(
                        selected_player[
                            "posicion_principal"
                        ]
                    )

                    if selected_player[
                        "posicion_principal"
                    ] in POSICIONES_PRINCIPALES

                    else 0
                )


                edited_main_position = (
                    c4.selectbox(
                        "Posición principal",
                        options=POSICIONES_PRINCIPALES,
                        index=principal_index,
                    )
                )


                secondary_options = [
                    "Sin posición secundaria",
                    *POSICIONES_SECUNDARIAS,
                ]


                current_secondary = (
                    selected_player[
                        "posicion_secundaria"
                    ]
                    or
                    "Sin posición secundaria"
                )


                secondary_index = (

                    secondary_options.index(
                        current_secondary
                    )

                    if current_secondary
                    in secondary_options

                    else 0
                )


                edited_secondary_position = (
                    c5.selectbox(
                        "Posición secundaria",
                        options=secondary_options,
                        index=secondary_index,
                    )
                )


                foot_index = (

                    FEET.index(
                        selected_player[
                            "pie"
                        ]
                    )

                    if selected_player[
                        "pie"
                    ] in FEET

                    else 0
                )


                edited_foot = (
                    c6.selectbox(
                        "Pie hábil",
                        options=FEET,
                        index=foot_index,
                    )
                )


                c7, c8, c9 = (
                    st.columns(3)
                )


                edited_height = (
                    c7.number_input(
                        "Altura (cm)",
                        min_value=0,
                        max_value=230,
                        value=(
                            int(
                                float(
                                    selected_player[
                                        "altura"
                                    ]
                                )
                            )
                            if selected_player[
                                "altura"
                            ]
                            else 0
                        ),
                    )
                )


                edited_weight = (
                    c8.number_input(
                        "Peso (kg)",
                        min_value=0,
                        max_value=180,
                        value=(
                            int(
                                float(
                                    selected_player[
                                        "peso"
                                    ]
                                )
                            )
                            if selected_player[
                                "peso"
                            ]
                            else 0
                        ),
                    )
                )


                try:

                    current_contract_date = (
                        pd.to_datetime(
                            selected_player[
                                "fin_contrato"
                            ]
                        ).date()
                    )

                except Exception:

                    current_contract_date = None


                edited_contract_date = (
                    c9.date_input(
                        "Fin de contrato",
                        value=current_contract_date,
                        format="DD/MM/YYYY",
                    )
                )


                c10, c11 = (
                    st.columns(2)
                )


                status_options = [
                    "Seguimiento activo",
                    "Pendiente",
                    "Cerrado",
                ]


                status_index = (

                    status_options.index(
                        selected_player[
                            "estado"
                        ]
                    )

                    if selected_player[
                        "estado"
                    ] in status_options

                    else 0
                )


                edited_status = (
                    c10.selectbox(
                        "Estado",
                        options=status_options,
                        index=status_index,
                    )
                )


                creator_index = (

                    USUARIOS_APP.index(
                        selected_player[
                            "creado_por"
                        ]
                    )

                    if selected_player[
                        "creado_por"
                    ] in USUARIOS_APP

                    else 0
                )


                edited_creator = (
                    c11.selectbox(
                        "Creado por",
                        options=USUARIOS_APP,
                        index=creator_index,
                    )
                )


                edited_link = (
                    st.text_input(
                        "Enlace externo",
                        value=selected_player[
                            "enlace_externo"
                        ],
                    )
                )


                save_changes = (
                    st.form_submit_button(
                        "Guardar cambios",
                        type="primary",
                    )
                )


            if save_changes:

                if not edited_name.strip():

                    st.error(
                        "El nombre del jugador es obligatorio."
                    )

                else:

                    updated_player = {

                        "player_id":
                            selected_manage_id,

                        "nombre":
                            edited_name.strip(),

                        "fecha_nacimiento":
                            (
                                edited_birth_date.isoformat()
                                if edited_birth_date
                                else ""
                            ),

                        "nacionalidad":
                            edited_nationality,

                        "club":
                            edited_club,

                        "competicion":
                            edited_category,

                        "posicion_principal":
                            edited_main_position,

                        "posicion_secundaria":
                            (
                                ""
                                if edited_secondary_position
                                == "Sin posición secundaria"
                                else edited_secondary_position
                            ),

                        "pie":
                            edited_foot,

                        "altura":
                            edited_height or "",

                        "peso":
                            edited_weight or "",

                        "fin_contrato":
                            (
                                edited_contract_date.isoformat()
                                if edited_contract_date
                                else ""
                            ),

                        "enlace_externo":
                            edited_link.strip(),

                        "estado":
                            edited_status,

                        "fecha_creacion":
                            selected_player[
                                "fecha_creacion"
                            ],

                        "creado_por":
                            edited_creator,
                    }


                    repo.upsert(
                        "jugadores",
                        updated_player,
                        key="player_id",
                    )


                    st.success(
                        "Los datos del jugador fueron actualizados."
                    )

                    st.cache_data.clear()

                    st.rerun()


        # ====================================================
        # ELIMINAR
        # ====================================================

        with delete_tab:

            reports = repo.read(
                "reportes"
            )

            player_reports = (
                reports[
                    reports[
                        "player_id"
                    ]
                    == selected_manage_id
                ]
            )


            report_ids = (
                player_reports[
                    "report_id"
                ]
                .astype(str)
                .tolist()
            )


            st.error(
                "Esta acción es irreversible."
            )

            st.warning(
                "Se eliminará el jugador, todos sus reportes, "
                "sus características, áreas y cualquier informe final."
            )


            st.write(
                f"**Jugador:** "
                f"{selected_player['nombre']}"
            )

            st.write(
                f"**Club:** "
                f"{selected_player['club']}"
            )

            st.write(
                f"**Reportes asociados:** "
                f"{len(report_ids)}"
            )


            confirmation = (
                st.text_input(
                    'Para confirmar escribí "ELIMINAR"',
                    key=(
                        f"delete_confirmation_"
                        f"{selected_manage_id}"
                    ),
                )
            )


            delete_player = (
                st.button(
                    "Eliminar jugador y todos sus reportes",
                    type="primary",
                    disabled=(
                        confirmation
                        != "ELIMINAR"
                    ),
                    key=(
                        f"delete_player_"
                        f"{selected_manage_id}"
                    ),
                )
            )


            if delete_player:

                # --------------------------------------------
                # Áreas y características de sus reportes
                # --------------------------------------------

                if report_ids:

                    repo.delete_where(
                        "areas_reporte",
                        "report_id",
                        report_ids,
                    )

                    repo.delete_where(
                        "caracteristicas",
                        "report_id",
                        report_ids,
                    )


                # --------------------------------------------
                # Reportes
                # --------------------------------------------

                repo.delete_where(
                    "reportes",
                    "player_id",
                    selected_manage_id,
                )


                # --------------------------------------------
                # Informe final
                # --------------------------------------------

                repo.delete_where(
                    "informes_finales",
                    "player_id",
                    selected_manage_id,
                )


                # --------------------------------------------
                # Jugador
                # --------------------------------------------

                repo.delete_where(
                    "jugadores",
                    "player_id",
                    selected_manage_id,
                )


                st.success(
                    "Jugador y todos sus datos asociados eliminados correctamente."
                )

                st.cache_data.clear()

                st.rerun()
