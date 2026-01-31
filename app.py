import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Config
st.set_page_config(page_title="Kuantan Top 10", page_icon="🍴", layout="wide")

# Hide Streamlit elements for a professional look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem; }
    </style>
""", unsafe_allow_html=True)

# 1. Connect to your Google Sheet
# Note: Ensure the sheet is shared with "Anyone with the link can edit"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1SMuUNaTpz-_hPP8DtZ8DTBoyRRkE_lFeRV40yeb3Kl4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Display your Premium HTML Content
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    # Height adjusted to show your lists; scrolling enabled
    components.html(html_code, height=1100, scrolling=True)
except FileNotFoundError:
    st.error("Please upload index.html to your GitHub repository.")

# 3. Integrated Submission Section (Python)
st.markdown("<div style='padding: 40px; background-color: #000; color: white;'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 📍 Submit Your Place")
    st.write("Is there a hidden gem missing? Add it to our community review queue.")
    
    with st.form("suggestion_form", clear_on_submit=True):
        res_name = st.text_input("Restaurant Full Name")
        res_reason = st.text_area("Why should it be in the Top 10?")
        category = st.selectbox("Category", ["Ayam Gepuk", "Mamak", "Nasi Lemak", "Cafes"])
        submit_btn = st.form_submit_button("SUBMIT FOR REVIEW")

        if submit_btn and res_name:
            # Read current data
            df = conn.read(spreadsheet=SHEET_URL)
            # Add new entry
            new_row = pd.DataFrame([{"Restaurant Name": res_name, "Reason": res_reason}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            # Update Google Sheet
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.success(f"Successfully submitted {res_name} to the database!")

with col2:
    st.markdown("### 🔥 Latest Suggestions")
    # Display the most recent 5 entries from your Google Sheet
    try:
        current_data = conn.read(spreadsheet=SHEET_URL).tail(5)
        for name in current_data["Restaurant Name"]:
            st.markdown(f"✅ {name}")
    except:
        st.write("Waiting for first suggestion...")

st.markdown("</div>", unsafe_allow_html=True)

