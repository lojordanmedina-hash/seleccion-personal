import streamlit as st
import sqlite3
import pandas as pd

def registro_candidatos():
    conn = sqlite3.connect("seleccion_personal.db", check_same_thread=False)
    cursor = conn.cursor()

    st.title("📋 Registro de Candidatos")

    with st.form("form_candidato"):
        col1, col2, col3 = st.columns(3)

        with col1:
            nombre = st.text_input("Nombre completo")
            edad = st.number_input("Edad", min_value=18, max_value=80)
            estado_civil = st.selectbox(
                "Estado civil",
                ["SOLTERO", "CASADO", "UNIÓN LIBRE", "DIVORCIADO"]
            )
            hijos = st.number_input("Hijos", min_value=0)

        with col2:
            cargo_postula = st.text_input("Cargo al que postula")
            titulo_tercer = st.selectbox("Título tercer nivel", ["SI", "NO"])
            titulo_cuarto = st.selectbox("Título cuarto nivel", ["SI", "NO"])
            anos_experiencia = st.number_input("Años de experiencia total", min_value=0)

        with col3:
            empresa = st.text_input("Última empresa")
            cargo = st.text_input("Último cargo desempeñado")
            sueldo = st.number_input("Último sueldo", min_value=0.0, step=50.0)
            disponibilidad = st.selectbox(
                "Disponibilidad",
                ["INMEDIATA", "15 DÍAS", "30 DÍAS"]
            )

        actividades = st.text_area("Actividades realizadas")
        motivo = st.text_area("Motivo de salida")
        observaciones = st.text_area("Observaciones")

        guardar = st.form_submit_button("💾 Guardar candidato")

    # ---------- GUARDAR EN BD ----------
    if guardar:
        cursor.execute("""
            INSERT INTO candidatos (
                nombre_completo,
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
                observaciones,
                cargo_postula
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            edad,
            estado_civil,
            hijos,
            titulo_tercer,
            titulo_cuarto,
            anos_experiencia,
            empresa,
            cargo,
            actividades,
            sueldo,
            motivo,
            disponibilidad,
            observaciones,
            cargo_postula
        ))

        conn.commit()
        st.success("✅ Candidato guardado correctamente")

    # ---------- TABLA TIPO EXCEL ----------
    st.divider()
    st.subheader("📊 Candidatos registrados")

    df = pd.read_sql("SELECT * FROM candidatos", conn)
    st.dataframe(df, use_container_width=True)

    conn.close()
