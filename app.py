import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Page Config
st.set_page_config(page_title="Kuantan Top 10", page_icon="🍴", layout="wide")

# 2. Premium Styling for the Streamlit Form
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem; background-color: #fcfaf8; }
        
        /* Form Styling to match your UI */
        .stForm {
            background-color: #ffffff;
            border: 1px solid #eee;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        div[data-testid="stForm"] h2 { font-family: 'Playfair Display', serif; color: #1a1a1a; }
        .stButton button {
            background-color: #1a1a1a;
            color: white;
            width: 100%;
            border-radius: 4px;
            font-weight: bold;
            letter-spacing: 0.1em;
        }
        .stButton button:hover { background-color: #b38b59; border-color: #b38b59; }
    </style>
""", unsafe_allow_html=True)

# 3. Google Sheets Connection
SHEET_URL = "https://docs.google.com/spreadsheets/d/1SMuUNaTpz-_hPP8DtZ8DTBoyRRkE_lFeRV40yeb3Kl4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Display the Top 10 Lists (HTML)
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=1050, scrolling=True)
except FileNotFoundError:
    st.error("Missing index.html file in repository.")

# 5. The SINGLE Integrated Submission Section
st.markdown("<div style='max-width: 1100px; margin: 0 auto; padding: 60px 20px;'>", unsafe_allow_html=True)
col1, col2 = st.columns([1.5, 1])

with col1:
    with st.form("submission_form", clear_on_submit=True):
        st.markdown("<h2 style='margin-bottom:0;'>Don't see your favorite?</h2>", unsafe_allow_html=True)
        st.write("Suggest a hidden gem for our next quarterly update.")
        
        res_name = st.text_input("Restaurant Full Name")
        res_reason = st.text_area("Why should it be in the Top 10?")
        cat = st.selectbox("Category", ["Ayam Gepuk", "Mamak", "Nasi Lemak", "Cafes"])
        
        submitted = st.form_submit_button("SUBMIT FOR REVIEW")
        
        if submitted and res_name:
            df = conn.read(spreadsheet=SHEET_URL)
            new_row = pd.DataFrame([{"Restaurant Name": res_name, "Reason": res_reason}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.balloons()
            st.success(f"Successfully added {res_name} to the queue!")

with col2:
    st.markdown("<h3 style='font-family:serif;'>🔥 Latest Suggestions</h3>", unsafe_allow_html=True)
    try:
        data = conn.read(spreadsheet=SHEET_URL).tail(5)
        for name in reversed(data["Restaurant Name"].tolist()):
            st.markdown(f"**{name}**")
            st.markdown("<hr style='margin:10px 0; opacity:0.1;'>", unsafe_allow_html=True)
    except:
        st.info("Start the trend by submitting the first spot!")

st.markdown("</div>", unsafe_allow_html=True)
