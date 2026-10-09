from vector_db import QdrantStorage
from data_indexing.data_handler import DataHandler
from pathlib import Path

def list_files(path: str):
    try:
        path: Path = Path(path)
        return '\n'.join(p.name for p in path.iterdir())
    except FileNotFoundError as e:
        return str(e)

def read_file(path: str) -> str:
    path: Path = Path(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            if not path.is_file():
                return f'{path} is not a file'
            return f.read()
    except FileNotFoundError as e:
        return str(e)

def write_file(path: str, content: str) -> str:
    path: Path = Path(path)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
        return f'wrote {path}'

def get_file_context(query: str, db_qdrant: QdrantStorage, data_handler: DataHandler) -> list[dict]:
    query_vector = data_handler.create_query_embedding(query)
    context = db_qdrant.search(query_vector)
    result = [{'file context': c['contexts'], 'source': c['sources']} for c in context]
    return result


if __name__ == "__main__":
    print(list_files('/Obsidian Vault'))
    print(read_file('/Obsidian Vault/AP.md'))