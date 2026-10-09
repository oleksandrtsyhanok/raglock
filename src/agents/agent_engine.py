from config.settings import Settings
from config.loader import get_config
from agents.tools.edit_tools import list_files, read_file, write_file

import os
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

TOOLS = {'list_files': list_files, 'read_file': read_file, 'write_file': write_file}

class Agent:
    def __init__(self, max_loop_iter = 10):
        self.backup_text: str = ''
        self.max_loop_iter = max_loop_iter

        cfg: Settings = get_config()

        load_dotenv()
        self.client = AsyncOpenAI(
            base_url=cfg.api_base_url,
            api_key=os.getenv("API_KEY")
        )
        self.model = cfg.llm_model
        self.workspace_root = cfg.workspace
        self.promt: list[dict] = cfg.promt_agent
        self.tool_schemas = cfg.tool_schemas

        self.messages = self.promt

    async def agent_loop(self, user_request: str) -> str:
        # print(f'{self.messages[:50]} \n\n')
        if len(self.messages) == 2:
            for msg in self.messages:
                msg['content'] = (
                    msg['content'].replace('user_request', user_request)
                    .replace('workspace', self.workspace_root)
                )
        else:
            self.messages.append(
                {
                    "role": "user",
                    "content": user_request
                }
            )
        current_iter = 0

        

        while current_iter <= self.max_loop_iter:
            current_iter += 1
            message = await self.llm_call()
            self.messages.append(message.model_dump())

            if not message.tool_calls:
                return message.content or ''

            self.messages.append(message.model_dump())

            for call in message.tool_calls:
                print('GIGIGIGIG')
                args = json.loads(call.function.arguments or '{}')
                if 'path' in args:
                    full_path = (f'{self.workspace_root}/{args['path']}')
                    args['path'] = full_path
                print(f'{call.function.name}({args})')
                result = TOOLS[call.function.name](**args)
                # print(result)
                self.messages.append(
                    {'role': 'tool', 'tool_call_id': call.id, 'content': result}
                )


    async def llm_call(self):
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tool_schemas
        )
        msg = response.choices[0].message
        return msg