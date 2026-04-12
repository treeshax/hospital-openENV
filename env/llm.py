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
        token = os.environ.get("HF_TOKEN", "dummy_token")
        self.client = OpenAI(
            base_url=API_BASE_URL,
            api_key=token,
        )
        self.model = MODEL_NAME

    def chat(self, system_prompt: str, user_prompt: str, json_mode: bool = False) -> str:
        response_format = {"type": "json_object"} if json_mode else None
        
        try:
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
        except Exception as e:
            print(f"[BRAIN ERROR] API failure: {e}")
            if json_mode:
                return json.dumps(self._get_hardcoded_fallback(user_prompt))
            return "Unable to generate medical analysis due to connectivity issues."

    def generate_json(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        content = self.chat(system_prompt, user_prompt, json_mode=True)
        try:
            return json.loads(content)
        except Exception:
            return self._get_hardcoded_fallback(user_prompt)

    def _get_hardcoded_fallback(self, user_prompt: str) -> Dict[str, Any]:
        """Emergency medical heuristics fallback."""
        return {
            "vignette": "Patient presenting with symptoms mentioned in prompt. (LLM Fallback Mode in effect)",
            "symptoms": ["general malaise", "unspecified pain"],
            "age": 45,
            "vitals": {
                "heart_rate": 88,
                "blood_pressure_sys": 125,
                "blood_pressure_dia": 82,
                "temperature_c": 37.0,
                "o2_saturation": 98,
                "respiratory_rate": 16
            },
            "true_seriousness": 3,
            "department": "general",
            "reasoning": "Fallback used due to API credit depletion.",
            "score": 0.5
        }

# Singleton instance
brain = LLMBrain()
