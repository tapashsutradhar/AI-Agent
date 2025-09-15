# AI Agent: QA + Forecast

An interactive AI agent that can:

* **Answer your questions** (via OpenAI API or local fallback)
* **Ask follow-up questions** for clarification
* **Forecast future values** from uploaded CSV time series

This project includes a **FastAPI backend** for AI + ML logic and a **React frontend** for the chat/forecast UI.

---

## 🚀 Features

* **Chat Agent**: Conversational interface powered by OpenAI (if API key provided) or local semantic search fallback.
* **Forecasting Engine**: Machine learning forecasts using scikit-learn RandomForest with fallback naive predictor for short data.
* **Frontend UI**: Chat window, CSV upload for forecasting, forecast table output.
* **Docker-ready**: Simple Dockerfile for backend.

---

## 📂 Project Structure

```
ai-agent-forecast/
├─ backend/
│  ├─ app/
│  │  ├─ main.py            # FastAPI entrypoint
│  │  ├─ qa_engine.py       # QA / Chat logic
│  │  ├─ forecast_engine.py # Forecast logic
│  │  ├─ utils.py
│  │  └─ __init__.py
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ src/
│  │  ├─ App.jsx            # Chat + Forecast UI
│  │  ├─ api.js             # API calls
│  │  └─ index.jsx
│  ├─ package.json
│  └─ vite.config.js
├─ demo_data/
│  └─ sample_timeseries.csv
├─ README.md
└─ .gitignore
```

---

## 🔧 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ai-agent-forecast.git
cd ai-agent-forecast
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt

# Run FastAPI
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend setup

```bash
cd ../frontend
npm install
npm run dev
```

The frontend runs on [http://localhost:3000](http://localhost:3000).

### 4. Environment Variables

* To use OpenAI answers, set your API key in the environment:

```bash
export OPENAI_API_KEY=sk-...
export OPENAI_MODEL=gpt-4o-mini   # or another available model
```

If not set, the app falls back to local semantic search.

---

## 📊 Usage

* Open the frontend in your browser.
* Type questions in the chat box.
* Upload a CSV file with columns:

  * `ds`: date in `YYYY-MM-DD`
  * `y`: numeric value
* View the forecast results in the table.

Example file: [`demo_data/sample_timeseries.csv`](./demo_data/sample_timeseries.csv)

---

## 🐳 Docker (Backend)

```bash
cd backend
docker build -t ai-agent-backend .
docker run -p 8000:8000 ai-agent-backend
```

---

## 🌱 Roadmap

* Add charts for forecast visualization
* Expand KB for local Q\&A
* Improve forecasting models (Prophet, ARIMA, LSTMs)
* Deploy on cloud (Render/Heroku/Vercel)
