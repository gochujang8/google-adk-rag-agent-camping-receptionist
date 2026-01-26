"""Streamlit UI for Camping La Rosaleda Agent."""

import streamlit as st
import asyncio
import uuid
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from rag.agent import root_agent

# Page config
st.set_page_config(
    page_title="Camping La Rosaleda",
    page_icon="🏕️",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏕️ Camping La Rosaleda")
st.markdown("*Asistente virtual de recepcion*")
st.divider()

# Constants
APP_NAME = "camping-la-rosaleda"
USER_ID = "streamlit-user"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "session_service" not in st.session_state:
    st.session_state.session_service = InMemorySessionService()

if "runner" not in st.session_state:
    st.session_state.runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=st.session_state.session_service,
    )

async def create_session_if_needed(session_service, user_id, session_id):
    """Create session if it doesn't exist."""
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )
    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
    return session

async def get_agent_response(runner, session_service, user_id, session_id, prompt):
    """Get response from the agent asynchronously."""
    # Ensure session exists
    await create_session_if_needed(session_service, user_id, session_id)

    content = types.Content(
        role="user",
        parts=[types.Part(text=prompt)]
    )

    response_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        response_text += part.text

    return response_text

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Escribe tu consulta aqui..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from agent
    with st.chat_message("assistant"):
        with st.spinner("Consultando..."):
            try:
                # Run async function
                response_text = asyncio.run(
                    get_agent_response(
                        st.session_state.runner,
                        st.session_state.session_service,
                        USER_ID,
                        st.session_state.session_id,
                        prompt
                    )
                )

                if not response_text:
                    response_text = "Lo siento, no he podido procesar tu consulta. Por favor, intenta de nuevo."

                st.markdown(response_text)

                # Add assistant message to history
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar with info
with st.sidebar:
    st.header("Informacion")
    st.markdown("""
    **Camping La Rosaleda**

    Puedes preguntarme sobre:
    - Precios de parcelas y bungalows
    - Disponibilidad
    - Servicios del camping
    - Normas y politicas
    - Reservas

    ---

    **Temporadas:**
    - Baja: Ene-Abr, Oct-Dic
    - Media: May-10Jul, 16Ago-Sep
    - Alta: 11Jul-15Ago
    """)

    if st.button("Nueva conversacion"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
