async function analyzeText() {

    const textInput = document.getElementById("textInput");
    const text = textInput.value.trim();

    if (!text) {
        alert("Please enter some text first.");
        return;
    }

    const button = document.querySelector(".primary-btn");

    button.disabled = true;
    button.textContent = "Analyzing...";

    try {

        const response = await fetch("/api/analyze-text", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                text: text
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || "Analysis failed.");
        }

        displayTextResults(result);

    } catch (error) {

        alert(error.message);

    } finally {

        button.disabled = false;
        button.textContent = "Analyze Text";
    }
}


function displayTextResults(result) {

    let resultBox = document.getElementById("textResults");

    if (!resultBox) {

        resultBox = document.createElement("div");

        resultBox.id = "textResults";
        resultBox.className = "result-box";

        document
            .querySelector(".analysis-card")
            .appendChild(resultBox);
    }

    resultBox.innerHTML = `
        <div class="result-header">
            <h3>Analysis Results</h3>
            <span class="score">
                ${result.communication_score}/100
            </span>
        </div>

        <div class="result-grid">

            <div class="result-item">
                <span>Sentiment</span>
                <strong>${result.sentiment}</strong>
            </div>

            <div class="result-item">
                <span>Confidence</span>
                <strong>${result.confidence}%</strong>
            </div>

            <div class="result-item">
                <span>Words</span>
                <strong>${result.word_count}</strong>
            </div>

            <div class="result-item">
                <span>Sentences</span>
                <strong>${result.sentence_count}</strong>
            </div>

        </div>

        <div class="keywords">
            <span>Keywords</span>

            <div class="keyword-list">
                ${
                    result.keywords.length
                    ? result.keywords.map(
                        keyword => `<span>${keyword}</span>`
                      ).join("")
                    : "<small>No keywords detected</small>"
                }
            </div>
        </div>
    `;
}


function analyzeSpeech() {

    const audio = document.getElementById("audioInput").files[0];

    if (!audio) {
        alert("Please upload an audio file first.");
        return;
    }

    alert("Speech analysis engine is coming next.");
}