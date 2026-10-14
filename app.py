"""
Rubshi AI Agent - Streamlit Edition
Pink Paradise with AI
"""

import os
import base64
import streamlit as st
from google import genai

st.set_page_config(page_title="Rubshi AI", page_icon="🌸", layout="centered")

BG_PATH = "background.jpg"
bg_base64 = ""

try:
    with open(BG_PATH, "rb") as f:
        bg_base64 = base64.b64encode(f.read()).decode()
except Exception:
    pass

if bg_base64:
    bg_css = f"background-image: url('data:image/jpeg;base64,{bg_base64}');"
else:
    bg_css = "background: linear-gradient(135deg, #ffd1dc 0%, #ffb6c1 50%, #ffc0cb 100%);"

st.markdown(f"""
<style>
.stApp {{
    {bg_css}
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}
h1 {{
    text-align: center !important;
    color: #ffffff !important;
    text-shadow: 0 0 25px rgba(255, 105, 180, 1), 2px 2px 10px rgba(0, 0, 0, 0.4) !important;
    font-size: 2.5em !important;
    font-weight: 800 !important;
}}
h3 {{
    text-align: center !important;
    color: #ffffff !important;
    text-shadow: 1px 1px 8px rgba(0, 0, 0, 0.5) !important;
}}
.stChatMessage {{
    background: rgba(255, 255, 255, 0.8) !important;
    border-radius: 16px !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 182, 193, 0.6) !important;
}}
.stChatInput textarea {{
    background: rgba(255, 255, 255, 0.95) !important;
    border-radius: 14px !important;
    border: 2px solid rgba(255, 182, 193, 0.9) !important;
    color: #4a1a2c !important;
}}
footer {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

st.markdown("# Rubshi AI")
st.markdown("### Tomar cute personal AI assistant")

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.environ.get("GEMINI_API_KEY", "")

if not api_key:
    st.error("API key nei. Streamlit Cloud e Secrets e GEMINI_API_KEY add koro.")
    st.stop()

client = genai.Client(api_key=api_key)

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
    "gemini-flash-latest",
]

SYSTEM_PROMPT = """Tumi "Rubshi" - ekta friendly, cute, smart personal AI assistant.

Rules:
- User jei bhashay likhbe, tumi sei bhashay uttor dibe. Bangla hole shohoj Bangla.
- Friendly, warm, helpful tone e kotha bolo. Majhe majhe emoji use koro.
- Short, clear uttor dao. Proyojon na thakle lamba lekho na.
- Jodi sure na hou, shotti kotha bolo - bhul information diye na.
"""


def build_prompt(message, history):
    parts = [SYSTEM_PROMPT, "", "Conversation so far:"]
    recent_history = (history or [])[-4:]

    for item in recent_history:
        role = item.get("role", "")
        content = item.get("content", "")
        content = str(content).strip()
        if role == "user" and content:
            parts.append(f"User: {content}")
        elif role == "assistant" and content:
            parts.append(f"Rubshi: {content}")

    parts.append(f"User: {message.strip()}")
    parts.append("Rubshi:")
    return "\n".join(parts)


def get_response(message, history):
    prompt = build_prompt(message, history)

    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip()
        except Exception:
            continue

    return "Dukkhito, ekhon uttor dite parchi na. Abar chesta koro."


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ekhane tomar proshno likho..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Rubshi bhabche..."):
            answer = get_response(prompt, st.session_state.messages[:-1])
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
