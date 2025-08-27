import os
from io import BytesIO
from pathlib import Path

from docling.datamodel.base_models import InputFormat, DocumentStream
from docling.datamodel.pdf_models import TableFormerMode
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.pdf.pdf_backend import PyPdfiumDocumentBackend
from docling.pipeline.pdf_pipeline import StandardPdfPipeline


def doc_converter():
    """
    Create and return a DocumentConverter with custom PDF options.
    """
    model_dir = Path("/tmp/docling_models")
    tmp_path = StandardPdfPipeline.download_models_hf(local_dir=model_dir)
    pdf_options = PdfPipelineOptions(artifacts_path=tmp_path)
    pdf_options.do_ocr = False
    pdf_options.do_table_structure = True
    pdf_options.table_structure_options.do_cell_matching = True
    pdf_options.ocr_options.use_gpu = False
    pdf_options.table_structure_options.mode = TableFormerMode.ACCURATE
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pdf_options,
                backend=PyPdfiumDocumentBackend,
            ),
        },
    )


def convert_pdf_to_markdown(file_path: str):
    """
    Convert a PDF file to Markdown using the DocumentConverter.
    """
    converter = doc_converter()
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        source = DocumentStream(name=file_name, stream=BytesIO(f.read()))
    result = converter.convert(source=source)
    return result.document.export_to_markdown()
