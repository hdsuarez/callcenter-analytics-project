# ==========================================================
# 📊 CALL CENTER ANALYTICS DASHBOARD (PRO VERSION)
# ==========================================================

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import streamlit as st
import pandas as pd

# ==========================================================
# CONFIGURACIÓN GENERAL DE LA APP
# ==========================================================

# Configuración principal del dashboard
st.set_page_config(
    page_title="Call Center Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CARGA DE DATOS
# ==========================================================

# @st.cache_data guarda los datos en memoria
# para que la app cargue más rápido

@st.cache_data
def load_data():

    # ======================================================
    # IMPORTANTE:
    # Como app.py está dentro de la carpeta /app
    # usamos ../ para salir una carpeta atrás
    # y entrar a /data
    # ======================================================

    df = pd.read_csv("/data/clean_interactions.csv")

    # Convertir fecha a formato datetime
    df["date"] = pd.to_datetime(df["date"])

    # Crear columna de mes
    df["mes"] = df["date"].dt.month_name()

    return df


# Cargar dataframe
df = load_data()

# ==========================================================
# SIDEBAR - FILTROS
# ==========================================================

st.sidebar.header("🔎 Filtros")

# ----------------------------------------------------------
# FILTRO MES
# ----------------------------------------------------------

mes = st.sidebar.multiselect(
    "Selecciona mes",
    options=df["mes"].unique(),
    default=df["mes"].unique()
)

# ----------------------------------------------------------
# FILTRO CANAL
# ----------------------------------------------------------

canal = st.sidebar.multiselect(
    "Selecciona canal",
    options=df["channel"].unique(),
    default=df["channel"].unique()
)

# ----------------------------------------------------------
# FILTRO AGENTE
# ----------------------------------------------------------

agente = st.sidebar.multiselect(
    "Selecciona agente",
    options=df["agent_name"].unique(),
    default=df["agent_name"].unique()
)

# ==========================================================
# APLICAR FILTROS
# ==========================================================

df_filtrado = df[
    (df["mes"].isin(mes)) &
    (df["channel"].isin(canal)) &
    (df["agent_name"].isin(agente))
]

# ==========================================================
# HEADER PRINCIPAL
# ==========================================================

st.title("📊 Call Center Analytics Dashboard")

st.markdown(
    """
    Dashboard interactivo para análisis de operaciones,
    rendimiento de agentes y métricas SLA.
    """
)

# ==========================================================
# KPIs PRINCIPALES
# ==========================================================

# ----------------------------------------------------------
# TOTAL INTERACCIONES
# ----------------------------------------------------------

total_interacciones = df_filtrado["interaction_id"].count()

# ----------------------------------------------------------
# HANDLE TIME PROMEDIO
# ----------------------------------------------------------

avg_handle = df_filtrado["handle_time_seconds"].mean()

# ----------------------------------------------------------
# WAIT TIME PROMEDIO
# ----------------------------------------------------------

avg_wait = df_filtrado["wait_time_seconds"].mean()

# ----------------------------------------------------------
# SLA GENERAL
# ----------------------------------------------------------

# True = 1
# False = 0
# mean() convierte automáticamente a porcentaje

sla_general = round(df_filtrado["sla_ok"].mean() * 100, 2)

# ============================================
# MÉTRICAS OPERATIVAS
# ============================================

# Interacciones atendidas
attended = df_filtrado[df_filtrado["status"] == "Attended"].shape[0]

# Interacciones abandonadas
abandoned = df_filtrado[df_filtrado["status"] == "Abandoned"].shape[0]

# Abandon Rate (%)
abandon_rate = round((abandoned / total_interacciones) * 100, 2)

# ==========================================================
# CREAR COLUMNAS KPI
# ==========================================================

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)


# KPI 1
col1.metric(
    "Total Interacciones",
    total_interacciones
)

# KPI 2
col2.metric(
    "Avg Handle Time (s)",
    round(avg_handle, 2)
)

# KPI 3
col3.metric(
    "Avg Wait Time (s)",
    round(avg_wait, 2)
)

# KPI 4
col4.metric(
    "SLA (%)",
    f"{sla_general}%"
)

# KPI 5
col5.metric(
    "Atendidas",
    attended
)

