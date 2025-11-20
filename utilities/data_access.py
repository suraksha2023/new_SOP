import openpyxl

def read_sop_data(filepath):
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active

    data = []
    headers = [cell.value for cell in sheet[1]]  # Read header row

    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Unpack values based on header order
        (
            role,
            username,
            password,
            sop_title,
            file_path
        ) = row

        # Skip empty or invalid rows
        if not role or not username or not password:
            continue

        # Append clean row to final list
        data.append({
            "role": role,
            "username": str(username).strip(),
            "password": str(password).strip(),
            "sop_title": sop_title,
            "file_path": file_path if file_path not in ("", None) else None
        })

    return data
