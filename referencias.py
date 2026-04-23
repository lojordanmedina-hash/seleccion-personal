import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO

def modulo_referencias():

    conn = sqlite3.connect("seleccion_personal.db", check_same_thread=False)
    cursor = conn.cursor()

    # ---------------- CREAR TABLA ----------------
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

    st.title("📞 Referencias laborales")

    # ---------------- CANDIDATOS ----------------
    df_candidatos = pd.read_sql(
        "SELECT id, nombre_completo FROM candidatos",
        conn
    )

    if df_candidatos.empty:
        st.warning("No hay candidatos registrados")
        conn.close()
        return

    candidato = st.selectbox(
        "Seleccione candidato",
        df_candidatos["nombre_completo"]
    )

    candidato_id = df_candidatos[
        df_candidatos["nombre_completo"] == candidato
    ]["id"].values[0]

    # ---------------- FORMULARIO ----------------
    with st.form("form_referencias"):

        empresa = st.text_input("Empresa donde trabajó")

        nombre_ref = st.text_input("Nombre del referente")
        cargo_ref = st.text_input("Cargo del referente")
        telefono = st.text_input("Teléfono")

        relacion = st.text_input("Relación (jefe, colega, etc.)")

        st.subheader("Evaluación del referente")

        desempeno = st.text_area("Desempeño del candidato")
        equipo = st.text_area("Trabajo en equipo")
        valores = st.text_area("Valores personales")

        recomendacion = st.selectbox(
            "¿Recomienda su contratación?",
            ["SI", "NO", "CON RESERVAS"]
        )

        guardar = st.form_submit_button("💾 Guardar referencia")

    # ---------------- GUARDAR ----------------
    if guardar:
        cursor.execute("""
            INSERT INTO referencias (
                candidato_id,
                empresa,
                nombre_referente,
                cargo_referente,
                telefono,
                relacion,
                desempeno,
                trabajo_equipo,
                valores,
                recomendacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidato_id,
            empresa,
            nombre_ref,
            cargo_ref,
            telefono,
            relacion,
            desempeno,
            equipo,
            valores,
            recomendacion
        ))

        conn.commit()
        st.success("✅ Referencia guardada correctamente")

    # ---------------- MOSTRAR DATOS ----------------
    st.divider()
    st.subheader("📋 Referencias registradas")

    try:
        df_ref = pd.read_sql(f"""
            SELECT
                r.empresa,
                r.nombre_referente,
                r.cargo_referente,
                r.telefono,
                r.relacion,
                r.recomendacion
            FROM referencias r
            WHERE r.candidato_id = {candidato_id}
            ORDER BY r.id DESC
        """, conn)

        if df_ref.empty:
            st.info("Este candidato aún no tiene referencias registradas")
        else:
            st.dataframe(df_ref, use_container_width=True)

            # ---------------- DESCARGAR EXCEL ----------------
            st.divider()
            st.subheader("⬇️ Descargar referencias")

            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df_ref.to_excel(writer, index=False, sheet_name="Referencias")

            st.download_button(
                label="📥 Descargar Excel de referencias",
                data=output.getvalue(),
                file_name=f"referencias_{candidato}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"Error al cargar referencias: {e}")

    conn.close()