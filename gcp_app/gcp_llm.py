from google.cloud import aiplatform
from typing import List, Dict, Any
from .config import Config

class GCPLLM:
    def __init__(self):
        aiplatform.init(project=Config.PROJECT_ID, location=Config.REGION)
        
    def generate_answer(self, context: str, query: str) -> str:
        """Generate answer using Vertex AI PaLM or Gemini"""
        
        prompt = f"""You are a helpful legal assistant. Use the following context from the Civil Procedure Rules and Practice Directions to answer the user's question. Always cite the source filename in your answer.

Context:
{context}

Question: {query}

Answer:"""

        if Config.LLM_MODEL == "text-bison@001":
            # Use PaLM
            model = aiplatform.TextGenerationModel.from_pretrained(Config.LLM_MODEL)
            response = model.predict(
                prompt,
                max_output_tokens=1024,
                temperature=0.1
            )
            return response.text
            
        elif Config.LLM_MODEL == "gemini-pro":
            # Use Gemini
            model = aiplatform.GenerativeModel(Config.LLM_MODEL)
            response = model.generate_content(prompt)
            return response.text
            
        else:
            raise ValueError(f"Unsupported model: {Config.LLM_MODEL}")
    
    def generate_checklist(self, context: str, query: str) -> List[Dict[str, str]]:
        """Generate a structured checklist from the legal process"""
        
        prompt = f"""Based on the following legal context, create a step-by-step checklist for the user's question. Return the answer as a JSON array of objects with 'step' and 'description' fields.

Context:
{context}

Question: {query}

Return only valid JSON like this:
[
  {{"step": "1", "description": "First step description"}},
  {{"step": "2", "description": "Second step description"}}
]"""

        if Config.LLM_MODEL == "text-bison@001":
            model = aiplatform.TextGenerationModel.from_pretrained(Config.LLM_MODEL)
            response = model.predict(
                prompt,
                max_output_tokens=1024,
                temperature=0.1
            )
            # Parse JSON response
            import json
            try:
                return json.loads(response.text)
            except:
                return [{"step": "1", "description": "Error parsing checklist"}]
                
        elif Config.LLM_MODEL == "gemini-pro":
            model = aiplatform.GenerativeModel(Config.LLM_MODEL)
            response = model.generate_content(prompt)
            import json
            try:
                return json.loads(response.text)
            except:
                return [{"step": "1", "description": "Error parsing checklist"}] 