import pandas as pd
import streamlit as st

from config import FINAL_REPORT_STATUS
from data_access import get_repository, make_id, now_iso
from utils import build_final_report_docx, player_label

st.set_page_config(page_title="Informes", page_icon="📄", layout="wide")
repo = get_repository()

players = repo.read("jugadores")
reports = repo.read("reportes")
areas = repo.read("areas_reporte")
characteristics = repo.read("caracteristicas")
final_reports = repo.read("informes_finales")

st.title("📄 Informes finales")

if players.empty or reports.empty:
    st.info("Se necesita al menos un jugador con un reporte guardado.")
    st.stop()

eligible_ids = sorted(set(players["player_id"]).intersection(set(reports["player_id"])))
eligible = players[players["player_id"].isin(eligible_ids)].copy()

selected_id = st.selectbox(
    "Jugador",
    eligible["player_id"].tolist(),
    format_func=lambda pid: player_label(eligible.loc[eligible["player_id"] == pid].iloc[0]),
)
player = eligible.loc[eligible["player_id"] == selected_id].iloc[0].to_dict()
player_reports = reports[reports["player_id"] == selected_id].copy()
report_ids = player_reports["report_id"].tolist()

left, right = st.columns([0.9, 1.4], gap="large")

with left:
    st.subheader("Antecedentes")
    st.caption(f"{len(player_reports)} reportes disponibles")

    for _, report in player_reports.sort_values("fecha_observacion", ascending=False).iterrows():
        with st.expander(f'{report["fecha_observacion"]} | vs. {report["rival"]}'):
            st.write(f'**Scout:** {report["scout"]}')
            st.write(f'**Valoración:** {report["valoracion_general"]}/5')
            st.write(f'**Recomendación:** {report["recomendacion"]}')
            if report["observaciones"]:
                st.write(report["observaciones"])

            report_areas = areas[areas["report_id"] == report["report_id"]]
            if not report_areas.empty:
                for area_type in ["Área consolidada", "Área de mejora"]:
                    values = report_areas[report_areas["tipo"] == area_type]["descripcion"].tolist()
                    if values:
                        st.markdown(f"**{area_type}**")
                        st.write("\n".join(f"- {x}" for x in values))

    player_chars = characteristics[characteristics["report_id"].isin(report_ids)]
    if not player_chars.empty:
        st.markdown("#### Características observadas")
        st.dataframe(
            player_chars[["categoria", "caracteristica", "valoracion"]],
            use_container_width=True,
            hide_index=True,
        )

existing = final_reports[final_reports["player_id"] == selected_id]
if existing.empty:
    current = {
        "final_report_id": make_id("FIN"),
        "player_id": selected_id,
        "estado": "Borrador",
        "observaciones": "",
        "perfil_fisico": "",
        "perfil_tactico": "",
        "perfil_tecnico": "",
        "perfil_mental": "",
        "fases_juego": "",
        "areas_consolidadas": "",
        "areas_mejora": "",
        "conclusion": "",
        "caracteristicas_determinantes": "",
        "enlaces_video": "",
        "autor": "",
        "fecha_creacion": now_iso(),
        "fecha_modificacion": now_iso(),
    }
else:
    current = existing.sort_values("fecha_modificacion", ascending=False).iloc[0].to_dict()

with right:
    st.subheader("Redacción final")
    with st.form("final_report_form"):
        estado = st.selectbox(
            "Estado",
            FINAL_REPORT_STATUS,
            index=FINAL_REPORT_STATUS.index(current.get("estado", "Borrador"))
            if current.get("estado", "Borrador") in FINAL_REPORT_STATUS else 0,
        )
        observaciones = st.text_area("Observaciones generales", current.get("observaciones", ""), height=110)
        perfil_fisico = st.text_area("Perfil físico", current.get("perfil_fisico", ""), height=110)
        perfil_tactico = st.text_area("Perfil táctico", current.get("perfil_tactico", ""), height=110)
        perfil_tecnico = st.text_area("Perfil técnico", current.get("perfil_tecnico", ""), height=110)
        perfil_mental = st.text_area("Perfil mental", current.get("perfil_mental", ""), height=110)
        fases_juego = st.text_area("Fases del juego", current.get("fases_juego", ""), height=110)
        areas_consolidadas = st.text_area(
            "Áreas consolidadas", current.get("areas_consolidadas", ""),
            placeholder="Una por línea", height=100
        )
        areas_mejora = st.text_area(
            "Áreas de mejora", current.get("areas_mejora", ""),
            placeholder="Una por línea", height=100
        )
        conclusion = st.text_area("Conclusión", current.get("conclusion", ""), height=160)
        caracteristicas_determinantes = st.text_area(
            "Características determinantes",
            current.get("caracteristicas_determinantes", ""),
            height=120,
        )
        enlaces_video = st.text_area(
            "Enlaces de video",
            current.get("enlaces_video", ""),
            placeholder="Uno por línea",
            height=90,
        )
        autor = st.text_input("Autor", current.get("autor", ""))

        save = st.form_submit_button("Guardar informe", type="primary")

    payload = {
        "final_report_id": current["final_report_id"],
        "player_id": selected_id,
        "estado": estado,
        "observaciones": observaciones,
        "perfil_fisico": perfil_fisico,
        "perfil_tactico": perfil_tactico,
        "perfil_tecnico": perfil_tecnico,
        "perfil_mental": perfil_mental,
        "fases_juego": fases_juego,
        "areas_consolidadas": areas_consolidadas,
        "areas_mejora": areas_mejora,
        "conclusion": conclusion,
        "caracteristicas_determinantes": caracteristicas_determinantes,
        "enlaces_video": enlaces_video,
        "autor": autor,
        "fecha_creacion": current.get("fecha_creacion") or now_iso(),
        "fecha_modificacion": now_iso(),
    }

    if save:
        repo.upsert("informes_finales", payload, key="final_report_id")
        st.success("Informe guardado correctamente.")
        st.cache_data.clear()

    st.download_button(
        "Exportar a Word",
        data=build_final_report_docx(player, payload),
        file_name=f'informe_{player["nombre"].lower().replace(" ", "_")}.docx',
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )
