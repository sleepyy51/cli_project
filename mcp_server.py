from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string"
)
def read_documents(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found!")
    
    return docs[doc_id]

@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string"
)
def edit_document(
        doc_id: str = Field(description="Id of the document that will be edited"),
        old_str: str = Field(description="The text to replace must match exactly including white space"),
        new_str: str = Field(description="The new text to insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found!")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

@mcp.prompt(
    name="format",
    description="Rewrite a document to markdown format"
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[base.Message]:
    promt = f"""
    Rewrite the following document in clean Markdown.

    Requirements:
    - Preserve all information
    - Do not change the wording or meaning
    - Use headings where appropriate
    - Use bullet lists when useful
    - Improve formatting only.
    - Do not add or remove content.

    Document:
    {doc_id}
    """
    return [base.UserMessage(promt)]

@mcp.prompt(
    name="summarize_doc",
    description="Summarize document"
)
def summarize_doc(
    doc_id: str = Field(description="Id of the document to summarize")
) -> list[base.Message]:
    promt = f"""
    Summarize the following document.

    Requeriments:
    - Keep the summary under 150 words
    - Preserve all the important facts
    - Do not invent information
    - Do not draw conclusions
    - Keep all information factual

    Document:
    {doc_id}
    """
    return [base.UserMessage(promt)]

if __name__ == "__main__":
    mcp.run(transport="stdio")
