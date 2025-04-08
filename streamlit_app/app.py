import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

# Título y descripción de la app
st.title("Análisis de Jugadores de Fútbol")
st.markdown("""
Esta aplicación interactiva carga datos de jugadores y presenta visualizaciones basadas en el CSV.
Compara el rendimiento de un jugador frente al promedio de su posición y muestra análisis visuales.
""")

# Cargar datos con caché
@st.cache_data
def load_data():
    data = pd.read_csv("/Users/sevi/Documents/tarea_mod.8/df_amf_final_copia2.csv")
    return data

data = load_data()

# Sidebar - Filtros
st.sidebar.header("Filtros")

# Filtro de posición (fijo)
posiciones = data["Position"].dropna().unique()
posicion_seleccionada = st.sidebar.selectbox("Selecciona posición:", posiciones)

# Filtro dinámico de jugador
jugadores_disponibles = data[data["Position"] == posicion_seleccionada]["Player Name"].unique()
jugador_seleccionado = st.sidebar.selectbox("Selecciona jugador:", jugadores_disponibles)

# Filtrar data para ese jugador y promedio
jugador_data = data[data["Player Name"] == jugador_seleccionado].iloc[0]
promedio_posicion = data[data["Position"] == posicion_seleccionada]

# Radar de rendimiento
st.header("Perfil de Rendimiento por Posición")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(jugador_data["Player Name"])
    st.image(jugador_data["Photo"], width=150)
    st.markdown(f"""
    - **Nacionalidad:** {jugador_data.get('Nationship', 'N/D')}
    - **Edad:** {jugador_data['Age']}
    - **Equipo:** {jugador_data['Team']}
    - **Posición:** {jugador_data['Position']}
    - **Perfil:** {jugador_data ['Profile Main Characteristic']}
    - **Valor de Mercado:** {jugador_data.get('Market Value (M)', 'N/D')} M
    """)

with col2:
    st.subheader("Jugador vs Promedio Posicional")

    radar_labels = [
        'Matches Index', 'Conditional index', 'Goal Involment Index',
        'Passing Index', 'Technical Skills Index', 'Offensive Index',
        'Defensive index', 'Performance Index', 'xPerformance Index', 'Scouting Index'
    ]

    jugador_vals = [jugador_data[label] for label in radar_labels]
    promedio_vals = promedio_posicion[radar_labels].mean().tolist()

    # Normalización para comparación visual
    max_val = max(jugador_vals + promedio_vals)
    jugador_norm = [v / max_val for v in jugador_vals]
    promedio_norm = [v / max_val for v in promedio_vals]

    # Radar
    angles = [n / float(len(radar_labels)) * 2 * pi for n in range(len(radar_labels))]
    jugador_norm += jugador_norm[:1]
    promedio_norm += promedio_norm[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, jugador_norm, label="Jugador", linewidth=2, color="green")
    ax.fill(angles, jugador_norm, alpha=0.3, color="green")
    ax.plot(angles, promedio_norm, label="Promedio", linewidth=2, color="deepskyblue")
    ax.fill(angles, promedio_norm, alpha=0.2, color="deepskyblue")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(radar_labels, fontsize=8)
    ax.set_title("Índices de Rendimiento", size=14, y=1.1)
    ax.set_yticklabels([])
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
    st.pyplot(fig)

# Tabla comparativa
st.subheader("Comparación Numérica de Índices")
tabla_comparativa = pd.DataFrame([jugador_vals, promedio_vals], columns=radar_labels, index=[jugador_data["Player Name"], "Promedio"])
st.dataframe(tabla_comparativa.style.format("{:.2f}"), use_container_width=True)


# Descripción breve de los índices
st.markdown("### Descripción de los Índices")
descripciones = {
    'Matches Index': "Participación e influencia en partidos jugados.",
    'Conditional index': "Desempeño bajo condiciones específicas de juego.",
    'Goal Involment Index': "Participación directa e indirecta en goles.",
    'Passing Index': "Precisión y calidad de pases.",
    'Technical Skills Index': "Habilidad técnica general del jugador.",
    'Offensive Index': "Contribución ofensiva al equipo.",
    'Defensive index': "Desempeño en labores defensivas.",
    'Performance Index': "Valoración global del rendimiento.",
    'xPerformance Index': "Rendimiento esperado o Potencial según datos avanzados.",
    'Scouting Index': "Puntuación basada en criterios de scouting para su fichaje."
}

for indice, descripcion in descripciones.items():
    st.markdown(f"- **{indice}**: {descripcion}")

# Visualizaciones generales
st.header("Visualizaciones Generales")

# Distribución de edades
st.subheader("Distribución de Edades")
fig1, ax1 = plt.subplots(figsize=(10, 5))
sns.histplot(data["Age"], bins=20, kde=True, ax=ax1, color='skyblue')
ax1.set_xlabel("Edad")
ax1.set_ylabel("Cantidad de Jugadores")
st.pyplot(fig1)

# Valor de mercado promedio por equipo
st.subheader("Valor de Mercado Promedio por Equipo")
team_values = data.groupby("Team")["Market Value (M)"].mean().reset_index()
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x="Team", y="Market Value (M)", data=team_values, ax=ax2, palette='viridis')
ax2.set_xlabel("Equipo")
ax2.set_ylabel("Valor Promedio (M)")
ax2.set_title("Promedio de Valor de Mercado por Equipo")
ax2.tick_params(axis='x', rotation=90)
st.pyplot(fig2)




