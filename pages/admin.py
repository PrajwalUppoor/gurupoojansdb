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
    get_id_by_name,
)
from models import SHAKHA_NAMES

# --- Config ---
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

# --- Shake Selector ---
st.title("📋 Admin Panel - Guru Pooja")
selected_shakhe = st.selectbox("Select Shake", SHAKHA_NAMES)
df = load_from_db(selected_shakhe)

# --- Display Data ---
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

    # --- Delete Entry ---
    st.subheader("🗑️ Delete Entry")
    idx_to_delete = st.selectbox("Choose Row to Delete", df.index)
    if st.button("Confirm Delete"):
        delete_from_db(df.loc[idx_to_delete]["id"])
        st.success("Deleted successfully")
        st.rerun()

    # --- Push to API ---
    st.subheader("📤 Push to API")
    PRANT_ID = "668cfdff529dc546a1f20929"
    VIBHAG_ID = "668cfe2b529dc546a1f2092b"
    NAGAR_ID = "668d00a0529dc546a1f242e0"

    if st.button("Upload Shake Data"):
        success, failed = 0, 0

        for _, row in df.iterrows():
            try:
                row_dict = row.to_dict()

                # Convert vasati/upavasati names to IDs
                vasati_id = get_id_by_name(row_dict.get("vasati"))
                upavasati_id = get_id_by_name(row_dict.get("upavasati"))

                if not vasati_id or not upavasati_id:
                    failed += 1
                    continue

                payload = {
                    "name": row_dict.get("name", ""),
                    "phone": row_dict.get("phone", ""),
                    "email": row_dict.get("email", ""),
                    "address1": row_dict.get("address1", ""),
                    "address2": row_dict.get("address2", ""),
                    "address3": row_dict.get("address3", ""),
                    "pincode": row_dict.get("pincode", ""),
                    "dob": row_dict.get("dob", ""),
                    "bloodgroup": row_dict.get("bloodgroup", ""),
                    "education": row_dict.get("education", ""),
                    "profession": row_dict.get("profession", ""),
                    "work": row_dict.get("work", ""),
                    "sanghShikshan": row_dict.get("sanghShikshan", ""),
                    "sanghaResponsibility": row_dict.get("sanghaResponsibility", ""),
                    "sanghOrganizationName": row_dict.get("sanghOrganizationName", ""),
                    "otherResponsibility": row_dict.get("otherResponsibility", ""),
                    "shakhe": row_dict.get("shakhe", ""),
                    "prant": PRANT_ID,
                    "vibhag": VIBHAG_ID,
                    "nagar": NAGAR_ID,
                    "vasati": vasati_id,
                    "upavasati": upavasati_id,
                }

                ok, _ = submit_entry(payload)
                if ok:
                    success += 1
                else:
                    failed += 1
            except Exception as e:
                failed += 1

        st.success(f"✅ Uploaded: {success} entries | ❌ Failed: {failed}")
else:
    st.info("No entries yet for this Shake.")
