# utils.py

from db import SessionLocal
from models import Swayamsevak
import pandas as pd
import openpyxl
import os
import requests


def save_to_db(data):
    db = SessionLocal()

    # Filter only valid column names for Swayamsevak
    valid_keys = {
        "name", "phone", "email", "address1", "address2", "address3",
        "pincode", "dob", "bloodgroup", "education", "profession", "work",
        "sanghShikshan", "sanghaResponsibility", "sanghOrganizationName",
        "otherResponsibility", "shakhe", "vasati", "upavasati"
    }
    filtered_data = {k: v for k, v in data.items() if k in valid_keys}

    entry = Swayamsevak(**filtered_data)
    db.add(entry)
    db.commit()
    db.close()

def get_id_by_name(children, name):
    for child in children:
        if child["name"].strip().lower() == name.strip().lower():
            return child["_id"]
    return None

# --- DB Load ---
def load_from_db(shakhe=None):
    db = SessionLocal()
    query = db.query(Swayamsevak)
    if shakhe:
        query = query.filter(Swayamsevak.shakhe == shakhe)
    rows = query.all()
    db.close()
    return pd.DataFrame([
        {k: v for k, v in row.__dict__.items() if not k.startswith('_')}
        for row in rows
    ])

# --- DB Delete ---
def delete_from_db(row_id):
    db = SessionLocal()
    db.query(Swayamsevak).filter(Swayamsevak.id == row_id).delete()
    db.commit()
    db.close()

# --- Excel Export ---
def export_to_excel(df, filename):
    # Ensure it ends with .xlsx
    if not filename.endswith(".xlsx"):
        filename += ".xlsx"

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    file_path = os.path.join("data", filename)
    df.to_excel(file_path, index=False)
    return file_path

# --- Submit to API ---
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://kardakshinprant.pinkrafter.in",
    "referer": "https://kardakshinprant.pinkrafter.in/addSSDetails",
    "user-agent": "Mozilla/5.0"
}

def submit_entry(row):
    response = requests.post(
        "https://kardakshinprant.pinkrafter.in/api/createSSData",
        headers=HEADERS,
        json=row
    )
    return response.status_code == 200, response.text

# --- ID ↔ Name Mapping ---
NAGAR_ID = "668d00a0529dc546a1f242e0"
ENTITY_URL = "https://kardakshinprant.pinkrafter.in/api/entityChildren"
_entity_cache = {}

def get_entity_children(parent_id):
    if parent_id in _entity_cache:
        return _entity_cache[parent_id]
    try:
        response = requests.get(f"{ENTITY_URL}?entityId={parent_id}", headers=HEADERS)
        if response.status_code == 200:
            children = response.json()
            _entity_cache[parent_id] = children
            return children
    except Exception as e:
        print("⚠️ Failed to fetch entity children:", e)
    return []

def build_id_name_map():
    id_name_map = {}
    vasatis = get_entity_children(NAGAR_ID)
    for vasati in vasatis:
        vasati_id = vasati["_id"]
        id_name_map[vasati_id] = vasati["name"]
        for upavasati in get_entity_children(vasati_id):
            id_name_map[upavasati["_id"]] = upavasati["name"]
    return id_name_map

def map_ids_to_names(df):
    id_name_map = build_id_name_map()
    def resolve(val): return id_name_map.get(val, val)
    if "vasati" in df.columns:
        df["vasati"] = df["vasati"].apply(resolve)
    if "upavasati" in df.columns:
        df["upavasati"] = df["upavasati"].apply(resolve)
    return df
