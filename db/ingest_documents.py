import os
import sys
import logging
import pymongo
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.embeddings.google_genai import GoogleGenerativeAIEmbeddings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Document loaders for multiple formats
from llama_index.readers.file import PDFReader
from llama_index.readers.file import DocxReader
from llama_index.readers.file import PandasExcelReader
from llama_index.core.schema import Document

from dotenv import load_dotenv

load_dotenv(".env")


# MongoDB connection details
MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = "embeddings_docs"


def load_pdf_documents(filename: str):
    """Load all PDF documents from the directory."""
    loader = PDFReader()
    docs = loader.load_data(filename)
    return docs


def load_docx_documents(filename: str):
    """Load all Word (.docx) documents from the directory."""
    loader = DocxReader()
    docs = loader.load_data(filename)
    return docs


def load_excel_documents(file_path: str):
    """Load all Excel (.xlsx) documents from the directory."""
    loader = PandasExcelReader()
    docs = loader.load_data(file_path)
    return docs


def load_text_documents(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    return text



def ingest_documents(directory_path: str) -> None:
    """
    Ingest documents from a directory, supporting Word, Excel, PDF, and text formats.
    Split them into sentences, embed, and store in MongoDB Atlas.

    Args:
        directory_path (str): Path to the directory containing documents.
    """
    documents = []
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(".xlsx"):
            documents.append(load_excel_documents(filename))
        elif filename.lower().endswith(".pdf"):
            documents.append(load_pdf_documents(filename))
        elif filename.lower().endswith(".docx"):
            documents.append(load_docx_documents(filename))
        elif filename.lower().endswith((".txt", ".md")):
            documents.append(load_text_documents(filename))

    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if filename.lower().endswith((".txt", ".md")):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            documents.append(Document(text=text, metadata={"filename": filename}))
        elif not filename.lower().endswith((".pdf", ".docx", ".xlsx", ".txt", ".md")):
            logging.warning(f"Unsupported file format: {filename}")

    logging.info(f"Loaded {len(documents)} documents from '{directory_path}'")

    vector_store = MongoDBAtlasVectorSearch(
        mongo_uri=MONGODB_URI,
        db_name=MONGO_DB,
        collection_name=MONGO_COLLECTION,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    embed_model = GoogleGenerativeAIEmbeddings()
    node_parser = SentenceSplitter(chunk_size=512)

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        node_parser=node_parser,
    )
    logging.info("Documents ingested and indexed successfully.")


def main():
    """Entry point for CLI usage."""
    if len(sys.argv) < 2:
        logging.error("Usage: python ingest_documents.py <directory_path>")
        sys.exit(1)
    ingest_documents(sys.argv[1])


if __name__ == "__main__":
    main()
