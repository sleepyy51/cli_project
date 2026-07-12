from mcp.server.fastmcp import FastMCP
from pydantic import Field

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

@mcp.tool(
    name="list_documents",
    description="Lists all documents ids and their number"
)
def list_documents():
    if not docs:
        raise ValueError("There aren't any documents in the list")
    
    return{
        "documents": list(docs.keys()),
        "count": len(docs)
    }
    
@mcp.tool(
    name="doc_contents",
    description="Returns the contents of a doc as a string"
)
def doc_contents(
    doc_id: str = Field(description="Id of the document we are looking for")
):
    if doc_id not in docs:
        raise ValueError(f"Document with id{doc_id} not found")
    
    return docs[doc_id]

@mcp.prompt(
    name="rewrite_doc_to_markdown",
    description="Rewrite a document to markdown format"
)
def rewrite_doc_to_markdown(document: str):
    return f"""
Rewrite the following document in clean Markdown.

Requirements:
- Preserve all information
- Do not change the wording or meaning
- Use headings where appropriate
- Use bullet lists when useful
- Improve formatting only.
- Do not add or remove content.

Document:
{document}
"""

@mcp.prompt(
    name="summarize_doc",
    description="Summarize document"
)
def summarize_doc(document : str):
    return f"""
    Summarize the following document.

    Requeriments:
    - Keep the summary under 150 words
    - Preserve all the important facts
    - Do not invent information
    - Do not draw conclusions
    - Keep all information factual

    Document:
    {document}
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")
