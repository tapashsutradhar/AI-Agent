export async function chat(message, conversation) {
  const res = await fetch("http://localhost:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, conversation }),
  });
  if (!res.ok) {
    throw new Error("Chat request failed");
  }
  return await res.json();
}

export async function forecast(series, horizon = 14) {
  const res = await fetch("http://localhost:8000/forecast", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ series, horizon }),
  });
  if (!res.ok) {
    throw new Error("Forecast request failed");
  }
  return await res.json();
}
