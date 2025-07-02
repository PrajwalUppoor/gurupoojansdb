import streamlit as st

st.set_page_config(
    page_title="Guru Pooja Utsava",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

st.title("🙏 Guru Pooja Utsava – Admin Dashboard")

st.markdown(
    """
    Welcome to the **Guru Pooja Utsava Data Portal**.  
    Use the sidebar to:
    - 📋 Fill and submit new participant data (`form.py`)
    - 🔐 Manage and upload data via the admin panel (`admin.py`)
    - 📊 View and export all submissions
    """
)

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Om_symbol.svg/512px-Om_symbol.svg.png", width=100)

st.markdown("---")

st.markdown("### 📌 Quick Links")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ➕ New Entry")
    st.write("Submit a new participant using the form.")
    st.page_link("pages/form.py", label="Open Form Page")

with col2:
    st.markdown("#### 🔐 Admin Panel")
    st.write("Upload data to the website, manage Excel sheet.")
    st.page_link("pages/admin.py", label="Open Admin Panel")

st.set_page_config(page_title="Guru Pooja Form", layout="centered")

st.sidebar.page_link("pages/form.py", label="📝 Submit Form")
st.sidebar.page_link("pages/admin.py", label="🔐 Admin Panel")
