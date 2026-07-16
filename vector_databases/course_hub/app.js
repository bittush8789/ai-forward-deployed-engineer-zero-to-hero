/* app.js — Vector Databases Academy Dashboard */
document.addEventListener("DOMContentLoaded", () => {
  const moduleListEl = document.getElementById("module-list");
  const searchInput  = document.getElementById("search-input");
  const contentArea  = document.getElementById("content-area");
  const topbarTitle  = document.getElementById("topbar-title");
  const topbarSub    = document.getElementById("topbar-sub");

  let currentModule = null;
  let activeTab = "theory";

  // --- Category colour key (first word of category) ---
  function catClass(cat) {
    return "cat-" + (cat || "").split(" ")[0].replace(/[^a-zA-Z]/g, "");
  }

  // --- Sidebar render ---
  function renderSidebar(filter = "") {
    moduleListEl.innerHTML = "";
    const q = filter.toLowerCase();
    const filtered = courseData.modules.filter(m =>
      m.title.toLowerCase().includes(q) ||
      m.description.toLowerCase().includes(q) ||
      (m.category || "").toLowerCase().includes(q)
    );

    if (filtered.length === 0) {
      moduleListEl.innerHTML = `<p style="color:var(--text-secondary);padding:16px;font-size:0.85rem;">No modules match your search.</p>`;
      return;
    }

    filtered.forEach(mod => {
      const isActive = currentModule && currentModule.id === mod.id;
      const item = document.createElement("div");
      item.className = `module-item ${isActive ? "active" : ""}`;
      item.innerHTML = `
        <div class="cat-dot ${catClass(mod.category)}"></div>
        <div class="mod-badge">${mod.id}</div>
        <div class="mod-info">
          <div class="mod-title">${mod.title}</div>
          <div class="mod-cat">${mod.category || ""}</div>
        </div>
      `;
      item.addEventListener("click", () => selectModule(mod));
      moduleListEl.appendChild(item);
    });
  }

  // --- Module selection ---
  function selectModule(mod) {
    currentModule = mod;
    activeTab = "theory";
    renderSidebar(searchInput.value);
    renderModuleView();
  }

  // --- Module view ---
  function renderModuleView() {
    const mod = currentModule;
    topbarTitle.textContent = mod.title;
    topbarSub.textContent = mod.category || "";

    const skillsHTML = (mod.skills || [])
      .map(s => `<span class="skill-tag">${s}</span>`).join("");

    contentArea.innerHTML = `
      <div class="module-view">
        <div class="module-hero">
          <h2>${mod.title}</h2>
          <p class="desc">${mod.description}</p>
          <div class="skills-row">${skillsHTML}</div>
        </div>

        <div class="tab-bar">
          <div class="tab ${activeTab === "theory"   ? "active" : ""}" data-tab="theory">Theory & Concepts</div>
          <div class="tab ${activeTab === "practice" ? "active" : ""}" data-tab="practice">Practice Tasks</div>
          ${mod.labFile ? `<div class="tab ${activeTab === "lab" ? "active" : ""}" data-tab="lab">Lab Script</div>` : ""}
        </div>

        <div class="detail-pane" id="detail-pane">
          <p style="color:var(--text-secondary)">Loading content...</p>
        </div>
      </div>
    `;

    // Bind tabs
    contentArea.querySelectorAll(".tab").forEach(t => {
      t.addEventListener("click", () => {
        activeTab = t.dataset.tab;
        contentArea.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
        t.classList.add("active");
        loadTabContent();
      });
    });

    loadTabContent();
  }

  // --- Load tab content ---
  async function loadTabContent() {
    const mod = currentModule;
    const pane = document.getElementById("detail-pane");
    if (!pane) return;

    let targetFile;
    if (activeTab === "theory")   targetFile = mod.file;
    else if (activeTab === "practice") targetFile = mod.taskFile || mod.file;
    else if (activeTab === "lab") targetFile = mod.labFile;

    if (!targetFile) {
      pane.innerHTML = `<p style="color:var(--text-secondary)">No content available for this tab.</p>`;
      return;
    }

    pane.innerHTML = `<p style="color:var(--text-secondary)">Loading ${targetFile}…</p>`;

    try {
      const resp = await fetch(targetFile);
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const text = await resp.text();

      // Plain text for lab scripts (.py)
      if (targetFile.endsWith(".py") || targetFile.endsWith(".sh")) {
        const escaped = text.replace(/</g, "&lt;").replace(/>/g, "&gt;");
        pane.innerHTML = `<pre><code>${escaped}</code></pre>`;
        return;
      }

      pane.innerHTML = parseMarkdown(text);
    } catch (err) {
      pane.innerHTML = `
        <div class="error-msg">
          <strong>Could not load file</strong><br>
          <code>${targetFile}</code><br><br>
          Ensure the module files are present in the <code>modules/</code>, <code>tasks/</code>, and <code>labs/</code> directories.
        </div>`;
    }
  }

  // --- Lightweight Markdown parser ---
  function parseMarkdown(md) {
    let html = md;

    // Fenced code blocks
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
      const esc = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return `<pre><code class="lang-${lang}">${esc}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`\n]+)`/g, "<code>$1</code>");

    // Headings
    html = html.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
    html = html.replace(/^### (.+)$/gm,  "<h3>$1</h3>");
    html = html.replace(/^## (.+)$/gm,   "<h2>$1</h2>");
    html = html.replace(/^# (.+)$/gm,    "<h1>$1</h1>");

    // HR
    html = html.replace(/^---+$/gm, "<hr>");

    // Bold / italic
    html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");

    // Tables (basic)
    html = html.replace(/(\|.+\|\n\|[-| :]+\|\n(?:\|.+\|\n?)+)/g, (table) => {
      const rows = table.trim().split("\n");
      const header = rows[0].split("|").filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join("");
      const body = rows.slice(2).map(row => {
        const cells = row.split("|").filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join("");
        return `<tr>${cells}</tr>`;
      }).join("");
      return `<table><thead><tr>${header}</tr></thead><tbody>${body}</tbody></table>`;
    });

    // Lists
    html = html.replace(/^(\s*)-\s+(.+)$/gm, (_, indent, content) => {
      return `<li style="margin-left:${indent.length * 16}px">${content}</li>`;
    });
    html = html.replace(/^(\s*)\d+\.\s+(.+)$/gm, (_, indent, content) => {
      return `<li style="margin-left:${indent.length * 16}px">${content}</li>`;
    });
    html = html.replace(/(<li[\s\S]*?<\/li>)/g, "<ul>$1</ul>");
    html = html.replace(/<\/ul>\s*<ul>/g, "");

    // Paragraph breaks
    html = html.replace(/\n\n+/g, "</p><p>");
    html = `<p>${html}</p>`;
    html = html.replace(/<p>\s*(<(?:h[1-6]|ul|ol|pre|table|hr))/g, "$1");
    html = html.replace(/(<\/(?:h[1-6]|ul|ol|pre|table|hr)>)\s*<\/p>/g, "$1");

    return html;
  }

  // --- Search ---
  searchInput.addEventListener("input", e => renderSidebar(e.target.value));

  // --- Init ---
  topbarTitle.textContent = "Vector Databases Academy";
  topbarSub.textContent = "Select a module to begin";
  renderSidebar();
});
