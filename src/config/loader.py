from src.config.settings import Settings
from pydantic import ValidationError
from pathlib import Path

CFGPATH = Path('src/config/cfg.json')

def get_config() -> Settings:
    with open(CFGPATH, 'r', encoding='utf-8') as f:
        try:
            return Settings.model_validate_json(f.read())
        except ValidationError as e:
            raise e