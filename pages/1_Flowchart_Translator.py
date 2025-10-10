# pages/1_Flowchart_Translator.py
import streamlit as st
import numpy as np
import cv2
from google import genai
from ultralytics import YOLO
import easyocr
from PIL import Image as PILImage
import json
import math
import os
import time
import base64

st.set_page_config(
    page_title="CodeCanvas: Flowchart Translator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Base64 Encoding Function (Guarantees Static Background Loads) ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception as e:
        return ""

# Get the Base64 String for background
BG_BASE64 = get_base64_image("static/blackpurple.jpg")

# --- ULTRA COOL APPLE-INSPIRED STYLE (Glassmorphism) ---
st.markdown(f"""
<style>
/* Global Reset */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

/* Background with your image */
.stApp {{
    background-image: url("data:image/jpg;base64,{BG_BASE64}");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
    color: #F5F5F7;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif;
}}

/* Dark overlay for readability */
.stApp::before {{
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5);
    z-index: 0;
    pointer-events: none;
}}

/* Hide Streamlit Branding */
#MainMenu, footer, header {{
    visibility: hidden;
    height: 0;
}}

[data-testid="stToolbar"] {{
    display: none;
}}

/* Main Container */
.main .block-container {{
    padding: 40px 60px;
    max-width: 1600px;
    position: relative;
    z-index: 1;
}}

/* HERO SECTION - Enhanced with gradient text */
.hero-section {{
    text-align: center;
    padding: 80px 0 100px 0;
    position: relative;
    z-index: 1;
}}

.hero-title {{
    font-size: 5.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -3px;
    margin-bottom: 24px;
    line-height: 1;
    text-shadow: none;
    animation: titleGlow 3s ease-in-out infinite;
}}

@keyframes titleGlow {{
    0%, 100% {{ filter: drop-shadow(0 4px 20px rgba(167, 139, 250, 0.3)); }}
    50% {{ filter: drop-shadow(0 4px 40px rgba(167, 139, 250, 0.6)); }}
}}

.hero-subtitle {{
    font-size: 1.8rem;
    color: rgba(255, 255, 255, 0.85);
    font-weight: 400;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
}}

/* Ultra Glass Cards - Enhanced */
.glass-card {{
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(80px) saturate(200%);
    -webkit-backdrop-filter: blur(80px) saturate(200%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 32px;
    padding: 48px;
    margin-bottom: 30px;
    transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    z-index: 1;
    box-shadow: 0 20px 80px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.1);
}}

.glass-card:hover {{
    border-color: rgba(167, 139, 250, 0.3);
    background: rgba(255, 255, 255, 0.08);
    transform: translateY(-10px) scale(1.005);
    box-shadow: 0 30px 100px rgba(167, 139, 250, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.15);
}}

/* Section Headers Inside Cards */
.section-label {{
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: rgba(167, 139, 250, 0.9);
    font-weight: 700;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid rgba(167, 139, 250, 0.2);
}}

/* Prominent Input Labels */
.input-header {{
    font-size: 1.8rem; 
    font-weight: 700; 
    background: linear-gradient(135deg, #FFFFFF 0%, #E9D5FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 0.5px;
    margin-bottom: 20px;
    margin-top: 0;
}}

/* Remove default Streamlit labels */
label {{
    display: none !important;
}}

/* Radio Buttons - Enhanced Pills */
div[data-testid="stRadio"] {{
    display: flex;
    gap: 16px;
    justify-content: flex-start;
    margin-top: 12px;
}}

div[data-testid="stRadio"] > div {{
    display: flex;
    gap: 16px;
    width: 100%;
}}

div[data-testid="stRadio"] > div > label {{
    display: flex !important;
    background: rgba(167, 139, 250, 0.08) !important;
    backdrop-filter: blur(40px);
    color: #FFFFFF !important;
    font-size: 1.05rem;
    font-weight: 500;
    border: 2px solid rgba(167, 139, 250, 0.2) !important;
    border-radius: 999px;
    padding: 20px 40px !important;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    flex: 1;
    justify-content: center;
    align-items: center;
    position: relative;
    overflow: hidden;
}}

div[data-testid="stRadio"] > div > label:hover {{
    background: rgba(167, 139, 250, 0.15) !important;
    border-color: rgba(167, 139, 250, 0.5) !important;
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 16px 48px rgba(167, 139, 250, 0.3);
}}

/* Hide radio circles */
div[data-testid="stRadio"] input[type="radio"] {{
    display: none;
}}

/* Selectbox - Premium Style */
.stSelectbox > div {{
    margin-top: 12px;
}}

.stSelectbox div[data-baseweb="select"] {{
    background: rgba(167, 139, 250, 0.1);
    backdrop-filter: blur(40px);
    border: 2px solid rgba(167, 139, 250, 0.25);
    border-radius: 24px;
    color: #FFFFFF;
    font-size: 1.2rem;
    font-weight: 500;
    transition: all 0.4s ease;
    padding: 12px 20px;
}}

.stSelectbox div[data-baseweb="select"]:hover {{
    border-color: rgba(167, 139, 250, 0.5);
    background: rgba(167, 139, 250, 0.15);
    box-shadow: 0 8px 32px rgba(167, 139, 250, 0.3);
    transform: translateY(-2px);
}}

.stSelectbox div[data-baseweb="select"] > div {{
    color: #FFFFFF;
}}

/* File Uploader - Epic Enhanced Style */
[data-testid="stFileUploader"] {{
    background: rgba(167, 139, 250, 0.06);
    backdrop-filter: blur(40px);
    border: 3px dashed rgba(167, 139, 250, 0.3);
    border-radius: 28px;
    padding: 60px;
    transition: all 0.5s ease;
    margin-top: 12px;
    text-align: center;
    position: relative;
}}

[data-testid="stFileUploader"]::before {{
    content: '📤';
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 2rem;
    opacity: 0.3;
}}

[data-testid="stFileUploader"]:hover {{
    border-color: rgba(167, 139, 250, 0.6);
    background: rgba(167, 139, 250, 0.12);
    transform: scale(1.01);
    box-shadow: 0 12px 48px rgba(167, 139, 250, 0.3);
}}

[data-testid="stFileUploader"] section {{
    border: none !important;
    background: transparent !important;
}}

[data-testid="stFileUploader"] button {{
    background: rgba(167, 139, 250, 0.15);
    border: 2px solid rgba(167, 139, 250, 0.3);
    border-radius: 999px;
    color: #FFFFFF;
    padding: 14px 32px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
}}

[data-testid="stFileUploader"] button:hover {{
    background: rgba(167, 139, 250, 0.25);
    border-color: rgba(167, 139, 250, 0.5);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(167, 139, 250, 0.4);
}}

/* Download Button - Premium */
.stDownloadButton button {{
    background: linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
    backdrop-filter: blur(40px);
    color: #FFFFFF;
    font-weight: 700;
    font-size: 1rem;
    border: 2px solid rgba(167, 139, 250, 0.4);
    border-radius: 999px;
    padding: 20px 44px;
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 1px;
    width: 100%;
    text-transform: uppercase;
    position: relative;
    overflow: hidden;
}}

.stDownloadButton button:hover {{
    background: linear-gradient(135deg, rgba(167, 139, 250, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
    border-color: rgba(167, 139, 250, 0.6);
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 20px 60px rgba(167, 139, 250, 0.5);
}}

/* Spinner */
.stSpinner > div {{
    border-color: rgba(167, 139, 250, 0.3) transparent transparent transparent !important;
}}

/* Code Block - Dark & Elegant */
.stCodeBlock {{
    background: rgba(0, 0, 0, 0.8) !important;
    border: 1px solid rgba(167, 139, 250, 0.2);
    border-radius: 24px;
    backdrop-filter: blur(30px);
    margin-top: 20px;
    box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.5), 0 4px 20px rgba(167, 139, 250, 0.1);
}}

/* Images - Enhanced */
.stImage {{
    border-radius: 24px;
    overflow: hidden;
    border: 2px solid rgba(167, 139, 250, 0.2);
    box-shadow: 0 20px 70px rgba(0, 0, 0, 0.6);
    transition: all 0.5s ease;
}}

.stImage:hover {{
    transform: scale(1.02);
    box-shadow: 0 30px 90px rgba(167, 139, 250, 0.4);
    border-color: rgba(167, 139, 250, 0.4);
}}

/* Success/Info Messages - Enhanced */
.stSuccess {{
    background: rgba(52, 199, 89, 0.15);
    border-left: 5px solid #34C759;
    backdrop-filter: blur(40px);
    border-radius: 20px;
    color: #FFFFFF;
    border: 1px solid rgba(52, 199, 89, 0.4);
    padding: 16px 20px;
    font-weight: 500;
}}

.stInfo {{
    background: rgba(96, 165, 250, 0.15);
    border-left: 5px solid #60A5FA;
    backdrop-filter: blur(40px);
    border-radius: 20px;
    color: #FFFFFF;
    border: 1px solid rgba(96, 165, 250, 0.4);
    padding: 16px 20px;
    font-weight: 500;
}}

.stError {{
    background: rgba(255, 59, 48, 0.15);
    border-left: 5px solid #FF3B30;
    backdrop-filter: blur(40px);
    border-radius: 20px;
    color: #FFFFFF;
    border: 1px solid rgba(255, 59, 48, 0.4);
    padding: 16px 20px;
    font-weight: 500;
}}

/* Columns */
[data-testid="column"] {{
    padding: 0 15px;
}}

/* Animations */
@keyframes fadeInUp {{
    from {{
        opacity: 0;
        transform: translateY(40px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

@keyframes glow {{
    0%, 100% {{
        box-shadow: 0 20px 80px rgba(0, 0, 0, 0.3);
    }}
    50% {{
        box-shadow: 0 20px 80px rgba(255, 255, 255, 0.1);
    }}
}}

.glass-card {{
    animation: fadeInUp 0.8s ease-out;
}}

/* Headings */
h2, h3 {{
    color: #FFFFFF;
    font-weight: 600;
    letter-spacing: -1px;
}}

/* Responsive */
@media (max-width: 768px) {{
    .hero-title {{
        font-size: 3rem;
    }}
    .hero-subtitle {{
        font-size: 1.2rem;
    }}
    .main .block-container {{
        padding: 30px 20px;
    }}
    .glass-card {{
        padding: 32px;
    }}
}}

/* Scrollbar */
::-webkit-scrollbar {{
    width: 12px;
}}

::-webkit-scrollbar-track {{
    background: rgba(0, 0, 0, 0.3);
}}

::-webkit-scrollbar-thumb {{
    background: rgba(255, 255, 255, 0.2);
    border-radius: 6px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: rgba(255, 255, 255, 0.3);
}}
</style>
""", unsafe_allow_html=True)


# --- INITIALIZATION & CACHING ---
@st.cache_resource
def load_models_and_client():
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key: raise ValueError("GEMINI_API_KEY not found in secrets.")
        client = genai.Client(api_key=api_key)
        yolo_model = YOLO('models/best.pt')
        reader = easyocr.Reader(['en'])
        return client, yolo_model, reader
    except Exception as e:
        st.error(f"Failed to load resources: {e}")
        return None, None, None

client, yolo_model, reader = load_models_and_client()
if not all([client, yolo_model, reader]): st.stop()


# --- UTILITY FUNCTIONS ---
def get_center_point(box): 
    return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)

