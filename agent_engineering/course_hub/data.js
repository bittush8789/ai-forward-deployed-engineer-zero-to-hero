// Unified Database - AI Agent Engineering Academy Dashboard
const COURSE_DATA = {
  modules: [
    {
      id: "m1",
      title: "Module 1: LangChain Fundamentals",
      summary: "Understand LCEL, prompt templates, output parsers, memory bindings, retrieval chains, and tool integration.",
      details: `
<h3>Key Concepts</h3>
<p>LangChain is a development framework that simplifies building applications with LLMs by providing standardized abstractions for chaining prompts, models, memory, and tools.</p>
<h4>1. LangChain Expression Language (LCEL)</h4>
<p>LCEL is a declarative language designed to easily chain components, supporting streaming, async executions, fallback options, and tracing out of the box.</p>
      `,
      fileLink: "../modules/01_langchain.md"
    },
    {
      id: "m2",
      title: "Module 2: LangGraph Stateful Agents",
      summary: "Explore stateful graph structures, nodes, edges, conditional routing, and Human-in-the-loop validation.",
      details: `
<h3>Key Concepts</h3>
<p>LangGraph extends LangChain to build multi-agent applications using stateful graphs, modeling workflows as cyclic nodes and edges.</p>
<h4>1. Checkpointing</h4>
<p>Saving the graph state database after every node execution allows long-running agent workflows to resume from their last state if a server fails, and supports human approval interrupts.</p>
      `,
      fileLink: "../modules/02_langgraph.md"
    },
    {
      id: "m3",
      title: "Module 3: CrewAI Team-Based Systems",
      summary: "Master CrewAI role configurations, goal descriptions, task assignments, and crew coordination.",
      details: `
<h3>Key Concepts</h3>
<p>CrewAI organizes agent collaboration around human roles, assigning backstories, tasks, and tools to crews of agents.</p>
<h4>1. Delegation & Collaboration</h4>
<p>Crews execute tasks sequentially or hierarchically, dynamically delegating sub-tasks to specialist agents to build a final report.</p>
      `,
      fileLink: "../modules/03_crewai.md"
    },
    {
      id: "m4",
      title: "Module 4: AutoGen Conversational Chats",
      summary: "Learn AutoGen UserProxy configurations, coder-executor loops, and sandboxed runtimes.",
      details: `
<h3>Key Concepts</h3>
<p>AutoGen orchestrates workflows as multi-agent chat rooms where agents (UserProxyAgent, AssistantAgent) converse to solve tasks.</p>
<h4>1. Sandboxed Run Loops</h4>
<p>The AssistantAgent generates code, and the UserProxyAgent runs it in an isolated container (like Docker), returning console logs and errors to resolve tasks dynamically.</p>
      `,
      fileLink: "../modules/04_autogen.md"
    },
    {
      id: "m5",
      title: "Module 5: Multi-Agent Systems (MAS)",
      summary: "Coordinate supervisor architectures, hierarchical routing, and conflict resolutions.",
      details: `
<h3>Key Concepts</h3>
<p>Multi-Agent Systems coordinate multiple specialist agents to partition complex workflows, reducing model confusion and optimizing performance.</p>
<h4>1. Supervisor Design</h4>
<p>A central supervisor agent acts as the coordinator, receiving tasks, delegating them to specialist agents, compiling outputs, and returning the final result.</p>
      `,
      fileLink: "../modules/05_multi_agent_systems.md"
    },
    {
      id: "m6",
      title: "Module 6: Tool Calling",
      summary: "Analyze function schemas, API gateways, database connectors, and security validations.",
      details: `
<h3>Key Concepts</h3>
<p>Tool calling allows the LLM to output structured JSON arguments for registered APIs, enabling agents to interact with external databases and systems.</p>
<h4>1. Security Guards</h4>
<p>All tool calls must route through validation wrappers and API gateways that handle authentication, input validation, and user access permissions.</p>
      `,
      fileLink: "../modules/06_tool_calling.md"
    },
    {
      id: "m7",
      title: "Module 7: Memory Systems",
      summary: "Explore memory taxonomy (short-term, long-term, semantic, episodic, vector) and caching.",
      details: `
<h3>Key Concepts</h3>
<p>Memory systems allow agents to maintain conversation state, recall past interactions, and retrieve relevant knowledge.</p>
<h4>1. Tiered Memory Architecture</h4>
<ul>
  <li><strong>Short-Term Context:</strong> Active thread dialogue stored in high-speed systems like Redis.</li>
  <li><strong>Long-Term Semantic Memory:</strong> User preferences, policies, and documents stored in vector databases (like ChromaDB).</li>
</ul>
      `,
      fileLink: "../modules/07_memory_systems.md"
    },
    {
      id: "m8",
      title: "Module 8: Agent Orchestration",
      summary: "Manage agent lifecycle, job queues, PostgreSQL state checkpoints, and reliability.",
      details: `
<h3>Key Concepts</h3>
<p>Agent orchestration manages the lifecycle, resource allocation, and state persistence of parallel agents running at scale.</p>
<h4>1. State Persistence</h4>
<p>Saving active session state checkpoints in relational databases (like PostgreSQL) to support rollback recovery and debugging.</p>
      `,
      fileLink: "../modules/08_agent_orchestration.md"
    }
  ],
  projects: [
    {
      id: "p1",
      title: "Project 1: Enterprise Knowledge Copilot",
      description: "LangChain Tool Binding. Simulates tool execution and prompt variable compilation.",
      systemPrompt: "Tool: retrieve_company_documents(search_term: str)\nInstruction: Query policies database. Use this tool only if policy details are requested.",
      inputs: [
        { name: "query", label: "User Inquiry", type: "text", default: "What is the maximum daily meal allowance for business trips?" }
      ],
      mockResponses: [
        { match: "meal", text: "[MODEL] Decision: Invoke tool 'retrieve_company_documents' with args: {'search_term': 'What is the maximum daily meal allowance for business trips?'}\n\n[TOOL] Executing retrieve_company_documents...\nObservation: Daily travel meal allowance is capped at $75 [Doc-2].\n\nFinal Copilot Response:\nBased on retrieved documentation: Reimbursement Policy: Daily travel meal allowance is capped at $75 [Doc-2]." },
        { match: "*", text: "[MODEL] Decision: Answer directly.\n\nFinal Copilot Response:\nHow can I assist you with general tasks today?" }
      ]
    },
    {
      id: "p2",
      title: "Project 2: Multi-Agent Research Platform",
      description: "CrewAI delegation log. Simulates sequential tasks between Researcher and Writer.",
      systemPrompt: "Researcher goal: Extract model stats. Writer goal: Compile briefs under 4 sentences.",
      inputs: [
        { name: "topic", label: "Research Topic", type: "text", default: "Llama-3-70B Specifications" }
      ],
      mockResponses: [
        { match: "llama", text: "[Research Specialist] Running deep queries on topic: 'Llama-3-70B Specifications'...\nObservation: { \"model_name\": \"Llama-3-70B\", \"mmlu_score\": 82.0, \"context_window\": \"128k\" }\n\n[Technical Writer] Received raw logs. Compiling brief...\n\nFinal Brief:\nExecutive Brief: Technical review of Llama-3-70B.\n- MMLU accuracy score: 82.0%.\n- Context window size: 128k tokens." },
        { match: "*", text: "[Research Specialist] No records found matching the topic query." }
      ]
    },
    {
      id: "p3",
      title: "Project 3: Autonomous IT Operations Agent",
      description: "AutoGen Coder-Executor chat simulator. Triggers correction loops on compiler errors.",
      systemPrompt: "CoderAgent generates python scripts. ExecutorAgent runs code in container sandbox.",
      inputs: [
        { name: "code", label: "Cleanup Script Draft", type: "textarea", default: "import os\ntarget_dir = '/tmp/logs'\nos.rmdir(target_dir)\nprint('Logs cleared.')" }
      ],
      mockResponses: [
        { match: "import", text: "[EXECUTOR] Received script payload for execution...\nConsole: Logs cleared.\n\n[SYSTEM] Execution successful (Exit code: 0)." },
        { match: "*", text: "[EXECUTOR] Received script payload for execution...\nConsole Error: NameError: name 'os' is not defined (Exit code: 1).\n\n[CODER] Refining script. Adding missing imports...\nUpdated Script:\nimport os\ntarget_dir = '/tmp/logs'\nos.rmdir(target_dir)\nprint('Logs cleared.')\n\n[EXECUTOR] Re-executing refined script...\nConsole: Logs cleared.\n[SYSTEM] Resolution successful." }
      ]
    },
    {
      id: "p4",
      title: "Project 4: Customer Support Multi-Agent System",
      description: "LangGraph State Routing. Tracks customer tier and routes to VIP or Standard nodes.",
      systemPrompt: "State schema: { customer_name: str, active_node: str, messages: list }\nAccounts Database: { 'Arthur Dent': 'PREMIUM', 'Trillian': 'STANDARD' }",
      inputs: [
        { name: "customer", label: "Customer Name ID", type: "text", default: "Arthur Dent" },
        { name: "message", label: "Message text", type: "text", default: "I have a billing question." }
      ],
      mockResponses: [
        { match: "Arthur", text: "[NODE: START] Processing message from customer: Arthur Dent\nCheckpoint 1 saved.\n\n[EDGE: ROUTER] Evaluating user metadata...\nConditional Match: Premium Tier. Routing to VIP_SUPPORT_AGENT.\n\n[NODE: VIP_SUPPORT_AGENT] Executing high-priority support workflow...\nCheckpoint 2 saved.\n\nFinal State: { \"active_node\": \"COMPLETED\", \"messages\": [\"I have a billing question.\", \"Hello Arthur Dent, welcome to our Priority Desk.\"] }" },
        { match: "*", text: "[NODE: START] Processing message...\nCheckpoint 1 saved.\n\n[EDGE: ROUTER] Evaluating user metadata...\nConditional Match: Standard Tier. Routing to STANDARD_SUPPORT_AGENT.\n\n[NODE: STANDARD_SUPPORT_AGENT] Executing standard support workflow...\nCheckpoint 2 saved.\n\nFinal State: { \"active_node\": \"COMPLETED\", \"messages\": [\"I have a billing question.\", \"Hello, thank you for reaching out.\"] }" }
      ]
    },
    {
      id: "p5",
      title: "Project 5: Enterprise AI Automation Platform",
      description: "Multi-agent supervisor with risk auditing and KYC approvals checkpoints.",
      systemPrompt: "Supervisor reviews auditor and compliance node logs. Suspends transactions if amount > $5000.",
      inputs: [
        { name: "amount", label: "Transaction Transfer Amount ($)", type: "number", default: 12500 }
      ],
      mockResponses: [
        { match: "12500", text: "[Security Auditor] Auditing transaction amount: $12500...\nReport: { \"risk_rating\": \"HIGH\", \"notes\": \"Exceeds $5,000 threshold.\" }\n\n[Compliance Officer] Auditing account status...\nReport: { \"kyc_status\": \"COMPLETED\", \"audit_status\": \"CLEAR\" }\n\n[Supervisor] Compiling final decision...\n\nFinal Decision JSON:\n{\n  \"pipeline_status\": \"SUSPENDED\",\n  \"required_action\": \"[REQUIRES_HUMAN_SIGN_OFF]\",\n  \"decision_rationale\": \"Transaction suspended. High risk rating detected. Human verification required.\"\n}" },
        { match: "*", text: "[Security Auditor] Auditing transaction amount...\nReport: { \"risk_rating\": \"LOW\", \"notes\": \"Amount lies within standard boundaries.\" }\n\n[Compliance Officer] Auditing account status...\nReport: { \"kyc_status\": \"COMPLETED\", \"audit_status\": \"CLEAR\" }\n\n[Supervisor] Compiling final decision...\n\nFinal Decision JSON:\n{\n  \"pipeline_status\": \"APPROVED\",\n  \"required_action\": \"None\",\n  \"decision_rationale\": \"Transaction matches all compliance and risk policies.\"\n}" }
      ]
    }
  ],
  quiz: [
    {
      question: "Which orchestration syntax in LangChain is used to build type-safe, streaming-native pipelines?",
      options: [
        "LLMChain",
        "LangChain Expression Language (LCEL)",
        "SequentialChain",
        "RouterChain"
      ],
      answer: 1,
      explanation: "LangChain Expression Language (LCEL) is the declarative language used to chain components, supporting streaming, async execution, and tracing natively."
    },
    {
      question: "What is the primary role of checkpointers in LangGraph state graphs?",
      options: [
        "To compile prompts into SFT datasets",
        "To save a serialized copy of the graph state, supporting workflow persistence and recovery",
        "To calculate cosine similarity search metrics",
        "To route API calls between model providers"
      ],
      answer: 1,
      explanation: "Checkpointers persist the graph state after every node executes, allowing long-running agent workflows to resume from checkpoints if a server fails."
    },
    {
      question: "How does AutoGen coordinate multi-agent workflows?",
      options: [
        "Using sequential task lists defined in YAML files",
        "Using state graph chart nodes and transition matrices",
        "As conversational chats between multiple specialized agents",
        "By fine-tuning models on SFT datasets"
      ],
      answer: 2,
      explanation: "AutoGen coordinates tasks by modeling workflows as conversational chats between multiple specialized agents (like UserProxy and Assistant agents)."
    },
    {
      question: "In agent memory systems, what is the role of Episodic Long-Term memory?",
      options: [
        "To store the active thread dialogue context",
        "To save historical summaries of previous runs and steps, helping agents learn from past tasks",
        "To run semantic vector searches over HR policy PDF files",
        "To log model training loss curves"
      ],
      answer: 1,
      explanation: "Episodic memory stores summaries and logs of previous agent runs, allowing the agent to recall previous tasks and decisions over time."
    },
    {
      question: "What is the purpose of a supervisor agent in a hierarchical multi-agent platform?",
      options: [
        "To write and test Python code scripts",
        "To route tasks, manage the shared state, compile specialist outputs, and coordinate decisions",
        "To calculate GPU VRAM training requirements",
        "To run BM25 keyword search indexes"
      ],
      answer: 1,
      explanation: "In hierarchical systems, the supervisor agent acts as the central coordinator, routing tasks to specialist agents, managing shared state updates, and compiling final results."
    }
  ]
};
const MODEL_PRICING = {
  "gpt-4o": { input: 2.50, output: 10.00 },
  "gpt-4o-mini": { input: 0.15, output: 0.60 },
  "claude-3-5-sonnet": { input: 3.00, output: 15.00 },
  "llama-3-8b": { input: 0.20, output: 0.20 }
};
const HARDWARE_HARDENING = {
  "RTX 4090": { vram: 24, costPerHour: 0.50 },
  "A100 (80GB)": { vram: 80, costPerHour: 2.21 },
  "H100 (80GB)": { vram: 80, costPerHour: 4.76 }
};
