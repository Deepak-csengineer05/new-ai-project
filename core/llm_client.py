import os
import time
import random
import json
import google.generativeai as genai
from typing import Any, Dict, List, Optional

class LLMClient:
    """
    Wrapper for Google Gemini API to handle text generation and structured JSON output.
    """
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API Key is required")
        
        genai.configure(api_key=api_key)
        
        # Dynamic Model Discovery - Prioritize Stable Models
        try:
            self.model = None
            all_models = [m for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Priority list: Flash > Pro > Stable > Experimental
            # We look for these substrings in order
            priorities = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro']
            
            for p in priorities:
                for m in all_models:
                    if p in m.name and 'exp' not in m.name: # Avoid experimental if possible
                        self.model = genai.GenerativeModel(m.name)
                        print(f"Selected stable model: {m.name}")
                        break
                if self.model: break
            
            # Fallback to any available model if no priority match
            if not self.model and all_models:
                self.model = genai.GenerativeModel(all_models[0].name)
                print(f"Fallback model: {all_models[0].name}")
                        
            if not self.model:
                raise ValueError("No suitable Gemini model found for this API key.")
                
        except Exception as e:
            print(f"Model discovery failed: {e}. Defaulting to gemini-1.5-flash")
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _retry_on_error(self, func, *args, **kwargs):
        """
        Retries a function call with exponential backoff on 429 errors.
        """
        max_retries = 3
        base_delay = 2
        
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        print(f"Rate limit hit. Retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                raise e

    def generate_text(self, prompt: str) -> str:
        """
        Generates free-form text response.
        """
        try:
            response = self._retry_on_error(self.model.generate_content, prompt)
            return response.text
        except Exception as e:
            print(f"Error generating text: {e}")
            return f"Error: {str(e)}"

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """
        Generates a response and attempts to parse it as JSON.
        Includes a system instruction to force JSON format.
        """
        json_prompt = f"""
        {prompt}
        
        IMPORTANT: Output ONLY valid JSON. Do not include markdown formatting like ```json ... ```. 
        Just the raw JSON string.
        """
        
        try:
            response = self._retry_on_error(self.model.generate_content, json_prompt)
            text = response.text.strip()
            
            # Clean up potential markdown code blocks
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
                
            return json.loads(text.strip())
        except json.JSONDecodeError:
            print(f"Failed to decode JSON. Raw output: {text}")
            return {"error": "Failed to parse JSON", "raw": text}
        except Exception as e:
            print(f"Error generating JSON: {e}")
            return {"error": str(e)}
