import streamlit as st
import pandas as pd
from utils import load_data, submit_entry, delete_row

# --- Config ---
st.set_page_config(
    page_title="Admin – Guru Pooja",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

st.title("🔐 Admin Panel – Guru Pooja Utsava")

# --- Admin Login ---
PASSWORD = st.secrets["admin"]["password"]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    pw = st.text_input("Enter Admin Password", type="password")
    if pw == PASSWORD:
        st.session_state.logged_in = True
        st.success("✅ Logged in successfully")
        st.rerun()
    else:
        st.warning("Incorrect password.")
        st.stop()

# --- Sidebar Logout ---
st.sidebar.markdown("👤 Logged in as **Admin**")
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- Load Data ---
def refresh_table():
    st.session_state.rows = load_data()
    st.session_state.df = pd.DataFrame(st.session_state.rows)

if "rows" not in st.session_state:
    refresh_table()

rows = st.session_state.rows
df = st.session_state.df

# --- Display Table ---
st.subheader("📊 All Submissions")

if df.empty:
    st.info("No submissions yet.")
else:
    st.dataframe(df, use_container_width=True)

    # --- Delete Any Row ---
    st.markdown("### 🗑️ Delete an Entry")
    delete_index = st.selectbox("Select row to delete (by index)", df.index, format_func=lambda i: f"{df.loc[i, 'name']} ({df.loc[i, 'phone']})")
    if st.button("Confirm Delete"):
        delete_row(delete_index)
        st.success(f"✅ Deleted: {df.loc[delete_index, 'name']}")
        refresh_table()
        st.rerun()

# --- Download CSV ---
st.markdown("### 📥 Download Submissions")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download as CSV",
    data=csv,
    file_name="ssdata.csv",
    mime="text/csv"
)

# --- Upload All to API ---
st.markdown("### 📤 Push All Data to Website")
if st.button("Upload All"):
    success, failed = 0, 0
    for row in rows:
        ok, msg = submit_entry(row)
        if ok:
            success += 1
        else:
            failed += 1
    st.success(f"✅ Upload complete: {success} success, {failed} failed")
