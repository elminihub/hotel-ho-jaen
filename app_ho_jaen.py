from datetime import date, datetime
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Gestión HO Ciudad de Jaén", page_icon="🏨", layout="wide"
)

st.title("🏨 HO Ciudad de Jaén - Operaciones y Cuadrante")

tab1, tab2, tab3 = st.tabs(
    [
        "📋 Agenda & Registro Eventos",
        "👥 Personal y Turnos (Maîtres/Camareros)",
        "📊 Resumen Operativo",
    ]
)

# Base de datos en sesión
if "eventos" not in st.session_state:
    st.session_state.eventos = [
        {
            "Fecha": "2026-11-02",
            "Hora": "13:30",
            "Evento": "Almuerzo Algeciras C.F.",
            "Salón": "Arrayanes",
            "Pax": 30,
            "Maitre": "Jamal",
            "Tipo": "Empresa",
        },
        {
            "Fecha": "2026-11-07",
            "Hora": "14:00",
            "Evento": "Enlace Ángela y José Antonio",
            "Salón": "Alcázar",
            "Pax": 198,
            "Maitre": "Jamal",
            "Tipo": "Boda",
        },
        {
            "Fecha": "2026-11-07",
            "Hora": "14:00",
            "Evento": "Enlace Manuel y Encarnación",
            "Salón": "Estrella",
            "Pax": 246,
            "Maitre": "Jamal",
            "Tipo": "Boda",
        },
        {
            "Fecha": "2026-11-07",
            "Hora": "14:00",
            "Evento": "Catering Colegio Gestores",
            "Salón": "Catering San Juan de Dios",
            "Pax": 64,
            "Maitre": "Por asignar",
            "Tipo": "Catering",
        },
    ]

if "personal" not in st.session_state:
    st.session_state.personal = [
        {
            "Nombre": "Jamal",
            "Rol": "Maître Principal",
            "Turno": "Sábado Mañana/Noche",
            "Evento Asignado": "Bodas Alcázar / Estrella",
            "Estado": "Confirmado",
        },
        {
            "Nombre": "Camarero Extra 1",
            "Rol": "Refuerzo Sala",
            "Turno": "Sábado 13:00 - 22:00",
            "Evento Asignado": "Boda Ángela y J.A.",
            "Estado": "Confirmado",
        },
        {
            "Nombre": "Camarero Extra 2",
            "Rol": "Refuerzo Sala",
            "Turno": "Sábado 13:00 - 22:00",
            "Evento Asignado": "Boda Manuel y Encarni",
            "Estado": "Pendiente",
        },
        {
            "Nombre": "Cortador de Jamón",
            "Rol": "Especialista",
            "Turno": "Sábado 14:00",
            "Evento Asignado": "Boda Ángela y J.A.",
            "Estado": "Confirmado",
        },
    ]

# TAB 1: REGISTRO Y MÓVIL
with tab1:
    st.header("➕ Registro Rápido de Nuevo Evento")
    with st.form("form_nuevo_evento", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha = st.date_input("Fecha del Evento", date(2026, 11, 7))
            hora = st.time_input("Hora de Inicio")
            nombre_evento = st.text_input("Nombre / Nombre del Cliente")
            salon = st.selectbox(
                "Salón / Ubicación",
                [
                    "Alcázar",
                    "Estrella",
                    "Arrayanes",
                    "Andújar",
                    "Linares",
                    "Bailén",
                    "Torredonjimeno",
                    "Catering Ext.",
                ],
            )
        with col2:
            pax = st.number_input(
                "Número de Comensales (Pax)", min_value=1, value=50
            )
            maitre = st.selectbox(
                "Maître Responsable", ["Jamal", "Juan", "Otro / Por Asignar"]
            )
            tipo = st.selectbox(
                "Tipo de Evento",
                [
                    "Boda",
                    "Comunión",
                    "Empresa / Formación",
                    "Catering",
                    "Grupo Turístico / Deportivo",
                ],
            )
            obs = st.text_area("Observaciones (Montaje, menús, extras...)")

        submitted = st.form_submit_button("💾 Guardar Evento en Agenda")
        if submitted:
            st.session_state.eventos.append({
                "Fecha": str(fecha),
                "Hora": str(hora),
                "Evento": nombre_evento,
                "Salón": salon,
                "Pax": pax,
                "Maitre": maitre,
                "Tipo": tipo,
            })
            st.success(f"¡Evento '{nombre_evento}' registrado correctamente!")

    st.markdown("---")
    st.subheader("📅 Eventos Programados")
    df_ev = pd.DataFrame(st.session_state.eventos)
    st.dataframe(df_ev, use_container_width=True)

# TAB 2: PERSONAL Y CUADRANTE DE TURNOS
with tab2:
    st.header("👥 Cuadrante y Gestión de Personal de Sala")

    col_p1, col_p2 = st.columns([1, 2])

    with col_p1:
        st.subheader("Asignar Personal / Extra")
        with st.form("form_personal"):
            nombre_p = st.text_input("Nombre del Empleado / Extra")
            rol = st.selectbox(
                "Puesto / Rol",
                [
                    "Maître",
                    "Camarero/a de Fijo",
                    "Camarero/a Extra",
                    "Cortador de Jamón",
                    "Limpieza / Limpiezas Aseos",
                ],
            )
            turno = st.text_input("Horario / Turno", "13:00 - 22:00")
            ev_asig = st.selectbox(
                "Evento Asignado",
                [e["Evento"] for e in st.session_state.eventos],
            )
            estado = st.radio(
                "Estado de Confirmación",
                ["Confirmado", "Pendiente", "Baja/Sustituido"],
            )

            sub_p = st.form_submit_button("📌 Asignar al Cuadrante")
            if sub_p:
                st.session_state.personal.append({
                    "Nombre": nombre_p,
                    "Rol": rol,
                    "Turno": turno,
                    "Evento Asignado": ev_asig,
                    "Estado": estado,
                })
                st.success(f"Asignación guardada para {nombre_p}.")

    with col_p2:
        st.subheader("📋 Lista de Personal Asignado por Servicio")
        df_pers = pd.DataFrame(st.session_state.personal)
        st.dataframe(df_pers, use_container_width=True)

        total_pax_sabado = sum([
            e["Pax"]
            for e in st.session_state.eventos
            if "2026-11-07" in e["Fecha"]
        ])
        st.info(
            f"💡 **Carga de Trabajo Sábado 07/11:** {total_pax_sabado} pax confirmados entre las dos bodas y el catering. Asegúrate de cubrir la ratio recomendada de camareros en sala."
        )

# TAB 3: RESUMEN OPERATIVO
with tab3:
    st.header("📊 Vista General del Servicio")
    st.metric("Total Eventos Registrados", len(st.session_state.eventos))
    st.metric("Personal en Cuadrante", len(st.session_state.personal))
