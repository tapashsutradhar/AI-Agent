from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from qa_engine import QAEngine
from forecast_engine import ForecastEngine
import os


app = FastAPI(title="AI Agent — QA + Forecast")


# initialize engines (singleton)
qa = QAEngine(api_key=os.getenv("OPENAI_API_KEY"))
forecast = ForecastEngine()


class ChatRequest(BaseModel):
conversation: List[Dict] # list of messages {"role":"user"/"assistant","text":...}
message: str


class ForecastRequest(BaseModel):
series: List[Dict] # list of {"ds":"YYYY-MM-DD","y":number}
horizon: int = 14


@app.post("/chat")
async def chat(req: ChatRequest):
try:
reply = qa.handle_message(req.conversation, req.message)
return {"reply": reply}
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))


@app.post("/forecast")
async def forecast_route(req: ForecastRequest):
try:
preds = forecast.predict(req.series, horizon=req.horizon)
return {"forecast": preds}
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8000)