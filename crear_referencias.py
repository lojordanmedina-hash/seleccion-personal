import sqlite3

conn = sqlite3.connect("seleccion_personal.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS referencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidato_id INTEGER,
    empresa TEXT,
    nombre_referente TEXT,
    cargo_referente TEXT,
    telefono TEXT,
    relacion TEXT,
    desempeno TEXT,
    trabajo_equipo TEXT,
    valores TEXT,
    recomendacion TEXT
)
""")

conn.commit()
conn.close()

print("✅ Tabla referencias creada correctamente")