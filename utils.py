import openpyxl
import os
import requests
import pandas as pd

# --- Constants ---
NAGAR_ID = "668d00a0529dc546a1f242e0"  # Padmanabhanagar
ENTITY_URL = "https://kardakshinprant.pinkrafter.in/api/entityChildren"
EXCEL_FILE = "ssdata.xlsx"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://kardakshinprant.pinkrafter.in",
    "referer": "https://kardakshinprant.pinkrafter.in/addSSDetails",
    "user-agent": "Mozilla/5.0"
}

_entity_cache = {}

# --- Excel Operations ---
def load_data():
    if not os.path.exists(EXCEL_FILE):
        return []

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    headers = [str(cell.value).strip().lower() for cell in next(ws.iter_rows(min_row=1, max_row=1))]

    return [dict(zip(headers, [cell.value for cell in row])) for row in ws.iter_rows(min_row=2)]

def save_row(row):
    if not os.path.exists(EXCEL_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(list(row.keys()))
    else:
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
    ws.append(list(row.values()))
    wb.save(EXCEL_FILE)

def delete_row(index):
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.delete_rows(index + 2)  # +2 to account for header row and 0-based index
    wb.save(EXCEL_FILE)

# --- API Calls ---
def submit_entry(row):
    response = requests.post(
        "https://kardakshinprant.pinkrafter.in/api/createSSData",
        headers=HEADERS,
        json=row
    )
    return response.status_code == 200, response.text

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

# --- ID ↔ Name Mapping ---
def build_id_name_map():
    """Build a map of {id: name} for all vasatis and upavasatis"""
    id_name_map = {}

    vasatis = get_entity_children(NAGAR_ID)
    for vasati in vasatis:
        vasati_id = vasati["_id"]
        id_name_map[vasati_id] = vasati["name"]

        upavasatis = get_entity_children(vasati_id)
        for upavasati in upavasatis:
            id_name_map[upavasati["_id"]] = upavasati["name"]

    return id_name_map

def map_ids_to_names(df):
    """Replace vasati/upavasati IDs in DataFrame with names"""
    id_name_map = build_id_name_map()

    def resolve(val):
        return id_name_map.get(val, val)

    df["vasati"] = df["vasati"].apply(resolve)
    df["upavasati"] = df["upavasati"].apply(resolve)

    return df
