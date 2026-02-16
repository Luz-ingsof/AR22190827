import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import time

# Configuración visual estilo "Hacker / Dark Mode"
st.set_page_config(page_title="Visual Traceroute Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; }
    stButton>button { background-color: #00ff41; color: black; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛰️ Visual Traceroute Global")
st.write("Rastrea la ruta física de tus datos por el mundo.")

# Entrada de usuario
target = st.text_input("Introduce Dominio o IP (ej: google.com)", "8.8.8.8")

if st.button("INICIAR RASTREO"):
    # Usamos una API gratuita para simular el traceroute y obtener geolocalización
    # Nota: Usamos ip-api que es excelente para aprendizaje
    with st.spinner('Conectando con nodos globales...'):
        try:
            # 1. Obtenemos la IP del destino si es un dominio
            res_dest = requests.get(f"http://ip-api.com/json/{target}").json()
            
            if res_dest['status'] == 'fail':
                st.error("No se pudo encontrar el destino. Revisa el nombre.")
            else:
                dest_lat, dest_lon = res_dest['lat'], res_dest['lon']
                
                # 2. Simulamos saltos intermedios para el mapa 
                # (En una versión Pro usarías una API de pago como Ip2Location)
                # Aquí creamos una ruta visual desde tu ubicación supuesta hacia el destino
                rutas = [
                    {"name": "Tu Red", "lat": -34.60, "lon": -58.38}, # Ejemplo: Buenos Aires
                    {"name": "Nodo Intermedio", "lat": 25.76, "lon": -80.19}, # Miami
                    {"name": "Servidor Destino", "lat": dest_lat, "lon": dest_lon}
                ]
                
                df = pd.DataFrame(rutas)

                # 3. Crear el Mapa con líneas (Trace)
                fig = go.Figure()

                # Dibujar las líneas entre los puntos
                fig.add_trace(go.Scattergeo(
                    lat = df['lat'],
                    lon = df['lon'],
                    mode = 'lines+markers',
                    line = dict(width = 2, color = '#00ff41'),
                    marker = dict(size = 8, color = '#00ff41', symbol = 'circle'),
                    text = df['name']
                ))

                fig.update_layout(
                    title = f'Ruta de conexión hacia {target}',
                    geo = dict(
                        scope='world',
                        projection_type='orthographic', # Mapa tipo Globo 3D
                        showland=True,
                        landcolor="rgb(30, 30, 30)",
                        oceancolor="rgb(10, 10, 10)",
                        showocean=True,
                        bgcolor="rgba(0,0,0,0)"
                    ),
                    margin=dict(l=0, r=0, t=40, b=0),
                    paper_bgcolor="black"
                )

                st.plotly_chart(fig, use_container_width=True)
                
                # Mostrar tabla de datos
                st.subheader("📊 Detalles de los saltos")
                st.table(df)

        except Exception as e:
            st.error(f"Error de conexión: {e}")

st.caption("Nota: Esta versión usa una ruta simplificada para garantizar compatibilidad en la nube.")
