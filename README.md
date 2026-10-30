# 🩺 Medical Image Analysis Tool

An AI-powered radiological diagnostic assistant designed to interpret complex medical imaging documents including **X-rays**, **MRIs**, **CT scans**, and **Ultrasounds**. This tool provides a structured, professional-grade clinical analysis coupled with patient-friendly explanations.

---

## ✨ Features

- **Multi-Modality Support:** Analyzes any medical imaging format (JPG, PNG, DICOM-derived images).
- **Structured Clinical Reporting:**
    - **Modality & Region Identification:** Precise anatomical positioning.
    - **Key Findings:** Systematic highlighting of abnormalities and measurements.
    - **Diagnostic Assessment:** Confidence-ranked primary and differential diagnoses.
- **Patient-Friendly Logic:** Translates clinical jargon into clear, relatable analogies for patients.
- **Research Grounding:** Automatically searches the web for the latest medical literature and treatment protocols supporting the findings.
- **Visual Intelligence:** Powered by **Groq (Qwen 3.8 27B)** for vision reasoning.

---

## 🛠️ Tech Stack

- **Model:** Groq `qwen/qwen3.8-27b` (vision-capable, or `llama-3.2-11b-vision-preview`)
- **Framework:** [Agno](https://github.com/agno-ai/agno)
- **Search Tool:** DuckDuckGo Tools
- **Image Processing:** PIL (Pillow)
- **UI:** Streamlit

---

## 🚀 How to Run

### Option A: Local Python Environment
1.  **Configure API Key:**
    Add your Groq key to `.env`:
    ```env
    GROQ_API_KEY=your_groq_api_key
    ```
2.  **Install dependencies & Launch:**
    ```bash
    pip install -r requirements.txt
    streamlit run medical.py
    ```

### Option B: Docker (Recommended)
1.  **Run with Docker Compose:**
    ```bash
    docker compose up --build
    ```
2.  **Or build and run manually:**
    ```bash
    docker build -t medical-image-app .
    docker run -p 8501:8501 --env-file .env medical-image-app
    ```
3.  Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔄 CI/CD Automation

This repository includes a GitHub Actions workflow in `.github/workflows/docker-ci-cd.yml` that:
- Automatically builds and tests the Docker container on pull requests and pushes to `main`.
- Publishes the validated container image to GitHub Container Registry (`ghcr.io`).

---

## 📋 Comprehensive Analysis Schema

The agent follows an expert-vetted reporting structure:
1. **Image Type & Region**
2. **Key Findings** (systematic observation)
3. **Diagnostic Assessment** (evidence-backed)
4. **Patient-Friendly Explanation**
5. **Research Context** (PubMed-adjacent grounding)

---

> [!IMPORTANT]
> **Disclaimer:** This tool is for educational and informational purposes only. All AI-generated analyses must be reviewed and validated by a qualified medical professional.

---

<div align="center">
    <b>AI-Assisted Diagnostics for the Modern Radiologist</b>
</div>
