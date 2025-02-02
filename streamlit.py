import streamlit as st
import pandas as pd
from data_pipeline import inquilinos_compatibles
from graphics import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

#Expande la aplicación para que ocupe toda la pantalla.
st.set_page_config(layout="wide")

#Se inicializa la variable resultado en None para almacenar el resultado de la búsqueda.
resultado = None
#Muestra una imagen en la parte superior de la aplicación.
#ajusta la imagen al ancho de la pagina 
st.image('./media/portada.png', use_container_width=True)
#Crea un espacio vertical de 60 píxeles utilizando st.markdown.
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True) #unsafe_allow_html=True → Permite usar HTML en Streamlit.

with st.sidebar:
    st.header("¿Quién está viviendo ya en el piso?") #agrega un titulo al menu lateral
    inquilino1 = st.text_input("Inquilino 1") #Crea campos de texto donde el usuario ingresa los IDs de los inquilinos actuales.
    inquilino2 = st.text_input("Inquilino 2")
    inquilino3 = st.text_input("Inquilino 3")

    num_compañeros = st.text_input("¿Cuántos nuevos compañeros quieres buscar?") #Permite ingresar cuántos compañeros nuevos se desean buscar.

    #Crea un botón que, al hacer clic, ejecuta el código dentro del if.
    if st.button('BUSCAR NUEVOS COMPAÑEROS'):
        try:
             topn = int(num_compañeros) #se convierte 'num_compañeros' a entero
        except ValueError:
             st.error("Por favor, ingresa un número válido para el número de compañeros.") # error para valores no numericos
             topn = None #ecitar fallos en el codigo

        id_inquilinos = obtener_id_inquilinos(inquilino1, inquilino2, inquilino3, topn) #Llama a la función obtener_id_inquilinos() para convertir los datos ingresados en números enteros.
        if id_inquilinos and topn is not None:
            resultado = inquilinos_compatibles(id_inquilinos, topn) #Solo busca si los IDs son válidos y topn es un número entero.

if isinstance(resultado, str):
    st.error(resultado) #Si el usuario ingresa IDs que no existen, se muestra Ningún ID coincide con la búsqueda de inquilinos.

elif resultado is not None:
    cols = st.columns((1, 2))  # Divide el layout en 2 columnas
    #Si resultado tiene datos válidos, se crean 2 columnas en la pantalla.
    #La primera columna será para el gráfico y la segunda para la tabla. 
    
    #mostrar el grafico de compatibilidad
    with cols[0]: #primera columna 
        st.write("Nivel de compatibilidad de cada nuevo compañero:") #muestra el titulo
        fig_grafico = generar_grafico_compatibilidad(resultado[1]) #genera un grafico de barras
        st.pyplot(fig_grafico) #muestra el grafico en la aplicacion 
     #Mostrar tabla comparativa
    with cols[1]: #segunda columna  
        st.write("Comparativa entre compañeros:")#muestra el titulo
        fig_tabla = generar_tabla_compatibilidad(resultado) #genera la tabla de comparacion
        st.plotly_chart(fig_tabla,use_container_width=True) #muestra la tabla interactiva en la aplicacion 