def distance(point1, point2): 
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# ===== NEW: Validate if image contains a flowchart =====
def validate_flowchart(yolo_results, _yolo_model):
    """Check if the image contains flowchart elements"""
    class_names = _yolo_model.names
    flowchart_classes = ['process', 'decision', 'start_end', 'arrow', 'scan']
    
    detected_shapes = []
    for r in yolo_results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            shape_type = class_names[class_id]
            confidence = float(box.conf[0])
            
            if shape_type in flowchart_classes:
                detected_shapes.append((shape_type, confidence))
    
    if len(detected_shapes) == 0:
        return False, 0.0, "❌ No flowchart elements detected! Please capture an image of a flowchart."
    elif len(detected_shapes) < 2:
        return False, detected_shapes[0][1], "⚠️ Only one flowchart element detected. Please ensure the entire flowchart is visible."
    else:
        avg_confidence = sum(conf for _, conf in detected_shapes) / len(detected_shapes)
        return True, avg_confidence, f"✅ Valid flowchart detected with {len(detected_shapes)} elements!"

def analyze_flowchart(yolo_results, reader, img_np, _yolo_model):
    shapes_data = []
    arrows_data = []
    class_names = _yolo_model.names

    for r in yolo_results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            shape_type = class_names[class_id]
            x1, y1, x2, y2 = box.xyxy[0].int().tolist()
            bbox = (x1, y1, x2, y2)

            if 'arrow' in shape_type:
                arrows_data.append({'type': shape_type, 'bbox': bbox})
            else:
                roi = img_np[y1:y2, x1:x2]
                try:
                    text_result = reader.readtext(roi, detail=0, paragraph=True)
                    extracted_text = " ".join(text_result).strip()
                except Exception:
                    extracted_text = "OCR_ERROR"

                shapes_data.append({
                    'id': len(shapes_data),
                    'type': shape_type,
                    'bbox': bbox,
                    'text': extracted_text
                })

    for arrow in arrows_data:
        arrow_center = get_center_point(arrow['bbox'])
        shapes_sorted_by_distance = sorted(shapes_data, key=lambda s: distance(get_center_point(s['bbox']), arrow_center))

        if len(shapes_sorted_by_distance) >= 2:
            shape1 = shapes_sorted_by_distance[0]
            shape2 = shapes_sorted_by_distance[1]
            
            if get_center_point(shape1['bbox'])[1] < get_center_point(shape2['bbox'])[1]:
                source_id = shape1['id']
                target_id = shape2['id']
            else:
                source_id = shape2['id']
                target_id = shape1['id']

            arrow['source'] = source_id
            arrow['target'] = target_id

    return {
        "shapes": shapes_data,
        "arrows": arrows_data
    }

