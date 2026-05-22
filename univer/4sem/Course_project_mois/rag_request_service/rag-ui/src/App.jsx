import { useState } from "react";
import { sendQuery } from "./api";
import "./App.css";

const examples = [
  {
    label: "Определение",
    text: "What is BERT used for?",
    language: "en",
  },
  {
    label: "Сравнение",
    text: "Compare BERT and GPT",
    language: "en",
  },
  {
    label: "Методы",
    text: "What methods does GPT use?",
    language: "en",
  },
  {
    label: "Русский запрос",
    text: "Для чего используется BERT?",
    language: "ru",
  },
];

function App() {
  const [text, setText] = useState("Compare BERT and GPT");
  const [language, setLanguage] = useState("en");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    const normalizedText = text.trim();

    if (!normalizedText) {
      setError({
        title: "Пустой запрос",
        detail: "Введите текст запроса перед отправкой.",
      });
      setResult(null);
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await sendQuery({
        text: normalizedText,
        language,
      });

      setResult(data);
    } catch (requestError) {
      setError({
        title: requestError.data?.title || "Ошибка backend",
        detail:
          requestError.data?.detail ||
          requestError.message ||
          "Не удалось получить ответ от backend.",
        status: requestError.status,
      });
    } finally {
      setIsLoading(false);
    }
  }

  function applyExample(example) {
    setText(example.text);
    setLanguage(example.language);
    setError(null);
    setResult(null);
  }

  return (
    <main className="page">
      <section className="card">
        <div className="header">
          <div>
            <h1>Справочная RAG-система</h1>
            <p>
              UI для отправки запросов в backend RAG-системы и отображения
              результата из базы знаний.
            </p>
          </div>

          <div className="status-badge">React + FastAPI</div>
        </div>

        <form onSubmit={handleSubmit} className="query-form">
          <label htmlFor="query">Запрос пользователя</label>

          <textarea
            id="query"
            value={text}
            onChange={(event) => setText(event.target.value)}
            placeholder="Например: Compare BERT and GPT"
          />

          <div className="form-row">
            <div className="language-block">
              <label htmlFor="language">Язык</label>
              <select
                id="language"
                value={language}
                onChange={(event) => setLanguage(event.target.value)}
              >
                <option value="en">English</option>
                <option value="ru">Русский</option>
              </select>
            </div>

            <button type="submit" disabled={isLoading}>
              {isLoading ? "Обработка..." : "Отправить"}
            </button>
          </div>
        </form>

        <div className="examples">
          <span>Примеры:</span>
          {examples.map((example) => (
            <button
              key={example.label}
              type="button"
              onClick={() => applyExample(example)}
            >
              {example.label}
            </button>
          ))}
        </div>

        {error && (
          <section className="result error">
            <h2>{error.title}</h2>
            <p>{error.detail}</p>
            {error.status && <span>HTTP status: {error.status}</span>}
          </section>
        )}

        {result && (
          <section className="result">
            <div className="result-header">
              <h2>Результат</h2>
              <span className={result.from_kb ? "kb-yes" : "kb-no"}>
                {result.from_kb ? "Ответ из БЗ" : "Контекста в БЗ не хватило"}
              </span>
            </div>

            <div className="meta-grid">
              <div>
                <strong>Тип запроса</strong>
                <span>{result.query_type || "unknown"}</span>
              </div>

              <div>
                <strong>Сущности</strong>
                <span>
                  {result.source_entities?.length
                    ? result.source_entities.join(", ")
                    : "не найдены"}
                </span>
              </div>
            </div>

            <div className="answer">
              <strong>Ответ</strong>
              <p>{result.answer}</p>
            </div>

            <details>
              <summary>Полный JSON-ответ</summary>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </details>
          </section>
        )}
      </section>
    </main>
  );
}

export default App;