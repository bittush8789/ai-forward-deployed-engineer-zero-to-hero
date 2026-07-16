// Application Logic - Generative AI & LLM Academy Dashboard

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initTheme();
  initLessons();
  initPlayground();
  initQuiz();
  initGpuCalculator();
});

// 1. Tab switching
function initTabs() {
  const navItems = document.querySelectorAll(".nav-item");
  const tabPanes = document.querySelectorAll(".tab-pane");
  const pageTitle = document.getElementById("page-title");

  navItems.forEach(item => {
    item.addEventListener("click", () => {
      const tabId = item.getAttribute("data-tab");
      
      navItems.forEach(n => n.classList.remove("active"));
      item.classList.add("active");
      
      tabPanes.forEach(pane => pane.classList.remove("active"));
      document.getElementById(`tab-${tabId}`).classList.add("active");
      
      pageTitle.textContent = item.textContent.trim();
    });
  });
}

// 2. Light / Dark theme toggler
function initTheme() {
  const toggleBtn = document.getElementById("theme-toggle");
  document.body.setAttribute("data-theme", "dark");
  
  toggleBtn.addEventListener("click", () => {
    const currentTheme = document.body.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";
    document.body.setAttribute("data-theme", newTheme);
    
    if (newTheme === "light") {
      toggleBtn.innerHTML = `<svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 9H3m3.343-5.657l-.707.707m2.828 9.9a9 9 0 1111.314 0l-.707-.707m-2.828-9.9l-.707-.707m2.828 9.9a9 9 0 11-11.314 0" /></svg>`;
    } else {
      toggleBtn.innerHTML = `<svg class="icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>`;
    }
  });
}

// 3. Syllabus Reader
function initLessons() {
  const searchInput = document.getElementById("lesson-search");
  const listContainer = document.getElementById("lesson-list-items");
  const placeholder = document.getElementById("lesson-viewer-placeholder");
  const contentPane = document.getElementById("lesson-viewer-content");
  
  const titleEl = document.getElementById("lesson-title");
  const bodyEl = document.getElementById("lesson-body");
  const linkEl = document.getElementById("lesson-markdown-link");

  function renderList(filteredModules) {
    listContainer.innerHTML = "";
    filteredModules.forEach(mod => {
      const btn = document.createElement("button");
      btn.className = "lesson-list-item";
      btn.innerHTML = `
        <h4>${mod.title}</h4>
        <p>${mod.summary}</p>
      `;
      btn.addEventListener("click", () => {
        document.querySelectorAll(".lesson-list-item").forEach(item => item.classList.remove("active"));
        btn.classList.add("active");
        
        placeholder.classList.add("hidden");
        contentPane.classList.remove("hidden");
        
        titleEl.textContent = mod.title;
        bodyEl.innerHTML = mod.details;
        linkEl.href = mod.fileLink;
      });
      listContainer.appendChild(btn);
    });
  }

  renderList(COURSE_DATA.modules);

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    const matches = COURSE_DATA.modules.filter(mod => 
      mod.title.toLowerCase().includes(term) || 
      mod.summary.toLowerCase().includes(term)
    );
    renderList(matches);
  });
}

