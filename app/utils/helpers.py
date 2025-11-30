import os
from fastapi import UploadFile
from typing import List

# ----------------------------
# Save uploaded files
# ----------------------------
def save_upload_file(upload_file: UploadFile, folder: str) -> str:
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, upload_file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return upload_file.filename

# ----------------------------
# Calculate total from order items
# ----------------------------
def calculate_order_total(items: List[dict]) -> float:
    return sum(item["price"] * item["qty"] for item in items)
