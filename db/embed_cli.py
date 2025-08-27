import argparse
import os
import logging
from ingest_documents import ingest_with_llamaindex

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description="Document embedding CLI for MongoDB using LlamaIndex")
    parser.add_argument('--doc_dir', type=str, default=os.path.join(os.path.dirname(__file__), 'sample_docs'), help='Path to the document directory (default: sample_docs)')
    args = parser.parse_args()

    if not os.path.isdir(args.doc_dir):
        logging.error(f"{args.doc_dir} is not a valid directory.")
        exit(1)

    logging.info(f"Starting embedding for documents in: {args.doc_dir}")
    # Đếm số lượng file hợp lệ
    from llama_index.core import SimpleDirectoryReader
    docs = SimpleDirectoryReader(input_dir=args.doc_dir).load_data()
    logging.info(f"Found {len(docs)} documents to process.")
    # Thực hiện embedding và lưu
    ingest_with_llamaindex(args.doc_dir)
    logging.info(f"Completed embedding for {len(docs)} documents.")
