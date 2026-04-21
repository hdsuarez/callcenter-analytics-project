# ============================================
# 📊 ETL + ANÁLISIS (CALL CENTER) - NIVEL PRO
# ============================================

import pandas as pd

# ============================================
# 1. CARGAR DATOS ORIGINALES (RAW)
# ============================================

# 👇 IMPORTANTE: usa tu archivo ORIGINAL
df = pd.read_excel("../data/call_center_interactions.xlsx")

print("\n✅ Datos originales cargados correctamente")

# ============================================
# 2. EXPLORACIÓN BÁSICA
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

# Eliminar duplicados
df = df.drop_duplicates()

# Convertir fecha
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Eliminar nulos importantes
df = df.dropna(subset=["interaction_id", "agent_name"])

# Crear columna de mes
df["mes"] = df["date"].dt.month_name()

print("\n🧹 Datos limpios")

# ============================================
# 4. ANÁLISIS
# ============================================

# Interacciones por agente
interacciones_por_agente = df.groupby("agent_name")["interaction_id"].count()

print("\n🔹 Interacciones por agente:")
print(interacciones_por_agente.sort_values(ascending=False))

# Interacciones por canal
interacciones_por_canal = df.groupby("channel")["interaction_id"].count()

print("\n🔹 Interacciones por canal:")
print(interacciones_por_canal.sort_values(ascending=False))

# Promedios
promedio_handle = df.groupby("agent_name")["handle_time_seconds"].mean()
promedio_wait = df.groupby("agent_name")["wait_time_seconds"].mean()

print("\n🔹 Promedio handle time:")
print(promedio_handle.sort_values(ascending=False))

print("\n🔹 Promedio wait time:")
print(promedio_wait.sort_values(ascending=False))

# ============================================
# 5. TOP AGENTES
# ============================================

top_agentes = interacciones_por_agente.sort_values(ascending=False).head(3)

print("\n🏆 Top 3 agentes:")
print(top_agentes)

# ============================================
# 6. GUARDAR DATA LIMPIA (CLAVE)
# ============================================

df.to_csv("../data/clean_interactions.csv", index=False)

print("\n💾 Dataset limpio guardado correctamente")

# ============================================
# 7. CONCLUSIONES
# ============================================

print("\n📌 CONCLUSIONES:")

print(f"- Total interacciones: {df['interaction_id'].count()}")
print(f"- Canal más usado: {interacciones_por_canal.idxmax()}")
print(f"- Agente con más carga: {interacciones_por_agente.idxmax()}")
print(f"- Mayor handle time: {promedio_handle.idxmax()}")
print(f"- Mayor wait time: {promedio_wait.idxmax()}")

# ============================================
# FIN
# ============================================