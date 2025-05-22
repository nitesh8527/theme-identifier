from fastapi import FastAPI, UploadFile, File
from typing import List
from services.upload_documents import upload_docs
from services.raw_text_to_vectors import start_pipeline
from services.extract_file_names import extracted_files
from services.documents_for_query import selected_docs
from services.llm_bot_response import llm_output
from models.schema import Selected_documents, chatbot_input

app = FastAPI()

selected_files_cache = []

@app.post("/upload")
async def handle_upload(files: List[UploadFile] = File(...)):
    return await upload_docs(files)


@app.get("/process")
async def handle_processing():
    return start_pipeline()

@app.get("/extractfiles")
async def files():
    return extracted_files()

@app.post("/selected_docs")
async def query_context(data: Selected_documents):
    global selected_files_cache
    selected_files_cache = selected_docs(data.documents)
    return  {"message": "Data cached"}



@app.post("/response")
async def response(data: chatbot_input):
    if selected_files_cache is None:
        return {"error": "No selected data cached"}
    #selected_data = selected_docs(selected_files=selected_files_cache)
    llm_response = llm_output(selected_data=selected_files_cache,query=data.query)

    return  {"llm_output": llm_response}