import streamlit as st
import google.generativeai as genai
import replicate
import os
import html
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GOOGLE_API_KEY")
replicate_api_key = os.getenv("REPLICATE_API_TOKEN")

# Check API keys
if not gemini_api_key or not replicate_api_key:
    st.error("Missing API Key(s)! Please ensure both GOOGLE_API_KEY and REPLICATE_API_TOKEN are in your .env file.")
    st.stop()

# Configure Gemini
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Configure Replicate
replicate.Client(api_token=replicate_api_key)

# Page settings
st.set_page_config(page_title="Multimodal Chatbot", layout="centered")
st.title("🤖 Multimodal Chatbot (Text ↔️ Image)")

# Session states
if "text_history" not in st.session_state:
    st.session_state.text_history = []
if "image_history" not in st.session_state:
    st.session_state.image_history = []
if "combined_history" not in st.session_state:
    st.session_state.combined_history = []

# --- TABS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "💬 Text Chat",
    "🖼️ Image Captioning",
    "🖼️💬 Image + Prompt",
])

# --- TAB 1: TEXT CHAT ---
with tab1:
    st.subheader("💬 Ask anything (Text only)")
    prompt = st.text_input("Enter your message:")
    if st.button("Generate Response", key="text_btn") and prompt.strip():
        with st.spinner("Gemini is thinking..."):
            try:
                response = model.generate_content(prompt)
                reply = html.escape(response.text).replace("\n", "<br>")
                escaped_prompt = html.escape(prompt).replace("\n", "<br>")
                st.markdown(f"""
                    <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; color:#ffffff;'>
                        <strong style='color:#64B5F6;'>🧑 You:</strong><br>{escaped_prompt}<br><br>
                        <strong style='color:#2E7D32;'>🤖 Gemini:</strong><br>{reply}
                    </div>
                """, unsafe_allow_html=True)
                st.session_state.text_history.append(("You", prompt))
                st.session_state.text_history.append(("Gemini", response.text))
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.text_history:
        st.markdown("---\n### 📜 Chat History")
        for i in range(0, len(st.session_state.text_history), 2):
            if i + 1 < len(st.session_state.text_history):
                user_msg = html.escape(st.session_state.text_history[i][1]).replace("\n", "<br>")
                bot_msg = html.escape(st.session_state.text_history[i + 1][1]).replace("\n", "<br>")
                st.markdown(f"""
                    <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; color:#ffffff;'>
                        <strong style='color:#64B5F6;'>🧑 You:</strong><br>{user_msg}<br><br>
                        <strong style='color:#2E7D32;'>🤖 Gemini:</strong><br>{bot_msg}
                    </div>
                """, unsafe_allow_html=True)

# --- TAB 2: IMAGE CAPTIONING ---
with tab2:
    st.subheader("🖼️ Upload an Image to Get a Caption")
    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Generate Caption", key="img_btn"):
            with st.spinner("Gemini is captioning..."):
                try:
                    response = model.generate_content([image])
                    caption = html.escape(response.text).replace("\n", "<br>")
                    st.markdown(f"""
                        <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; color:#ffffff;'>
                            <strong style='color:#2E7D32;'>🖋️ Caption:</strong><br>{caption}
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.image_history.append(("🖼️ Uploaded", uploaded.name))
                    st.session_state.image_history.append(("🤖 Caption", response.text))
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.image_history:
        st.markdown("---\n### 🖼️ Image Caption History")
        for i in range(0, len(st.session_state.image_history), 2):
            if i + 1 < len(st.session_state.image_history):
                label = html.escape(st.session_state.image_history[i][1])
                caption = html.escape(st.session_state.image_history[i + 1][1]).replace("\n", "<br>")
                st.markdown(f"""
                    <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; color:#ffffff;'>
                        <strong style='color:#64B5F6;'>🧑 Image:</strong><br>{label}<br><br>
                        <strong style='color:#2E7D32;'>🤖 Caption:</strong><br>{caption}
                    </div>
                """, unsafe_allow_html=True)

# --- TAB 3: IMAGE + TEXT ---
with tab3:
    st.subheader("🖼️💬 Upload Image + Ask a Question")
    img_input = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key="combo")
    text_input = st.text_input("Enter your question about the image:")
    if img_input:
        image = Image.open(img_input).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image + Prompt"):
            with st.spinner("Gemini is analyzing..."):
                try:
                    response = model.generate_content([image, text_input])
                    reply = html.escape(response.text).replace("\n", "<br>")
                    escaped_prompt = html.escape(text_input).replace("\n", "<br>")
                    st.markdown(f"""
                        <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; color:#ffffff;'>
                            <strong style='color:#64B5F6;'>🧑 You:</strong><br>{escaped_prompt}<br><br>
                            <strong style='color:#2E7D32;'>🤖 Gemini:</strong><br>{reply}
                        </div>
                    """, unsafe_allow_html=True)
                    st.session_state.combined_history.append(("📷 Image + Prompt", text_input))
                    st.session_state.combined_history.append(("🤖 Gemini", response.text))
                except Exception as e:
                    st.error(f"Error: {e}")

    if st.session_state.combined_history:
        st.markdown("---\n### 📜 Combined History")
        for i in range(0, len(st.session_state.combined_history), 2):
            if i + 1 < len(st.session_state.combined_history):
                q = html.escape(st.session_state.combined_history[i][1]).replace("\n", "<br>")
                a = html.escape(st.session_state.combined_history[i + 1][1]).replace("\n", "<br>")
                st.markdown(f"""
                    <div style='background-color:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:15px; color:#ffffff;'>
                        <strong style='color:#64B5F6;'>🧑 Question:</strong><br>{q}<br><br>
                        <strong style='color:#2E7D32;'>🤖 Gemini:</strong><br>{a}
                    </div>
                """, unsafe_allow_html=True)