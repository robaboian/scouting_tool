import streamlit as st

st.set_page_config(
    page_title="Scouting Tool",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ Scouting Tool")
st.write(
    """
    Herramienta interna para registrar jugadores, cargar observaciones por partido
    y consolidar informes finales.
    """
)

st.info(
    """
    Utilizá el menú lateral para navegar:

    - **Explorador:** buscar jugadores y consultar sus reportes.
    - **Crear jugador / reporte:** dar de alta jugadores o agregar observaciones.
    - **Informes:** redactar, guardar y exportar conclusiones finales.
    """
)

st.subheader("Flujo de trabajo")
st.markdown(
    """
    **1. Crear** el jugador y registrar una primera observación.  
    **2. Consultar** su historial desde el explorador.  
    **3. Consolidar** los reportes en un informe final.
    """
)
