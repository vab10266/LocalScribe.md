import lancedb
import pyarrow as pa
from pathlib import Path
from config import VAULT_PATH, client

# Connect to local database (creates directory if needed)
db = lancedb.connect("./campaign_vault")


# --- EMBEDDING HELPER ---
def embed(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-nomic-embed-text-v1.5",
        input=text
    )
    return response.data[0].embedding

# --- SCHEMA ---

schema = pa.schema([
    pa.field("id",       pa.string()),
    pa.field("text",     pa.string()),
    pa.field("file",     pa.string()),
    pa.field("tags",     pa.list_(pa.string())),
    pa.field("note_type",   pa.string()),   # rules | setting | campaign | general_tips
    pa.field("vector",   pa.list_(pa.float32(), 768)),  # nomic-embed-text dim
])

table = db.create_table("notes", schema=schema, exist_ok=True)
table.create_fts_index("text", replace=True)

# --- INGESTION ---
def ingest_note(file_path: str, text: str, tags: list[str], note_type: str):
    chunk_id = Path(file_path).stem
    table.add([{
        "id":     chunk_id,
        "text":   text,
        "file":   file_path,
        "tags":   tags,
        "note_type": note_type,
        "vector": embed(text),
    }])





# --- SEARCH MODES ---

# 1. Pure semantic search
def semantic_search(query: str, chunk_limit: int = 5):
    return (
        table.search(embed(query), vector_column_name="vector")
             .limit(chunk_limit)
             .to_list()
    )


# 2. Full-text keyword search (BM25)
def keyword_search(query: str, chunk_limit: int = 5):
    return (
        table.search(query, query_type="fts")
             .limit(chunk_limit)
             .to_list()
    )


# 3. Hybrid search — semantic + BM25 combined
def hybrid_search(query: str, chunk_limit: int = 5):
    return (
        table.search(query, query_type="hybrid")
             .limit(chunk_limit)
             .to_list()
    )


# 4. Hybrid + metadata filter (your core search agent tool)
def search_notes(query: str, note_type: str = None, tags: list[str] = None, chunk_limit: int = 5):
    search = table.search(query, query_type="hybrid").limit(chunk_limit)

    conditions = []
    if note_type:
        conditions.append(f"note_type = '{note_type}'")
    if tags:
        for tag in tags:
            conditions.append(f"array_has(tags, '{tag}')")

    if conditions:
        search = search.where(" AND ".join(conditions))

    return search

