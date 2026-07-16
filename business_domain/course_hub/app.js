document.addEventListener("DOMContentLoaded", () => {
  const moduleList = document.getElementById("module-list");
  const searchInput = document.getElementById("search-input");
  const contentArea = document.getElementById("content-area");
  
  let currentModule = null;
  let activeTab = "theory"; // "theory" or "practice"

  // Render sidebar items
  function renderSidebar(filter = "") {
    moduleList.innerHTML = "";
    const filtered = courseData.modules.filter(m => 
      m.title.toLowerCase().includes(filter.toLowerCase()) ||
      m.description.toLowerCase().includes(filter.toLowerCase())
    );

    filtered.forEach(mod => {
      const item = document.createElement("div");
      item.className = `module-item ${currentModule && currentModule.id === mod.id ? 'active' : ''}`;
      item.innerHTML = `
        <div class="module-badge">${mod.id}</div>
        <div class="module-info">
          <div class="module-title">${mod.title}</div>
        </div>
      `;
      item.addEventListener("click", () => selectModule(mod));
      moduleList.appendChild(item);
    });
  }

  // Handle module selection
  function selectModule(mod) {
    currentModule = mod;
    renderSidebar(searchInput.value);
    renderModuleContent();
  }

  // Simple Markdown Parser for UI Display
  function parseMarkdown(mdText) {
    if (!mdText) return "<p>No content loaded.</p>";
    
    let html = mdText;
    
    // Replace code blocks
    html = html.replace(/```([\s\S]*?)```/g, (match, code) => {
      const escaped = code.replace(/</g, "&lt;").replace(/>/g, "&gt;");
      return `<pre><code>${escaped}</code></pre>`;
    });

    // Replace inline code
    html = html.replace(/`([^`\n]+)`/g, "<code>$1</code>");

    // Replace headers
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');

    // Replace bullet points
    html = html.replace(/^\s*-\s+(.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
    // Clean up adjacent UL lists
    html = html.replace(/<\/ul>\s*<ul>/g, "");

    // Replace line breaks to paragraphs
    html = html.replace(/\n\n/g, "<p></p>");
    
    return html;
  }

  // Fetch and display module content
  async function renderModuleContent() {
    if (!currentModule) return;

    contentArea.innerHTML = `
      <div class="module-header-card">
        <h2>${currentModule.title}</h2>
        <p>${currentModule.description}</p>
        <div class="tags">
          ${currentModule.skills.map(s => `<span class="tag">${s}</span>`).join("")}
        </div>
      </div>
      <div class="tabs-container">
        <div class="tab ${activeTab === 'theory' ? 'active' : ''}" id="tab-theory">Theory & Concepts</div>
        <div class="tab ${activeTab === 'practice' ? 'active' : ''}" id="tab-practice">Practical Tasks & Labs</div>
      </div>
      <div class="detail-panel" id="detail-panel">
        <div class="welcome-screen">
          <p>Loading module content...</p>
        </div>
      </div>
    `;

    // Bind tab events
    document.getElementById("tab-theory").addEventListener("click", () => switchTab("theory"));
    document.getElementById("tab-practice").addEventListener("click", () => switchTab("practice"));

    loadTabContent();
  }

  function switchTab(tabName) {
    activeTab = tabName;
    document.getElementById("tab-theory").classList.toggle("active", tabName === "theory");
    document.getElementById("tab-practice").classList.toggle("active", tabName === "practice");
    loadTabContent();
  }

  async function loadTabContent() {
    const detailPanel = document.getElementById("detail-panel");
    const targetFile = activeTab === "theory" ? currentModule.file : (currentModule.taskFile || currentModule.file);

    try {
      const response = await fetch(targetFile);
      if (!response.ok) throw new Error("File not found");
      const text = await response.text();
      detailPanel.innerHTML = parseMarkdown(text);
    } catch (err) {
      detailPanel.innerHTML = `
        <div style="padding: 20px; color: #ef4444;">
          <h4>Error Loading Content</h4>
          <p>Could not retrieve: <code>${targetFile}</code>. Ensure the course files exist in the target paths.</p>
        </div>
      `;
    }
  }

  // Search input filter event
  searchInput.addEventListener("input", (e) => {
    renderSidebar(e.target.value);
  });

  // Initial render
  renderSidebar();
});
