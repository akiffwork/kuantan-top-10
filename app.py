import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Kuantan Top 10", page_icon="🍴", layout="wide")

# 2. High-Contrast Integrated Styling
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem; background-color: #fcfaf8; }
        
        /* Unified Form Styling with DEEP SHADES for readability */
        [data-testid="stForm"] {
            background-color: #f4f1ee;
            border: 2px solid #d1cec8;
            border-radius: 15px;
            padding: 3rem;
            max-width: 1000px;
            margin: 20px auto 50px auto;
        }
        
        /* Making the labels and text deep black/charcoal */
        label, p, span, h2, h3 { 
            color: #1a1a1a !important; 
            font-weight: 700 !important;
        }
        
        .stTextInput input, .stTextArea textarea, .stSelectbox div {
            border: 1px solid #1a1a1a !important;
            color: #1a1a1a !important;
        }

        .stButton button {
            background-color: #1a1a1a;
            color: white !important;
            width: 100%;
            border-radius: 0px;
            padding: 15px;
            font-weight: 900;
            letter-spacing: 0.1em;
            border: none;
            margin-top: 10px;
        }
        .stButton button:hover { background-color: #b38b59; }
    </style>
""", unsafe_allow_html=True)

# 3. Secure Google Sheets Connection
SHEET_URL = "https://docs.google.com/spreadsheets/d/1SMuUNaTpz-_hPP8DtZ8DTBoyRRkE_lFeRV40yeb3Kl4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Render the Premium Lists (HTML)
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=1000, scrolling=True)
except FileNotFoundError:
    st.error("Ensure index.html is in your GitHub folder.")

# 5. THE SINGLE INTEGRATED SUBMISSION SECTION (Deep Contrast)
st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
with st.form("suggestion_form", clear_on_submit=True):
    st.markdown("<span style='color:#b38b59; font-weight:900; font-size:12px; text-transform:uppercase; letter-spacing:2px;'>COMMUNITY DRIVEN</span>", unsafe_allow_html=True)
    st.markdown("<h2 style='font-size: 32px; margin-bottom: 5px;'>Don't see your favorite?</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; margin-bottom: 25px;'>Suggest a hidden gem for our next quarterly update.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("RESTAURANT NAME (REQUIRED)")
    with col2:
        cat = st.selectbox("CATEGORY", ["Ayam Gepuk", "Mamak", "Nasi Lemak", "Cafes"])
    
    reason = st.text_area("WHY SHOULD IT BE IN THE TOP 10?")
    
    if st.form_submit_button("SUBMIT FOR REVIEW"):
        if res_name:
            # Load and Update Sheet
            df = conn.read(spreadsheet=SHEET_URL)
            new_row = pd.DataFrame([{"Restaurant Name": res_name, "Reason": reason}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            
            st.balloons()
            st.success(f"SUBMITTED: {res_name} is now in our queue!")
        else:
            st.error("PLEASE ENTER THE RESTAURANT NAME TO SUBMIT.")

# 6. Community Trending Section
st.markdown("<div style='max-width:1000px; margin: 40px auto 100px auto;'>", unsafe_allow_html=True)
st.markdown("<h3 style='border-bottom: 2px solid #1a1a1a; padding-bottom: 10px;'>🔥 LATEST SUGGESTIONS</h3>", unsafe_allow_html=True)
try:
    latest_data = conn.read(spreadsheet=SHEET_URL).tail(3)
    for name in reversed(latest_data["Restaurant Name"].tolist()):
        st.markdown(f"""
            <div style='background:white; padding:20px; border:2px solid #1a1a1a; margin-top:10px; display:flex; justify-content:space-between;'>
                <span style='font-weight:900; color:#1a1a1a;'>{name.upper()}</span>
                <span style='color:#b38b59; font-weight:900; font-size:11px;'>VERIFIED SUBMISSION</span>
            </div>
        """, unsafe_allow_html=True)
except:
    st.write("Waiting for community input...")
st.markdown("</div></div>", unsafe_allow_html=True)
