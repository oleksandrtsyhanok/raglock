import os
import uuid
import yaml
import math
from openai import OpenAI
from dotenv import load_dotenv

class DataHandler:
    def __init__(self, chunk_size=1000, overlap=100):
        self.chunk_size = chunk_size
        self.separators = ["\n---", "\n# ", "\n## ", "\n### ", "\n\n", "\n- ", "\n"]
        self.overlap = overlap

        load_dotenv()
        self.client = OpenAI(
            base_url='https://integrate.api.nvidia.com/v1',
            api_key=os.getenv("API_KEY")
        )
        self.model = 'nvidia/nemotron-3-embed-1b'

    def chunk_data(self, data):
        chunked_data = []
        for item in data:
            text: str = item['text']
            source = item['source']
            parsed_yaml = {}
            if text.startswith('---'):
                parts = text.split("---", 2)
                string_yaml = parts[1]
                parsed_yaml = yaml.safe_load(string_yaml)
                text = parts[2]
            
            raw_chunks = self.splitter(text, self.separators)
            chunks = self.overlap_merger(raw_chunks)
            for chunk in chunks:
                if chunk:
                    chunked_data.append({
                        'text': chunk.strip(),
                        'source': source,
                        'tags': parsed_yaml.get('tags', 'none'),
                        'status': parsed_yaml.get('status', 'none')
                    })
        return chunked_data

    def create_embeddings(self, data: list):
        ids = []
        vectors = []
        payloads = []
        texts_to_embed = [item['text'] for item in data]
        window_index = 0
        batch_size = 256
        for i in range(math.ceil(len(texts_to_embed) / batch_size)):
            batch = texts_to_embed[window_index:window_index+batch_size]
            batch_data = data[window_index:window_index+batch_size]
            window_index+=batch_size

            chunk_response = self.client.embeddings.create(
                input=batch,
                model=self.model,
                extra_body={'input_type': 'passage'}
            )

            for j, item in enumerate(batch_data):
                vector = chunk_response.data[j].embedding
                vectors.append(vector)
                
                ids.append(str(uuid.uuid4()))
                payloads.append(item)

        return ids, vectors, payloads

    def create_query_embedding(self, text_query):
        query_embedding = self.client.embeddings.create(
            input=text_query,
            model=self.model,
            extra_body={'input_type': 'query'}
        )
        vector_query = query_embedding.data[0].embedding
        return vector_query

    def splitter(self, text: str, current_separ: list):
        if len(text) < self.chunk_size or len(current_separ) == 0:
            return [text]
        
        final = []

        sep = current_separ[0]
        chunks = text.split(sep)
        for chunk in chunks:
            smaller = self.splitter(chunk, current_separ[1:])
            final.extend(smaller)
        return final

    def overlap_merger(self, pieces):
        current_chunk = ''
        final_list = []
        for piece in pieces:
            if len(current_chunk) + len(piece) > self.chunk_size:
                final_list.append(current_chunk)
                current_chunk = current_chunk[-self.overlap:] + piece
            else:
                current_chunk += piece

        if current_chunk:
            final_list.append(current_chunk)
        
        return final_list