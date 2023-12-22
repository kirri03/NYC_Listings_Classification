# Práctica final programación II

   # Instrucciones de ejecución:
   
   Para ejecutar mi aplicación es necesario que el docker engine esté corriendo y desde la terminal desplazarse hasta la carpeta practica_ufv.
   Una vez dentro de está carpeta se tiene que hacer un docker-compose up para crear los servicios de streamlit y fastapi, creando un contenedor
   para cada uno de estos servicios, en caso de no estar creados (primera vez que se ejecuta este comando)  y poniendolos en funcionamiento según las especificaciones de dicho archivo. Además la BBDD no va a aparecer en local, aparecerá en el volumne de docker 'practica_ufv_mis_datos' dentro del contenedor fastapi en la carpeta fastapi como nyc_data.db. Después el usuario debería de poder ver la aplicación en localhost:8501.

   Una vez que se introduzca localhost:8501, se podrá ver una breve introducción sobre lo que se va a exponer y si seleccionamos la pagina dashboard, visualizaremos un dashboard que analizará un dataset correspondiente a alojamientos de AirBNB de la ciudad de Nueva York que encontré en kaggle: https://www.kaggle.com/datasets/thedevastator/airbnbs-nyc-overview/data. Este dashboard mostrará unas tarjetas en las que se puede ver el precio mínimo, máximo de entre todos los alojamientos, así como el precio medio de alojarse en cada distrito (todos estos precios son por noche). Luego tiene 4 pestañas.

   En la primera pestaña podemos seleccionar el tipo de vivienda que queremos analizar entre los tres tipos que hay: habitación privada, casa o apartamento y habitación compartida (por defecto estará seleccionado habitación privada). Una vez seleccionado el tipo, el mapa se actualiza y solo nos muestra información relativa a este tipo. En este mapa cada distrito tiene un color según su precio medio y que aparecen puntos naranjas y rojos. Estos puntos representan alojamientos del tipo seleccionado baratos en comparación con el resto de alojamientos del mismo tipo y distrito. Los puntos rojos son aquellos cuyo precio es menor a 1/4 del precio medio de los alojamientos del mismo tipo y distrito y los puntos naranjas son aquellos cuyo precio es menor a 1/2 pero mayor a 1/4 del precio medio de los alojamientos de su tipo y distrito.

   En la segunda pestaña se muestra un gráfico de tarta en el cual se ve la cantidad de viviendas que hay en cada barrio respecto al total de viviendas. Si pasamos el ratón por encima también podremos ver cuál es el precio medio de cada uno de estos barrios.

   La tercera y cuarta pestaña son relativas a una funcionalidad que he incluido en la app para enviar y visualizar reseñas de los usuarios. Estas reseñas tienen los campos email, calificación (de 1 a 5 estrellas) y la posiblidad de dejar un comentario.

   Para desarrollar esta aplicación he utilizado streamlit para el frontend y fastapi para el backend.
   
   En el frontend también he tenido que utiizar librerías como pandas para poder usar dataframes que facilitan el manejo de datos, requests para enviar solicitudes al servidor, geopandas y folium para los mapas y para el gráfico de tarta utilizo plotly.express

   En el backend también he utilizado pandas para el manejo de datos, basemodel para las validaciones y el ORM SQLAlchemy para facilitar las tareas asociadas con la base de datos. EL SGBD que empleé es SQLite puesto que me pareció el más sencillo de implementar y para este proyecto tampoco necesitaba características más avanzadas que pueden ofrecer otros SGBD como PostgreSQL por ejemplo.

   Además he separado el volcado de datos en 3 métodos get separados:
   
   El primer metodo get obtiene las 5000 primeras filas de la tabla de la base de datos (puesto que con más filas había veces que no se cargaban correctamente los mapas) que contiene la información relativa al id, nombre, distrito, barrio, latitud, longitud, tipo de habitación y precio de los AirBNB de NY que utilizaré para los mapas y el gráfico de tarta.

   El segundo método get obtiene únicamente la información que se muestra a través de las tarjetas y que se calcula desde el backend utilizando todas las filas de la tabla "nyc_listings".

   El tercer método get obtiene las reseñas de la tabla "reviews" de la base de datos que se muestran al usuario en la pestaña "Ver reseñas".

   Además hay un método post que es el encargado de mandar al servidor las reviews realizadas por el usuario. Estás reviews son incluidas en la BBDD y se pueden enviar a través de la pestaña "Enviar reseña de la app".
