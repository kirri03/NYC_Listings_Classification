
import streamlit as st
import time

st.set_page_config(page_title='Analisis AirBNB NY', layout='wide',     page_icon="📈")
st.image('ufv.png')

placeholder = st.empty()
with placeholder:
    for seconds in range(5):
        placeholder.write(f"⏳ {seconds} Cargando sistema")
        time.sleep(1)
placeholder.empty()


st.markdown(
    """
    Este dashboard mostrará unas tarjetas en las que se puede ver el precio mínimo, máximo de entre todos los alojamientos, así como el precio medio de alojarse en cada distrito (todos estos precios son por noche).Luego tiene 4 pestañas.

   En la primera pestaña podemos seleccionar el tipo de vivienda que queremos analizar entre los tres tipos que hay: habitación privada, casa o apartamento y habitación compartida (por defecto estará seleccionado habitación privada). Una vez seleccionado el tipo, el mapa se actualiza y solo nos muestra información relativa a este tipo.
   
   En este mapa cada distrito tiene un color según su precio medio y que aparecen puntos naranjas y rojos. Estos puntos representan alojamientos del tipo seleccionado baratos en comparación con el resto de alojamientos del mismo tipo y distrito. Los puntos rojos son aquellos cuyo precio es menor a 1/4 del precio medio de los alojamientos del mismo tipo y distrito y los puntos naranjas son aquellos cuyo precio es menor a 1/2 pero mayor a 1/4 del precio medio de los alojamientos de su tipo y distrito.

   En la segunda pestaña se muestra un gráfico de tarta en el cual se ve la cantidad de viviendas que hay en cada barrio respecto al total de viviendas. Si pasamos el ratón por encima también podremos ver cuál es el precio medio de cada uno de estos barrios.

   La tercera y cuarta pestaña son relativas a una funcionalidad que he incluido en la app para enviar y visualizar reseñas de los usuarios. Estas reseñas tienen los campos email, calificación (de 1 a 5 estrellas) y la posiblidad de dejar un comentario.
"""
)
