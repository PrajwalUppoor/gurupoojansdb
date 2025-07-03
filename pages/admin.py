# pages/admin.py

import streamlit as st
import pandas as pd
import os

from utils import (
    load_from_db,
    delete_from_db,
    submit_entry,
    map_ids_to_names,
    export_to_excel,
)
from models import SHAKHA_NAMES

st.set_page_config(page_title="Admin - Guru Pooja", layout="wide")

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
        st.stop()

st.sidebar.markdown("👤 Logged in as **Admin**")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- Shake Selection ---
st.title("📋 Admin Panel - Guru Pooja")
selected_shakhe = st.selectbox("Select Shake", SHAKHA_NAMES)
df = load_from_db(selected_shakhe)

if not df.empty:
    df = map_ids_to_names(df)
    st.dataframe(df, use_container_width=True)

    # --- Download Excel ---
    file_path = export_to_excel(df, f"{selected_shakhe}.xlsx")
    with open(file_path, "rb") as f:
        st.download_button(
            "⬇ Download Excel",
            f.read(),
            file_name=f"{selected_shakhe}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # --- Delete Entry by DB ID ---
    st.subheader("🗑️ Delete Entry")
    delete_options = df[["id", "name"]].apply(lambda row: f"{row['id']}: {row['name']}", axis=1).tolist()
    selected_label = st.selectbox("Select entry to delete", delete_options)

    if selected_label:
        selected_id = int(selected_label.split(":")[0])
        if st.button("Confirm Delete"):
            delete_from_db(selected_id)
            st.success(f"Entry ID {selected_id} deleted successfully")
            st.rerun()

    # --- Submit to API ---
    st.subheader("📤 Push to API")
    if st.button("Upload Shake Data"):
        success, failed = 0, 0
        for _, row in df.iterrows():
            full_row = row.to_dict()
            # Remove unwanted columns like SQLAlchemy _sa_instance_state
            full_row.pop("_sa_instance_state", None)
            ok, _ = submit_entry(full_row)
            if ok:
                success += 1
            else:
                failed += 1
        st.success(f"Uploaded: ✅ {success}, ❌ {failed}")
else:
    st.info("No entries yet for this Shake.")
