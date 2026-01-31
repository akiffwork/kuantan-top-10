import streamlit as st
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(
    page_title="Kuantan Top 10 | 2026 Guide", 
    page_icon="🍴", 
    layout="wide"
)

# 2. High-Contrast Styling (Clean & Minimal)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Set background to match your HTML exactly */
        .stApp {
            background-color: #fcfaf8;
        }

        /* Ensure all text is Deep Black for readability */
        h1, h2, h3, p, span {
            color: #000000 !important;
            font-weight: 800 !important;
        }

        /* Remove extra padding at the top */
        .block-container {
            padding: 0rem;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Render the HTML List
# This will now be the only thing on the page
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    
    # We use a large height so the whole list is visible without a double scrollbar
    components.html(html_code, height=1500, scrolling=True)

except FileNotFoundError:
    st.error("⚠️ Error: 'index.html' not found. Please ensure it is in your GitHub folder.")

# 4. Optional: Simple Footer (Pure Text)
st.markdown("<br><p style='text-align: center; font-size: 12px; opacity: 0.6;'>© 2026 Kuantan Dining Guide</p>", unsafe_allow_html=True)
