from pymongo import MongoClient
import sys
import os
# Add the parent directory (backend) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config

MONGO_URL = config.MONGO_URL

client = MongoClient(MONGO_URL)

database = client[config.DOCUMENT_DATABASE]  # globally initialized
