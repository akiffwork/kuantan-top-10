import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection  # This stays the same
import pandas as pd

# 1. Page Configuration
st.set_page_config(
    page_title="Kuantan Top 10",
    page_icon="🍴",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS to hide Streamlit UI for a cleaner "Website" look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container { padding: 0rem; }
        iframe { border: none; }
    </style>
""", unsafe_allow_html=True)

# 3. Connect to Google Sheets
# Ensure your Sheet URL is in Streamlit Secrets or used here
SHEET_URL = "https://docs.google.com/spreadsheets/d/1SMuUNaTpz-_hPP8DtZ8DTBoyRRkE_lFeRV40yeb3Kl4/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. Load the Premium HTML Frontend
try:
    with open("index.html", "r", encoding="utf-8") as f:
        html_code = f.read()
    components.html(html_code, height=1350, scrolling=True)
except FileNotFoundError:
    st.error("HTML file not found. Please ensure index.html is in the same folder.")

# 5. Community Submission Section (Python/Streamlit)
st.markdown("<div style='padding: 40px; background-color: #fcfaf8;'>", unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    st.title("📍 Submit Your Place")
    st.write("Is there a hidden gem missing? Add it to our community review queue.")
    
    with st.form("suggestion_form", clear_on_submit=True):
        res_name = st.text_input("Restaurant Full Name")
        category = st.selectbox("Category", ["Ayam Gepuk", "Mamak", "Nasi Lemak", "Cafes"])
        submit_btn = st.form_submit_button("SUBMIT FOR REVIEW")

        if submit_btn and res_name:
            try:
                # Read existing data
                df = conn.read(spreadsheet=SHEET_URL)
                # Create new row
                new_data = pd.DataFrame([{"Restaurant Name": res_name}])
                # Combine and Update
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(spreadsheet=SHEET_URL, data=updated_df)
                st.success(f"Successfully submitted {res_name}!")
            except Exception as e:
                st.error(f"Error: {e}. Make sure the Google Sheet is set to 'Anyone with the link can edit'.")

with col2:
    st.subheader("🔥 Latest Suggestions")
    try:
        # Show the last 5 names submitted to the sheet
        display_df = conn.read(spreadsheet=SHEET_URL).tail(5)
        for name in display_df["Restaurant Name"]:
            st.markdown(f"✅ **{name}**")
    except:
        st.write("No suggestions yet. Be the first!")


st.markdown("</div>", unsafe_allow_html=True)
