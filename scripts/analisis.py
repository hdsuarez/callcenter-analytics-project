# ============================================
# 📊 ETL + ANÁLISIS CALL CENTER (RTA PROJECT)
# ============================================

# ============================================
# IMPORTAR LIBRERÍAS
# ============================================

import pandas as pd

# ============================================
# 1. CARGAR DATOS ORIGINALES
# ============================================

# Leemos el archivo Excel original
# Este archivo representa la fuente RAW (sin procesar)

df = pd.read_excel("../data/call_center_interactions.xlsx")

print("\n✅ Datos originales cargados correctamente")

# ============================================
# 2. EXPLORACIÓN INICIAL
# ============================================

# Mostrar primeras filas
print("\n🔹 Primeras filas:")
print(df.head())

# Mostrar nombres de columnas
print("\n🔹 Columnas del dataset:")
print(df.columns)

# Información general del dataset
print("\n🔹 Información del dataset:")
print(df.info())

# ============================================
# 3. LIMPIEZA DE DATOS
# ============================================

# --------------------------------------------
# Eliminar duplicados
# --------------------------------------------

df = df.drop_duplicates()

# --------------------------------------------
# Convertir columna fecha
# --------------------------------------------

# Convertimos la columna "date" a formato datetime
# errors="coerce" convierte errores en NaT

df["date"] = pd.to_datetime(df["date"], errors="coerce")

# --------------------------------------------
# Eliminar registros importantes nulos
# --------------------------------------------

df = df.dropna(subset=["interaction_id", "agent_name"])

# --------------------------------------------
# Crear columna MES
# --------------------------------------------

# Extraemos el nombre del mes desde la fecha

df["mes"] = df["date"].dt.month_name()

# ============================================
# 4. MÉTRICAS RTA (SLA)
# ============================================

# SLA = Service Level Agreement
# Regla:
# Si wait_time_seconds <= 60
# entonces cumplió SLA

df["sla_ok"] = df["wait_time_seconds"] <= 60

# ============================================
# PERFORMANCE LEVEL (AHT)
# ============================================

def clasificar_rendimiento(aht):

    if aht < 220:
        return "Excelente"

    elif aht <= 260:
        return "Bueno"

    else:
        return "Crítico"


# Crear nueva columna
df["performance_level"] = df["handle_time_seconds"].apply(clasificar_rendimiento)

print("\n📌 Performance Level agregado correctamente")

print("\n📌 SLA agregado correctamente")

# ============================================
# 5. ANÁLISIS PRINCIPAL
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
# Promedio Handle Time
# --------------------------------------------

promedio_handle = (
    df.groupby("agent_name")["handle_time_seconds"]
    .mean()
    .sort_values(ascending=False)
)

print("\n🔹 Promedio handle time:")
print(promedio_handle)

# --------------------------------------------
# Promedio Wait Time
# --------------------------------------------

promedio_wait = (
    df.groupby("agent_name")["wait_time_seconds"]
    .mean()
    .sort_values(ascending=False)
)

print("\n🔹 Promedio wait time:")
print(promedio_wait)

# ============================================
# 6. TOP AGENTES
# ============================================

top_agentes = interacciones_por_agente.head(3)

print("\n🏆 Top 3 agentes:")
print(top_agentes)

# ============================================
# 7. KPI SLA
# ============================================

# Calculamos porcentaje SLA

sla_porcentaje = round(df["sla_ok"].mean() * 100, 2)

print(f"\n📌 SLA GENERAL: {sla_porcentaje}%")

# ============================================
# 8. EXPORTAR DATA LIMPIA
# ============================================

# Guardamos dataset limpio para:
# Power BI
# Streamlit
# futuros análisis

df.to_csv("../data/clean_interactions.csv", index=False)

print("\n💾 Dataset limpio guardado correctamente")

# ============================================
# 9. CONCLUSIONES AUTOMÁTICAS
# ============================================

print("\n📌 CONCLUSIONES:")

print(f"- Total interacciones: {df['interaction_id'].count()}")
print(f"- Canal más usado: {interacciones_por_canal.idxmax()}")
print(f"- Agente con más carga: {interacciones_por_agente.idxmax()}")
print(f"- Mayor handle time: {promedio_handle.idxmax()}")
print(f"- Mayor wait time: {promedio_wait.idxmax()}")
print(f"- SLA general: {sla_porcentaje}%")

# ============================================
# FIN DEL PROCESO
# ============================================