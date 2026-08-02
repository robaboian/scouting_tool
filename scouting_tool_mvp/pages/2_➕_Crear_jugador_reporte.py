from datetime import date

import pandas as pd
import streamlit as st

from config import (
    FEET, POSITIONS, REPORT_RECOMMENDATIONS, REPORT_TYPES,
    CHARACTERISTIC_CATEGORIES, CHARACTERISTIC_RATINGS,
)
from data_access import get_repository, make_id, now_iso
from utils import player_label

st.set_page_config(page_title="Crear jugador / reporte", page_icon="➕", layout="wide")
repo = get_repository()

st.title("➕ Crear jugador / reporte")

players = repo.read("jugadores")

tab_new, tab_existing = st.tabs(["Crear jugador nuevo", "Agregar reporte a jugador existente"])

with tab_new:
    st.subheader("Datos del jugador")
    with st.form("new_player_form", clear_on_submit=False):
        c1, c2, c3 = st.columns(3)
        nombre = c1.text_input("Nombre completo *")
        fecha_nacimiento = c2.date_input("Fecha de nacimiento", value=None)
        nacionalidad = c3.text_input("Nacionalidad")

        c4, c5, c6 = st.columns(3)
        club = c4.text_input("Club actual *")
        competicion = c5.text_input("Competición")
        posicion_principal = c6.selectbox("Posición principal *", POSITIONS)

        c7, c8, c9 = st.columns(3)
        posicion_secundaria = c7.selectbox("Posición secundaria", [""] + POSITIONS)
        pie = c8.selectbox("Pie hábil", FEET)
        altura = c9.number_input("Altura (cm)", min_value=0, max_value=230, value=0)

        c10, c11, c12 = st.columns(3)
        peso = c10.number_input("Peso (kg)", min_value=0, max_value=180, value=0)
        fin_contrato = c11.date_input("Fin de contrato", value=None)
        estado = c12.selectbox("Estado", ["Seguimiento activo", "Pendiente", "Cerrado"])

        enlace_externo = st.text_input("Enlace externo")
        creado_por = st.text_input("Creado por")

        submitted = st.form_submit_button("Crear jugador", type="primary")

    if submitted:
        if not nombre.strip() or not club.strip():
            st.error("Nombre y club son obligatorios.")
        else:
            possible = players[
                players["nombre"].str.lower().str.strip().eq(nombre.lower().strip())
            ] if not players.empty else pd.DataFrame()

            if not possible.empty:
                st.warning("Ya existe un jugador con el mismo nombre. Revisá la pestaña de jugador existente.")
            else:
                player_id = make_id("PLY")
                repo.append("jugadores", [{
                    "player_id": player_id,
                    "nombre": nombre.strip(),
                    "fecha_nacimiento": fecha_nacimiento.isoformat() if fecha_nacimiento else "",
                    "nacionalidad": nacionalidad.strip(),
                    "club": club.strip(),
                    "competicion": competicion.strip(),
                    "posicion_principal": posicion_principal,
                    "posicion_secundaria": posicion_secundaria,
                    "pie": pie,
                    "altura": altura or "",
                    "peso": peso or "",
                    "fin_contrato": fin_contrato.isoformat() if fin_contrato else "",
                    "enlace_externo": enlace_externo.strip(),
                    "estado": estado,
                    "fecha_creacion": now_iso(),
                    "creado_por": creado_por.strip(),
                }])
                st.success(f"Jugador creado correctamente: {nombre}")
                st.info("Ahora podés agregarle un reporte desde la segunda pestaña.")
                st.cache_data.clear()

