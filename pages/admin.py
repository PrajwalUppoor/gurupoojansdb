import streamlit as st
import pandas as pd
from utils import load_data, submit_entry

st.set_page_config(page_title="Admin – Guru Pooja", layout="wide")
st.title("🔐 Admin Panel – Guru Pooja Utsava")

# --- Login ---
PASSWORD = st.secrets["admin"]["password"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pw = st.text_input("Enter Admin Password", type="password")
    if pw == PASSWORD:
        st.session_state.logged_in = True
        st.success("✅ Logged in successfully")
    else:
        st.warning("Incorrect password.")
        st.stop()

# --- Load Data ---
rows = load_data()
if not rows:
    st.warning("No data found in the Excel sheet.")
    st.stop()

# --- Display Table ---
st.subheader("📝 Submissions")
df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True)

# --- CSV Download Button ---
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download as CSV",
    data=csv,
    file_name="ssdata.csv",
    mime="text/csv"
)

# --- Upload to API Button ---
if st.button("📤 Upload All to API"):
    success, failed = 0, 0
    for row in rows:
        ok, msg = submit_entry(row)
        if ok:
            success += 1
        else:
            failed += 1
    st.success(f"✅ Upload complete. Success: {success}, Failed: {failed}")
