import streamlit as st

st.set_page_config(
    page_title="Guru Pooja Utsava",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# --- Title & Welcome ---
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Om_symbol.svg/512px-Om_symbol.svg.png", width=100)
st.title("🙏 Guru Pooja Utsava – Nagagiri Shake")

st.markdown(
    """
    Welcome! Kindly take a moment to share your details for this year's **Guru Pooja Utsava** at **Nagagiri Shake**.

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
