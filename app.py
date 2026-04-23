import streamlit as st
import sqlite3
import pandas as pd
from io import BytesIO
from referencias import modulo_referencias   # ✅ IMPORT CORRECTO

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(page_title="Sistema de Selección", layout="wide")

# ---------------- ESTILO PROFESIONAL ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #f1f5f9;
}

section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

div[role="radiogroup"] label {
    color: #ffffff !important;
    font-weight: 500;
}

h1, h2, h3 {
    color: #facc15;
}

label {
    color: #e2e8f0 !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #1e293b !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 8px;
}

.stSelectbox div {
    background-color: #1e293b !important;
    color: #ffffff !important;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}

[data-testid="stDataFrame"] {
    background-color: #1e293b;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CONEXIÓN ----------------
conn = sqlite3.connect("seleccion_personal.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- MENÚ ----------------
st.sidebar.title("📂 Menú")

menu = st.sidebar.radio(
    "Seleccione una opción",
    [
        "➕ Registrar candidato",
        "📋 Ver candidatos",
        "✏️ Editar candidato",
        "📞 Referencias laborales"   # ✅ NUEVO
    ]
)

# =================================================
# ➕ REGISTRAR CANDIDATO
# =================================================
if menu == "➕ Registrar candidato":

    st.title("📋 Registro completo de Candidatos")

    with st.form("form_candidato"):

        st.subheader("🧑 Datos personales")
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", 18, 80)
        estado_civil = st.selectbox(
            "Estado civil",
            ["Soltero/a", "Casado/a", "Unión libre", "Divorciado/a", "Viudo/a"]
        )
        hijos = st.number_input("Número de hijos", 0, 10)

        st.subheader("🎓 Formación académica")
        formacion_tercer = st.selectbox("Formación tercer nivel", ["Sí", "No"])
        titulo_cuarto = st.text_input("Título de cuarto nivel")

        st.subheader("💼 Experiencia laboral")
        anos_experiencia = st.number_input("Años de experiencia", 0, 40)
        empresa = st.text_input("Última empresa")
        cargo = st.text_input("Último cargo")
        actividades = st.text_area("Actividades realizadas")
        sueldo_ultimo = st.number_input("Último sueldo", min_value=0.0, step=10.0)
        motivo_salida = st.text_input("Motivo de salida")

        st.subheader("📌 Postulación")
        cargo_postula = st.text_input("Cargo al que postula")
        disponibilidad = st.selectbox(
            "Disponibilidad",
            ["Inmediata", "15 días", "30 días", "A convenir"]
        )

        observaciones = st.text_area("Observaciones")

        guardar = st.form_submit_button("💾 Guardar candidato")

    if guardar:
        cursor.execute("""
            INSERT INTO candidatos (
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
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            cargo_postula,
            edad,
            estado_civil,
            hijos,
            formacion_tercer,
            titulo_cuarto,
            anos_experiencia,
            empresa,
            cargo,
            actividades,
            sueldo_ultimo,
            motivo_salida,
            disponibilidad,
            observaciones
        ))

        conn.commit()
        st.success("✅ Candidato registrado correctamente")

# =================================================
# 📋 VER CANDIDATOS
# =================================================
elif menu == "📋 Ver candidatos":

    st.title("📋 Candidatos registrados")

    df = pd.read_sql_query("""
        SELECT *
        FROM candidatos
        ORDER BY id DESC
    """, conn)

    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("⬇️ Exportar a Excel")

    if not df.empty:
        cantidad = st.number_input(
            "¿Cuántos candidatos deseas descargar?",
            min_value=1,
            max_value=len(df),
            value=3
        )

        df_exportar = df.head(cantidad)

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_exportar.to_excel(writer, index=False)

        st.download_button(
            label="📥 Descargar Excel",
            data=output.getvalue(),
            file_name="candidatos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# =================================================
# ✏️ EDITAR CANDIDATO
# =================================================
elif menu == "✏️ Editar candidato":

    st.title("✏️ Editar candidato")

    df = pd.read_sql("SELECT * FROM candidatos", conn)

    if df.empty:
        st.warning("No hay candidatos registrados")

    else:
        candidato = st.selectbox(
            "Seleccione un candidato",
            df["nombre_completo"]
        )

        fila = df[df["nombre_completo"] == candidato].iloc[0]

        with st.form("editar"):

            edad = st.number_input(
                "Edad",
                min_value=18,
                max_value=80,
                value=int(fila["edad"]) if pd.notnull(fila["edad"]) else 18
            )

            estado = st.text_input(
                "Estado civil",
                fila["estado_civil"] if pd.notnull(fila["estado_civil"]) else ""
            )

            cargo_postula = st.text_input(
                "Cargo al que postula",
                fila["cargo_postula"] if pd.notnull(fila["cargo_postula"]) else ""
            )

            experiencia = st.number_input(
                "Años experiencia",
                min_value=0,
                max_value=40,
                value=int(fila["anos_experiencia"]) if pd.notnull(fila["anos_experiencia"]) else 0
            )

            observaciones = st.text_area(
                "Observaciones",
                fila["observaciones"] if pd.notnull(fila["observaciones"]) else ""
            )

            guardar = st.form_submit_button("💾 Guardar cambios")

        if guardar:
            cursor.execute("""
                UPDATE candidatos SET
                    edad = ?,
                    estado_civil = ?,
                    cargo_postula = ?,
                    anos_experiencia = ?,
                    observaciones = ?
                WHERE id = ?
            """, (
                edad,
                estado,
                cargo_postula,
                experiencia,
                observaciones,
                fila["id"]
            ))

            conn.commit()
            st.success("✅ Candidato actualizado correctamente")

# =================================================
# 📞 REFERENCIAS LABORALES
# =================================================
elif menu == "📞 Referencias laborales":
    modulo_referencias()   # ✅ LLAMADA AL MÓDULO

# ---------------- CIERRE ----------------
conn.close()