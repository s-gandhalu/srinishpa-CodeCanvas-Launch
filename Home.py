# Home.py

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CodeCanvas: Launch",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Define the Video Background URL ---
VIDEO_URL = "https://res.cloudinary.com/ddxi6jnjj/video/upload/v1760111509/dark_eb0hh2.mp4" 

# CRITICAL: Remove ALL Streamlit elements and scrolling
st.markdown("""
    <style>
    /* Nuke everything */
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    header {display: none !important;}
    
    /* Kill ALL padding */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    section.main > div {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* KILL SCROLLING COMPLETELY */
    html {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    body {
        overflow: hidden !important;
        height: 100vh !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    [data-testid="stAppViewContainer"], 
    .main,
    section {
        overflow: hidden !important;
        height: 100vh !important;
    }
    
    /* Hide scrollbars */
    ::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
    }
    
    * {
        scrollbar-width: none !important;
        -ms-overflow-style: none !important;
    }
    
    /* Make iframe take full screen */
    iframe {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        border: none !important;
    }
    
    /* Hide ALL buttons */
    button {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Create the full page HTML component - APPLE STYLE
html_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        html, body {{
            overflow: hidden !important;
            height: 100vh;
            width: 100vw;
            position: fixed;
        }}
        
        .container {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #000;
            overflow: hidden;
        }}
        
        .video-background {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
        }}
        
        .video-background video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            filter: brightness(0.45) contrast(1.1);
        }}
        
        /* Subtle gradient overlay for depth */
        .video-background::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.3) 100%);
        }}
        
        .content {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            z-index: 10;
            color: white;
            max-width: 90%;
        }}
        
        .title {{
            font-size: 4.5rem;
            font-weight: 600;
            color: #FFFFFF;
            letter-spacing: -0.5px;
            margin-bottom: 16px;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif;
            line-height: 1.1;
        }}
        
        .subtitle {{
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.7);
            font-weight: 400;
            letter-spacing: 0.2px;
            margin-bottom: 48px;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
            line-height: 1.5;
        }}
        
        .button {{
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            color: #FFFFFF;
            font-size: 1.05rem;
            font-weight: 500;
            border: 1.5px solid rgba(255, 255, 255, 0.2);
            border-radius: 980px;
            padding: 16px 40px;
            cursor: pointer;
            letter-spacing: 0.3px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        }}
        
        .button:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        }}
        
        .button:active {{
            transform: translateY(-1px);
            transition: all 0.1s;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .title {{
                font-size: 2.5rem;
            }}
            .subtitle {{
                font-size: 1rem;
                margin-bottom: 36px;
            }}
            .button {{
                font-size: 0.95rem;
                padding: 14px 32px;
            }}
        }}
        
        /* Smooth fade-in animation */
        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .content > * {{
            animation: fadeIn 0.8s ease-out forwards;
        }}
        
        .title {{
            animation-delay: 0.2s;
            opacity: 0;
        }}
        
        .subtitle {{
            animation-delay: 0.4s;
            opacity: 0;
        }}
        
        .button {{
            animation-delay: 0.6s;
            opacity: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="video-background">
            <video autoplay loop muted playsinline>
                <source src="{VIDEO_URL}" type="video/mp4">
            </video>
        </div>
        
        <div class="content">
            <div class="title">CodeCanvas</div>
            <div class="subtitle">Turning visual logic into executable code, instantly.</div>
            <button class="button" onclick="window.location.href='?page=flowchart'">
                <span>Get Started</span>
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 3L11 8L6 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
        </div>
    </div>
</body>
</html>
"""

# Render fullscreen
components.html(html_code, height=None, scrolling=False)

# Check URL params and navigate ONLY when button is clicked
query_params = st.query_params
if "page" in query_params and query_params["page"] == "flowchart":
    st.switch_page("pages/1_Flowchart_Translator.py")