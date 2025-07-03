import streamlit as st
import pandas as pd
from utils import load_data, submit_entry, delete_row, map_ids_to_names
import plotly.express as px
import os

st.set_page_config(
    page_title="Admin – Guru Pooja",
    layout="wide",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

st.title("🔐 Admin Panel – Guru Pooja Utsava")

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
        st.warning("Incorrect password.")
        st.stop()

# --- Sidebar Logout ---
st.sidebar.markdown("👤 Logged in as **Admin**")
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# --- Shake Files ---
SHAKES = [
    "Nagagiri", "Maheshwara", "Chiranjeevi", "Vasudeva", "Keshava",
    "Brindavana", "Arehalli", "Ramanjaneya", "Kanaka"
]

selected_shake = st.selectbox("📂 Select Shake", SHAKES)
selected_file = f"ssdata_{selected_shake.lower()}.xlsx"

# --- Load Data ---
def refresh_table():
    if os.path.exists(selected_file):
        st.session_state.rows = load_data(selected_file)
        df = pd.DataFrame(st.session_state.rows)
        if not df.empty:
            df.columns = [col.strip().lower() for col in df.columns]
            df = map_ids_to_names(df)
        st.session_state.df = df
    else:
        st.session_state.rows = []
        st.session_state.df = pd.DataFrame()

if "rows" not in st.session_state:
    refresh_table()

rows = st.session_state.rows
df = st.session_state.df

# --- Display All Submissions ---
st.subheader("📋 All Submissions")
if df.empty:
    st.info("No data available.")
else:
    st.dataframe(df, use_container_width=True)

# --- Delete Section ---
st.markdown("### 🗑️ Delete an Entry")
if not df.empty:
    delete_index = st.selectbox("Select row to delete (by index)", df.index, format_func=lambda i: f"{df.loc[i, 'name']} ({df.loc[i, 'phone']})")
    if st.button("Confirm Delete"):
        delete_row(delete_index, selected_file)
        st.success(f"✅ Deleted: {df.loc[delete_index, 'name']}")
        refresh_table()
        st.rerun()

# --- Download Full CSV ---
csv_full = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download All Data as CSV", csv_full, f"{selected_shake.lower()}.csv", "text/csv")

# --- Upload All to API ---
st.markdown("### 📤 Push Shake Data to Website")
if st.button("Upload Shake Data"):
    success, failed = 0, 0
    for row in rows:
        ok, msg = submit_entry(row)
        if ok:
            success += 1
        else:
            failed += 1
    st.success(f"✅ Upload complete: {success} success, {failed} failed")

# --- Search & Filter Section ---
st.markdown("---")
st.subheader("🔍 Search by Vasati & Upavasati")

if df.empty or "vasati" not in df.columns:
    st.warning("No records available to search or filter yet.")
    st.stop()

with st.form("filter_form"):
    vasatis = df["vasati"].dropna().unique()
    selected_vasati = st.selectbox("Select Vasati", ["All"] + sorted(vasatis.tolist()))

    filtered_df = df.copy()
    if selected_vasati != "All":
        filtered_df = filtered_df[filtered_df["vasati"] == selected_vasati]

    upavasatis = filtered_df["upavasati"].dropna().unique()
    selected_upavasati = st.selectbox("Select Upavasati", ["All"] + sorted(upavasatis.tolist()))

    if selected_upavasati != "All":
        filtered_df = filtered_df[filtered_df["upavasati"] == selected_upavasati]

    clear = st.form_submit_button("🔁 Clear Filters")
    submit = st.form_submit_button("🔍 Apply Filters")

    if clear:
        st.experimental_rerun()

st.markdown(f"📦 **Total Filtered Results: {len(filtered_df)}**")

PAGE_SIZE = 10
total_pages = (len(filtered_df) - 1) // PAGE_SIZE + 1
page = st.number_input("Page", 1, max(1, total_pages), step=1)

start = (page - 1) * PAGE_SIZE
end = start + PAGE_SIZE
paginated_df = filtered_df.iloc[start:end]

st.dataframe(paginated_df, use_container_width=True)

csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Results", csv_filtered, f"filtered_{selected_shake.lower()}.csv", "text/csv")

st.markdown("### 📊 Vasati-wise Count")
vasati_counts = df["vasati"].value_counts().reset_index()
vasati_counts.columns = ["Vasati", "Count"]
chart = px.bar(vasati_counts, x="Vasati", y="Count", title="Number of Entries by Vasati", color="Vasati", height=400)
st.plotly_chart(chart, use_container_width=True)
