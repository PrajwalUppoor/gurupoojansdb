import streamlit as st
from utils import load_data, submit_entry

# --- Login ---
st.title("🔐 Admin Panel – Guru Pooja Utsava")

PASSWORD = "r$$@100"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pw = st.text_input("Enter Admin Password", type="password")
    if pw == PASSWORD:
        st.session_state.logged_in = True
        st.success("✅ Logged in successfully")
    else:
        st.stop()

# --- Load Data ---
rows = load_data()
if not rows:
    st.warning("No data found in the Excel sheet.")
    st.stop()

# --- Display Table ---
st.subheader("📝 Submissions")
st.dataframe(rows, use_container_width=True)

# --- Trigger API Upload ---
if st.button("📤 Upload All to API"):
    success, failed = 0, 0
    for row in rows:
        ok, msg = submit_entry(row)
        if ok:
            success += 1
        else:
            failed += 1
    st.success(f"✅ Upload complete. Success: {success}, Failed: {failed}")
