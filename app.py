import streamlit as st

st.set_page_config(
    page_title="Guru Pooja Utsava",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# --- Title & Welcome ---
st.image("https://hindutone.com/wp-content/uploads/2024/11/rss-1296x700.webp", width=100)
st.title("🙏 Guru Pooja Utsava – Padmanabhanagara")

st.markdown(
    """
    Welcome! Kindly take a moment to share your details for this year's **Guru Pooja Utsava**.

    Your participation helps us plan and serve better.  
    Please click below to proceed to the form.
    """
)

st.markdown("---")

# --- CTA Button ---
st.markdown("### 📋 Participate Now")
st.page_link("pages/form.py", label="📝 Fill the Registration Form", icon="📝")

# --- Footer ---
st.markdown("---")
st.caption("Designed with devotion ✨")


st.sidebar.page_link("pages/form.py", label="📝 Submit Form")
st.sidebar.page_link("pages/admin.py", label="🔐 Admin Panel")
