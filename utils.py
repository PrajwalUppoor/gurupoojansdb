import openpyxl
import os
import requests

EXCEL_FILE = "ssdata.xlsx"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    "origin": "https://kardakshinprant.pinkrafter.in",
    "referer": "https://kardakshinprant.pinkrafter.in/addSSDetails",
    "user-agent": "Mozilla/5.0"
}

def load_data():
    if not os.path.exists(EXCEL_FILE):
        return []
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    headers = [cell.value for cell in next(ws.iter_rows(min_row=1, max_row=1))]
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

def submit_entry(row):
    response = requests.post(
        "https://kardakshinprant.pinkrafter.in/api/createSSData",
        headers=HEADERS,
        json=row
    )
    return response.status_code == 200, response.text
def delete_row(index):
    import openpyxl
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active
    ws.delete_rows(index + 2)  # +2 because Excel rows are 1-indexed and row 1 is header
    wb.save(EXCEL_FILE)

