const state = {
  running: false,
  lastReport: "",
};

function qs(selector) {
  const element = document.querySelector(selector);
  if (!element) throw new Error(`Missing element: ${selector}`);
  return element;
}

function setStatus(message, { error = false } = {}) {
  const status = qs("#status");
  status.textContent = message;
  status.classList.toggle("show", Boolean(message));
  status.classList.toggle("error", error);
}

function setRunning(running) {
  state.running = running;
  qs("#run").disabled = running;
  qs("#query").disabled = running;
  qs("#copy").disabled = running || !state.lastReport;
  qs("#download").disabled = running || !state.lastReport;
  qs("#run").textContent = running ? "Working…" : "Generate";
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function inlineFormat(text) {
  let out = escapeHtml(text);
  out = out.replaceAll(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  out = out.replaceAll(/`(.+?)`/g, "<code>$1</code>");
  out = out.replaceAll(/\[(.+?)\]\((https?:\/\/[^\s]+)\)/g, '<a href="$2" target="_blank" rel="noreferrer">$1</a>');
  return out;
}

function renderMarkdownLight(markdown) {
  const lines = markdown.split(/\r?\n/);
  const html = [];

  let inCode = false;
  let listOpen = false;

  const closeList = () => {
    if (listOpen) {
      html.push("</ul>");
      listOpen = false;
    }
  };

  for (const raw of lines) {
    const line = raw.trimEnd();

    if (line.startsWith("```")) {
      closeList();
      if (!inCode) {
        inCode = true;
        html.push("<pre><code>");
      } else {
        inCode = false;
        html.push("</code></pre>");
      }
      continue;
    }

    if (inCode) {
      html.push(escapeHtml(raw));
      continue;
    }

    if (!line) {
      closeList();
      continue;
    }

    if (line.startsWith("# ")) {
      closeList();
      html.push(`<h1>${inlineFormat(line.slice(2))}</h1>`);
      continue;
    }
    if (line.startsWith("## ")) {
      closeList();
      html.push(`<h2>${inlineFormat(line.slice(3))}</h2>`);
      continue;
    }
    if (line.startsWith("### ")) {
      closeList();
      html.push(`<h3>${inlineFormat(line.slice(4))}</h3>`);
      continue;
    }

    if (line === "---" || line === "***") {
      closeList();
      html.push("<hr />");
      continue;
    }

    const listMatch = line.match(/^[-*]\s+(.+)$/);
    if (listMatch) {
      if (!listOpen) {
        html.push("<ul>");
        listOpen = true;
      }
      html.push(`<li>${inlineFormat(listMatch[1])}</li>`);
      continue;
    }

    closeList();
    html.push(`<p>${inlineFormat(line)}</p>`);
  }

  closeList();

  if (inCode) {
    html.push("</code></pre>");
  }

  return html.join("\n");
}

function setReport(text) {
  state.lastReport = text || "";
  const report = qs("#report");
  report.innerHTML = text
    ? renderMarkdownLight(text)
    : '<p class="hint">Your report will appear here.</p>';
  qs("#copy").disabled = !state.lastReport;
  qs("#download").disabled = !state.lastReport;
}

async function run() {
  const query = qs("#query").value.trim();
  if (!query) {
    setStatus("Write a query first.", { error: true });
    return;
  }

  setRunning(true);
  setStatus("Gathering sources and composing the memo…");
  setReport("");

  try {
    const resp = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    if (!resp.ok) {
      const message = await resp.text();
      throw new Error(`${resp.status} ${resp.statusText}: ${message}`);
    }

    const data = await resp.json();
    if (!data.report) throw new Error("No report in response");
    setReport(data.report);
    setStatus("Done.");
  } catch (err) {
    setStatus(err instanceof Error ? err.message : String(err), { error: true });
    setReport("");
  } finally {
    setRunning(false);
  }
}

async function copyReport() {
  if (!state.lastReport) return;
  await navigator.clipboard.writeText(state.lastReport);
  setStatus("Copied to clipboard.");
  setTimeout(() => {
    if (!state.running) setStatus("");
  }, 1100);
}

function downloadReport() {
  if (!state.lastReport) return;
  const blob = new Blob([state.lastReport], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "venturemind_report.md";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

window.addEventListener("DOMContentLoaded", () => {
  qs("#run").addEventListener("click", run);
  qs("#query").addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === "Enter") run();
  });
  qs("#copy").addEventListener("click", copyReport);
  qs("#download").addEventListener("click", downloadReport);
  setReport("");
  setRunning(false);
});

