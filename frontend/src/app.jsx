import { useState } from "react";
import { chat, forecast } from "./api";

export default function App() {
  const [conversation, setConversation] = useState([]);
  const [input, setInput] = useState("");
  const [forecastData, setForecastData] = useState(null);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const newConv = [...conversation, { role: "user", text: input }];
    setConversation(newConv);
    setInput("");

    try {
      const res = await chat(input, newConv);
      const reply = res.reply || { text: "No reply", ask_followup: false };
      setConversation((prev) => [...prev, { role: "assistant", text: reply.text }]);
    } catch (err) {
      console.error(err);
      setConversation((prev) => [...prev, { role: "assistant", text: "⚠️ Error reaching server" }]);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const text = await file.text();
    const rows = text.trim().split("\n");
    const series = rows.slice(1).map((row) => {
      const [ds, y] = row.split(",");
      return { ds, y: parseFloat(y) };
    });

    try {
      const res = await forecast(series, 14);
      setForecastData(res.forecast);
    } catch (err) {
      console.error(err);
      alert("Forecast failed: " + err.message);
    }
  };

  return (
    <div className="p-4 max-w-2xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">AI Agent: QA + Forecast</h1>

      <div className="border rounded p-3 h-80 overflow-y-auto bg-gray-50 mb-3">
        {conversation.map((m, idx) => (
          <div
            key={idx}
            className={`mb-2 ${
              m.role === "user" ? "text-right" : "text-left text-blue-700"
            }`}
          >
            <span className="inline-block px-2 py-1 rounded bg-white shadow">
              {m.text}
            </span>
          </div>
        ))}
      </div>

      <div className="flex gap-2 mb-4">
        <input
          className="flex-1 border rounded px-2 py-1"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-3 py-1 rounded"
        >
          Send
        </button>
      </div>

      <div className="mb-4">
        <label className="block mb-1 font-medium">Upload CSV for Forecasting</label>
        <input type="file" accept=".csv" onChange={handleFileUpload} />
      </div>

      {forecastData && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold mb-2">Forecast Results</h2>
          <table className="border w-full text-sm">
            <thead>
              <tr>
                <th className="border px-2 py-1">Date</th>
                <th className="border px-2 py-1">Prediction</th>
              </tr>
            </thead>
            <tbody>
              {forecastData.map((row, idx) => (
                <tr key={idx}>
                  <td className="border px-2 py-1">{row.ds}</td>
                  <td className="border px-2 py-1">{row.y.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
