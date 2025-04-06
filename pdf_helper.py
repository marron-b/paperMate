from mcp.server.fastmcp import FastMCP
import mcp.types as types
from docx import Document
from PyPDF2 import PdfReader, PdfMerger
import os
import re

mcp = FastMCP("PDFHelper", dependencies=["PyPDF2", "python-docx"])


@mcp.tool(
    name="convert_pdf_to_word",
    description="Convert a PDF file to a Word document (.docx).",
)
def convert_pdf_to_word(file_path: str) -> str:
    """
    Extracts text from a PDF file and saves it as a Word document (.docx).
    """
    text = extract_text_from_pdf(file_path)
    text = remove_reference_section(text)

    word_file_path = file_path.replace(".pdf", ".docx")
    save_to_word_doc(text, word_file_path)

    return word_file_path


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text content from a PDF file."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"

    return text.strip() if text.strip() else "No text could be extracted from the PDF."


def remove_reference_section(text: str) -> str:
    """
    Removes the reference section from the extracted text.
    Looks for keywords like 'References', 'Bibliography', 'Works Cited', etc.
    """
    pattern = r"(?:\n|\r|\r\n)(References|REFERENCES|Bibliography|Works Cited|참고문헌|참고 자료|참고서적|참고 문헌)(?:\n|\r|\r\n).*"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return text[: match.start()]
    return text


def save_to_word_doc(text: str, word_path: str):
    """Save the given text to a Word (.docx) file."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(word_path)


@mcp.tool(
    name="merge_pdfs",
    description="Merge multiple PDF files into a single PDF document.",
)
def merge_pdfs(
    pdf_files: list[str] | None, output_path: str | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Merges a list of PDF files into one and saves it to the given output path.
    Returns a success or error message.
    """
    if not pdf_files:
        raise ValueError("Missing list of PDF files.")
    if not output_path:
        raise ValueError("Missing output file path.")

    merger = PdfMerger()

    try:
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                return [
                    types.TextContent(
                        type="text", text=f"Error: File not found - {pdf_file}"
                    )
                ]
            with open(pdf_file, "rb") as pf:
                merger.append(pf)

        with open(output_path, "wb") as of:
            merger.write(of)

        return [
            types.TextContent(
                type="text",
                text=f"Successfully merged {len(pdf_files)} PDF files into '{output_path}'.",
            )
        ]

    except Exception as e:
        return [
            types.TextContent(
                type="text", text=f"An error occurred while merging PDFs: {str(e)}"
            )
        ]
    finally:
        merger.close()
