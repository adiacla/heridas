# streamlit_audio_recorder y whisper by Alfredo Diaz - version Mayo 2024

# En VsC seleccione la version de Python (recomiendo 3.9) 
#CTRL SHIFT P  para crear el enviroment (Escriba Python Create Enviroment) y luego venv 

#o puede usar el siguiente comando en el shell
#Vaya a "view" en el menú y luego a terminal y lance un terminal.
#python -m venv env

#Verifique que el terminal inicio con el enviroment o en la carpeta del proyecto active el env.
#cd .venv\Scripts\
#.\activate 

#Debe quedar asi: (.venv) (.venv) C:\Users\adiaz\Documents\heridas>
#Regrese al directorio colnado

#Puedes verificar que no tenga ningun libreria preinstalada con
#pip freeze
#Actualice pip con pip install --upgrade pip

#pip install tensorflow==2.15 La que tiene instalada Google Colab o con la versión qu fué entrenado el modelo
#Verifique se se instaló numpy, no trate de instalar numpy con pip install numpy, que puede instalar una version diferente
#pi freeze  Verifique l version instalada, numpy y PILLOW
#pip install streamlit
#Verifique se se instaló no trante de instalar con pip install pillow
#Esta instalacion se hace si la requiere pip install opencv-python

#Descargue una foto de una flor que le sirva de ícono 

# importing the libraries and dependencies needed for creating the UI and supporting the deep learning models used in the project
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import streamlit as st  
import tensorflow as tf # TensorFlow is required for Keras to work
from PIL import Image
import numpy as np

# ocultar advertencias de desuso que no afectan directamente el funcionamiento de la aplicación
import warnings
warnings.filterwarnings("ignore")

# establecer algunas configuraciones predefinidas para la página, como el título de la página, el ícono del logotipo, el estado de carga de la página (si la página se carga automáticamente o si necesita realizar alguna acción para cargar)
st.set_page_config(
    page_title="Reconocimiento de heridas o suturas de cirugia de corazon abierto",
    page_icon = ":smile:",
    initial_sidebar_state = 'auto'
)

# ocultar la parte del código, ya que esto es solo para agregar algún estilo CSS personalizado pero no es parte de la idea principal
hide_streamlit_style = """
	<style>
  #MainMenu {visibility: hidden;}
	footer {visibility: hidden;}
  </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True) # Oculta el código CSS de la pantalla, ya que están incrustados en el texto de rebajas. Además, permita que Streamlit se procese de forma insegura como HTML

#st.set_option('deprecation.showfileUploaderEncoding', False)

@st.cache_resource
def load_model():
    model=tf.keras.models.load_model('./model/heridas_model.h5')
    return model
with st.spinner('Modelo está cargando..'):
    model=load_model()
    


with st.sidebar:
        st.image('corazon3.jpg')
        st.title("Identificación de Heridas o suturas Alteradas")
        st.subheader("Reconocimiento de imagen para heridas o sutura de cirugia de corazón abierto")
        confianza = st.slider("Nivel de confianza esperado?", 0.0, 1.0, 0.1)

st.image('corazon.jpg')
st.title("Inteligencia Artificial")
st.write("Somos un equipo apasionado de profesionales dedicados a hacer la diferencia")
st.write("""
         # Reconocimiento de Imagen para heridas o sutura de corazón abierto
         """
         )


def import_and_predict(image_data, model, class_names):
    
    image_data = image_data.resize((180, 180))
    
    img_array  = tf.keras.utils.img_to_array(image_data)
    img_array  = tf.expand_dims(image, 0) # Create a batch

    
    # Hacer la predicción
    predictions = model.predict(img_array)
    print(predictions)
    # Interpretar la predicción
    if predictions[0] > 0.5:
        class_name='Alterada'
    else:
        class_name='No_alterada'
    
    return class_name, predictions[0] 


class_names = open("./model/clases.txt", "r").readlines()

img_file_buffer = st.camera_input("Capture una foto referiblemente centrada en la herida o sutura")
if img_file_buffer is None:
    st.text("Por favor tome una foto")
else:
    image = Image.open(img_file_buffer)
    st.image(image, use_column_width=True)
    
    # Realizar la predicción
    class_name, score = import_and_predict(image, model, class_names)
    
    # Mostrar el resultado

    if np.max(score)>confianza:
        st.header(f"Estado de la sutura: {class_name}")
        st.subheader(f"Puntuación de confianza: {100 * np.max(score) :.2f}%")
    else:
        st.subheader(f"Con el nivel de confianza {confianza:.2f}% no podria identificar el estado de la sutura")
        