import streamlit as st
import pandas as pd
from utils import load_data, submit_entry, delete_row

# --- Config ---
st.set_page_config(
    page_title="Admin – Guru Pooja",
    layout="wide",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
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
        st.experimental_rerun()
    else:
        st.warning("Incorrect password.")
        st.stop()

# --- Sidebar Info and Logout ---
st.sidebar.markdown("👤 Logged in as **Admin**")
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.experimental_rerun()

# --- Load Data ---
def refresh_table():
    st.session_state.rows = load_data()
    st.session_state.df = pd.DataFrame(st.session_state.rows)

if "rows" not in st.session_state:
    refresh_table()

rows = st.session_state.rows
df = st.session_state.df

# --- Display Entries ---
st.subheader("📝 Submissions")

if df.empty:
    st.info("No submissions found.")
else:
    for i, row in df.iterrows():
        cols = st.columns([5, 1])
        with cols[0]:
            st.markdown(
                f"""
                **{row['name']}** | {row['phone']} | {row['email']}  
                **DOB**: {row['dob']} | **Shakhe**: {row['shakhe']}  
                **Vasati → Upavasati**: {row['vasati']} → {row['upavasati']}
                """
            )
        with cols[1]:
            if st.button("🗑️", key=f"del_{i}"):
                delete_row(i)
                st.success(f"✅ Deleted: {row['name']}")
                refresh_table()
                st.experimental_rerun()

# --- Download CSV ---
st.markdown("### 📥 Download Data")
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
