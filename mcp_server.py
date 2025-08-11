from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts.base import UserMessage

mcp = FastMCP("DocumentMCP", log_level="ERROR")

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# Tool to read a document
@mcp.tool(
    name="read_doc_content",
    description="Read the content of a document and return it as a string"
)
def read_document(
    doc_id: str = Field(description="Id of the document to read")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]

# Tool to edit a document
@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the document's content with a new string"
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The text to replace. Must match exactly, including whitespaces"),
    new_str: str = Field(description="The new text to insert in place of the old text")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)

# Resource to list all document IDs
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())

# Resource to fetch the content of a particular document
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
    description="Rewrite the contents of the document in markdown format."
)
def format_document(
    doc_id: str = Field(description="Id of the document to format")
) -> list[UserMessage]:
    prompt = f"""Your goal is to refactor the document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc. as necessary. Use the 'edit_document' tool to edit the document.
"""
    return [UserMessage(prompt)]

# Prompt to summarize a document
@mcp.prompt(
    name="summarize",
    description="Summarize the contents of a document in a concise way."
)
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize")
) -> list[UserMessage]:
    prompt = f"""Your goal is to summarize the document in a concise and clear way.

The id of the document you need to summarize is:
<document_id>
{doc_id}
</document_id>

Focus only on the most important points. Use the 'read_doc_content' tool if needed.
"""
    return [UserMessage(prompt)]

if __name__ == "__main__":
    mcp.run(transport="stdio")
