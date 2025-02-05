import streamlit as st
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Cargar variables de entorno
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

# Crear cliente de Azure Question Answering
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

# Diseño de la aplicación en Streamlit
st.set_page_config(page_title="Chatbot AI", page_icon="💬", layout="centered")
st.title("🤖 Chatbot con Azure QnA")
st.write("Hazme una pregunta sobre la base de conocimientos.")

# Input de usuario
user_question = st.text_input("Escribe tu pregunta aquí:")

if st.button("Preguntar"):
    if user_question:
        try:
            response = ai_client.get_answers(question=user_question,
                                            project_name=ai_project_name,
                                            deployment_name=ai_deployment_name)
            
            if response.answers:
                for candidate in response.answers:
                    st.markdown(f"### 📝 Respuesta: {candidate.answer}")
                    st.write(f"📊 **Confianza:** {candidate.confidence:.2f}")
                    st.write(f"📚 **Fuente:** {candidate.source}")
            else:
                st.warning("No se encontró una respuesta relevante.")
        except Exception as ex:
            st.error(f"Error: {ex}")
    else:
        st.warning("Por favor, ingresa una pregunta antes de hacer clic en 'Preguntar'.")

# Pie de página
st.markdown("---")
st.write("Desarrollado con ❤️ usando Streamlit y Azure AI.")
