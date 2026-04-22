# ============================================
# 📊 CALL CENTER ANALYTICS DASHBOARD (PRO)
# ============================================

import streamlit as st
import pandas as pd

# ============================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================

st.set_page_config(
    page_title="Call Center Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================
# CARGA DE DATOS
# ============================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/clean_interactions.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["mes"] = df["date"].dt.month_name()
    return df

df = load_data()

# ============================================
# SIDEBAR (FILTROS)
# ============================================

st.sidebar.header("🔎 Filtros")

mes = st.sidebar.multiselect(
    "Selecciona mes",
    options=df["mes"].unique(),
    default=df["mes"].unique()
)

canal = st.sidebar.multiselect(
    "Selecciona canal",
    options=df["channel"].unique(),
    default=df["channel"].unique()
)

agente = st.sidebar.multiselect(
    "Selecciona agente",
    options=df["agent_name"].unique(),
    default=df["agent_name"].unique()
)

# Aplicar filtros
df_filtrado = df[
    (df["mes"].isin(mes)) &
    (df["channel"].isin(canal)) &
    (df["agent_name"].isin(agente))
]

# ============================================
# HEADER
# ============================================

st.title("📊 Call Center Analytics Dashboard")
st.markdown("Análisis de rendimiento de agentes y operaciones")

# ============================================
# KPIs (TOP)
# ============================================

total_interacciones = df_filtrado["interaction_id"].count()
avg_handle = df_filtrado["handle_time_seconds"].mean()
avg_wait = df_filtrado["wait_time_seconds"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Interacciones", total_interacciones)
col2.metric("Tiempo Promedio Atención (s)", round(avg_handle, 2))
col3.metric("Tiempo Promedio Espera (s)", round(avg_wait, 2))

# ============================================
# GRÁFICOS
# ============================================

st.markdown("---")

col1, col2 = st.columns(2)

# 📊 Interacciones por agente
with col1:
    st.subheader("Carga de trabajo por agente")
    interacciones_agente = df_filtrado.groupby("agent_name")["interaction_id"].count().sort_values(ascending=False)
    st.bar_chart(interacciones_agente)

# 🍩 Interacciones por canal
with col2:
    st.subheader("Distribución por canal")
    interacciones_canal = df_filtrado.groupby("channel")["interaction_id"].count()
    st.write(interacciones_canal)

# ============================================
# SEGUNDA FILA
# ============================================

col3, col4 = st.columns(2)

# 📈 Interacciones por mes
with col3:
    st.subheader("Interacciones por mes")
    interacciones_mes = df_filtrado.groupby("mes")["interaction_id"].count()
    st.line_chart(interacciones_mes)

# 📋 Tabla de datos
with col4:
    st.subheader("Datos filtrados")
    st.dataframe(df_filtrado)

# ============================================
# INSIGHTS AUTOMÁTICOS
# ============================================

st.markdown("---")
st.subheader("📌 Insights automáticos")

if not df_filtrado.empty:
    st.write(f"• Canal más utilizado: **{df_filtrado['channel'].mode()[0]}**")
    st.write(f"• Agente con más carga: **{df_filtrado['agent_name'].mode()[0]}**")
    st.write(f"• Mayor tiempo de atención: **{df_filtrado.groupby('agent_name')['handle_time_seconds'].mean().idxmax()}**")
    st.write(f"• Mayor tiempo de espera: **{df_filtrado.groupby('agent_name')['wait_time_seconds'].mean().idxmax()}**")
else:
    st.warning("No hay datos con los filtros seleccionados")