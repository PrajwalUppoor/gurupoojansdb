import streamlit as st

from db import init_db

init_db()


st.set_page_config(
    page_title="Guru Pooja Utsava – Padmanabhanagara",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": None
    }
)

# --- Language Toggle ---
language = st.selectbox("🌐 Choose Language / ಭಾಷೆ ಆಯ್ಕೆ", ["English", "ಕನ್ನಡ"])

# --- OM Symbol ---
st.image("https://hindutone.com/wp-content/uploads/2024/11/rss-1296x700.webp", width=100)

# --- English Content ---
if language == "English":
    st.title("🙏 Guru Pooja Utsava – Padmanabhanagara")

    st.markdown(
        """
        Welcome! Kindly take a moment to share your details for this year's **Guru Pooja Utsava**.

        In the **Rashtriya Swayamsevak Sangh (RSS)** tradition, *Guru Pooja* is a sacred occasion where swayamsevaks express their **gratitude to the eternal Guru – the Bhagwa Dhwaj (Saffron Flag)**, which symbolizes sacrifice, purity, and dedication to the nation.

        On this day, swayamsevaks make an *Arpane* (humble offering) — not as a donation, but as an expression of their **commitment to seva, discipline, and national reconstruction**. It is an opportunity to reflect on our journey and renew our spiritual and social dedication.

        At **Padmanabhanagara Shake**, this Utsava brings together all swayamsevaks, families, and well-wishers to celebrate unity, values, and service. Your participation strengthens the fabric of our shakha and the larger Sangh parivar.
        """
    )

    st.markdown("### 📋 Participate Now")
    st.page_link("pages/form.py", label="📝 Fill the Registration Form")

# --- Kannada Content ---
else:
    st.title("🙏 ಗುರುಪೂಜೆ ಉತ್ಸವ – ಪದ್ಮನಾಭನಗರ")

    st.markdown(
        """
        ಸ್ವಾಗತ! ಈ ವರ್ಷದ **ಗುರುಪೂಜೆ ಉತ್ಸವ**ದಲ್ಲಿ ಭಾಗವಹಿಸಲು ದಯವಿಟ್ಟು ನಿಮ್ಮ ವಿವರಗಳನ್ನು ಹಂಚಿಕೊಳ್ಳಿ.

        **ರಾಷ್ಟ್ರೀಯ ಸ್ವಯಂಸೇವಕ ಸಂಘ**ದಲ್ಲಿ ಗುರುಪೂಜೆಯು ಅತ್ಯಂತ ಪವಿತ್ರವಾದ ದಿನ. ನಾವು ಭಗವಧ್ವಜಕ್ಕೆ ಪೂಜೆ ಸಲ್ಲಿಸುತ್ತೇವೆ — ಅದು ನಮ್ಮ ಶಾಶ್ವತ ಗುರು, ತ್ಯಾಗ, ಶುದ್ಧತೆ ಮತ್ತು ರಾಷ್ಟ್ರನಿರ್ಮಾಣದ ಪ್ರತೀಕವಾಗಿದೆ.

        ಈ ದಿನ *ಅರ್ಪಣೆ* ನೀಡುವುದು ದಾನವಲ್ಲ — ಇದು **ಸೇವಾಭಾವನೆ, ಶಿಸ್ತಿನ ಜೀವನ ಮತ್ತು ದೇಶದ ನವ ನಿರ್ಮಾಣದ ಸಂಕಲ್ಪ**. ಗುರುಪೂಜೆ ನಮ್ಮ ಆತ್ಮವಿಶ್ವಾಸವನ್ನೂ, ಸಂಘದ ಪ್ರಣಾಳಿಕೆಯ ಮೇಲಿನ ನಿಷ್ಠೆಯನ್ನೂ ಪುನರ್ ದೃಢಪಡಿಸುವ ಸಂದರ್ಭವಾಗಿದೆ.

        **ಪದ್ಮನಾಭನಗರ ಶಾಖೆಯಲ್ಲಿ**, ಈ ಉತ್ಸವವು ಎಲ್ಲ ಸ್ವಯಂಸೇವಕರು, ಕುಟುಂಬದ ಸದಸ್ಯರು ಮತ್ತು ಸಂಘಾಭಿಮಾನಿಗಳನ್ನು ಒಂದುಗೂಡಿಸುವ ಪವಿತ್ರ ಕ್ಷಣ. ನಿಮ್ಮ ಭಾಗವಹಿಸುವಿಕೆ ಶಾಖೆಯ ಸಂಘಟಿತ ಶಕ್ತಿ ಮತ್ತು ಮೌಲ್ಯಗಳನ್ನು ಬಲಪಡಿಸುತ್ತದೆ.
        """
    )

    st.markdown("### 📋 ಈಗ ಭಾಗವಹಿಸಿ")
    st.page_link("pages/form.py", label="📝 ನೋಂದಣಿ ಫಾರ್ಮ್ ಭರ್ತಿ ಮಾಡಿ")

# --- Footer ---
st.markdown("---")
st.caption("Designed with devotion ✨ / ಭಕ್ತಿಯಿಂದ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ ✨")
