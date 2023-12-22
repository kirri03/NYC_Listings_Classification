import pandas as pd

import streamlit as st
import plotly.express as px

import requests

import geopandas as gpd
import folium
from streamlit_folium import folium_static 

@st.cache_data()
def load_data(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return pd.DataFrame(r.json())


@st.cache_data()
def load_tarjetas(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def submit_review(email, rating, comment):
    data = {"email": email, "rating": rating, "comment": comment}
    respuesta = requests.post("http://fastapi:8000/submit_review", json=data)
    return respuesta.text

def load_reviews(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def info_box (texto, color=None):
    st.markdown(f'<div style = "background-color:#4EBAE1;opacity:70%"><p style="text-align:center;color:white;font-size:30px;">{texto}</p></div>', unsafe_allow_html=True)

def display_stars(rating):
    stars = '⭐️' * rating
    return stars

tarjetas=load_tarjetas('http://fastapi:8000/retrieve_tarjetas')

st.header("Información general")

col1, col2= st.columns(2)

col3, col4, col5, col6, col7 = st.columns(5)

with col1:
    col1.subheader("Precio más barato")
    info_box(tarjetas[0])
with col2:
    col2.subheader("Precio más caro")
    info_box(tarjetas[1])
with col3:
    col3.subheader("Precio medio Brooklyn")
    info_box(tarjetas[2])
with col4:
    col4.subheader("Precio medio Manhattan")
    info_box(tarjetas[3])
with col5:
    col5.subheader("Precio medio Queens")
    info_box(tarjetas[4])
with col6:
    col6.subheader("Precio medio Bronx")
    info_box(tarjetas[5])
with col7:
    col7.subheader("Precio medio Staten Island")
    info_box(tarjetas[6])

tab1, tab2, tab3, tab4 = st.tabs(["Mapa", "Cantidad de viviendas y precio según barrio", "Enviar reseña de la app", "Ver reseñas"])


with tab1:
    # Hacemos solicitud get de las primeras 5000 filas que son las que vamos a analizar
    data = load_data('http://fastapi:8000/retrieve_data')

    # Obtenemos los tipos de vivienda que hay
    tipos_vivienda = data['room_type'].unique()

    # Subtitulo
    st.subheader("Precio medio de la zona y viviendas más baratas de la zona")

    # Información
    st.markdown(f'<div><p style="text-align:center;color:blue;font-size:15px;">Este mapa representa el precio medio de cada barrio (ver leyenda). Los puntos rojos que aparecen representan alojamientos muy baratos en comparación con alojamientos del mismo tipo en el mismo barrio. Los puntos naranjas son también baratos en comparación, pero no tanto como los puntos rojos.</p></div>', unsafe_allow_html=True)
    
    # Widget de selección para el tipo de vivienda
    tipo_vivienda_seleccionado = st.selectbox('Selecciona el tipo de vivienda:', tipos_vivienda)

    # Filtramos datos según el tipo de vivienda seleccionado
    filtro = data[data['room_type'] == tipo_vivienda_seleccionado]

    # Calculamos el precio promedio por barrio
    precio_promedio = filtro.groupby('neighbourhood_group')['price'].mean().reset_index()

    # Cargamos los límites de los barrios de Nueva York
    nyc = gpd.read_file(gpd.datasets.get_path('nybb'))

    # Fusionamos los límites de los barrios con los precios promedio filtrados por tipo de vivienda
    nyc = nyc.merge(precio_promedio, left_on='BoroName', right_on='neighbourhood_group')

    # Creamos un mapa centrado en Nueva York
    nyc_map = folium.Map(location=[40.7, -74], zoom_start=10)

    # Agregamos los límites de los barrios con colores según el precio promedio
    folium.Choropleth(
        geo_data=nyc,
        name='Precio Promedio',
        data=nyc,
        columns=['neighbourhood_group', 'price'],
        key_on='feature.properties.neighbourhood_group',
        fill_color='YlGnBu',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name='Precio Promedio'
    ).add_to(nyc_map)

    # Mostramos puntos de viviendas filtradas por tipo y cuyo precio sea inferior a la mitad del precio promedio del barrio
    for _, row in filtro.iterrows():
        if row['price'] < nyc[nyc['neighbourhood_group'] == row['neighbourhood_group']]['price'].values[0] / 4:
            folium.CircleMarker(location=[row['latitude'], row['longitude']],
                                radius=1.5,
                                color='red',
                                fill=True,
                                fill_color='red',
                                fill_opacity=0.7,
                                tooltip=f"Nombre: {row['name']}<br>Precio: ${row['price']:.2f}"
                                ).add_to(nyc_map)
            
        elif row['price'] < nyc[nyc['neighbourhood_group'] == row['neighbourhood_group']]['price'].values[0] / 2:
            folium.CircleMarker(location=[row['latitude'], row['longitude']],
                                radius=0.2,
                                color='orange',
                                fill=True,
                                fill_color='orange',
                                fill_opacity=0.7,
                                tooltip=f"Nombre: {row['name']}<br>Precio: ${row['price']:.2f}"
                                ).add_to(nyc_map)
            
        
    folium.LayerControl().add_to(nyc_map)
    folium_static(nyc_map)

with tab2:
    # Obtenemos el precio medio por barrio
    precio_promedio_barrio = data.groupby('neighbourhood')['price'].mean().reset_index()
    precio_promedio_barrio.columns = ['neighbourhood', 'avg_price']

    # Obtenemos el porcentaje de viviendas por barrio
    porcentaje_viviendas = data['neighbourhood'].value_counts(normalize=True).reset_index()
    porcentaje_viviendas.columns = ['neighbourhood', 'percentage']

    # Multiplicamos el porcentaje por 100
    porcentaje_viviendas['percentage'] *= 100

    # Fusionamos los DataFrames para tener precio promedio y porcentaje de viviendas por barrio
    datos_grafico = precio_promedio_barrio.merge(porcentaje_viviendas, on='neighbourhood')

    # Gráfico de tarta con porcentaje de viviendas por barrio y precio medio
    fig_pie = px.pie(datos_grafico, values='percentage', names='neighbourhood', 
                     hover_data={'avg_price': True}, 
                     title='Porcentaje de viviendas por barrio y precio medio')
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("Reseña de la Aplicación")
    st.write("Dejanos saber tu opinión sobre la aplicación.")

    # Formulario para enviar la reseña
    email = st.text_input("Email")
    rating = st.slider("Calificación (1-5)", min_value=1, max_value=5, value=3)
    comment = st.text_area("Comentario")

    if st.button("Enviar Reseña"):
        if email and rating:
            response = submit_review(email, rating, comment)
            st.success("Reseña enviada exitosamente.")
        else:
            st.warning("Por favor, complete al menos los dos primeros campos antes de enviar la reseña.")

with tab4:
    reviews= load_reviews('http://fastapi:8000/retrieve_reviews')
    if reviews:
        for review in reviews:
            #info_box(f"Email: {review['email']}<br>Calificación: {review['rating']}<br>Comentario: {review['comment']}")
            st.markdown(f"<div style= 'padding:20px;border:1px solid #4EBAE1;border-radius:5px;margin:20px;background-color:#4EBAE1; opacity:70%;'><p style='color:white;'>Email: {review['email']}<br>Calificación: {display_stars(review['rating'])}<br>Comentario: {review['comment']}</p></div>",unsafe_allow_html=True)
    else:
        st.warning("No hay reseñas disponibles en este momento.")