def create_dynamic_prompt_flow(graph, target_language):
    shapes = {s['id']: s for s in graph['shapes']}
    flow_instructions = ["START PROGRAM"]
    
    for shape_id in sorted(shapes.keys()):
        node = shapes[shape_id]
        current_text = node['text'].strip()
        current_type = node['type']
        
        if current_text.lower() == 'start': continue
        if current_text.lower() == 'end' or current_text.lower() == 'stop':
            flow_instructions.append("END PROGRAM")
            break
            
        if current_type == 'process' or current_type == 'scan':
            flow_instructions.append(f"ACTION: {current_text}")
        elif current_type == 'decision':
            flow_instructions.append(f"DECISION: IF ({current_text}):")
            flow_instructions.append(f"  // The LLM must determine TRUE/FALSE branching based on the image.")
        elif current_type == 'start_end':
            flow_instructions.append(f"DISPLAY output: '{current_text}'")
            
    prompt_text = f"""
    You are an expert software engineer. Your task is to analyze the flowchart structure and logic commands below.
    
    **Goal:** Write a complete, standalone {target_language} program that strictly follows the procedural logic. 
    The output must contain ONLY the executable code block, nothing else (no explanations, no extra text).

    Flowchart Logic:
    {chr(10).join(flow_instructions)}

    Output ONLY the {target_language} code:
    """
    return prompt_text

