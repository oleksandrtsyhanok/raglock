import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

class Generator:
    def __init__(self):
        load_dotenv()
        self.client = AsyncOpenAI(
            base_url='https://integrate.api.nvidia.com/v1',
            api_key=os.getenv("API_KEY")
        )
        self.model = 'nvidia/nemotron-3-super-120b-a12b'

    async def generate_answer(self, query: str, contexts: list[str], sources: list[str]) -> str:
        context = '\n'.join(f'- {item}' for item in contexts)
        prompt = [
            {
                "role": "system",
                "content": (
                    "Answer the user's question using only the provided context. "
                    "If the context doesn't contain enough information, say so.\n\n"
                    f"Context:\n{context}"
                ),
            },
            {"role": "user", "content": query},
        ]

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=prompt
        )
        response_text = response.choices[0].message.content
        formatted = self.format_response(response_text, sources)
        return formatted


    def format_response(self, response_text, metadatas):
        formatted = response_text + '\n\n'
        formatted += 'References: \n'
        for meta in metadatas:
            formatted += f' - [{meta}] \n'
        return formatted