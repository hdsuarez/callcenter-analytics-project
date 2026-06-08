# ============================================
# 📊 ETL + ANÁLISIS CALL CENTER
# Proyecto Portafolio Data Analytics
# Fase 1 → RTA
# Fase 2 → Reporting Analyst
# ============================================

# ============================================
# IMPORTAR LIBRERÍAS
# ============================================

import pandas as pd

# ============================================
# 1. CARGAR DATOS RAW
# ============================================

# Fuente original de datos
# (simula una extracción desde Excel)

df = pd.read_excel("../data/call_center_interactions.xlsx")

print("\n✅ Datos originales cargados correctamente")

# ============================================
# 2. EXPLORACIÓN INICIAL
# ============================================

print("\n🔹 Primeras filas:")
print(df.head())

print("\n🔹 Columnas del dataset:")
print(df.columns)

print("\n🔹 Información del dataset:")
print(df.info())

# ============================================
# 3. LIMPIEZA DE DATOS
# ============================================

# --------------------------------------------
# Eliminar registros duplicados
# --------------------------------------------

df = df.drop_duplicates()

# --------------------------------------------
# Convertir fecha a datetime
# --------------------------------------------

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

# --------------------------------------------
# Eliminar registros críticos nulos
# --------------------------------------------

df = df.dropna(
    subset=[
        "interaction_id",
        "agent_name"
    ]
)

# --------------------------------------------
# Crear columna MES
# --------------------------------------------

df["mes"] = df["date"].dt.month_name()

print("\n🧹 Datos limpiados correctamente")

# ============================================
# 4. KPI RTA → SLA
# ============================================

# Regla:
# SLA OK si espera <= 60 segundos

df["sla_ok"] = df["wait_time_seconds"] <= 60

print("\n📌 SLA agregado correctamente")

# ============================================
# 5. PERFORMANCE LEVEL
# ============================================

# Clasificación básica basada en AHT
# (Average Handle Time)

def clasificar_rendimiento(aht):

    if aht < 220:
        return "Excelente"

    elif aht <= 260:
        return "Bueno"

    else:
        return "Crítico"


df["performance_level"] = (
    df["handle_time_seconds"]
    .apply(clasificar_rendimiento)
)

print("\n📌 Performance Level agregado correctamente")

# ============================================
# 6. ANÁLISIS PRINCIPAL
# ============================================

# --------------------------------------------
# Interacciones por agente
# --------------------------------------------

interacciones_por_agente = (
    df.groupby("agent_name")["interaction_id"]
    .count()
    .sort_values(ascending=False)
)

print("\n🔹 Interacciones por agente:")
print(interacciones_por_agente)

# --------------------------------------------
# Interacciones por canal
# --------------------------------------------

interacciones_por_canal = (
    df.groupby("channel")["interaction_id"]
    .count()
    .sort_values(ascending=False)
)

print("\n🔹 Interacciones por canal:")
print(interacciones_por_canal)

# --------------------------------------------
# Handle Time Promedio
# --------------------------------------------

promedio_handle = (
    df.groupby("agent_name")["handle_time_seconds"]
    .mean()
    .sort_values(ascending=False)
)

print("\n🔹 Promedio Handle Time:")
print(promedio_handle)

# --------------------------------------------
# Wait Time Promedio
# --------------------------------------------

promedio_wait = (
    df.groupby("agent_name")["wait_time_seconds"]
    .mean()
    .sort_values(ascending=False)
)

print("\n🔹 Promedio Wait Time:")
print(promedio_wait)

# ============================================
# 7. TOP AGENTES
# ============================================

top_agentes = (
    interacciones_por_agente
    .head(3)
)

print("\n🏆 TOP 3 AGENTES")
print(top_agentes)

# ============================================
# 8. KPI SLA GENERAL
# ============================================

sla_porcentaje = round(
    df["sla_ok"].mean() * 100,
    2
)

print(f"\n📌 SLA GENERAL: {sla_porcentaje}%")

# ============================================
# 9. PERFORMANCE POR AGENTE
# ============================================

# Primer análisis de nivel
# Reporting Analyst

performance_agente = (
    df.groupby("agent_name")
    .agg({
        "interaction_id": "count",
        "handle_time_seconds": "mean",
        "wait_time_seconds": "mean",
        "sla_ok": "mean"
    })
)

# Renombrar columnas

performance_agente.columns = [
    "total_interacciones",
    "avg_handle_time",
    "avg_wait_time",
    "sla_pct"
]

# SLA a porcentaje

performance_agente["sla_pct"] = (
    performance_agente["sla_pct"] * 100
).round(2)

print("\n📊 PERFORMANCE POR AGENTE")
print(performance_agente)

