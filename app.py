import streamlit as st

st.set_page_config(page_title="Guru Pooja Form", layout="centered")

st.sidebar.page_link("pages/form.py", label="📝 Submit Form")
st.sidebar.page_link("pages/admin.py", label="🔐 Admin Panel")
