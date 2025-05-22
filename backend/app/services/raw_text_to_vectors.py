import warnings
warnings.filterwarnings("ignore")
import os, time
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import chromadb
from services.embedding import MyEmbeddingFunction
import shutil, gridfs
from db.mongodb import database, client
import config

Persistent_folder = config.PRESISTENT_FOLDER
   

def text_to_vector(file:dict):    
    file_name = file['filename'].split(".")[0]
    try:

        db = chromadb.PersistentClient(path=Persistent_folder)

        embedding_fn=MyEmbeddingFunction()
        collection = db.get_or_create_collection(name=file_name, embedding_function=embedding_fn)

        if file['filename'].endswith(".jpg"):
            documents = [file['documents']]
            metadatas = [file['metadatas']]
            ids = [f"{file_name}_{str(uuid4())[:8]}" for _ in range(len(documents))]
        else:
            documents = file['documents']
            metadatas = file['metadatas']
            ids = [f"{file_name}_{str(uuid4())[:8]}" for _ in range(len(documents))]


        collection.add(documents=documents, ids=ids, metadatas=metadatas)

        #Persist the collection after adding
        collection.persist()

        
        return f"{file_name} vector created"

    except Exception as e:
        return f"❌ {file_name} failed: {e}"
    
def vector_to_mongodb(folder_path:str):
    try:
        # zip vector folder
        shutil.make_archive(config.MONGO_VECTOR_DB, 'zip', folder_path)

        # zip file to mongodb
        vector_storage = client[config.MONGO_VECTOR_STORAGE]

        fs = gridfs.GridFS(vector_storage)
        
        # Upload ZIP file
        with open(config.MONGO_VECTOR_DB_ZIP_NAME, "rb") as file_data:
            file_id = fs.put(file_data, filename=config.MONGO_VECTOR_DB_ZIP_NAME)

        # clean up
        shutil.rmtree(Persistent_folder)
        shutil.rmtree(config.MONGO_VECTOR_DB_ZIP_NAME)

        return "vector uploaded"

    except Exception as e:
        return "❌ failed: {e}"



# funcation for thread processing for high efficiently
def Thread_processing(data_list:list):
    try:
        start_time = time.time()
        results = []

        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = {executor.submit(text_to_vector, file): file for file in data_list}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Indexing PDFs"):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"❌ Error in file {futures[future]['filename']}: {e}")

        print(f"✅ Completed in {time.time() - start_time:.2f} seconds")
        return results
        

    except Exception as e:
        return "❌ failed: {e}"
    
def get_data_list():
    
    coll = database['text_&_metadata']
    data = [i for i in coll.find()]

    return data
    

def start_pipeline():
    try:
        
        Thread_processing(data_list=get_data_list())
        
        vector_to_mongodb(folder_path=Persistent_folder)

        return {"message": "text processing complete..."}

    except Exception as e:
        return "❌ failed: {e}"


