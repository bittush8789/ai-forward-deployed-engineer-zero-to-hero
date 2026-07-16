// Application Logic - AI Agent Engineering Academy Dashboard

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initTheme();
  initLessons();
  initPlayground();
  initQuiz();
  initAgentCalculator();
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
      template = `Retrieve top matching passages.\nUser Query: "{query}"`;
    } else if (proj.id === "p2") {
      template = `Run CrewAI Research Platform topic.\nTopic: {topic}`;
    } else if (proj.id === "p3") {
      template = `Execute clean script in Sandbox container.\nScript code:\n{code}`;
    } else if (proj.id === "p4") {
      template = `Initiate Support State Graph.\nCustomer: {customer}\nMessage: {message}`;
    } else if (proj.id === "p5") {
      template = `Process transaction automation.\nAmount: ${"{amount}"}`;
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

    outputPanel.innerHTML = "<em>Executing multi-agent simulation run logs...</em>";
    
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
      q: "Explain why checkpointers are essential in state chart executors.",
      a: "Checkpointers serialize and save the graph state after every step. If the execution crashes mid-workflow, it can resume from the last saved state using a unique thread ID."
    },
    {
      q: "How do you protect database tools from prompt injection in agent platforms?",
      a: "Do not grant write permissions directly to LLM agents. Run all tool arguments through validation layers and API gateways to check parameter values."
    },
    {
      q: "When is AutoGen's conversational model preferred over LangGraph's DAG graphs?",
      a: "AutoGen is ideal for tasks requiring back-and-forth interactions between specialist agents (like coder-executor debugging loops). LangGraph is better suited for structured workflows with defined pathways."
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

// 6. Agent Latency & Cost Calculator
function initAgentCalculator() {
  const modelSelect = document.getElementById("agent-model");
  
  const stepsSlider = document.getElementById("agent-steps-slider");
  const stepsVal = document.getElementById("agent-steps-val");
  
  const countSlider = document.getElementById("agent-count-slider");
  const countVal = document.getElementById("agent-count-val");
  
  const inputSlider = document.getElementById("agent-input-slider");
  const inputVal = document.getElementById("agent-input-val");
  
  const outputSlider = document.getElementById("agent-output-slider");
  const outputVal = document.getElementById("agent-output-val");

  const volInput = document.getElementById("agent-volume");
  const sumCheckbox = document.getElementById("agent-toggle-summarization");

  const avgLatencyEl = document.getElementById("agent-est-latency");
  const monthlyCostEl = document.getElementById("agent-monthly-cost");
  const optimizedCostEl = document.getElementById("agent-optimized-cost");

  function calculateAgenticModel() {
    const model = modelSelect.value;
    const rateIn = MODEL_PRICING[model].input;
    const rateOut = MODEL_PRICING[model].output;

    const steps = parseInt(stepsSlider.value);
    const agents = parseInt(countSlider.value);
    const inTokens = parseInt(inputSlider.value);
    const outTokens = parseInt(outputSlider.value);
    const volume = parseInt(volInput.value) || 0;
    const sumOn = sumCheckbox.checked;

    // Update Slider Displays
    stepsVal.textContent = steps + (steps === 1 ? " loop" : " loops");
    countVal.textContent = agents + (agents === 1 ? " agent" : " agents");
    inputVal.textContent = inTokens.toLocaleString() + " tokens";
    outVal.textContent = outTokens.toLocaleString() + " tokens";

    // 1. Raw Monthly Cost Calculation
    // Total Input Tokens = steps * inTokens
    // Total Output Tokens = steps * outTokens
    const inputCostRaw = (steps * inTokens * rateIn) / 1000000;
    const outputCostRaw = (steps * outTokens * rateOut) / 1000000;
    const monthlyRaw = (inputCostRaw + outputCostRaw) * volume;

    // 2. Optimized Monthly Cost Calculation (Memory summarization saves 40% of inputs)
    const inputMultiplier = sumOn ? 0.60 : 1.00;
    const inputCostOpt = (steps * inTokens * inputMultiplier * rateIn) / 1000000;
    const monthlyOpt = (inputCostOpt + outputCostRaw) * volume;

    // 3. Average Latency Heuristic (seconds)
    // Formula: steps * (input processing time + output generation time) + routing overhead
    // Output token generation is slow (~0.015s per token). Input prefill is fast (~0.0001s per token).
    // Plus 0.4s network overhead per agent swap.
    const latencyPerStep = (inTokens * 0.0001) + (outTokens * 0.015);
    const avgLatency = (steps * latencyPerStep) + (agents * 0.4);

    // Render results
    avgLatencyEl.textContent = avgLatency.toFixed(1) + "s";
    monthlyCostEl.textContent = "$" + monthlyRaw.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    optimizedCostEl.textContent = "$" + monthlyOpt.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " (Est. Savings: " + (sumOn ? "40% input tokens" : "0%") + ")";
  }

  [modelSelect, stepsSlider, countSlider, inputSlider, outputSlider, volInput, sumCheckbox].forEach(el => {
    el.addEventListener("input", calculateAgenticModel);
    el.addEventListener("change", calculateAgenticModel);
  });

  // Run initial calculation
  calculateAgenticModel();
}
