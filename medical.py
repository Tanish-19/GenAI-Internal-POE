import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from PIL import Image as PILImage

from agno.agent import Agent
from agno.media import Image as AgnoImage
from agno.models.groq import Groq

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("Set GROQ_API_KEY in .env or in your environment before starting the app.")

# Default to Groq's supported vision model (can be overridden via GROQ_MODEL_ID)
MODEL_ID = os.getenv("GROQ_MODEL_ID", "qwen/qwen3.8-27b")

medical_agent = Agent(
    model=Groq(id=MODEL_ID, api_key=GROQ_API_KEY),
    markdown=True,
)

QUERY = """
You are a medical-imaging education assistant. Analyze the supplied image cautiously
and produce a structured markdown report with these sections:

1. Image Type & Region: modality, anatomy, positioning, and image quality.
2. Key Findings: systematic observations and possible abnormalities.
3. Diagnostic Assessment: likely interpretation, confidence, differentials, and any
   potentially urgent findings. State clearly when the image is insufficient.
4. Patient-Friendly Explanation: explain the observations in plain language.
5. Educational context: describe relevant general clinical concepts. Do not claim to
   have searched the web or provide unverified citations.

This is educational information, not a diagnosis. Recommend evaluation by a qualified
clinician and immediate care for possible emergency findings.
"""


def analyze_medical_image(image_file) -> str:
    """Resize an uploaded image and request a Groq vision analysis."""
    suffix = Path(image_file.name).suffix or ".png"
    temp_path = None
    try:
        with PILImage.open(image_file) as image:
            image = image.convert("RGB")
            image.thumbnail((1200, 1200))
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
                temp_path = temp_file.name
            image.save(temp_path)

        response = medical_agent.run(QUERY, images=[AgnoImage(filepath=temp_path)])
        return response.content
    except Exception as exc:
        return f"Analysis error: {exc}"
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


st.set_page_config(page_title="Medical Image Analysis", layout="centered")
st.title("Medical Image Analysis Tool")
st.caption("Educational use only — not a substitute for a clinician's interpretation.")

uploaded_file = st.file_uploader(
    "Upload a medical image",
    type=["jpg", "jpeg", "png", "bmp", "gif"],
)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded image", width="stretch")
    if st.button("Analyze image", type="primary"):
        with st.spinner("Analyzing the image..."):
            report = analyze_medical_image(uploaded_file)
        st.subheader("Analysis report")
        st.markdown(report)
else:
    st.info("Upload an image to begin.")
