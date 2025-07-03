# pages/form.py
import streamlit as st
import requests
from utils import save_row, save_to_db, get_entity_children, get_id_by_name

# Constants
PRANT_ID = "668cfdff529dc546a1f20929"
VIBHAG_ID = "668d001d529dc546a1f23148"
BHAG_ID = "668d0094529dc546a1f2409c"
NAGAR_ID = "668d00a0529dc546a1f242e0"

shakha_options = [
    "Nagagiri", "Maheshwara", "Chiranjeevi", "Vasudeva",
    "Keshava", "Brindavana", "Arehalli", "Ramanjaneya", "Kanaka"
]

st.set_page_config(page_title="Swayamsevak Form", layout="centered")
st.title("📝 Swayamsevak Information – RSS Padmanabhanagara")

# --- Form Inputs ---
name = st.text_input("Name *")
phone = st.text_input("Phone *")
email = st.text_input("Email")
address1 = st.text_input("Address Line 1 *")
address2 = st.text_input("Address Line 2 *")
address3 = st.text_input("Address Line 3 *")
pincode = st.text_input("Pincode *")
dob = st.text_input("Year of Birth (YYYY) *")
bloodgroup = st.selectbox("Blood Group *", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
education = st.selectbox("Education *", [
    "1 - 9 Standard", "10th Standard", "11th Standard / PUC 1st Year",
    "12th Standard / PUC 2nd Year", "Degree", "Post Graduation", "PhD"
])
profession = st.selectbox("Profession *", [
    "Student", "Teacher", "Engineer", "Doctor", "Lawyer", "Buisness",
    "Farmer", "ಪ್ರಚಾರಕ/Pracharaka", "Retired", "Other"
])
work = st.text_input("Work Details (Company, Designation) *")

sanghShikshan = st.selectbox("Sangh Shikshan *", [
    "ಪ್ರಾರಂಭಿಕ ವರ್ಗ / Prarambhik Varga",
    "ಪ್ರಾಥಮಿಕ ಶಿಕ್ಷಾ ವರ್ಗ / Prathamik Shiksha Varga",
    "ಸಂಘ ಶಿಕ್ಷಾ ವರ್ಗ / Sangha Shiksha Varga",
    "ಕಾರ್ಯಕರ್ತ ವಿಕಾಸ ವರ್ಗ - 1 / Karyakarta Vikas Varga - 1",
    "ಕಾರ್ಯಕರ್ತ ವಿಕಾಸ ವರ್ಗ - 2 / Karyakarta Vikas Varga - 2",
    "ಸಂಘ ಶಿಕ್ಷಾ ವರ್ಗ - ದ್ವಿತೀಯ / Sangha Shiksha Varga - Dvitiiya",
    "ಸಂಘ ಶಿಕ್ಷಾ ವರ್ಗ - ತೃತೀಯ / Sangha Shiksha Varga - Tritiiya",
    "ಇನ್ನೂ ಆಗಬೇಕಿದೆ / Yet to attend"
])

sanghaResponsibility = st.selectbox("Sangha Responsibility *", [
    "ಸಂಘ ಜವಾಬ್ದಾರಿ/Sangha Responsibility",
    "ವಿವಿಧ ಕ್ಷೇತ್ರದ ಜವಾಬ್ದಾರಿ/Vividh Khsetra Responsibility",
    "ಸ್ವಯಂಸೇವಕ/Swayamsevak"
])

sanghOrganizationName, otherResponsibility = "", ""
if sanghaResponsibility == "ವಿವಿಧ ಕ್ಷೇತ್ರದ ಜವಾಬ್ದಾರಿ/Vividh Khsetra Responsibility":
    sanghOrganizationName = st.text_input("Organization Name *")
    otherResponsibility = st.text_input("Please specify your responsibility *")
elif sanghaResponsibility == "ಸಂಘ ಜವಾಬ್ದಾರಿ/Sangha Responsibility":
    otherResponsibility = st.text_input("Please specify your responsibility *")

shakhe = st.selectbox("Shake *", shakha_options)

# --- Vasati and Upavasati ---
if "vasati_children" not in st.session_state:
    st.session_state.vasati_children = get_entity_children(NAGAR_ID)
    st.session_state.vasati_names = [v["name"] for v in st.session_state.vasati_children]
    st.session_state.vasati_name = st.session_state.vasati_names[0]
    st.session_state.vasati_id = get_id_by_name(st.session_state.vasati_children, st.session_state.vasati_name)

selected_vasati = st.selectbox("Vasati *", st.session_state.vasati_names, key="vasati_name")
st.session_state.vasati_id = get_id_by_name(st.session_state.vasati_children, selected_vasati)

upavasati_children = get_entity_children(st.session_state.vasati_id)
upavasati_names = [u["name"] for u in upavasati_children]
upavasati_id = None
if upavasati_names:
    selected_upavasati = st.selectbox("Upavasati *", upavasati_names, key="upavasati_name")
    upavasati_id = get_id_by_name(upavasati_children, selected_upavasati)

# --- Submit Button ---
if st.button("Submit"):
    required = [name, phone, address1, address2, address3, pincode, dob, work]
    if not all(required):
        st.error("❌ Please fill all required fields.")
    elif not st.session_state.vasati_id or not upavasati_id:
        st.error("❌ Vasati/Upavasati missing.")
    elif sanghaResponsibility.startswith("ವಿವಿಧ") and (not sanghOrganizationName or not otherResponsibility):
        st.error("❌ Responsibility fields missing.")
    elif sanghaResponsibility.startswith("ಸಂಘ") and not otherResponsibility:
        st.error("❌ Responsibility detail required.")
    else:
        row = {
            "prant": PRANT_ID, "vibhag": VIBHAG_ID, "bhag": BHAG_ID, "nagar": NAGAR_ID,
            "vasati": st.session_state.vasati_id, "upavasati": upavasati_id,
            "shakhe": shakhe, "name": name, "phone": phone, "email": email,
            "address1": address1, "address2": address2, "address3": address3,
            "pincode": pincode, "dob": dob, "bloodgroup": bloodgroup,
            "education": education, "otherEducation": "", "profession": profession,
            "otherProfession": "", "work": work, "sanghShikshan": sanghShikshan,
            "sanghaResponsibility": sanghaResponsibility,
            "sanghOrganizationName": sanghOrganizationName,
            "otherResponsibility": otherResponsibility
        }
        save_to_db(row)
        save_row(row, f"ssdata_{shakhe.lower()}.xlsx")
        st.success("✅ Submitted successfully!")
