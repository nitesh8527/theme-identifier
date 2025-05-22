
from chromadb.api.types import EmbeddingFunction
from sentence_transformers import SentenceTransformer

class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    def __call__(self, texts):
        return [self.model.encode(t, convert_to_numpy=True).tolist() for t in texts]


"""
class MyEmbeddingFunction(EmbeddingFunction):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2",device="cpu")

    def __call__(self, input):
        return self.model.encode(input).tolist()
"""