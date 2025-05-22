import chromadb
from services.embedding import MyEmbeddingFunction
from db.mongodb import client
import zipfile, gridfs
import config



def selected_docs(selected_files:list)->list:
    try:

        db = client[config.MONGO_VECTOR_STORAGE] 
        fs = gridfs.GridFS(db)

        # Retrieve the file by filename or ID
        output_data = fs.get_last_version(filename=config.MONGO_VECTOR_DB_ZIP_NAME)

        # Save it locally again
        with open(config.MONGO_VECTOR_DB_DOWNLOADED_ZIP, "wb") as f:
            f.write(output_data.read())

        # unzip
        with zipfile.ZipFile(config.MONGO_VECTOR_DB_DOWNLOADED_ZIP, 'r') as zip_ref:
            zip_ref.extractall(config.VECTOR_DB_UNZIP)  # target folder to extract into

        db = chromadb.PersistentClient(path=config.VECTOR_DB_UNZIP)

        embedding_fn=MyEmbeddingFunction()
        selected_coll_data = []
        for collection_name in selected_files:
            try:
                coll = db.get_collection(
                    name=collection_name.split(".")[0],
                    embedding_function=embedding_fn
                )
                selected_coll_data.append(coll)
            except Exception as e:
                print(f"⚠️ Skipping missing collection: {collection_name} — {e}")
                continue
                
        return selected_coll_data
    except Exception as e:
        return f"❌  failed {e}"