# ============================================
# PERFORMANCE SCORE
# ============================================

# Fórmula sencilla para empezar:
# 70% peso SLA
# 30% peso volumen de interacciones

max_interacciones = performance_agente[
    "total_interacciones"
].max()

performance_agente["score"] = (
    (performance_agente["sla_pct"] * 0.7)
    +
    (
        performance_agente["total_interacciones"]
        / max_interacciones
        * 100
        * 0.3
    )
).round(2)

# Ranking de agentes

ranking_agentes = (
    performance_agente
    .sort_values(
        by="score",
        ascending=False
    )
)

print("\n🏆 RANKING DE AGENTES")
print(
    ranking_agentes[
        [
            "total_interacciones",
            "sla_pct",
            "score"
        ]
    ]
)

# ============================================
# AGENTES EN RIESGO
# ============================================

def clasificar_score(score):

    if score >= 70:
        return "Top Performer"

    elif score >= 60:
        return "Estable"

    else:
        return "En Riesgo"


ranking_agentes["categoria"] = (
    ranking_agentes["score"]
    .apply(clasificar_score)
)

print("\n🚨 CLASIFICACIÓN DE AGENTES")
print(
    ranking_agentes[
        [
            "score",
            "categoria"
        ]
    ]
)

# ============================================
# ANÁLISIS POR CANAL
# ============================================

canal_performance = (
    df.groupby("channel")
    .agg({
        "interaction_id": "count",
        "wait_time_seconds": "mean",
        "handle_time_seconds": "mean",
        "sla_ok": "mean"
    })
)

canal_performance.columns = [
    "total_interacciones",
    "avg_wait_time",
    "avg_handle_time",
    "sla_pct"
]

canal_performance["sla_pct"] = (
    canal_performance["sla_pct"] * 100
).round(2)

print("\n📞 PERFORMANCE POR CANAL")
print(canal_performance)

# ============================================
# AGENTES CRÍTICOS
# ============================================

agentes_criticos = ranking_agentes[
    ranking_agentes["categoria"] == "En Riesgo"
]

print("\n🚨 AGENTES CRÍTICOS")
print(
    agentes_criticos[
        [
            "score",
            "sla_pct",
            "avg_wait_time"
        ]
    ]
)

# ==========================================================
# TOP Y BOTTOM PERFORMERS
# ==========================================================

st.markdown("---")

st.subheader("🏅 Top & Bottom Performers")

col1, col2 = st.columns(2)

with col1:

    mejor_agente = agent_perf.loc[
        agent_perf["score"].idxmax()
    ]

    st.success(
        f"""
        🏆 Mejor Agente

        Nombre: {mejor_agente['agent_name']}

        Score: {mejor_agente['score']}
        """
    )

with col2:

    peor_agente = agent_perf.loc[
        agent_perf["score"].idxmin()
    ]

    st.error(
        f"""
        ⚠️ Agente con Riesgo

        Nombre: {peor_agente['agent_name']}

        Score: {peor_agente['score']}
        """
    )

# ============================================
# EXPORTAR
# ============================================

agentes_criticos.to_csv(
    "../data/agentes_criticos.csv",
    index=True
)

print(
    "\n💾 Archivo agentes_criticos.csv exportado"
)

# ============================================
# EXPORTAR PERFORMANCE POR CANAL
# ============================================

canal_performance.to_csv(
    "../data/channel_performance.csv"
)

print(
    "\n💾 channel_performance.csv guardado correctamente"
)

# ============================================
# EXPORTAR PERFORMANCE DE AGENTES
# ============================================

ranking_agentes.to_csv(
    "../data/agent_performance.csv"
)

print(
    "\n💾 Archivo agent_performance.csv guardado correctamente"
)

# ============================================
# 10. EXPORTAR DATA LIMPIA
# ============================================

df.to_csv(
    "../data/clean_interactions.csv",
    index=False
)

print("\n💾 Dataset limpio guardado correctamente")

# ============================================
# 11. CONCLUSIONES AUTOMÁTICAS
# ============================================

print("\n📌 CONCLUSIONES")

print(
    f"- Total interacciones: "
    f"{df['interaction_id'].count()}"
)

print(
    f"- Canal más usado: "
    f"{interacciones_por_canal.idxmax()}"
)

print(
    f"- Agente con más carga: "
    f"{interacciones_por_agente.idxmax()}"
)

print(
    f"- Mayor Handle Time: "
    f"{promedio_handle.idxmax()}"
)

print(
    f"- Mayor Wait Time: "
    f"{promedio_wait.idxmax()}"
)

print(
    f"- SLA General: "
    f"{sla_porcentaje}%"
)

# ============================================
# FIN DEL PROCESO
# ============================================