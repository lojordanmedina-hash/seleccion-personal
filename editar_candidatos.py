import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Editar Candidatos", layout="wide")

conn = sqlite3.connect("seleccion_personal.db", check_same_thread=False)

df = pd.read_sql("SELECT * FROM candidatos", conn)

st.title("✏️ Editar candidatos")

candidato = st.selectbox(
    "Seleccione un candidato",
    df["nombre_completo"]
)

fila = df[df["nombre_completo"] == candidato].iloc[0]

with st.form("editar"):
    edad = st.number_input("Edad", value=int(fila["edad"]))
    estado = st.text_input("Estado civil", fila["estado_civil"])
    cargo_postula = st.text_input("Cargo al que postula", fila["cargo_postula"])
    experiencia = st.text_input("Años experiencia", fila["anos_experiencia"])
    observaciones = st.text_area("Observaciones", fila["observaciones"])

    guardar = st.form_submit_button("💾 Guardar cambios")

if guardar:
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE candidatos SET
            edad = ?, estado_civil = ?, cargo_postula = ?,
            anos_experiencia = ?, observaciones = ?
        WHERE id = ?
    """, (
        edad, estado, cargo_postula,
        experiencia, observaciones,
        fila["id"]
    ))
    conn.commit()
    st.success("✅ Candidato actualizado")

conn.close()
