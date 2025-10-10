💡 CodeCanvas: Flowchart-to-Code Translator
CodeCanvas is an innovative, production-ready web application that transforms conceptual logic (flowcharts, pseudocode) into executable source code using a combination of computer vision and generative AI.

The application features an advanced, interactive frontend aesthetic that provides a seamless user experience.

✨ Core Features
Premium Aesthetic: Features a high-contrast, interactive interface with a full-screen video background on the launch page and a Glassmorphism-styled dashboard for the translator.

Seamless Multipage Navigation: Uses the most stable methods for navigation and CSS injection to ensure a perfectly centered, non-scrolling launch experience.

Multilingual Generation: Converts visual logic into Python, Java, C++, or C by dynamically adapting the prompt for the Gemini LLM.

Intelligent Backend Pipeline:

Computer Vision (YOLOv8 & EasyOCR): Detects shapes, arrows, and extracts handwritten text.

Generative AI (Gemini 2.5 Flash): Analyzes the structured flow to generate clean, executable code output.

Stability: Utilizes @st.cache_resource to ensure heavy ML/API components load only once and run without caching errors.

🚀 Getting Started (Local Setup)
1. Prerequisites
You must have Python 3.9+ installed and a Gemini API Key.

2. File Structure
Your project directory must match this structure (crucial for deployment stability):CodeCanvas_App/
├── .streamlit/         # Contains secrets.toml (for local dev)
├── models/             # Contains best.pt (YOLO weights)
├── static/             # Contains background media (blackpurple.jpg, dark.mp4)
├── pages/
│   └── 1_Flowchart_Translator.py
├── requirements.txt    # Project dependencies
└── Home.py             # Video launch page (Entry Point)

3. Installation and Secrets
Install Dependencies:
pip install -r requirements.txt

Configure API Key: Place your API key securely in the following file (ensure this file is in your .gitignore):
.streamlit/secrets.toml
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

4. Run the Application
Run the application using the entry point:
streamlit run Home.py

☁️ Deployment
The application is configured for deployment on Streamlit Community Cloud via your repository: https://github.com/AAC-Open-Source-Pool/25AACL03.

Deployment File: The main file path must be set to Home.py.

Secrets Injection: The GEMINI_API_KEY must be pasted into the Secrets panel on the Streamlit Cloud dashboard before deployment.

🗃️ Repository Contents Overview
File	Description
Home.py	The Launch Page: Contains the fullscreen video embed logic and the final aesthetic injection.
pages/1_Flowchart_Translator.py	The Core App: Contains all backend utility functions, ML logic, caching fixes, and the final Glass Card aesthetic CSS.
models/best.pt	The trained YOLOv8 model weights.
requirements.txt	Lists all required Python dependencies.
