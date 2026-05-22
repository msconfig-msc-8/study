const queryInput = document.getElementById("queryInput");
const sendButton = document.getElementById("sendButton");

const queryType = document.getElementById("queryType");
const classificationSource = document.getElementById("classificationSource");
const llmError = document.getElementById("llmError");
const scenario = document.getElementById("scenario");
const answer = document.getElementById("answer");
const rawResponse = document.getElementById("rawResponse");

sendButton.addEventListener("click", async () => {
    const query = queryInput.value;

    sendButton.disabled = true;
    sendButton.textContent = "Обработка...";

    queryType.textContent = "—";
    classificationSource.textContent = "—";
    llmError.textContent = "—";
    scenario.textContent = "—";
    answer.textContent = "Ожидание ответа...";
    rawResponse.textContent = "";

    try {
        const response = await fetch("/api/query", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
        });

        const data = await response.json();

        if (!response.ok) {
            answer.textContent = data.detail || "Ошибка обработки запроса";
            rawResponse.textContent = JSON.stringify(data, null, 2);
            return;
        }

        queryType.textContent = data.type || "—";
        classificationSource.textContent = data.classification_source || "—";
        llmError.textContent = data.llm_error || "—";
        scenario.textContent = data.scenario || "—";
        answer.textContent = data.answer || "—";

        rawResponse.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        answer.textContent = "Не удалось отправить запрос на сервер.";
        rawResponse.textContent = String(error);
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Отправить запрос";
    }
});