from md_indexing.hybrid_search import search_notes, ingest_note

# Example ingestion
ingest_note(
    file_path="npcs/valdris.md",
    text="Valdris is the aging king of Thornmere, secretly dying of a curse placed by his advisor Serath.",
    tags=["npc", "royalty", "thornmere"],
    note_type="npc"
)

ingest_note(
    file_path="locations/ironhaven.md",
    text="Ironhaven is a port city controlled by the Merchant's Compact, known for its black market.",
    tags=["location", "city", "faction"],
    note_type="location"
)


# --- USAGE EXAMPLE ---
results = search_notes(
    query="enemies of the throne who might betray the king",
    note_type="npc",
    tags=["royalty"]
)
print(f"Search Results: {results}")
print(f"Search Results: {results.to_list()}")
# for r in results:
#     print(f"[{r['file']}] {r['text'][:80]}...")