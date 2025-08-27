import argparse
import os
import logging
from ingest_documents import ingest_documents

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    parser = argparse.ArgumentParser(
        description="Document embedding CLI for MongoDB using LlamaIndex"
    )
    parser.add_argument(
        "--doc_dir",
        type=str,
        default=os.path.join(os.path.dirname(__file__), "sample_docs"),
        help="Path to the document directory (default: sample_docs)",
    )
    args = parser.parse_args()

    if not os.path.isdir(args.doc_dir):
        logging.error(f"{args.doc_dir} is not a valid directory.")
        exit(1)

    logging.info(f"Starting embedding for documents in: {args.doc_dir}")
    ingest_documents(args.doc_dir)
