# backend/app/qa_engine.py
import os
from typing import List, Dict

class QAEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if self.api_key:
            try:
                import openai
                openai.api_key = api_key
                self.client = openai
            except Exception as e:
                print("OpenAI package not available or API key invalid:", e)
                self.client = None
        else:
            self.client = None

        # Local fallback resources
        try:
            from sentence_transformers import SentenceTransformer, util
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            # small example KB
            self.kb = [
                "This agent can forecast time series and answer questions.",
                "Upload a CSV of date,value to use forecasting.",
                "For forecasting we recommend using scikit-learn or statsmodels.",
                "You can set horizon (days) when asking for predictions."
            ]
            self.kb_emb = self.embedder.encode(self.kb, convert_to_tensor=True)
            self.util = util
        except Exception:
            self.embedder = None
            self.kb = []
            self.kb_emb = None
            self.util = None

    def handle_message(self, conversation: List[Dict], message: str) -> Dict:
        """
        Returns a dict: {"text": str, "ask_followup": bool}
        """
        text = (message or "").lower()
        # If user asks for forecast but didn't provide data, ask for data/upload
        if any(k in text for k in ["forecast", "predict", "prediction", "forecasting"]):
            # The conversation may include attachments in a real app; here we ask for CSV upload
            return {
                "text": "I can run forecasts. Please upload a CSV with columns `ds` (YYYY-MM-DD) and `y` (value), or POST data to /forecast. What horizon (days) do you want — e.g., 7 or 30?",
                "ask_followup": True
            }

        # If OpenAI client available, call it to generate an answer and optionally a follow-up question
        if self.client:
            try:
                messages = [{"role": "system", "content": "You are a helpful assistant that may ask one clarifying question when appropriate."}]
                if conversation:
                    for m in conversation:
                        role = m.get('role', 'user')
                        content = m.get('text') or m.get('content') or ''
                        messages.append({"role": role, "content": content})
                messages.append({"role": "user", "content": message})

                # Prefer ChatCompletion if available
                if hasattr(self.client, 'ChatCompletion'):
                    resp = self.client.ChatCompletion.create(
                        model=os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
                        messages=messages,
                        max_tokens=400,
                    )
                    out = resp.choices[0].message.content
                else:
                    resp = self.client.Completion.create(
                        model=os.getenv('OPENAI_MODEL', 'text-davinci-003'),
                        prompt=message,
                        max_tokens=400,
                    )
                    out = resp.choices[0].text

                return {"text": out.strip(), "ask_followup": False}
            except Exception as e:
                # Fall through to local fallback
                print("OpenAI call failed, falling back to local QA:", e)

        # Local semantic-search fallback
        if self.embedder and self.kb_emb is not None and self.util:
            q_emb = self.embedder.encode(message, convert_to_tensor=True)
            hits = self.util.semantic_search(q_emb, self.kb_emb, top_k=2)[0]
            snippets = [self.kb[h['corpus_id']] for h in hits]
            answer = "\n".join(snippets)
            followup = "Would you like me to run a forecast on your data?" if any(w in text for w in ["data", "forecast", "predict"]) else ""
            return {"text": answer + ("\n" + followup if followup else ""), "ask_followup": bool(followup)}

        # Last-resort message
        return {"text": "Sorry — I don't have enough resources to answer that right now. Try providing a CSV for forecasting or set OPENAI_API_KEY for better answers.", "ask_followup": False}