// 4. Project Playground
function initPlayground() {
  const selector = document.getElementById("project-selector");
  const titleEl = document.getElementById("project-title");
  const descEl = document.getElementById("project-description");
  const varsContainer = document.getElementById("project-variables-container");
  
  const systemPromptArea = document.getElementById("playground-system-prompt");
  const userPromptArea = document.getElementById("playground-user-prompt");
  const outputPanel = document.getElementById("playground-output");
  
  const compileBtn = document.getElementById("btn-compile");
  const testBtn = document.getElementById("btn-test-prompt");

  // Populate selector
  COURSE_DATA.projects.forEach(proj => {
    const opt = document.createElement("option");
    opt.value = proj.id;
    opt.textContent = proj.title;
    selector.appendChild(opt);
  });

  function loadProject(projId) {
    const proj = COURSE_DATA.projects.find(p => p.id === projId);
    if (!proj) return;

    titleEl.textContent = proj.title;
    descEl.textContent = proj.description;
    systemPromptArea.value = proj.systemPrompt;
    
    varsContainer.innerHTML = "";
    proj.inputs.forEach(input => {
      const group = document.createElement("div");
      group.className = "form-group";
      
      const label = document.createElement("label");
      label.textContent = input.label;
      
      let field;
      if (input.type === "textarea") {
        field = document.createElement("textarea");
        field.className = "form-control h-24";
        field.value = input.default;
      } else {
        field = document.createElement("input");
        field.type = "text";
        field.className = "form-control";
        field.value = input.default;
      }
      field.id = `play-var-${input.name}`;
      field.setAttribute("data-varname", input.name);
      
      group.appendChild(label);
      group.appendChild(field);
      varsContainer.appendChild(group);
    });

    userPromptArea.value = "";
    outputPanel.innerHTML = "<em>Inference logs will display here...</em>";
  }

  loadProject(COURSE_DATA.projects[0].id);

  selector.addEventListener("change", (e) => {
    loadProject(e.target.value);
  });

  function getCompiledUserPrompt() {
    const proj = COURSE_DATA.projects.find(p => p.id === selector.value);
    if (!proj) return "";

    let template = "";
    if (proj.id === "p1") {
      template = `Retrieve top matching passages.\nUser Query: "{query}"\nCorpus:\n{corpus}`;
    } else if (proj.id === "p2") {
      template = `Call Tool Parameter Validation.\nArguments: {args}`;
    } else if (proj.id === "p3") {
      template = `IT Service Agent verification.\nCustomer: {customer}\nOrder Number: {order}`;
    } else if (proj.id === "p4") {
      template = `Supervised Fine-Tuning dataset compiler.\nContract Extract: {text}\nGoverning Law: {law}\nStatus: {status}`;
    } else if (proj.id === "p5") {
      template = `Multi-Agent Routing State node loop.\nTask request: {task}`;
    }

    let compiled = template;
    proj.inputs.forEach(input => {
      const val = document.getElementById(`play-var-${input.name}`).value;
      compiled = compiled.replace(`{${input.name}}`, val);
    });
    return compiled;
  }

  compileBtn.addEventListener("click", () => {
    userPromptArea.value = getCompiledUserPrompt();
  });

  testBtn.addEventListener("click", () => {
    const proj = COURSE_DATA.projects.find(p => p.id === selector.value);
    if (!proj) return;

    if (!userPromptArea.value) {
      userPromptArea.value = getCompiledUserPrompt();
    }

    outputPanel.innerHTML = "<em>Executing python script node evaluation...</em>";
    
    setTimeout(() => {
      const fullText = userPromptArea.value.toLowerCase();
      let matchedResponse = proj.mockResponses[proj.mockResponses.length - 1].text;
      
      for (let r of proj.mockResponses) {
        if (r.match !== "*" && fullText.includes(r.match.toLowerCase())) {
          matchedResponse = r.text;
          break;
        }
      }
      outputPanel.textContent = matchedResponse;
    }, 600);
  });
}

// 5. Quiz & Interview Practice
let currentQuizIdx = 0;
let quizScore = 0;
const totalQuizQuestions = 5;

function initQuiz() {
  const qText = document.getElementById("quiz-question-text");
  const optionsBox = document.getElementById("quiz-options-container");
  const progressTag = document.getElementById("quiz-progress");
  const feedbackPanel = document.getElementById("quiz-feedback");
  const nextBtn = document.getElementById("btn-next-question");
  const completionBox = document.getElementById("quiz-completion");
  
  const resetBtn = document.getElementById("btn-reset-quiz");
  const scoreVal = document.getElementById("quiz-score-val");
  const totalVal = document.getElementById("quiz-total-val");

  function loadQuestion() {
    feedbackPanel.classList.add("hidden");
    nextBtn.classList.add("hidden");
    optionsBox.innerHTML = "";

    if (currentQuizIdx >= totalQuizQuestions) {
      qText.classList.add("hidden");
      optionsBox.classList.add("hidden");
      progressTag.classList.add("hidden");
      completionBox.classList.remove("hidden");
      
      scoreVal.textContent = quizScore;
      totalVal.textContent = totalQuizQuestions;
      return;
    }

    qText.classList.remove("hidden");
    optionsBox.classList.remove("hidden");
    progressTag.classList.remove("hidden");
    completionBox.classList.add("hidden");

    const q = COURSE_DATA.quiz[currentQuizIdx];
    progressTag.textContent = `Question ${currentQuizIdx + 1} of ${totalQuizQuestions}`;
    qText.textContent = q.question;

    q.options.forEach((opt, idx) => {
      const btn = document.createElement("button");
      btn.className = "quiz-option-btn";
      btn.textContent = opt;
      btn.addEventListener("click", () => {
        document.querySelectorAll(".quiz-option-btn").forEach(b => b.disabled = true);
        
        const correctIdx = q.answer;
        if (idx === correctIdx) {
          btn.classList.add("correct");
          quizScore++;
          document.getElementById("feedback-badge").className = "badge-success";
          document.getElementById("feedback-badge").textContent = "Correct";
        } else {
          btn.classList.add("wrong");
          optionsBox.children[correctIdx].classList.add("correct");
          document.getElementById("feedback-badge").className = "badge-danger font-red";
          document.getElementById("feedback-badge").textContent = "Incorrect";
        }
        
        feedbackPanel.classList.remove("hidden");
        document.getElementById("feedback-text").textContent = q.explanation;
        nextBtn.classList.remove("hidden");
      });
      optionsBox.appendChild(btn);
    });
  }

  nextBtn.addEventListener("click", () => {
    currentQuizIdx++;
    loadQuestion();
  });

  resetBtn.addEventListener("click", () => {
    currentQuizIdx = 0;
    quizScore = 0;
    loadQuestion();
  });

  // Render Interview Questions
  const qaContainer = document.getElementById("interview-qa-container");
  const interviewQuestions = [
    {
      q: "How does QLoRA achieve parameter efficiency during training?",
      a: "Quantizes base weights to 4-bit NormalFloat (NF4), while utilizing double quantization to compress scale coefficients. 16-bit LoRA adapter parameters are then updated, minimizing GPU VRAM."
    },
    {
      q: "Why are grammar validation layers preferred over raw system prompts for structured JSON extractions?",
      a: "Raw prompts depend on model probabilities, which drift and format incorrectly. Grammar rules (Outlines/Instructor) adjust logit selection probabilities, guaranteeing 100% syntactical JSON compliance."
    },
    {
      q: "What is the primary security threat in Multi-Agent Graph loops?",
      a: "Indirect Prompt Injection, where untrusted data fetched by one agent contains instructions that hijack subsequent graph loops or execute tool calls on other agents."
    }
  ];

  interviewQuestions.forEach(item => {
    const itemEl = document.createElement("div");
    itemEl.className = "qa-item";
    itemEl.innerHTML = `
      <h4>Q: ${item.q}</h4>
      <p><strong>A:</strong> ${item.a}</p>
    `;
    qaContainer.appendChild(itemEl);
  });

  loadQuestion();
}

