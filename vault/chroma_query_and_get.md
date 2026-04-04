# Chroma Docs
4–5 minutes

You can query a Chroma collection to run a similarity search using the .query method:

Python
```
collection.query(
    query_texts=["thus spake zarathustra", "the oracle speaks"]
)
```
Chroma will use the collection's embedding function to embed your text queries, and use the output to run a vector similarity search against your collection.

Instead of provided query_texts, you can provide query embeddings directly. You will be required to do so if you also added embeddings directly to your collection, instead of using its embedding function. If the provided query embeddings are not of the same dimensions as those in your collection, an exception will be raised.

Python
```
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...]
)
```
By default, Chroma will return 10 results per input query. You can modify this number using the n_results argument:

Python
```
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    n_results=5
)
```
The ids argument lets you constrain the search only to records with the IDs from the provided list:

Python
```
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    n_results=5,
    ids=["id1", "id2"]
)
```
You can also retrieve records from a collection by using the .get method. It supports the following arguments:

- ids - get records with IDs from this list. If not provided, the first 100 records will be retrieved, in the order of their addition to the collection.
- limit - the number of records to retrieve. The default value is 100.
- offset - The offset to start returning results from. Useful for paging results with limit. The default value is 0.

Python
```
collection.get(ids=["id1", "ids2", ...])
```
Both query and get have the where argument for metadata filtering and where_document for full-text search and regex:

Python
```
collection.query(
    query_embeddings=[[11.1, 12.1, 13.1],[1.1, 2.3, 3.2], ...],
    n_results=5,
    where={"page": 10}, # query records with metadata field 'page' equal to 10
    where_document={"$contains": "search string"} # query records with the search string in the records' document
)
```
## Results Shape

Chroma returns .query and .get results in columnar form. You will get a results object containing lists of ids, embeddings, documents, and metadatas of the records that matched your .query or get requests. Embeddings are returned as 2D-numpy arrays.

Python
```
class QueryResult(TypedDict):
    ids: List[IDs]
    embeddings: Optional[List[Embeddings]],
    documents: Optional[List[List[Document]]]
    metadatas: Optional[List[List[Metadata]]]
    distances: Optional[List[List[float]]]
    included: Include

class GetResult(TypedDict):
    ids: List[ID]
    embeddings: Optional[Embeddings],
    documents: Optional[List[Document]],
    metadatas: Optional[List[Metadata]]
    included: Include
```
.query results also contain a list of distances. These are the distances of each of the results from your input queries. .query results are also indexed by each of your input queries. For example, results["ids"][0] contains the list of records IDs for the results of the first input query.

Python
```
results = collection.query(query_texts=["first query", "second query"])
```
## Choosing Which Data is Returned

By default, .query and .get always return the documents and metadatas. You can use the include argument to modify what gets returned. ids are always returned:

Python

```
collection.query(query_texts=["my query"]) # 'ids', 'documents', and 'metadatas' are returned

collection.get(include=["documents"]) # Only 'ids' and 'documents' are returned

collection.query(
    query_texts=["my query"],
    include=["documents", "metadatas", "embeddings"]
) # 'ids', 'documents', 'metadatas', and 'embeddings' are returned
```
