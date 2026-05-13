import os
import uuid
from PIL import Image
from fastapi import UploadFile

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_image(file: UploadFile, resize=None):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    if resize:
        img = img.resize(resize, Image.Resampling.LANCZOS)
    img.save(filepath)
    return f"/static/uploads/{filename}"