// 6. GPU VRAM Memory Calculator
function initGpuCalculator() {
  const modelSizeSelect = document.getElementById("gpu-model-size");
  const precisionSelect = document.getElementById("gpu-precision");
  const optimizerSelect = document.getElementById("gpu-optimizer");
  
  const seqSlider = document.getElementById("gpu-seq-slider");
  const seqVal = document.getElementById("gpu-seq-val");
  
  const batchSlider = document.getElementById("gpu-batch-slider");
  const batchVal = document.getElementById("gpu-batch-val");

  const vramWeightsEl = document.getElementById("vram-weights");
  const vramOptimizerEl = document.getElementById("vram-optimizer");
  const vramKVCacheEl = document.getElementById("vram-kvcache");
  const vramTotalEl = document.getElementById("vram-total");
  const hardwareSuggestionEl = document.getElementById("gpu-hardware-suggestion");

  function calculateVram() {
    const pSize = parseFloat(modelSizeSelect.value); // e.g. 8B, 14B, 32B, 70B
    const precisionBytes = parseFloat(precisionSelect.value); // FP16: 2, INT8: 1, INT4: 0.5
    const optimizerBytes = parseFloat(optimizerSelect.value); // Adam: 8, SGD: 4, LoRA: 0.1, None: 0
    
    const seqLength = parseInt(seqSlider.value);
    const batchSize = parseInt(batchSlider.value);

    // Update Slider Displays
    seqVal.textContent = seqLength.toLocaleString() + " tokens";
    batchVal.textContent = batchSize.toLocaleString() + " batch size";

    // 1. Model Weights Memory (GB)
    // Formula: parameters * bytes per parameter
    const modelMemory = pSize * precisionBytes;

    // 2. Optimizer State Memory (GB)
    // Formula: parameters * optimizer bytes per parameter (or adapter approximation)
    const optimizerMemory = pSize * optimizerBytes;

    // 3. KV Cache / Activation Memory Heuristics (GB)
    // Heuristic: (pSize * 0.08) * (batch_size * seq_len) / 10^5
    const kvCacheMemory = (pSize * 0.08) * (batchSize * seqLength) / 100000;

    // 4. Total Memory (GB) with 20% system overhead buffer
    const rawTotal = modelMemory + optimizerMemory + kvCacheMemory;
    const totalMemory = rawTotal * 1.20;

    // Render results
    vramWeightsEl.textContent = modelMemory.toFixed(2) + " GB";
    vramOptimizerEl.textContent = optimizerMemory.toFixed(2) + " GB";
    vramKVCacheEl.textContent = kvCacheMemory.toFixed(2) + " GB";
    vramTotalEl.textContent = totalMemory.toFixed(2) + " GB";

    // Suggest hardware configuration
    let hardware = "RTX 4090 (24GB) or L4 GPU (24GB)";
    if (totalMemory >= 320) {
      hardware = "8x H100 GPU Cluster (640GB VRAM) or distributed Cloud TPUs";
    } else if (totalMemory >= 80) {
      hardware = "4x A100 (320GB) or 4x H100 (320GB) distributed node cluster";
    } else if (totalMemory >= 48) {
      hardware = "1x H100 SXM (80GB) or 1x A100 PCIe (80GB)";
    } else if (totalMemory >= 24) {
      hardware = "1x RTX A6000 (48GB) or A40 (48GB)";
    }

    hardwareSuggestionEl.textContent = hardware;
  }

  [modelSizeSelect, precisionSelect, optimizerSelect, seqSlider, batchSlider].forEach(el => {
    el.addEventListener("input", calculateVram);
    el.addEventListener("change", calculateVram);
  });

  // Initial Calculation
  calculateVram();
}
