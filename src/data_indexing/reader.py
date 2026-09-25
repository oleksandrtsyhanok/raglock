from pathlib import Path

class Reader:
    def __init__(self, path: str):
        self.path = Path(path)
        self.data = []

    def read_files(self):
        for p in self.path.rglob('*.md'):
            with open(p, 'r', encoding='utf-8') as f:
                self.data.append({'text': f.read(), 'source': str(p)})
        return self.data