@st.cache_data(show_spinner=False)
def run_codecanvas_pipeline(image_np, target_language, _client, _yolo_model, _reader):
    time.sleep(2) 
    
    # 1. Run YOLO object detection
    yolo_results = _yolo_model.predict(source=image_np, save=False, conf=0.5, verbose=False)

    # 2. ===== NEW: Validate flowchart =====
    is_valid, confidence, validation_msg = validate_flowchart(yolo_results, _yolo_model)
    
    if not is_valid:
        return None, None, validation_msg

    # 3. Analyze the flowchart structure
    flowchart_graph = analyze_flowchart(yolo_results, _reader, image_np, _yolo_model)

    # 4. Prepare the final prompt for Gemini
    final_prompt_text = create_dynamic_prompt_flow(flowchart_graph, target_language)

    # 5. Prepare image for Gemini (convert OpenCV BGR/RGB to PIL)
    original_image_pil = PILImage.fromarray(cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB))
    
    # 6. Call Gemini API (using _client)
    response = _client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[final_prompt_text, original_image_pil]
    )

    # 7. Generate the annotated image for display
    annotated_image_np = yolo_results[0].plot()
    
    generated_code = response.text.strip()
    
    return generated_code, annotated_image_np, validation_msg


# --- HERO SECTION ---
st.markdown("""
<div class="hero-section">
    <div class="hero-title">Flowchart Translator</div>
    <div class="hero-subtitle">Transform your flowcharts into production-ready code</div>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
col_lang, col_input = st.columns([1, 2], gap="large")

with col_lang:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="input-header">Target Language</div>', unsafe_allow_html=True)
        target_language = st.selectbox(
            "lang",
            ("Python", "Java", "C++", "C"),
            index=0,
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

with col_input:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<div class="input-header">Input Source</div>', unsafe_allow_html=True)
        
        input_method = st.radio(
            "input",
            ("🖼️ Upload Image", "📸 Live Camera"),
            horizontal=True,
            label_visibility="collapsed"
        )
        
        uploaded_file = None
        camera_image = None
        
        # ===== NEW: Camera input added =====
        if input_method == "🖼️ Upload Image":
            uploaded_file = st.file_uploader(
                "upload", 
                type=['png', 'jpg', 'jpeg'],
                label_visibility="collapsed"
            )
        elif input_method == "📸 Live Camera":
            camera_image = st.camera_input(
                "capture",
                label_visibility="collapsed"
            )
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- RESULTS SECTION (MODIFIED TO HANDLE BOTH SOURCES) ---
image_np = None

# ===== NEW: Process both uploaded file and camera image =====
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
elif camera_image is not None:
    file_bytes = np.asarray(bytearray(camera_image.read()), dtype=np.uint8)
    image_np = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

# ===== MODIFIED: Updated to handle validation =====
if image_np is not None:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.spinner('🔍 Analyzing flowchart with AI...'):
        try:
            result = run_codecanvas_pipeline(
                image_np, target_language, client, yolo_model, reader
            )
            
            generated_code, annotated_image_np, validation_msg = result
            
            # Check if validation failed
            if generated_code is None:
                st.error(validation_msg)
                st.info("💡 **Tips for better results:**\n\n"
                       "• Ensure the entire flowchart is visible\n\n"
                       "• Use good lighting without shadows\n\n"
                       "• Make sure flowchart shapes are clear\n\n"
                       "• Avoid glare or reflections")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.success(validation_msg)
                st.markdown('</div>', unsafe_allow_html=True)
                
                viz_col, code_col = st.columns([1, 1.5], gap="large")

                with viz_col:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown('<div class="section-label">Visual Analysis (CV Output)</div>', unsafe_allow_html=True)
                    st.image(
                        cv2.cvtColor(annotated_image_np, cv2.COLOR_BGR2RGB), 
                        use_container_width=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

                with code_col:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown(f'<div class="section-label">Generated {target_language} Code</div>', unsafe_allow_html=True)
                    st.code(generated_code, language=target_language.lower(), line_numbers=True)
                    st.download_button(
                        label=f"⬇️ Download Code",
                        data=generated_code.encode("utf-8"),
                        file_name=f"codecanvas_output.{'py' if target_language == 'Python' else target_language.lower()}",
                        mime="text/plain"
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
        except Exception as e:
            st.error(f"❌ Error during pipeline: {e}")
            st.markdown('</div>', unsafe_allow_html=True)