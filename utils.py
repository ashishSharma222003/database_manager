
from langchain_core.documents import Document


def prepare_documents_for_vector_db(annotations, summarized_schema):
    documents = []
    for table, ann in annotations.items():
        schema_info = summarized_schema.get(table, {})
        # Build document text
        doc_text = f"Table: {table}\nDescription: {ann['table_description']}\n"
        doc_text += "Columns:\n"
        for col in schema_info.get("columns", []):
            col_name = col["name"]
            col_type = col["type"]
            col_desc = ann["columns"].get(col_name, "")
            doc_text += f"  - {col_name} ({col_type}): {col_desc}\n"
        if schema_info.get("relationships"):
            doc_text += "Relationships:\n"
            for rel in schema_info["relationships"]:
                doc_text += f"  - {rel}\n"
        # Metadata for vector DB
        metadata = {
            "table_name": table,
            "table_description": ann["table_description"],
            "columns": schema_info.get("columns", []),
            "relationships": schema_info.get("relationships", [])
        }
        documents.append({"content": doc_text, "metadata": metadata})
    return documents



def prepare_documents_for_vector_db(annotations, summarized_schema):
    documents = []
    for table, ann in annotations.items():
        schema_info = summarized_schema.get(table, {})
        # Build document text
        doc_text = f"Table: {table}\nDescription: {ann['table_description']}\n"
        doc_text += "Columns:\n"
        enriched_columns = []
        for col in schema_info.get("columns", []):
            col_name = col["name"]
            col_type = col["type"]
            col_desc = ann["columns"].get(col_name, "")
            doc_text += f"  - {col_name} ({col_type}): {col_desc}\n"
            enriched_columns.append({
                "name": col_name,
                "type": col_type,
                "description": col_desc
            })
        if schema_info.get("relationships"):
            doc_text += "Relationships:\n"
            for rel in schema_info["relationships"]:
                doc_text += f"  - {rel}\n"
        # Metadata for vector DB
        metadata = {
            "table_name": table,
            "table_description": ann["table_description"],
            "columns": enriched_columns,
            "relationships": schema_info.get("relationships", [])
        }
        documents.append(
            Document(
                page_content=doc_text,
                metadata=metadata
            )
        )
        # documents.append({"content": doc_text, "metadata": metadata})
    return documents

# Usage:
# docs = prepare_documents_for_vector_db(st.session_state["annotations"], summarized)
# Now you can upload docs to your vector DB