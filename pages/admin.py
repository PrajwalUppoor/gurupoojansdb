# pages/admin.py

import streamlit as st
import pandas as pd
import os

from utils import (
    load_from_db,
    delete_from_db,
    submit_entry,
    map_ids_to_names,
    export_to_excel
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

# --- Shake Select ---
st.title("📋 Admin Panel - Guru Pooja")
selected_shakhe = st.selectbox("Select Shake", SHAKHA_NAMES)

# Load raw data (contains IDs) and mapped data (for display)
raw_df = load_from_db(selected_shakhe)

if not raw_df.empty:
    display_df = map_ids_to_names(raw_df.copy())
    st.dataframe(display_df, use_container_width=True)

    # --- Download Excel ---
    file_path = export_to_excel(display_df, f"{selected_shakhe}.xlsx")
    with open(file_path, "rb") as f:
        st.download_button(
            "⬇ Download Excel",
            f.read(),
            file_name=f"{selected_shakhe}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # --- Delete Entry ---
    st.subheader("🗑️ Delete Entry")
    row_options = raw_df[["id", "name", "phone"]].astype(str)
    row_labels = row_options.apply(lambda x: f"{x['id']} - {x['name']} ({x['phone']})", axis=1)
    selected_index = st.selectbox("Select Entry", options=row_labels.index, format_func=row_labels.__getitem__)
    if st.button("Confirm Delete"):
        delete_id = raw_df.loc[selected_index]["id"]
        delete_from_db(delete_id)
        st.success("✅ Entry deleted successfully")
        st.rerun()

    # --- Push to API ---
    st.subheader("📤 Push to API")
    if st.button("Upload Shake Data"):
        success, failed = 0, 0
        for _, row in raw_df.iterrows():
            full_row = row.to_dict()
            full_row.pop("_sa_instance_state", None)
            ok, msg = submit_entry(full_row)
            if ok:
                success += 1
            else:
                failed += 1
                st.error(f"❌ Failed to upload: {msg}")
        st.success(f"Uploaded: ✅ {success}, ❌ {failed}")
else:
    st.info("No entries yet for this Shake.")
