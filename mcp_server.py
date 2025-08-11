from pydantic import Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool (
    name = "read_doc_content",
    description= " Read the content of a document and return it as a string"
)

def read_document (
    doc_id: str = Field(description = "Id of the document to read")
):
    if doc_id not in docs :
        raise ValueError(f"Doc with id {doc_id} not found")
    
    return docs[doc_id]
# TODO: Write a tool to edit a doc
@mcp.tool(
    name= "edit_document",
    description="Edit a document by replacing a string in the documents content wth a new string"
)
def edit_document(
    doc_id:str = Field(description="Id of the document that will be edited"),
    old_str:str = Field(description="The text to replace. Must match exactly, including the whitespaces"),
    new_str:str = Field(description="The new text to innsert in place of the old text")
):
    if doc_id not in docs :
        raise ValueError(f"Doc with id {doc_id} not found")
    docs[doc_id] = docs[doc_id].replace(old_str, new_str)
    

# TODO: Write a resource to return all doc id's
mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs() -> list[str]:
    return list(docs.keys())


# TODO: Write a resource to return the contents of a particular doc
mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plane"
)
def fetch_doc(doc_id:str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")
