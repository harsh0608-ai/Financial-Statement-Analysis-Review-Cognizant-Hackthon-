from ingestion.indexer import build_index

if __name__ == "__main__":
    print(f"Indexed {build_index(reset=True)} WP-514 chunks")
