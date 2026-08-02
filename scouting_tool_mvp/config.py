import streamlit as st

APP_TITLE = "Scouting Tool"

POSITIONS = [
    "Arquero",
    "Lateral derecho",
    "Defensor central",
    "Lateral izquierdo",
    "Mediocentro defensivo",
    "Mediocentro",
    "Interior",
    "Mediapunta",
    "Extremo derecho",
    "Extremo izquierdo",
    "Delantero centro",
]

FEET = ["Derecho", "Izquierdo", "Ambidiestro", "Sin definir"]

REPORT_RECOMMENDATIONS = [
    "Descartar",
    "Continuar seguimiento",
    "Priorizar seguimiento",
    "Recomendar",
]

REPORT_TYPES = [
    "Partido completo",
    "Partido parcial",
    "Video",
    "Entrenamiento",
    "Otro",
]

FINAL_REPORT_STATUS = ["Borrador", "Definitivo"]

CHARACTERISTIC_CATEGORIES = [
    "Físico",
    "Táctico",
    "Técnico",
    "Mental",
    "Biotipo",
    "Fases del juego",
]

CHARACTERISTIC_RATINGS = [
    "Muy bajo",
    "Bajo",
    "Aceptable",
    "Bueno",
    "Muy bueno",
    "Destacado",
    "No observado",
]


def using_google_sheets() -> bool:
    return bool(st.secrets.get("google_sheets", {}).get("spreadsheet_id"))
