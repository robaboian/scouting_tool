# Scouting Tool MVP

Aplicación de Streamlit con tres páginas:

1. **Explorador de jugadores**
2. **Crear jugador / reporte**
3. **Informes finales**

## Ejecución local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Sin credenciales, la aplicación usa archivos CSV dentro de `data/`.

## Conexión con Google Sheets

1. Crear un proyecto en Google Cloud.
2. Activar Google Sheets API y Google Drive API.
3. Crear una cuenta de servicio.
4. Descargar sus credenciales JSON.
5. Crear un Google Sheet.
6. Compartir el Sheet con el correo `client_email` de la cuenta de servicio.
7. Copiar `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml`.
8. Completar el ID del Sheet y las credenciales.

La aplicación crea automáticamente estas pestañas si no existen:

- `jugadores`
- `reportes`
- `areas_reporte`
- `caracteristicas`
- `informes_finales`

## Notas

- Los nombres no funcionan como claves: cada entidad recibe un ID único.
- Un jugador puede tener múltiples reportes.
- El informe final se guarda por separado.
- La exportación inicial está implementada en Word.
- Para producción conviene agregar autenticación antes de habilitar la edición.
