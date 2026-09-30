"""
=============================================================================
DOCUMENT PARSER HELPER — Text & PDF Document Ingestion (Skill 04)
Autonomous Data-to-Decision Application Framework
Powered by Gemini 3.6 Flash & google-genai SDK
=============================================================================
"""

import os
import json
from pathlib import Path
from pypdf import PdfReader
from google import genai
from google.genai import types

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract plain text from PDF using pypdf as fallback/pre-processor."""
    reader = PdfReader(pdf_path)
    text = ""
    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        text += f"\n--- Page {idx + 1} ---\n{page_text}"
    return text

def parse_document_with_gemini(
    file_path: str,
    api_key: str = None,
    tenant_id: str = "tenant_demo"
) -> dict:
    """
    Ingests PDF, TXT, or Markdown documents and extracts structured entities
    and qualitative insights using Gemini 3.6 Flash.
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lower()
    
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Initialize Gemini Client
    client = genai.Client(api_key=api_key or os.getenv("GEMINI_API_KEY"))

    # Prepare input for Gemini 3.6 Flash
    if ext == ".pdf":
        # Native PDF processing via Gemini File API or inline bytes
        print(f"Uploading PDF '{file_path.name}' to Gemini File API...")
        uploaded_file = client.files.upload(file=file_path)
        contents = [
            uploaded_file,
            "Extract structured qualitative context, management notes, contract terms, duplicate payment flags, and key financial entities from this document."
        ]
    elif ext in [".txt", ".md"]:
        print(f"Reading text file '{file_path.name}'...")
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        contents = [
            f"Document Content ({file_path.name}):\n\n{raw_text}\n\nExtract structured qualitative context, management notes, contract terms, duplicate payment flags, and key financial entities."
        ]
    else:
        raise ValueError(f"Unsupported document format: {ext}. Supported: .pdf, .txt, .md")

    # Define extraction schema for structured JSON output
    system_instruction = """
    You are the Document Understanding Agent (Agent A1 / Skill 04).
    Extract explicit contract terms, qualitative variance drivers, risk notes, milestone commitments, and duplicate payment flags.
    Return strictly valid JSON matching the schema.
    """

    # Call Gemini 3.6 Flash with JSON Schema enforcement
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.1,
            response_mime_type="application/json",
            response_schema={
                "type": "OBJECT",
                "properties": {
                    "document_title": {"type": "STRING"},
                    "author_or_parties": {"type": "STRING"},
                    "reporting_period_or_date": {"type": "STRING"},
                    "summary": {"type": "STRING"},
                    "extracted_entities": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "entity_type": {"type": "STRING", "enum": ["contract_value", "duplicate_flag", "outlier_expense", "milestone", "risk_note"]},
                                "key": {"type": "STRING"},
                                "value": {"type": "STRING"},
                                "verbatim_excerpt": {"type": "STRING"},
                                "page_or_section": {"type": "STRING"}
                            },
                            "required": ["entity_type", "key", "value", "verbatim_excerpt"]
                        }
                    },
                    "linked_gl_accounts": {
                        "type": "ARRAY",
                        "items": {"type": "STRING"}
                    }
                },
                "required": ["document_title", "summary", "extracted_entities"]
            }
        )
    )

    result = json.loads(response.text)
    print(f"Successfully processed {file_path.name} with Gemini 3.6 Flash!")
    return result

if __name__ == "__main__":
    print("Document Parser Helper initialized.")
