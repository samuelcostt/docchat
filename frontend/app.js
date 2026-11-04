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
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ document: documentText, question }),
    });
    const data = await response.json();

    if (!response.ok) {
      const message = typeof data.detail === "string" ? data.detail : "Algo deu errado.";
      showAnswer(message, true);
      return;
    }

    showAnswer(data.answer);
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