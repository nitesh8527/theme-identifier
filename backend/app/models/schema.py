from pydantic import BaseModel, Field
from typing import List

class Selected_documents(BaseModel):
    documents: List[str]


class chatbot_input(BaseModel):
    query: str


# structure model
# Per-document structured output
class DocumentAnswer(BaseModel):
    Document_ID: str = Field(description="The document or filename.")
    Theme : str = Field(description="Given a user question return all extracted answer only.")
    Extracted_Answer : str = Field(
        description="Be concise, but clear. Return the list of themes with the related text.")
    
    Citation: str = Field(description="Page number or reference from the document.")

# Top-level output model
class structure_output(BaseModel):
    """
    Return a valid JSON array of all the extracted answers across documents.
    """
    results: List[DocumentAnswer] = Field(description="List of answers extracted from multiple documents.")