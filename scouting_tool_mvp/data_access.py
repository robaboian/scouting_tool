from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable
from uuid import uuid4

import pandas as pd
import streamlit as st

from config import using_google_sheets

DATA_DIR = Path(__file__).resolve().parent / "data"

TABLE_COLUMNS = {
    "jugadores": [
        "player_id", "nombre", "fecha_nacimiento", "nacionalidad", "club",
        "competicion", "posicion_principal", "posicion_secundaria", "pie",
        "altura", "peso", "fin_contrato", "enlace_externo", "estado",
        "fecha_creacion", "creado_por",
    ],
    "reportes": [
        "report_id", "player_id", "fecha_observacion", "equipo", "rival",
        "competicion", "tipo_observacion", "minutos_observados",
        "posicion_observada", "scout", "observaciones", "perfil_fisico",
        "perfil_tactico", "perfil_tecnico", "perfil_mental", "fases_juego",
        "valoracion_general", "recomendacion", "video_url", "fecha_carga",
    ],
    "areas_reporte": [
        "area_id", "report_id", "tipo", "descripcion",
    ],
    "caracteristicas": [
        "characteristic_id", "report_id", "categoria", "caracteristica",
        "valoracion",
    ],
    "informes_finales": [
        "final_report_id", "player_id", "estado", "observaciones",
        "perfil_fisico", "perfil_tactico", "perfil_tecnico", "perfil_mental",
        "fases_juego", "areas_consolidadas", "areas_mejora", "conclusion",
        "caracteristicas_determinantes", "enlaces_video", "autor",
        "fecha_creacion", "fecha_modificacion",
    ],
}


def make_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8].upper()}"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


class LocalCSVRepository:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._ensure_tables()

    def _path(self, table: str) -> Path:
        return self.data_dir / f"{table}.csv"

    def _ensure_tables(self) -> None:
        for table, columns in TABLE_COLUMNS.items():
            path = self._path(table)
            if not path.exists():
                pd.DataFrame(columns=columns).to_csv(path, index=False)

    def read(self, table: str) -> pd.DataFrame:
        path = self._path(table)
        try:
            df = pd.read_csv(path, dtype=str).fillna("")
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=TABLE_COLUMNS[table])
        for column in TABLE_COLUMNS[table]:
            if column not in df.columns:
                df[column] = ""
        return df[TABLE_COLUMNS[table]]

    def append(self, table: str, rows: Iterable[dict]) -> None:
        rows = list(rows)
        if not rows:
            return
        current = self.read(table)
        incoming = pd.DataFrame(rows)
        for column in TABLE_COLUMNS[table]:
            if column not in incoming.columns:
                incoming[column] = ""
        updated = pd.concat([current, incoming[TABLE_COLUMNS[table]]], ignore_index=True)
        updated.to_csv(self._path(table), index=False)

    def upsert(self, table: str, row: dict, key: str) -> None:
        current = self.read(table)
        value = str(row[key])
        if key in current.columns and (current[key].astype(str) == value).any():
            idx = current.index[current[key].astype(str) == value][0]
            for column in TABLE_COLUMNS[table]:
                current.loc[idx, column] = str(row.get(column, current.loc[idx, column]))
        else:
            incoming = {column: str(row.get(column, "")) for column in TABLE_COLUMNS[table]}
            current = pd.concat([current, pd.DataFrame([incoming])], ignore_index=True)
        current.to_csv(self._path(table), index=False)


class GoogleSheetsRepository:
    def __init__(self):
        import gspread
        from google.oauth2.service_account import Credentials

        settings = st.secrets["google_sheets"]
        credentials = Credentials.from_service_account_info(
            dict(st.secrets["gcp_service_account"]),
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ],
        )
        client = gspread.authorize(credentials)
        self.book = client.open_by_key(settings["spreadsheet_id"])
        self._ensure_tables()

    def _worksheet(self, table: str):
        return self.book.worksheet(table)

    def _ensure_tables(self):
        existing = {ws.title for ws in self.book.worksheets()}
        for table, columns in TABLE_COLUMNS.items():
            if table not in existing:
                ws = self.book.add_worksheet(title=table, rows=1000, cols=max(20, len(columns)))
                ws.append_row(columns)

    def read(self, table: str) -> pd.DataFrame:
        records = self._worksheet(table).get_all_records()
        df = pd.DataFrame(records)
        for column in TABLE_COLUMNS[table]:
            if column not in df.columns:
                df[column] = ""
        return df[TABLE_COLUMNS[table]].astype(str).fillna("")

    def append(self, table: str, rows: Iterable[dict]) -> None:
        rows = list(rows)
        if not rows:
            return
        values = [
            [str(row.get(column, "")) for column in TABLE_COLUMNS[table]]
            for row in rows
        ]
        self._worksheet(table).append_rows(values, value_input_option="USER_ENTERED")

    def upsert(self, table: str, row: dict, key: str) -> None:
        ws = self._worksheet(table)
        df = self.read(table)
        value = str(row[key])

        payload = [str(row.get(column, "")) for column in TABLE_COLUMNS[table]]

        matches = df.index[df[key].astype(str) == value].tolist()
        if matches:
            sheet_row = matches[0] + 2
            ws.update(f"A{sheet_row}", [payload], value_input_option="USER_ENTERED")
        else:
            ws.append_row(payload, value_input_option="USER_ENTERED")


@st.cache_resource
def get_repository():
    if using_google_sheets():
        return GoogleSheetsRepository()
    return LocalCSVRepository()
