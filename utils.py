# utils.py
import os
import openpyxl
import requests
from db import SessionLocal
from models import Swayamsevak

# API Constants
NAGAR_ID = "668d00a0529dc546a1f242e0"
ENTITY_URL = "https://kardakshinprant.pinkrafter.in/api/entityChildren"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://kardakshinprant.pinkrafter.in",
    "referer": "https://kardakshinprant.pinkrafter.in/addSSDetails",
    "user-agent": "Mozilla/5.0"
}
_entity_cache = {}

# --- Save to DB ---
def save_to_db(data):
    db = SessionLocal()
    db.add(Swayamsevak(**data))
    db.commit()
    db.close()

# --- Excel Fallback ---
def save_row(row, file_path):
    if not os.path.exists(file_path):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(list(row.keys()))
    else:
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active
    ws.append(list(row.values()))
    wb.save(file_path)

# --- API ---
def get_entity_children(parent_id):
    if parent_id in _entity_cache:
        return _entity_cache[parent_id]
    try:
        res = requests.get(f"{ENTITY_URL}?entityId={parent_id}", headers=HEADERS)
        if res.status_code == 200:
            _entity_cache[parent_id] = res.json()
            return _entity_cache[parent_id]
    except Exception as e:
        print("⚠️ Error fetching children:", e)
    return []

def get_id_by_name(children, name):
    for child in children:
        if child["name"].strip().lower() == name.strip().lower():
            return child["_id"]
    return None

# --- ID-to-Name mapping ---
def build_id_name_map():
    id_name_map = {}
    for vasati in get_entity_children(NAGAR_ID):
        id_name_map[vasati["_id"]] = vasati["name"]
        for upa in get_entity_children(vasati["_id"]):
            id_name_map[upa["_id"]] = upa["name"]
    return id_name_map

def map_ids_to_names(df):
    mapping = build_id_name_map()
    if "vasati" in df.columns:
        df["vasati"] = df["vasati"].apply(lambda v: mapping.get(v, v))
    if "upavasati" in df.columns:
        df["upavasati"] = df["upavasati"].apply(lambda v: mapping.get(v, v))
    return df

# --- API Submission (Optional Push) ---
def submit_entry(row):
    try:
        res = requests.post("https://kardakshinprant.pinkrafter.in/api/createSSData", headers=HEADERS, json=row)
        return res.status_code == 200, res.text
    except Exception as e:
        return False, str(e)
