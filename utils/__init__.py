from pathlib import Path

import pandas as pd


def load_prompt_templates():
    path = Path(__file__).parent.parent / "templates"
    return [f.name for f in path.glob("*.json")]


def load_prompts(template_name):
    if template_name:
        path = Path(__file__).parent.parent / "templates" / template_name
        return pd.read_json(path).drop_duplicates(subset='act').set_index('act')  # act, prompt
