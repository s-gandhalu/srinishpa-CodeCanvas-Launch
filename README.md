# 💡 CodeCanvas: Flowchart-to-Code Translator


CodeCanvas is an innovative, multi-lingual educational tool that bridges the gap between conceptual logic and executable syntax. It allows students and developers to convert handwritten algorithms (flowcharts or pseudocode) directly into clean, functional code using a sophisticated blend of computer vision and generative AI.

The application is built using a modern **Streamlit frontend** and designed with a premium, high-contrast aesthetic to provide a seamless user experience.

## ✨ Core Features

* **Multimodal Translation:** Converts visual logic (flowcharts) into production-ready code in multiple languages (Python, Java, C++, C).
* **Aesthetic UI:** Features a high-contrast, interactive interface built on Streamlit with custom CSS and a video-backed launch page.
* **Intelligent Backend Pipeline:**
    1.  **Computer Vision (YOLOv8):** Detects and isolates flowchart shapes and arrows.
    2.  **OCR (EasyOCR):** Extracts handwritten text from the detected shapes.
    3.  **Generative AI (Gemini):** Analyzes the structured flow and generates the final code output.
* **Model Stability:** Utilizes Streamlit's resource caching to ensure the heavy YOLO and Gemini models load quickly and remain stable across user sessions.

## 🚀 Getting Started (Deployment & Setup)

This project requires Python 3.9+ and is designed for easy deployment on Streamlit Community Cloud.

### 1. Prerequisites

Ensure you have your **Gemini API Key** and a local copy of the trained YOLO model weights (`best.pt`).

### 2. Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/AAC-Open-Source-Pool/25AACL03.git](https://github.com/AAC-Open-Source-Pool/25AACL03.git)
    cd 25AACL03
    ```

2.  **Create and Activate Environment:**
    ```bash
    python -m venv .venv
    ./.venv/Scripts/Activate.ps1  # (For Windows PowerShell)
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Running Locally

Before running, place your API key securely in the following file:

**`.streamlit/secrets.toml`**
```toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

Then, run the main launch file:
streamlit run Home.py

4. Deployment on Streamlit Cloud
The app is configured to run via Home.py. To deploy:

Connect your GitHub repository to Streamlit Cloud.

Set the main file to Home.py.

CRITICAL STEP: Paste your GEMINI_API_KEY into the Secrets management panel on the Streamlit Cloud dashboard.

🗃️ Project Structure
CodeCanvas_App/
├── .streamlit/         # Contains secrets.toml (for local dev)
├── models/             # Contains best.pt (YOLO weights)
├── pages/
│   └── 1_Flowchart_Translator.py  # Main functionality
├── static/             # Contains blackpurple.jpg (Background image)
├── requirements.txt    # Project dependencies
└── Home.py             # Video launch page (Entry Point)

🧑‍💻 Contribution
Feel free to open issues or submit pull requests!
