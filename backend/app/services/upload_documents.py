from fastapi import UploadFile, File
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from db.mongodb import database
import config
import easyocr
import os
import tempfile
import shutil

# OCR Reader
reader = easyocr.Reader([config.OCR_LANGUAGE])

# MongoDB
coll = database[config.DOCUMENT_COLLECTION]

async def upload_docs(files: List[UploadFile] = File(...)):
    for uploaded_file in files:
        filename = uploaded_file.filename.lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            shutil.copyfileobj(uploaded_file.file, temp_file)
            temp_file_path = temp_file.name

        collection = {}

        if filename.endswith(".pdf"):
            try:
                loader = PyPDFLoader(temp_file_path)
                document = loader.load()
                doc = [page.page_content for page in document]
                meta = [page.metadata for page in document]
                collection['filename'] = filename
                collection['documents'] = doc
                collection['metadatas'] = meta
            except Exception as e:
                return {"error": f"PDF processing failed: {filename}, Error: {e}"}

        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            try:
                result = reader.readtext(temp_file_path)
                extracted_text = ' '.join([text for _, text, _ in result])
                collection['filename'] = filename
                collection['documents'] = extracted_text
                collection['metadatas'] = {'source': filename}
            except Exception as e:
                return {"error": f"OCR failed for: {filename}, Error: {e}"}

        else:
            continue

        coll.insert_one(collection)
        os.remove(temp_file_path)

    return {"message": f"{len(files)} files processed and stored successfully."}
