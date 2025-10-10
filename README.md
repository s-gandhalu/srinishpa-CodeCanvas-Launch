# 💡 CodeCanvas: Flowchart-to-Code Translator

CodeCanvas is an innovative, production-ready web application that transforms conceptual logic (flowcharts, pseudocode) into executable source code using a combination of computer vision and generative AI.

The application features an advanced, interactive frontend aesthetic that provides a seamless user experience.

## ✨ Core Features

* **Premium Aesthetic:** Features a high-contrast, interactive interface with a **full-screen video background** on the launch page and a **Glassmorphism-styled dashboard** for the translator.
* **Seamless Multipage Navigation:** Uses the most stable methods for navigation and CSS injection to ensure a perfectly centered, non-scrolling launch experience.
* **Multilingual Generation:** Converts visual logic into **Python, Java, C++, or C** by dynamically adapting the prompt for the Gemini LLM.
* **Intelligent Backend Pipeline:**
    1.  **Computer Vision (YOLOv8 & EasyOCR):** Detects shapes, arrows, and extracts handwritten text.
    2.  **Generative AI (Gemini 2.5 Flash):** Analyzes the structured flow to generate clean, executable code output.
* **Stability:** Utilizes `@st.cache_resource` to ensure heavy ML/API components load only once and run without caching errors.

## 🧑‍💻 Contribution

Feel free to open issues or submit pull requests!
