import streamlit as st
import requests
import openpyxl
from openpyxl import Workbook
import os
from utils import save_row

# Constants
PRANT_ID = "668cfdff529dc546a1f20929"
VIBHAG_ID = "668d001d529dc546a1f23148"
BHAG_ID = "668d0094529dc546a1f2409c"
NAGAR_ID = "668d00a0529dc546a1f242e0"
EXCEL_FILE = "ssdata.xlsx"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://kardakshinprant.pinkrafter.in",
    "referer": "https://kardakshinprant.pinkrafter.in/addSSDetails",
    "user-agent": "Mozilla/5.0"
}

# API Helper
def get_entity_children(parent_id):
    url = f"https://kardakshinprant.pinkrafter.in/api/entityChildren?entityId={parent_id}"
    res = requests.get(url, headers=HEADERS)
    return res.json() if res.status_code == 200 else []

def get_id_by_name(children, name):
    for child in children:
        if child["name"].strip().lower() == name.strip().lower():
            return child["_id"]
    return None

# Excel Helper
def save_to_excel(data):
    if not os.path.exists(EXCEL_FILE):
        wb = Workbook()
        ws = wb.active
        ws.append(list(data.keys()))
    else:
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
    ws.append(list(data.values()))
    wb.save(EXCEL_FILE)

def submit_to_api(data):
    response = requests.post("https://kardakshinprant.pinkrafter.in/api/createSSData", headers=HEADERS, json=data)
    return response.status_code == 200, response.text

# Dropdown Values
blood_groups = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
education_levels = [
    "1 - 9 Standard", "10th Standard", "11th Standard / PUC 1st Year",
    "12th Standard / PUC 2nd Year", "Degree", "Post Graduation", "PhD"
]
professions = [
    "Student", "Teacher", "Engineer", "Doctor", "Lawyer", "Buisness",
    "Farmer", "ಪ್ರಚಾರಕ/Pracharaka", "Retired", "Other"
]
shikshan_options = [
    "ಪ್ರಾರಂಭಿಕ ವರ್ಗ / Prarambhik Varga",
    "ಪ್ರಾಥಮಿಕ ಶಿಕ್ಷಾ ವರ್ಗ / Prathamik Shiksha Varga",
    "ಸಂಘ ಶಿಕ್ಷಾ ವರ್ಗ / Sangha Shiksha Varga",
    "ಕಾರ್ಯಕರ್ತ ವಿಕಾಸ ವರ್ಗ - 1 / Karyakarta Vikas Varga - 1",
    "ಕಾರ್ಯಕರ್ತ ವಿಕಾಸ ವರ್ಗ - 2 / Karyakarta Vikas Varga - 2",
    "ಸಂಘ ಶಿಕ್ಷಾ ವರ್ಗ - ದ್ವಿತೀಯ / Sangha Shiksha Varga - Dvitiiya",
    "ಸಂಘ ಶಿಕ್ಷಾ ವರ್ಗ - ತೃತೀಯ / Sangha Shiksha Varga - Tritiiya",
    "ಇನ್ನೂ ಆಗಬೇಕಿದೆ / Yet to attend"
]
responsibility_options = [
    "ಸಂಘ ಜವಾಬ್ದಾರಿ/Sangha Responsibility",
    "ವಿವಿಧ ಕ್ಷೇತ್ರದ ಜವಾಬ್ದಾರಿ/Vividh Khsetra Responsibility",
    "ಸ್ವಯಂಸೇವಕ/Swayamsevak"
]

# Title
st.title("Guru Pooja Utsava Nagagiri Shake Form")

name = st.text_input("Name *")
phone = st.text_input("Phone *")
email = st.text_input("Email ")
address1 = st.text_input("Address Line 1 *")
address2 = st.text_input("Address Line 2 *")
address3 = st.text_input("Address Line 3 *")
pincode = st.text_input("Pincode *")
dob = st.text_input("Year of Birth (YYYY) *")
bloodgroup = st.selectbox("Blood Group *", blood_groups)
education = st.selectbox("Education *", education_levels)
profession = st.selectbox("Profession *", professions)
work = st.text_input("Work Details (Company, Designation) *")
sanghShikshan = st.selectbox("Sangh Shikshan *", shikshan_options, index=shikshan_options.index("ಇನ್ನೂ ಆಗಬೇಕಿದೆ / Yet to attend"))
sanghaResponsibility = st.selectbox("Sangha Responsibility *", responsibility_options, index=responsibility_options.index("ಸ್ವಯಂಸೇವಕ/Swayamsevak"))
shakhe = "Naga Giri Prabhat"
st.markdown(f"**Shake**: {shakhe}")

# Fetch Vasati ONCE
if "vasati_children" not in st.session_state:
    with st.spinner("Loading vasati options..."):
        st.session_state.vasati_children = get_entity_children(NAGAR_ID)
        st.session_state.vasati_names = [v["name"] for v in st.session_state.vasati_children]
        st.session_state.vasati_name = st.session_state.vasati_names[0]
        st.session_state.vasati_id = get_id_by_name(st.session_state.vasati_children, st.session_state.vasati_name)

# Vasati select (fixed list)
selected_vasati = st.selectbox("Vasati *", st.session_state.vasati_names, key="vasati_name")
st.session_state.vasati_id = get_id_by_name(st.session_state.vasati_children, selected_vasati)

# Update Upavasati based on vasati
with st.spinner("Loading upavasati options..."):
    upavasati_children = get_entity_children(st.session_state.vasati_id)
    upavasati_names = [u["name"] for u in upavasati_children]
    if upavasati_names:
        if "upavasati_name" not in st.session_state or st.session_state.upavasati_name not in upavasati_names:
            st.session_state.upavasati_name = upavasati_names[0]
        upavasati_name = st.selectbox("Upavasati *", upavasati_names, key="upavasati_name")
        upavasati_id = get_id_by_name(upavasati_children, upavasati_name)
    else:
        st.warning("No upavasatis found.")
        upavasati_id = None

# Inputs


# Submit
if st.button("Submit"):
    required_fields = [name, phone, address1, address2, address3, pincode, dob, work]
    if not all(required_fields):
        st.error("❌ Please fill all the mandatory (*) fields.")
    elif not st.session_state.vasati_id or not upavasati_id:
        st.error("❌ Vasati or Upavasati selection failed.")
    else:
        data = {
            "prant": PRANT_ID, "vibhag": VIBHAG_ID, "bhag": BHAG_ID,
            "nagar": NAGAR_ID, "vasati": st.session_state.vasati_id, "upavasati": upavasati_id,
            "shakhe": shakhe, "name": name, "phone": phone, "email": email,
            "address1": address1, "address2": address2, "address3": address3,
            "pincode": pincode, "bloodgroup": bloodgroup, "dob": dob,
            "education": education, "otherEducation": "", "profession": profession,
            "otherProfession": "", "work": work, "sanghShikshan": sanghShikshan,
            "sanghaResponsibility": sanghaResponsibility,
            "sanghOrganizationName": "", "otherResponsibility": ""
        }

        save_row(data)       
        st.success("✅ Data submitted and saved to Excel successfully.")