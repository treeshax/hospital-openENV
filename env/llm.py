import os
import json
from openai import OpenAI
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
API_BASE_URL = "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.1-70B-Instruct") # Default high-power model

class LLMBrain:
    def __init__(self):
        self.client = OpenAI(
            base_url=API_BASE_URL,
            api_key=os.environ["HF_TOKEN"],
        )
        self.model = MODEL_NAME

    def chat(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        response_format = {"type": "json_object"} if json_mode else None
        
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=response_format,
            temperature=0.7 if not json_mode else 0.2
        )
        return completion.choices[0].message.content

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        content = self.chat(system_prompt, user_prompt, json_mode=True)
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print(f"Failed to decode JSON from LLM: {content}")
            return {}

# Singleton instance
brain = LLMBrain()
