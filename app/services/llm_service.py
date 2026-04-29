import json
import google.generativeai as genai
from app.core.config import settings

# Configure the SDK globally
genai.configure(api_key=settings.LLM_API_KEY)

class ResumeLLMService:
    def __init__(self):
        # Gemini 1.5 Flash is the ideal model here: fast, cheap, and highly capable of formatting
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_experience_bullets(self, target_role: str, raw_input: str) -> list[str]:
        """
        Takes a user's raw brain-dump and returns exactly 3 ATS-friendly bullet points.
        """
        prompt = (
            "You are an expert executive resume writer. "
            f"The user is applying for a '{target_role}' role. "
            "Transform their raw input into exactly 3 professional, impactful resume bullet points. "
            "Start each bullet with a strong action verb and include metrics where implied. "
            f"Raw input: {raw_input}"
        )

        try:
            # We enforce a strict JSON schema so the AI CANNOT return conversational text
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=list[str], # Strictly enforces an array of strings
                    temperature=0.7 # Gives a good balance of creativity and professionalism
                ),
            )

            # Gemini returns a JSON string like '["bullet 1", "bullet 2"]', so we parse it into a Python list
            bullets = json.loads(response.text)
            
            # Ensure we only return 3 just in case the LLM gets overzealous
            return bullets[:3] 

        except Exception as e:
            print(f"--- Gemini API Error: {e} ---")
            # Safe fallback so our app doesn't crash if the API times out
            return ["Failed to generate content. Please try again."]

# Create a singleton instance to use across our API routes
llm_service = ResumeLLMService()