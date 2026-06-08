# ==========================================================
# 📊 CALL CENTER ANALYTICS DASHBOARD (PRO VERSION)
# ==========================================================

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================================
# CONFIGURACIÓN GENERAL DE LA APP
# ==========================================================

st.set_page_config(
    page_title="Call Center Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CARGA DE DATOS
# ==========================================================

@st.cache_data
def load_data():
    # ======================================================
    # SOLUCIÓN PROFESIONAL PARA RUTAS
    # ======================================================
    
    # CORRECCIÓN 1: Usar __file__ solo si existe, si no, usar directorio actual
    try:
        BASE_DIR = Path(__file__).resolve().parent.parent
    except NameError:
        # Para cuando se ejecuta en un entorno interactivo
        BASE_DIR = Path.cwd()
    
    # ======================================================
    # DATASET PRINCIPAL
    # ======================================================
    
    clean_path = BASE_DIR / "data" / "clean_interactions.csv"
    
    # CORRECCIÓN 2: Verificar si el archivo existe
    if not clean_path.exists():
        st.error(f"No se encontró el archivo: {clean_path}")
        # Crear datos de ejemplo para pruebas
        return create_sample_data()
    
    df = pd.read_csv(clean_path)
    df["date"] = pd.to_datetime(df["date"])
    df["mes"] = df["date"].dt.month_name()
    
    # ======================================================
    # PERFORMANCE POR AGENTE
    # ======================================================
    
    agent_path = BASE_DIR / "data" / "agent_performance.csv"
    
    if agent_path.exists():
        agent_perf = pd.read_csv(agent_path)
    else:
        agent_perf = pd.DataFrame()  # DataFrame vacío como fallback
    
    # ======================================================
    # PERFORMANCE POR CANAL
    # ======================================================
    
    channel_path = BASE_DIR / "data" / "channel_performance.csv"
    
    if channel_path.exists():
        channel_perf = pd.read_csv(channel_path)
    else:
        channel_perf = pd.DataFrame()  # DataFrame vacío como fallback
    
    # ======================================================
    # RETORNAR LOS 3 DATAFRAMES
    # ======================================================
    
    return df, agent_perf, channel_perf

# Función auxiliar para crear datos de ejemplo
def create_sample_data():
    import numpy as np
    from datetime import datetime, timedelta
    
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', '2024-12-31', freq='H')
    dates = np.random.choice(dates, 1000)
    
    df = pd.DataFrame({
        'interaction_id': range(1, 1001),
        'date': dates,
        'channel': np.random.choice(['Phone', 'Chat', 'Email', 'Social'], 1000),
        'agent_name': np.random.choice(['Ana', 'Luis', 'Carlos', 'Marta', 'Jorge'], 1000),
        'status': np.random.choice(['Attended', 'Abandoned'], 1000, p=[0.85, 0.15]),
        'handle_time_seconds': np.random.randint(30, 600, 1000),
        'wait_time_seconds': np.random.randint(0, 120, 1000),
        'sla_ok': np.random.choice([True, False], 1000, p=[0.75, 0.25])
    })
    
    df['mes'] = df['date'].dt.month_name()
    
    return df, pd.DataFrame(), pd.DataFrame()



# ==========================================================
# CARGAR DATAFRAMES
# ==========================================================

df, agent_perf, channel_perf = load_data()

# CORRECCIÓN 3: Eliminar la línea duplicada
# df = load_data()  # <--- ESTA LÍNEA ESTABA DUPLICADA Y MAL

# ==========================================================
# SIDEBAR - FILTROS
# ==========================================================

st.sidebar.header("🔎 Filtros")

# Verificar que df no esté vacío
if df.empty:
    st.error("No se pudieron cargar los datos. Verifica los archivos.")
    st.stop()

# ----------------------------------------------------------
# FILTRO MES
# ----------------------------------------------------------

mes = st.sidebar.multiselect(
    "Selecciona mes",
    options=df["mes"].unique(),
    default=df["mes"].unique().tolist()  # CORRECCIÓN 4: Convertir a lista
)

# ----------------------------------------------------------
# FILTRO CANAL
# ----------------------------------------------------------

canal = st.sidebar.multiselect(
    "Selecciona canal",
    options=df["channel"].unique(),
    default=df["channel"].unique().tolist()  # CORRECCIÓN 4: Convertir a lista
)

# ----------------------------------------------------------
# FILTRO AGENTE
# ----------------------------------------------------------

agente = st.sidebar.multiselect(
    "Selecciona agente",
    options=df["agent_name"].unique(),
    default=df["agent_name"].unique().tolist()  # CORRECCIÓN 4: Convertir a lista
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

st.markdown("""
    Dashboard interactivo para análisis de operaciones,
    rendimiento de agentes y métricas SLA.
""")

# ==========================================================
# KPIs PRINCIPALES
# ==========================================================

# Verificar que df_filtrado no esté vacío
if df_filtrado.empty:
    st.warning("No hay datos con los filtros seleccionados")
    st.stop()

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

sla_general = round(
    df_filtrado["sla_ok"].mean() * 100,
    2
)

# ==========================================================
# MÉTRICAS OPERATIVAS
# ==========================================================

# Interacciones atendidas
attended = df_filtrado[
    df_filtrado["status"] == "Attended"
].shape[0]

# Interacciones abandonadas
abandoned = df_filtrado[
    df_filtrado["status"] == "Abandoned"
].shape[0]

# Evitar división por cero
if total_interacciones > 0:
    abandon_rate = round(
        (abandoned / total_interacciones) * 100,
        2
    )
else:
    abandon_rate = 0

# ==========================================================
# CREAR COLUMNAS KPI
# ==========================================================

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

# KPI 1
col1.metric(
    "Total Interacciones",
    f"{total_interacciones:,}"  # CORRECCIÓN 5: Formato con miles
)

# KPI 2
col2.metric(
    "Avg Handle Time (s)",
    round(avg_handle, 2) if not pd.isna(avg_handle) else 0  # CORRECCIÓN 6: Manejar NaN
)

# KPI 3
col3.metric(
    "Avg Wait Time (s)",
    round(avg_wait, 2) if not pd.isna(avg_wait) else 0  # CORRECCIÓN 6: Manejar NaN
)

# KPI 4
col4.metric(
    "SLA (%)",
    f"{sla_general}%"
)

# KPI 5
col5.metric(
    "Atendidas",
    f"{attended:,}"
)

# KPI 6
col6.metric(
    "Abandonadas",
    f"{abandoned:,}"
)

# ==========================================================
# MÉTRICAS OPERATIVAS
# ==========================================================

st.markdown("---")

st.subheader("📉 Métricas Operativas")

# CORRECCIÓN 7: Mostrar abandon rate con mejor formato
col_abandon1, col_abandon2, col_abandon3 = st.columns(3)
with col_abandon1:
    st.metric("Abandon Rate", f"{abandon_rate}%")

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
    
    if not interacciones_agente.empty:
        st.bar_chart(interacciones_agente)
    else:
        st.info("No hay datos para mostrar")

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
    
    if not interacciones_canal.empty:
        # CORRECCIÓN 8: Usar gráfico de barras en lugar de dataframe
        st.bar_chart(interacciones_canal)
        # Mostrar también los datos numéricos
        with st.expander("Ver datos detallados"):
            st.dataframe(interacciones_canal)
    else:
        st.info("No hay datos para mostrar")

# ==========================================================
# SEGUNDA FILA DE VISUALIZACIONES
# ==========================================================

col3, col4 = st.columns(2)

# ==========================================================
# GRÁFICO: INTERACCIONES POR MES
# ==========================================================

with col3:
    st.subheader("📈 Interacciones por mes")
    
    # CORRECCIÓN 9: Ordenar meses cronológicamente
    orden_meses = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    interacciones_mes = (
        df_filtrado
        .groupby("mes")["interaction_id"]
        .count()
        .reindex(orden_meses)  # Reordenar meses
        .dropna()  # Eliminar meses sin datos
    )
    
    if not interacciones_mes.empty:
        st.line_chart(interacciones_mes)
    else:
        st.info("No hay datos para mostrar")

# ==========================================================
# TABLA DETALLADA
# ==========================================================

with col4:
    st.subheader("📋 Datos filtrados")
    # CORRECCIÓN 10: Mostrar solo primeras filas y columnas relevantes
    columnas_mostrar = ['interaction_id', 'date', 'channel', 'agent_name', 
                        'status', 'handle_time_seconds', 'wait_time_seconds', 'sla_ok']
    columnas_existentes = [col for col in columnas_mostrar if col in df_filtrado.columns]
    st.dataframe(df_filtrado[columnas_existentes].head(100))

# ==========================================================
# ALERTAS OPERATIVAS (RTA)
# ==========================================================

st.markdown("---")

st.subheader("🚨 Alertas operativas")

# ----------------------------------------------------------
# ALERTA SLA
# ----------------------------------------------------------

if sla_general < 50:
    st.error(f"⚠️ SLA crítico: {sla_general}% - Se requiere acción inmediata")
elif sla_general < 70:
    st.warning(f"⚠️ SLA bajo: {sla_general}% - Monitorear rendimiento")
else:
    st.success(f"✅ SLA saludable: {sla_general}%")

# ----------------------------------------------------------
# ALERTA WAIT TIME
# ----------------------------------------------------------

if avg_wait > 60:
    st.warning(
        f"⏱️ Tiempo de espera elevado: "
        f"{round(avg_wait, 2)} segundos"
    )
else:
    st.success(
        f"✅ Tiempo de espera estable: "
        f"{round(avg_wait, 2)} segundos"
    )

# ----------------------------------------------------------
# AGENTE MÁS CRÍTICO
# ----------------------------------------------------------

if not df_filtrado.empty and 'wait_time_seconds' in df_filtrado.columns:
    try:
        # CORRECCIÓN 11: Mejor manejo de errores
        wait_by_agent = df_filtrado.groupby("agent_name")["wait_time_seconds"].mean()
        if not wait_by_agent.empty:
            agente_critico = wait_by_agent.idxmax()
            mayor_wait = wait_by_agent.max()
            st.info(
                f"📌 Agente con mayor wait time: "
                f"**{agente_critico}** ({round(mayor_wait, 2)}s)"
            )
    except Exception as e:
        st.warning(f"No se pudo calcular el agente más crítico: {e}")

# ==========================================================
# INSIGHTS AUTOMÁTICOS
# ==========================================================

st.markdown("---")

st.subheader("📌 Insights automáticos")

if not df_filtrado.empty:

    mejor_agente = agent_perf.loc[
        agent_perf["score"].idxmax(),
        "agent_name"
    ]

    peor_agente = agent_perf.loc[
        agent_perf["score"].idxmin(),
        "agent_name"
    ]

    mejor_canal = channel_perf.loc[
        channel_perf["sla_pct"].idxmax(),
        "channel"
    ]

    st.write(
        f"🏆 Mejor agente del periodo: **{mejor_agente}**"
    )

    st.write(
        f"⚠️ Agente con menor score: **{peor_agente}**"
    )

    st.write(
        f"📞 Canal con mejor SLA: **{mejor_canal}**"
    )

    st.write(
        f"📊 SLA General actual: **{sla_general}%**"
    )

else:

    st.warning(
        "⚠️ No hay datos con los filtros seleccionados"
    )

# ==========================================================
# RESUMEN EJECUTIVO
# ==========================================================

st.markdown("---")

st.subheader("📌 Resumen Ejecutivo")

col1, col2, col3, col4 = st.columns(4)

# Mejor agente
mejor_agente = agent_perf.loc[
    agent_perf["score"].idxmax(),
    "agent_name"
]

# Peor agente
peor_agente = agent_perf.loc[
    agent_perf["score"].idxmin(),
    "agent_name"
]

# Mejor canal
mejor_canal = channel_perf.loc[
    channel_perf["sla_pct"].idxmax(),
    "channel"
]

# Agentes en riesgo
agentes_riesgo = (
    agent_perf["categoria"] == "En Riesgo"
).sum()

col1.metric(
    "🏆 Mejor Agente",
    mejor_agente
)

col2.metric(
    "⚠️ Agente Crítico",
    peor_agente
)

col3.metric(
    "📞 Mejor Canal",
    mejor_canal
)

col4.metric(
    "🚨 Agentes en Riesgo",
    agentes_riesgo
)


# ==========================================================
# RANKING DE AGENTES
# ==========================================================
st.markdown("---")

st.header("👥 Workforce Performance")

st.markdown("---")

st.subheader("🏆 Ranking de Agentes")

# ==========================================================
# AGENTES CRÍTICOS
# ==========================================================

st.markdown("---")

st.subheader("🚨 Agentes Críticos")

agentes_criticos = agent_perf[
    agent_perf["categoria"] == "En Riesgo"
]

if not agentes_criticos.empty:

    st.dataframe(
        agentes_criticos[
            [
                "agent_name",
                "score",
                "sla_pct",
                "avg_wait_time"
            ]
        ]
    )

else:

    st.success(
        "✅ No existen agentes en riesgo"
    )

# ----------------------------------------------------------
# TABLA DE RANKING
# ----------------------------------------------------------

st.dataframe(
    agent_perf.sort_values(
        by="score",
        ascending=False
    )
)

# ==========================================================
# NUEVO: VISUALIZACIONES REPORTING ANALYST
# ==========================================================

col_graf1, col_graf2 = st.columns(2)

# ----------------------------------------------------------
# SCORE POR AGENTE
# ----------------------------------------------------------

with col_graf1:

    st.subheader("📊 Score por Agente")

    score_chart = (
        agent_perf
        .sort_values(
            by="score",
            ascending=False
        )
        .set_index("agent_name")["score"]
    )

    st.bar_chart(score_chart)

# ----------------------------------------------------------
# SLA POR CANAL
# ----------------------------------------------------------

with col_graf2:

    st.subheader("📞 SLA por Canal")

    sla_channel_chart = (
        channel_perf
        .set_index("channel")["sla_pct"]
    )

    st.bar_chart(sla_channel_chart)

# ==========================================================
# INSIGHTS AUTOMÁTICOS
# ==========================================================

if not df_filtrado.empty:

    try:

        # --------------------------------------------------
        # INSIGHTS DEL DATASET FILTRADO
        # --------------------------------------------------

        canal_top = (
            df_filtrado["channel"]
            .mode()[0]
            if not df_filtrado["channel"].mode().empty
            else "N/A"
        )

        carga_agente = (
            df_filtrado["agent_name"]
            .value_counts()
        )

        agente_top = (
            carga_agente.index[0]
            if not carga_agente.empty
            else "N/A"
        )

        handle_by_agent = (
            df_filtrado
            .groupby("agent_name")["handle_time_seconds"]
            .mean()
        )

        mayor_handle = (
            handle_by_agent.idxmax()
            if not handle_by_agent.empty
            else "N/A"
        )

        wait_by_agent = (
            df_filtrado
            .groupby("agent_name")["wait_time_seconds"]
            .mean()
        )

        mayor_wait = (
            wait_by_agent.idxmax()
            if not wait_by_agent.empty
            else "N/A"
        )

        # --------------------------------------------------
        # NUEVOS INSIGHTS REPORTING ANALYST
        # --------------------------------------------------

        mejor_agente = agent_perf.loc[
            agent_perf["score"].idxmax(),
            "agent_name"
        ]

        peor_agente = agent_perf.loc[
            agent_perf["score"].idxmin(),
            "agent_name"
        ]

        mejor_canal = channel_perf.loc[
            channel_perf["sla_pct"].idxmax(),
            "channel"
        ]

        # --------------------------------------------------
        # MOSTRAR INSIGHTS
        # --------------------------------------------------

        col_insight1, col_insight2 = st.columns(2)

        with col_insight1:

            st.write("### 🎯 Indicadores Clave")

            st.write(
                f"• **SLA General:** {sla_general}%"
            )

            st.write(
                f"• **Abandon Rate:** {abandon_rate}%"
            )

            st.write(
                f"• **Canal más utilizado:** {canal_top}"
            )

            st.write(
                f"• **Canal con mejor SLA:** {mejor_canal}"
            )

        with col_insight2:

            st.write("### 👥 Rendimiento por Agente")

            st.write(
                f"• **Mayor carga operativa:** {agente_top}"
            )

            st.write(
                f"• **Mayor Handle Time:** {mayor_handle}"
            )

            st.write(
                f"• **Mayor Wait Time:** {mayor_wait}"
            )

            st.write(
                f"• **Mejor agente:** {mejor_agente}"
            )

            st.write(
                f"• **Agente en riesgo:** {peor_agente}"
            )

        # --------------------------------------------------
        # EFICIENCIA OPERATIVA
        # --------------------------------------------------

        eficiencia = (
            attended / total_interacciones * 100
        ) if total_interacciones > 0 else 0

        if eficiencia < 80:

            st.warning(
                f"⚠️ Tasa de atención baja: "
                f"{round(eficiencia, 2)}%"
            )

        else:

            st.success(
                f"✅ Buena tasa de atención: "
                f"{round(eficiencia, 2)}%"
            )

    except Exception as e:

        st.warning(
            f"Error al generar insights: {e}"
        )

else:

    st.warning(
        "⚠️ No hay datos con los filtros seleccionados"
    )

# ==========================================================
# PERFORMANCE POR CANAL
# ==========================================================

st.markdown("---")

st.subheader("📞 Performance por Canal")

st.dataframe(
    channel_perf.sort_values(
        by="sla_pct",
        ascending=False
    )
)

# ==========================================================
# TENDENCIA DE INTERACCIONES
# ==========================================================

st.markdown("---")

st.header("📊 Operational Analytics")

st.markdown("---")

st.subheader("📈 Tendencia de Interacciones")

interacciones_mes = (
    df
    .groupby("mes")["interaction_id"]
    .count()
)

st.line_chart(interacciones_mes)

# ==========================================================
# INSIGHTS POR CANAL
# ==========================================================

mejor_canal = channel_perf.loc[
    channel_perf["sla_pct"].idxmax()
]

peor_canal = channel_perf.loc[
    channel_perf["sla_pct"].idxmin()
]

col1, col2 = st.columns(2)

with col1:

    st.success(
        f"""
        🏆 Mejor Canal

        {mejor_canal['channel']}

        SLA: {round(mejor_canal['sla_pct'], 2)}%
        """
    )

with col2:

    st.error(
        f"""
        ⚠️ Canal Crítico

        {peor_canal['channel']}

        SLA: {round(peor_canal['sla_pct'], 2)}%
        """
    )

# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

st.markdown("---")

st.header("📈 Executive Dashboard")

st.markdown("---")

st.subheader("📋 Executive Summary")

mejor_agente = agent_perf.loc[
    agent_perf["score"].idxmax(),
    "agent_name"
]

peor_agente = agent_perf.loc[
    agent_perf["score"].idxmin(),
    "agent_name"
]

mejor_canal = channel_perf.loc[
    channel_perf["sla_pct"].idxmax(),
    "channel"
]

st.success(
    f"""
    🏆 Mejor agente: {mejor_agente}

    📞 Mejor canal: {mejor_canal}

    📊 SLA General: {sla_general}%

    ⚠️ Agente que requiere seguimiento:
    {peor_agente}
    """
)

agentes_riesgo = (
    agent_perf["categoria"] == "En Riesgo"
).sum()

# ==========================================================
# KPI SUMMARY
# ==========================================================

st.subheader("📈 KPI Summary")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric(
    "Interacciones",
    total_interacciones
)

kpi2.metric(
    "SLA",
    f"{sla_general}%"
)

kpi3.metric(
    "Handle Time",
    round(avg_handle, 2)
)

kpi4.metric(
    "Wait Time",
    round(avg_wait, 2)
)

# ==========================================================
# EXECUTIVE PERFORMANCE TABLE
# ==========================================================

st.markdown("---")

st.subheader("📋 Executive Performance Table")

tabla_ejecutiva = (
    agent_perf[
        [
            "agent_name",
            "total_interacciones",
            "sla_pct",
            "score",
            "categoria"
        ]
    ]
    .sort_values(
        by="score",
        ascending=False
    )
)

st.dataframe(
    tabla_ejecutiva,
    use_container_width=True
)

# ==========================================================
# HEALTH CHECK OPERACIONAL
# ==========================================================

st.markdown("---")

st.subheader("📈 Health Check Operacional")

col_h1, col_h2, col_h3 = st.columns(3)

# SLA
if sla_general >= 70:
    col_h1.success("✅ SLA Saludable")
elif sla_general >= 50:
    col_h1.warning("⚠️ SLA Moderado")
else:
    col_h1.error("🚨 SLA Crítico")

# Wait Time
if avg_wait <= 60:
    col_h2.success("✅ Wait Time Controlado")
else:
    col_h2.warning("⚠️ Wait Time Elevado")

# Abandon Rate
if abandon_rate <= 10:
    col_h3.success("✅ Abandono Controlado")
else:
    col_h3.error("🚨 Alto Abandono")

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

# CORRECCIÓN 13: Mostrar información adicional
col_footer1, col_footer2, col_footer3 = st.columns(3)

with col_footer1:
    st.caption(f"📊 Total de registros: {len(df_filtrado):,}")

with col_footer2:
    st.caption("📅 Período: Datos históricos")

with col_footer3:
    st.caption(
        "Proyecto desarrollado con Python, Pandas y Streamlit | "
        "Portafolio de Data Analytics"
    )