# KPI 6
col6.metric(
    "Abandonadas",
    abandoned
)

# ==========================================================
# SEPARADOR VISUAL
# ==========================================================

st.markdown("---")

st.subheader("📉 Métricas Operativas")

st.write(f"✅ Abandon Rate: {abandon_rate}%")



# ==========================================================
# PRIMERA FILA DE GRÁFICOS
# ==========================================================

col1, col2 = st.columns(2)

# ==========================================================
# GRÁFICO: CARGA POR AGENTE
# ==========================================================

with col1:

    st.subheader("📊 Carga de trabajo por agente")

    interacciones_agente = (
        df_filtrado
        .groupby("agent_name")["interaction_id"]
        .count()
        .sort_values(ascending=False)
    )

    st.bar_chart(interacciones_agente)

# ==========================================================
# GRÁFICO: DISTRIBUCIÓN POR CANAL
# ==========================================================

with col2:

    st.subheader("📞 Distribución por canal")

    interacciones_canal = (
        df_filtrado
        .groupby("channel")["interaction_id"]
        .count()
    )

    # Mostrar tabla simple
    st.dataframe(interacciones_canal)

# ==========================================================
# SEGUNDA FILA DE VISUALIZACIONES
# ==========================================================

col3, col4 = st.columns(2)

# ==========================================================
# GRÁFICO: INTERACCIONES POR MES
# ==========================================================

with col3:

    st.subheader("📈 Interacciones por mes")

    interacciones_mes = (
        df_filtrado
        .groupby("mes")["interaction_id"]
        .count()
    )

    st.line_chart(interacciones_mes)

# ==========================================================
# TABLA DETALLADA
# ==========================================================

with col4:

    st.subheader("📋 Datos filtrados")

    st.dataframe(df_filtrado)

# ==========================================================
# INSIGHTS AUTOMÁTICOS
# ==========================================================

# ============================================
# 🚨 ALERTAS OPERATIVAS (RTA)
# ============================================

st.markdown("---")
st.subheader("🚨 Alertas operativas")

# ALERTA SLA
if sla_general < 50:
    st.error(f"SLA crítico: {sla_general}%")
elif sla_general < 70:
    st.warning(f"SLA bajo: {sla_general}%")
else:
    st.success(f"SLA saludable: {sla_general}%")

# ALERTA WAIT TIME
if avg_wait > 60:
    st.warning(
        f"Tiempo de espera elevado: {round(avg_wait,2)} segundos"
    )
else:
    st.success(
        f"Tiempo de espera estable: {round(avg_wait,2)} segundos"
    )

# AGENTE MÁS CRÍTICO
agente_critico = (
    df_filtrado
    .groupby("agent_name")["wait_time_seconds"]
    .mean()
    .idxmax()
)

mayor_wait = (
    df_filtrado
    .groupby("agent_name")["wait_time_seconds"]
    .mean()
    .max()
)

st.error(
    f"Agente con mayor wait time: "
    f"{agente_critico} ({round(mayor_wait,2)}s)"
)

st.markdown("---")

st.subheader("📌 Insights automáticos")

# Validar que existan datos
if not df_filtrado.empty:

    # Canal más usado
    canal_top = df_filtrado["channel"].mode()[0]

    # Agente con más carga
    agente_top = df_filtrado["agent_name"].mode()[0]

    # Mayor handle time
    mayor_handle = (
        df_filtrado
        .groupby("agent_name")["handle_time_seconds"]
        .mean()
        .idxmax()
    )

    # Mayor wait time
    mayor_wait = (
        df_filtrado
        .groupby("agent_name")["wait_time_seconds"]
        .mean()
        .idxmax()
    )

    # SLA actual
    st.write(f"• SLA General: **{sla_general}%**")

    # Mostrar insights
    st.write(f"• Canal más utilizado: **{canal_top}**")

    st.write(f"• Agente con mayor carga operativa: **{agente_top}**")

    st.write(f"• Agente con mayor Handle Time: **{mayor_handle}**")

    st.write(f"• Agente con mayor Wait Time: **{mayor_wait}**")

else:

    st.warning("⚠️ No hay datos con los filtros seleccionados")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Proyecto desarrollado con Python, Pandas y Streamlit | Portafolio de Data Analytics"
)