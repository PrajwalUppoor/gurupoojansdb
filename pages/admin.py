# pages/admin.py

import streamlit as st
import pandas as pd
import os
import json

from utils import (
    load_from_db,
    delete_from_db,
    submit_entry,
    map_ids_to_names,
    export_to_excel,
    update_db_entry,
    get_id_by_name,
    get_entity_children
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
    selected_index = st.selectbox("Select Entry to Delete", options=raw_df.index, format_func=row_labels.__getitem__)
    if st.button("Confirm Delete"):
        delete_id = int(raw_df.loc[selected_index]["id"])
        delete_from_db(delete_id)
        st.success("✅ Entry deleted successfully")
        st.rerun()

    # --- Edit Entry ---
    st.subheader("✏️ Edit Entry")
    edit_index = st.selectbox("Select Entry to Edit", options=raw_df.index, format_func=row_labels.__getitem__, key="edit_select")
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
    PRANT_ID = "668cfdff529dc546a1f20929"
    VIBHAG_ID = "668cfe2b529dc546a1f2092b"
    NAGAR_ID = "668d00a0529dc546a1f242e0"
    BHAG_ID = "668d0094529dc546a1f2409c"

    if st.button("Upload Shake Data"):
        success, failed = 0, 0

        for _, row in raw_df.iterrows():
            try:
                row_dict = row.to_dict()
                # Get all vasatis under Nagar
                vasati_list = get_entity_children(NAGAR_ID)
                vasati_id = get_id_by_name(vasati_list, row_dict.get("vasati"))

                # Get upavasatis under the resolved vasati
                upavasati_list = get_entity_children(vasati_id) if vasati_id else []
                upavasati_id = get_id_by_name(upavasati_list, row_dict.get("upavasati"))

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
                    "bhag": BHAG_ID,
                    "upavasati": upavasati_id,
                }

                # Remove empty/NaN
                payload = {k: v for k, v in payload.items() if v not in [None, "", "NaN", "nan"]}

                # Log the curl equivalent
                curl_cmd = f"""curl -X POST https://kardakshinprant.pinkrafter.in/api/createSSData \\
  -H 'accept: application/json' \\
  -H 'content-type: application/json' \\
  -H 'origin: https://kardakshinprant.pinkrafter.in' \\
  -H 'referer: https://kardakshinprant.pinkrafter.in/addSSDetails' \\
  -H 'user-agent: Mozilla/5.0' \\
  -d '{json.dumps(payload, ensure_ascii=False)}'"""
                with st.expander(f"📤 Payload Preview: {row_dict.get('name')}"):
                     st.code(curl_cmd, language="bash")


                ok, res = submit_entry(payload)
                if ok:
                    success += 1
                else:
                    st.error(f"❌ API rejected entry: {res}")
                    failed += 1
            except Exception as e:
                st.error(f"❌ Exception for {row_dict.get('name')}: {e}")
                failed += 1

        st.success(f"✅ Uploaded: {success} entries | ❌ Failed: {failed}")
else:
    st.info("No entries yet for this Shake.")
