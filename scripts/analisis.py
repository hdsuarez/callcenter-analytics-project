# ============================================
# 📊 ANÁLISIS DE INTERACCIONES (CALL CENTER)
# ============================================

# Importar librería principal
import pandas as pd

# ============================================
# 1. CARGAR DATOS
# ============================================

# Leer archivo CSV (ajusta la ruta si es necesario)
df = pd.read_csv("interactions.csv")

# Mostrar las primeras filas
print("\n🔹 Primeras filas del dataset:")
print(df.head())


# ============================================
# 2. EXPLORACIÓN BÁSICA
# ============================================

# Ver información general del dataset
print("\n🔹 Información del dataset:")
print(df.info())

# Ver estadísticas básicas
print("\n🔹 Estadísticas descriptivas:")
print(df.describe())


# ============================================
# 3. INTERACCIONES POR AGENTE
# ============================================

# Contar cuántas interacciones tiene cada agente
interacciones_por_agente = df.groupby("agent_name")["interaction_id"].count()

print("\n🔹 Interacciones por agente:")
print(interacciones_por_agente.sort_values(ascending=False))


# ============================================
# 4. INTERACCIONES POR CANAL
# ============================================

# Contar interacciones por canal (Call, Chat, Email)
interacciones_por_canal = df.groupby("channel")["interaction_id"].count()

print("\n🔹 Interacciones por canal:")
print(interacciones_por_canal.sort_values(ascending=False))


# ============================================
# 5. PROMEDIO DE TIEMPO DE ATENCIÓN
# ============================================

# Calcular el promedio de handle time por agente
promedio_handle = df.groupby("agent_name")["handle_time_seconds"].mean()

print("\n🔹 Promedio de tiempo de atención por agente:")
print(promedio_handle.sort_values(ascending=False))


# ============================================
# 6. PROMEDIO DE TIEMPO DE ESPERA
# ============================================

# Calcular el promedio de wait time por agente
promedio_wait = df.groupby("agent_name")["wait_time_seconds"].mean()

print("\n🔹 Promedio de tiempo de espera por agente:")
print(promedio_wait.sort_values(ascending=False))


# ============================================
# 7. INTERACCIONES POR MES
# ============================================

# Convertir la columna date a formato fecha (por si acaso)
df["date"] = pd.to_datetime(df["date"])

# Crear columna de mes
df["mes"] = df["date"].dt.month_name()

# Contar interacciones por mes
interacciones_por_mes = df.groupby("mes")["interaction_id"].count()

print("\n🔹 Interacciones por mes:")
print(interacciones_por_mes)


# ============================================
# 8. TOP 3 AGENTES CON MÁS INTERACCIONES
# ============================================

top_agentes = interacciones_por_agente.sort_values(ascending=False).head(3)

print("\n🏆 Top 3 agentes con más interacciones:")
print(top_agentes)


# ============================================
# 9. CONCLUSIONES AUTOMÁTICAS (BÁSICAS)
# ============================================

print("\n📌 CONCLUSIONES:")

print(f"- Total de interacciones: {df['interaction_id'].count()}")
print(f"- Canal más usado: {interacciones_por_canal.idxmax()}")
print(f"- Agente con más carga: {interacciones_por_agente.idxmax()}")
print(f"- Agente con mayor tiempo promedio de atención: {promedio_handle.idxmax()}")
print(f"- Agente con mayor tiempo de espera: {promedio_wait.idxmax()}")

# ============================================
# FIN DEL SCRIPT
# ============================================