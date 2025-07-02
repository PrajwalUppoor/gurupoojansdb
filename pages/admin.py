import streamlit as st
import pandas as pd
from utils import load_data, submit_entry, delete_row

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

# --- Refresh & Load Data ---
def refresh_table():
    st.session_state.rows = load_data()
    st.session_state.df = pd.DataFrame(st.session_state.rows)

if "rows" not in st.session_state:
    refresh_table()

# --- Display Submissions with Delete Option ---
st.subheader("📝 Submissions")

for i, row in enumerate(st.session_state.rows):
    with st.expander(f"{i+1}. {row['name']} ({row['phone']})"):
        st.write(row)
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Delete", key=f"del_{i}"):
                delete_row(i)
                st.success(f"✅ Deleted row {i+1}")
                refresh_table()
                st.experimental_rerun()

# --- Download CSV ---
df = pd.DataFrame(st.session_state.rows)
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download as CSV",
    data=csv,
    file_name="ssdata.csv",
    mime="text/csv"
)

# --- Upload to API ---
if st.button("📤 Upload All to API"):
    success, failed = 0, 0
    for row in st.session_state.rows:
        ok, msg = submit_entry(row)
        if ok:
            success += 1
        else:
            failed += 1
    st.success(f"✅ Upload complete. Success: {success}, Failed: {failed}")