with tab_existing:
    players = repo.read("jugadores")
    if players.empty:
        st.info("Primero tenés que crear un jugador.")
        st.stop()

    selected_id = st.selectbox(
        "Buscar jugador",
        players["player_id"].tolist(),
        format_func=lambda pid: player_label(players.loc[players["player_id"] == pid].iloc[0]),
    )
    player = players.loc[players["player_id"] == selected_id].iloc[0]
    st.caption(f'{player["nombre"]} | {player["club"]} | {player["posicion_principal"]}')

    st.subheader("Nueva observación")
    with st.form("new_report_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        fecha = c1.date_input("Fecha de observación", value=date.today())
        equipo = c2.text_input("Equipo", value=player["club"])
        rival = c3.text_input("Rival *")

        c4, c5, c6 = st.columns(3)
        competicion = c4.text_input("Competición", value=player["competicion"])
        tipo = c5.selectbox("Tipo de observación", REPORT_TYPES)
        minutos = c6.number_input("Minutos observados", min_value=0, max_value=130, value=90)

        c7, c8 = st.columns(2)
        posicion = c7.selectbox(
            "Posición observada",
            POSITIONS,
            index=POSITIONS.index(player["posicion_principal"]) if player["posicion_principal"] in POSITIONS else 0,
        )
        scout = c8.text_input("Scout *")

        observaciones = st.text_area("Observaciones generales", height=100)
        perfil_fisico = st.text_area("Perfil físico", height=100)
        perfil_tactico = st.text_area("Perfil táctico", height=100)
        perfil_tecnico = st.text_area("Perfil técnico", height=100)
        perfil_mental = st.text_area("Perfil mental", height=100)
        fases_juego = st.text_area("Fases del juego", height=100)

        st.markdown("#### Áreas consolidadas y de mejora")
        fortalezas = st.text_area(
            "Áreas consolidadas",
            placeholder="Una por línea",
            height=100,
        )
        mejoras = st.text_area(
            "Áreas de mejora",
            placeholder="Una por línea",
            height=100,
        )

        st.markdown("#### Características determinantes")
        characteristics = st.data_editor(
            pd.DataFrame(
                [{"categoria": "", "caracteristica": "", "valoracion": ""}]
            ),
            column_config={
                "categoria": st.column_config.SelectboxColumn(
                    "Categoría", options=CHARACTERISTIC_CATEGORIES
                ),
                "caracteristica": st.column_config.TextColumn("Característica"),
                "valoracion": st.column_config.SelectboxColumn(
                    "Valoración", options=CHARACTERISTIC_RATINGS
                ),
            },
            num_rows="dynamic",
            use_container_width=True,
        )

        c9, c10 = st.columns(2)
        valoracion = c9.slider("Valoración general", 1, 5, 3)
        recomendacion = c10.selectbox("Recomendación", REPORT_RECOMMENDATIONS)

        video_url = st.text_input("Enlace de video")
        save_report = st.form_submit_button("Guardar reporte", type="primary")

    if save_report:
        if not rival.strip() or not scout.strip():
            st.error("Rival y scout son obligatorios.")
        else:
            report_id = make_id("REP")
            repo.append("reportes", [{
                "report_id": report_id,
                "player_id": selected_id,
                "fecha_observacion": fecha.isoformat(),
                "equipo": equipo.strip(),
                "rival": rival.strip(),
                "competicion": competicion.strip(),
                "tipo_observacion": tipo,
                "minutos_observados": minutos,
                "posicion_observada": posicion,
                "scout": scout.strip(),
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
            }])

            area_rows = []
            for line in fortalezas.splitlines():
                if line.strip():
                    area_rows.append({
                        "area_id": make_id("ARE"),
                        "report_id": report_id,
                        "tipo": "Área consolidada",
                        "descripcion": line.strip(),
                    })
            for line in mejoras.splitlines():
                if line.strip():
                    area_rows.append({
                        "area_id": make_id("ARE"),
                        "report_id": report_id,
                        "tipo": "Área de mejora",
                        "descripcion": line.strip(),
                    })
            repo.append("areas_reporte", area_rows)

            characteristic_rows = []
            for _, row in characteristics.fillna("").iterrows():
                if row["caracteristica"].strip():
                    characteristic_rows.append({
                        "characteristic_id": make_id("CHR"),
                        "report_id": report_id,
                        "categoria": row["categoria"],
                        "caracteristica": row["caracteristica"].strip(),
                        "valoracion": row["valoracion"],
                    })
            repo.append("caracteristicas", characteristic_rows)

            st.success(f"Reporte guardado para {player['nombre']}.")
            st.cache_data.clear()
