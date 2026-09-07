const fileInput = document.getElementById("pdfFile");
const fileNameLabel = document.getElementById("fileName");

fileInput.addEventListener("change", () => {
    fileNameLabel.textContent = fileInput.files.length
        ? fileInput.files[0].name
        : "Choose a PDF";
});

async function uploadPDF() {
    const status = document.getElementById("uploadStatus");

    if (!fileInput.files.length) {
        status.textContent = "Please select a PDF first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    status.textContent = "Uploading and indexing…";

    try {
        const response = await fetch("/upload", { method: "POST", body: formData });
        const data = await response.json();
        status.textContent = `${data.filename} indexed — ${data.chunks_created} chunks ready.`;
        loadPapers();
    } catch (err) {
        status.textContent = "Upload failed. Please try again.";
    }
}

async function sendQuestion() {
    const input = document.getElementById("questionInput");
    const emptyState = document.getElementById("emptyState");
    const question = input.value.trim();

    if (!question) return;

    if (emptyState) emptyState.remove();

    addMessage(escapeHtml(question), "user-message");
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question, paper: selectedPaper})
        });
        const data = await response.json();

        const sourcesHtml = data.sources
            .map(s => `Page ${s.page}: ${escapeHtml(s.content_preview)}…`)
            .join("<br>");

        addMessage(
            `<span class="provider-tag">${data.provider}</span><div>${escapeHtml(data.answer)}</div>
             <div class="sources">Sources<br>${sourcesHtml}</div>`,
            "bot-message"
        );
    } catch (err) {
        addMessage("Something went wrong. Please try again.", "bot-message");
    }
}

function addMessage(html, className) {
    const chatBox = document.getElementById("chatBox");
    const div = document.createElement("div");
    div.className = `message ${className}`;
    div.innerHTML = html;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

document.getElementById("questionInput").addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendQuestion();
});

let selectedPaper = null;

async function loadPapers() {
    const response = await fetch("/papers");
    const data = await response.json();
    renderPapers(data.papers);
}

function renderPapers(papers) {
    const list = document.getElementById("papersList");
    list.innerHTML = "";

    // "All papers" chip
    const allChip = document.createElement("div");
    allChip.className = "paper-chip" + (selectedPaper === null ? " active" : "");
    allChip.textContent = "All papers";
    allChip.onclick = () => { selectedPaper = null; renderPapers(papers); };
    list.appendChild(allChip);

    papers.forEach(path => {
        const filename = path.split(/[/\\]/).pop(); // display filename only
        const chip = document.createElement("div");
        chip.className = "paper-chip" + (selectedPaper === path ? " active" : "");
        chip.textContent = filename;
        chip.onclick = () => { selectedPaper = path; renderPapers(papers); };
        list.appendChild(chip);
    });
}

// call this once on page load
loadPapers();