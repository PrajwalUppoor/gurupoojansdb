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
    update_db_entry
)
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
    selected_index = st.selectbox("Select Entry to Delete", options=row_labels.index, format_func=row_labels.__getitem__)
    if st.button("Confirm Delete"):
        delete_id = int(raw_df.loc[selected_index]["id"])
        delete_from_db(delete_id)
        st.success("✅ Entry deleted successfully")
        st.rerun()

    # --- Edit Entry ---
    st.subheader("✏️ Edit Entry")
    edit_index = st.selectbox("Select Entry to Edit", options=row_labels.index, format_func=row_labels.__getitem__, key="edit_select")
    selected_row = raw_df.loc[edit_index]

    with st.form("edit_form"):
        name = st.text_input("Name", selected_row["name"])
        phone = st.text_input("Phone", selected_row["phone"])
        email = st.text_input("Email", selected_row["email"])
        address1 = st.text_input("Address1", selected_row["address1"])
        profession = st.text_input("Profession", selected_row["profession"])
        work = st.text_input("Work", selected_row["work"])

        submitted = st.form_submit_button("Update Entry")
        if submitted:
            updated_data = {
                "name": name,
                "phone": phone,
                "email": email,
                "address1": address1,
                "profession": profession,
                "work": work
            }
            update_db_entry(int(selected_row["id"]), updated_data)
            st.success("✅ Entry updated")
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
                st.error(f"❌ Failed: {full_row.get('name', '')} – {msg}")
        st.success(f"Uploaded: ✅ {success}, ❌ {failed}")
else:
    st.info("No entries yet for this Shake.")
