import pandas as pd
import streamlit as st

from data_access import get_repository
from utils import calculate_age, player_label

st.set_page_config(page_title="Explorador", page_icon="🔍", layout="wide")
repo = get_repository()

players = repo.read("jugadores")
reports = repo.read("reportes")
final_reports = repo.read("informes_finales")

st.title("🔍 Explorador de jugadores")

if players.empty:
    st.info("Todavía no hay jugadores cargados.")
    st.stop()

players["edad"] = players["fecha_nacimiento"].apply(calculate_age)

if not reports.empty:
    report_counts = (
        reports.groupby("player_id")
        .size()
        .reset_index(name="cantidad_reportes")
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

with st.expander("Filtros", expanded=True):
    c1, c2, c3, c4 = st.columns(4)
    search = c1.text_input("Nombre")
    clubs = sorted([x for x in players["club"].unique() if x])
    club = c2.selectbox("Club", ["Todos"] + clubs)
    positions = sorted([x for x in players["posicion_principal"].unique() if x])
    position = c3.selectbox("Posición", ["Todas"] + positions)
    foot_options = sorted([x for x in players["pie"].unique() if x])
    foot = c4.selectbox("Pie", ["Todos"] + foot_options)

    c5, c6, c7 = st.columns(3)
    competitions = sorted([x for x in players["competicion"].unique() if x])
    competition = c5.selectbox("Competición", ["Todas"] + competitions)
    min_reports = c6.number_input("Cantidad mínima de reportes", min_value=0, value=0)
    status_options = sorted([x for x in players["estado"].unique() if x])
    status = c7.selectbox("Estado", ["Todos"] + status_options)

filtered = players.copy()
if search:
    filtered = filtered[filtered["nombre"].str.contains(search, case=False, na=False)]
if club != "Todos":
    filtered = filtered[filtered["club"] == club]
if position != "Todas":
    filtered = filtered[filtered["posicion_principal"] == position]
if foot != "Todos":
    filtered = filtered[filtered["pie"] == foot]
if competition != "Todas":
    filtered = filtered[filtered["competicion"] == competition]
if status != "Todos":
    filtered = filtered[filtered["estado"] == status]
filtered = filtered[filtered["cantidad_reportes"] >= min_reports]

st.caption(f"{len(filtered)} jugadores encontrados")

if filtered.empty:
    st.warning("No se encontraron jugadores con esos filtros.")
    st.stop()

selected_id = st.selectbox(
    "Seleccionar jugador",
    filtered["player_id"].tolist(),
    format_func=lambda pid: player_label(filtered.loc[filtered["player_id"] == pid].iloc[0]),
)

player = filtered.loc[filtered["player_id"] == selected_id].iloc[0]

st.divider()
st.subheader(player["nombre"])

m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Club", player["club"] or "—")
m2.metric("Edad", player["edad"] or "—")
m3.metric("Posición", player["posicion_principal"] or "—")
m4.metric("Pie", player["pie"] or "—")
m5.metric("Altura", f'{player["altura"]} cm' if player["altura"] else "—")
m6.metric("Reportes", int(player["cantidad_reportes"]))

player_reports = reports[reports["player_id"] == selected_id].copy()

st.subheader("Reportes por partido")
if player_reports.empty:
    st.info("Este jugador todavía no tiene reportes.")
else:
    player_reports = player_reports.sort_values("fecha_observacion", ascending=False)
    for _, report in player_reports.iterrows():
        title = f'{report["fecha_observacion"]} | {report["equipo"]} vs. {report["rival"]}'
        with st.expander(title):
            c1, c2, c3, c4 = st.columns(4)
            c1.write(f'**Scout:** {report["scout"] or "—"}')
            c2.write(f'**Posición:** {report["posicion_observada"] or "—"}')
            c3.write(f'**Valoración:** {report["valoracion_general"] or "—"}/5')
            c4.write(f'**Recomendación:** {report["recomendacion"] or "—"}')

            sections = [
                ("Observaciones", "observaciones"),
                ("Perfil físico", "perfil_fisico"),
                ("Perfil táctico", "perfil_tactico"),
                ("Perfil técnico", "perfil_tecnico"),
                ("Perfil mental", "perfil_mental"),
                ("Fases del juego", "fases_juego"),
            ]
            for label, field in sections:
                if report[field]:
                    st.markdown(f"**{label}**")
                    st.write(report[field])

            if report["video_url"]:
                st.link_button("Abrir video", report["video_url"])

st.subheader("Informe final")
player_final = final_reports[final_reports["player_id"] == selected_id]
if player_final.empty:
    st.info("Todavía no se creó una conclusión final.")
else:
    final = player_final.sort_values("fecha_modificacion", ascending=False).iloc[0]
    st.write(f'**Estado:** {final["estado"]}')
    st.write(f'**Última modificación:** {final["fecha_modificacion"]}')
    if final["conclusion"]:
        st.markdown("**Conclusión**")
        st.write(final["conclusion"])
