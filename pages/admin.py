# pages/admin.py
import streamlit as st
import pandas as pd
import os
from utils import load_from_db, delete_from_db, submit_entry, map_ids_to_names, export_to_excel
from models import SHAKHA_NAMES

st.set_page_config(page_title="Admin - Guru Pooja", layout="wide")

# --- Login ---
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
        st.stop()

st.sidebar.markdown("👤 Logged in as **Admin**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- Shake Select ---
st.title("📋 Admin Panel - Guru Pooja")
selected_shakhe = st.selectbox("Select Shake", SHAKHA_NAMES)
df = load_from_db(selected_shakhe)

if not df.empty:
    df = map_ids_to_names(df)
    st.dataframe(df, use_container_width=True)

    # --- Download ---
    if st.download_button("⬇ Download Excel", export_to_excel(df, selected_shakhe), file_name=f"{selected_shakhe}.xlsx"):
        st.success("Excel downloaded!")

    # --- Delete Entry ---
    st.subheader("🗑️ Delete Entry")
    idx_to_delete = st.selectbox("Choose Row to Delete", df.index)
    if st.button("Confirm Delete"):
        delete_from_db(df.loc[idx_to_delete]["id"])
        st.success("Deleted successfully")
        st.rerun()

    # --- Submit to API ---
    st.subheader("📤 Push to API")
    if st.button("Upload Shake Data"):
        success, failed = 0, 0
        for _, row in df.iterrows():
            ok, _ = submit_entry(row.to_dict())
            if ok: success += 1
            else: failed += 1
        st.success(f"Uploaded: ✅ {success}, ❌ {failed}")
else:
    st.info("No entries yet for this Shake.")
