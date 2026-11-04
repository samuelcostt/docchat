const docInput = document.getElementById("document");
const questionInput = document.getElementById("question");
const askBtn = document.getElementById("ask-btn");
const answerBox = document.getElementById("answer");

function showAnswer(text, isError = false) {
  answerBox.hidden = false;
  answerBox.textContent = text;
  answerBox.classList.toggle("error", isError);
}

async function ask() {
  const documentText = docInput.value.trim();
  const question = questionInput.value.trim();

  if (!documentText || !question) {
    showAnswer("Preencha o documento e a pergunta.", true);
    return;
  }

  askBtn.disabled = true;
  askBtn.textContent = "Pensando...";

  try {
    const response = await fetch("/ask/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ document: documentText, question }),
    });

    if (!response.ok) {
      const data = await response.json();
      const message = typeof data.detail === "string" ? data.detail : "Algo deu errado.";
      showAnswer(message, true);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let text = "";
    showAnswer("...");

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      text += decoder.decode(value, { stream: true });
      showAnswer(text);
    }
  } catch (error) {
    showAnswer("Não consegui falar com o servidor.", true);
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = "Perguntar";
  }
}

askBtn.addEventListener("click", ask);
questionInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") ask();
});