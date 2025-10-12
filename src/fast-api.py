from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
import asyncio
from main import run
import io
import zipfile
from pathlib import Path

app = FastAPI(title="Markdown File Saver & Zipper")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@app.post("/upload-markdown-zip/")
async def upload_markdown_zip(
    markdown: UploadFile = File(...),
):
    files = [markdown]
    saved_paths = []

    # Save uploaded files locally
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        saved_paths.append(file_path)

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("output/report.txt", arcname="report.txt")

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": 'attachment; filename="uploaded_markdowns.zip"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )
