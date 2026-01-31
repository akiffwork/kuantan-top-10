import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Kuantan Top 10", page_icon="🍴", layout="wide")

# 2. Integration Styling (Matching your HTML aesthetic)
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem; background-color: #fcfaf8; }
        
        /* Unified Form Styling */
        [data-testid="stForm"] {
            background-color: #f4f1ee;
            border: 1px solid #e5e5e5;
            border-radius: 15px;
            padding: 3rem;
            max-width: 1000px;
            margin: 0 auto 50px auto;
        }
        h2, h3 { font-family: 'Playfair Display', serif; color: #1a1a1a; }
        .stButton button {
            background-color: #1a1a1a;
            color: white;
            width: 100%;
            border-radius: 0px;
            padding: 15px;
            font-weight: bold;
            letter-spacing: 0.1em;
            border: none;
        }
        .stButton button:hover { background-color: #b38b59; }
    </style>
""", unsafe_allow_html=True)

# 3. Secure Google Sheets Connection
# Ensure your Sheet is shared with "Anyone with link can edit"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1SMuUNaTpz-_hPP8DtZ8DTBoyRRkE_lFeRV40yeb3Kl4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Render the Premium Lists (HTML)
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=1000, scrolling=True)
except FileNotFoundError:
    st.error("Make sure index.html is in the same folder as app.py")

# 5. THE SINGLE INTEGRATED SUBMISSION SECTION
st.markdown("<div style='padding: 0 20px;'>", unsafe_allow_html=True)
with st.form("suggestion_form", clear_on_submit=True):
    st.markdown("<span style='color:#b38b59; font-weight:bold; font-size:10px; text-transform:uppercase; letter-spacing:2px;'>Community Driven</span>", unsafe_allow_html=True)
    st.markdown("<h2>Don't see your favorite?</h2>", unsafe_allow_html=True)
    st.write("Suggest a hidden gem for our next quarterly update.")
    
    col1, col2 = st.columns(2)
    with col1:
        res_name = st.text_input("Restaurant Name")
    with col2:
        cat = st.selectbox("Category", ["Ayam Gepuk", "Mamak", "Nasi Lemak", "Cafes"])
    
    reason = st.text_area("Why should it be in the Top 10?")
    
    if st.form_submit_button("SUBMIT FOR REVIEW"):
        if res_name:
            # INTEGRATION LOGIC
            df = conn.read(spreadsheet=SHEET_URL)
            new_row = pd.DataFrame([{"Restaurant Name": res_name, "Reason": reason}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            
            st.balloons()
            st.success(f"Verified! {res_name} has been added to our review queue.")
        else:
            st.warning("Please enter a restaurant name.")

# 6. Community Trending (Live from Google Sheets)
st.markdown("<div style='max-width:1000px; margin: 0 auto; padding-bottom:100px;'>", unsafe_allow_html=True)
st.markdown("<h3><i class='fa-solid fa-fire-flame-curved'></i> Community Trending</h3>", unsafe_allow_html=True)
try:
    latest_data = conn.read(spreadsheet=SHEET_URL).tail(3)
    for name in reversed(latest_data["Restaurant Name"].tolist()):
        st.markdown(f"""
            <div style='background:white; padding:15px; border:1px solid #eee; margin-bottom:10px; border-radius:8px; display:flex; justify-content:space-between;'>
                <span style='font-weight:600;'>{name}</span>
                <span style='color:#b38b59; font-size:12px;'>RECENTLY SUGGESTED</span>
            </div>
        """, unsafe_allow_html=True)
except:
    st.write("Suggestions are being processed...")
st.markdown("</div></div>", unsafe_allow_html=True)
