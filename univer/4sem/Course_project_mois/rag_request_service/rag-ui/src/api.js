const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function sendQuery({ text, language }) {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      text,
      language,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    const error = new Error(data.detail || data.title || "Ошибка запроса");
    error.status = response.status;
    error.data = data;
    throw error;
  }

  return data;
}