import sqlite3
import pandas as pd

# ---------------- CONEXIÓN ----------------
conn = sqlite3.connect("seleccion_personal.db")

# ---------------- CONSULTA COMPLETA ----------------
df = pd.read_sql_query("""
    SELECT
        id,
        nombre_completo,
        cargo_postula,
        edad,
        estado_civil,
        hijos,
        formacion_tercer_nivel,
        titulo_cuarto_nivel,
        anos_experiencia,
        empresa,
        cargo,
        actividades,
        sueldo_ultimo,
        motivo_salida,
        disponibilidad,
        observaciones
    FROM candidatos
    ORDER BY id DESC
""", conn)

conn.close()

# ---------------- MOSTRAR EN CONSOLA (SE MANTIENE) ----------------
print("\n📋 CANDIDATOS REGISTRADOS (DETALLE COMPLETO):\n")
print(df.to_string(index=False))

# ---------------- EXPORTAR A EXCEL ----------------
try:
    cantidad = int(input("\n👉 ¿Cuántos últimos candidatos desea exportar a Excel?: "))
except ValueError:
    cantidad = 3

df_exportar = df.head(cantidad)

nombre_archivo = "candidatos_ultimos.xlsx"

df_exportar.to_excel(
    nombre_archivo,
    index=False,
    sheet_name="Candidatos"
)

print(f"\n✅ Excel generado correctamente: {nombre_archivo}")
print("📂 Ubicación: misma carpeta donde ejecutó el script")
