// Course Hub database for Prompt Engineering Academy
const COURSE_DATA = {
  modules: [
    {
      id: "m1",
      title: "Module 1: Prompt Engineering Fundamentals",
      summary: "Explore prompt anatomy, components, constraints, and lifecycle management in enterprise systems.",
      details: `
<h3>Key Concepts</h3>
<p>Prompt engineering is the systematic design of inputs to LLMs to make responses reliable and reproducible. In production, a prompt behaves like code—defining constraints, contexts, and instructions for the inference engine.</p>
<h4>1. Anatomy of a Prompt</h4>
<ul>
  <li><strong>Instructions:</strong> Core directives detailing what the model must execute.</li>
  <li><strong>Context:</strong> Background data or corpus (e.g. retrieved manuals, logs).</li>
  <li><strong>Constraints:</strong> Operating boundaries (e.g. word limits, forbidden topics).</li>
  <li><strong>Examples:</strong> Few-shot inputs showcasing target behavior.</li>
  <li><strong>Output Formatting:</strong> Specifications for structure (JSON, XML).</li>
</ul>
<h4>2. The Prompt Lifecycle</h4>
<p>From requirements gathering and customer discovery to initial drafts, regression testing, and CI/CD versioned deployment.</p>
      `,
      fileLink: "../modules/01_fundamentals.md"
    },
    {
      id: "m2",
      title: "Module 2: LLM Behavior Understanding",
      summary: "Analyze context windows, tokenization quirks, attention mechanisms, and hallucination behaviors.",
      details: `
<h3>Key Concepts</h3>
<p>LLMs process token representations, not words. Understanding their underlying behavioral limitations avoids production failures.</p>
<h4>1. Lost in the Middle</h4>
<p>LLMs pay maximum attention to tokens at the beginning and end of prompts. Critical rules or context placed in the middle of long payloads are frequently ignored.</p>
<h4>2. Tokenization Quirks</h4>
<p>Numbers, special characters, and code symbols are fragmented into tokens. Mathematical verification inside context windows is unreliable; extract data and verify mathematically in backend code.</p>
      `,
      fileLink: "../modules/02_llm_behavior.md"
    },
    {
      id: "m3",
      title: "Module 3: Prompt Design Principles",
      summary: "Understand role assignment, context injection, and structured instruction constraints.",
      details: `
<h3>Key Concepts</h3>
<p>Robust prompt layouts replace conversational text with structured configuration templates.</p>
<h4>1. Role Assignment</h4>
<p>Giving the model a specific persona (e.g., "Underwriting Auditor") aligns its attention with relevant training patterns, adjusting its tone and vocabulary.</p>
<h4>2. Structural Separation</h4>
<p>Use XML tags (like &lt;context&gt; and &lt;instructions&gt;) to cleanly isolate dynamic inputs from system guidelines, protecting against delimiter collisions.</p>
      `,
      fileLink: "../modules/03_design_principles.md"
    },
    {
      id: "m4",
      title: "Module 4: Prompting Techniques",
      summary: "Master zero-shot, few-shot, Chain-of-Thought (CoT), self-consistency, and structured formatting.",
      details: `
<h3>Key Concepts</h3>
<p>Deploy specialized techniques depending on the complexity of the reasoning task.</p>
<ul>
  <li><strong>Few-Shot:</strong> Show the model exact input-output examples to teach it custom structures and edge cases.</li>
  <li><strong>Chain-of-Thought (CoT):</strong> Force the model to write out its reasoning steps before outputting the final answer, improving logical and math accuracy.</li>
  <li><strong>Self-Consistency:</strong> Run multiple parallel runs and take the majority answer to improve stability.</li>
</ul>
      `,
      fileLink: "../modules/04_prompting_techniques.md"
    },
    {
      id: "m5",
      title: "Module 5: System Prompts",
      summary: "Learn system prompt design, safety controls, business rules, and enterprise governance.",
      details: `
<h3>Key Concepts</h3>
<p>System instructions establish identity, boundaries, policies, and safety rules, acting as the foundation of the conversation.</p>
<h4>1. Priority Guidelines</h4>
<p>System prompts are prioritized by API engines over user prompts, ensuring that safety guidelines remain active even when user inputs are hostile.</p>
<h4>2. Tone and Voice</h4>
<p>System prompts define the company's voice. They should be audited, versioned, and registry-managed rather than hardcoded.</p>
      `,
      fileLink: "../modules/05_system_prompts.md"
    },
    {
      id: "m6",
      title: "Module 6: Enterprise Prompt Frameworks",
      summary: "Build reusable prompt templates, version control, and automated registries.",
      details: `
<h3>Key Concepts</h3>
<p>Scale prompt engineering across organizations with standardization, templating engines (like Jinja2), and semantic versioning.</p>
<h4>1. Prompt Registry</h4>
<p>Decouple prompts from core application code. Store prompts in databases or central repositories to allow instant updates without rolling out new code.</p>
<h4>2. SemVer for Prompts</h4>
<p>Track changes: Patch for text fixes, Minor for prompt enhancements, Major for changes that alter output schemas and break downstream code.</p>
      `,
      fileLink: "../modules/06_enterprise_frameworks.md"
    },
    {
      id: "m7",
      title: "Module 7: Prompt Engineering for RAG",
      summary: "Optimize context injection, document citation, hallucination mitigation, and grounding.",
      details: `
<h3>Key Concepts</h3>
<p>RAG grounds responses in verified data. Prompting must verify retrieval accuracy and prevent hallucinations when search results are missing.</p>
<h4>1. Grounding Constraints</h4>
<p>Instruct the model: "Answer using only the retrieved documents. If not found, write 'I cannot find the answer'."</p>
<h4>2. Strict Citations</h4>
<p>Require the model to cite specific document IDs (e.g., "[Doc-1]") for every claim to support human review and audits.</p>
      `,
      fileLink: "../modules/07_prompt_for_rag.md"
    },
    {
      id: "m8",
      title: "Module 8: Prompt Engineering for AI Agents",
      summary: "Explore ReAct planning, tool descriptions, execution loops, and error handling.",
      details: `
<h3>Key Concepts</h3>
<p>Agent prompts instruct the model to choose actions, evaluate outputs, and navigate loops dynamically.</p>
<h4>1. Tool Descriptions</h4>
<p>The LLM selects tools based on descriptions. Write clear, detailed descriptions: "Use get_balance ONLY after employee ID is verified."</p>
<h4>2. Fail-safe Rules</h4>
<p>Instruct the agent on how to handle tool errors, and implement system limits to prevent infinite execution loops.</p>
      `,
      fileLink: "../modules/08_prompt_for_agents.md"
    },
    {
      id: "m9",
      title: "Module 9: Prompt Evaluation",
      summary: "Understand LLM-as-a-judge, automated metrics, assertions, and evaluation frameworks.",
      details: `
<h3>Key Concepts</h3>
<p>Systematically evaluate prompts using structured datasets to measure accuracy, consistency, and safety.</p>
<ul>
  <li><strong>Deterministic Checks:</strong> Run code validations to verify JSON formats and key matches.</li>
  <li><strong>LLM-as-a-Judge:</strong> Use a separate, high-end model to grade reasoning quality based on evaluation guidelines.</li>
  <li><strong>Golden Datasets:</strong> Run regressions on a standard set of test inputs before upgrading prompts in production.</li>
</ul>
      `,
      fileLink: "../modules/09_prompt_evaluation.md"
    },
    {
      id: "m10",
      title: "Module 10: Prompt Optimization",
      summary: "Reduce costs and latency while maximizing response quality and performance.",
      details: `
<h3>Key Concepts</h3>
<p>Scale applications cost-effectively by reducing token lengths and leveraging model caching.</p>
<ul>
  <li><strong>API-Level Caching:</strong> Keep system instructions and examples static to enable provider caching, saving up to 50% on prefill costs.</li>
  <li><strong>Token Pruning:</strong> Compress context inputs and remove verbose prose to reduce latency and costs.</li>
</ul>
      `,
      fileLink: "../modules/10_prompt_optimization.md"
    },
    {
      id: "m11",
      title: "Module 11: Prompt Security",
      summary: "Harden prompts against injection, jailbreaks, PII leakage, and formatting exploits.",
      details: `
<h3>Key Concepts</h3>
<p>Protect LLM applications from malicious inputs that overwrite system instructions.</p>
<ul>
  <li><strong>Input Sanitization:</strong> Strip out XML delimiters and code characters from user inputs before merging them into templates.</li>
  <li><strong>Layered Defenses:</strong> Implement separate guardrail filters (like Llama Guard) rather than relying only on the system prompt for safety.</li>
</ul>
      `,
      fileLink: "../modules/11_prompt_security.md"
    },
    {
      id: "m12",
      title: "Module 12: Prompt Engineering for AI FDE",
      summary: "Translate business problems into prompt designs, calculate ROI, and align stakeholders.",
      details: `
<h3>Key Concepts</h3>
<p>An FDE translates client requirements and domain rules into secure, reliable, and cost-effective prompt architectures.</p>
<ul>
  <li><strong>Discovery Workshops:</strong> Extract business rules from domain experts to build system rules and few-shot examples.</li>
  <li><strong>Step-by-Step Chains:</strong> Split complex business goals into simple, focused prompts that are easy to test and validate.</li>
</ul>
      `,
      fileLink: "../modules/12_fde_perspective.md"
    }
  ],
  projects: [
    {
      id: "p1",
      title: "Project 1: Enterprise Knowledge Assistant",
      description: "RAG Prompt Compiler. Inject documents into XML schemas and test citation logic.",
      systemPrompt: "You are the Apex Corporate Knowledge Assistant.\nAnswer using ONLY retrieved context documents. Cite source IDs like [Doc-1]. If answer not found, write 'I am sorry, but the provided documentation does not contain the information required to answer your question.'",
      inputs: [
        { name: "query", label: "User Query", type: "text", default: "What is the daily meal limit for business trips?" },
        { name: "context", label: "Retrieved Documents (YAML/JSON)", type: "textarea", default: `[
  {"id": "Doc-1", "title": "WFH Guidelines", "content": "Remote work is limited to 2 days per week."},
  {"id": "Doc-2", "title": "Expense Reimbursement", "content": "Daily meal allowance is capped at $75."}
]` }
      ],
      mockResponses: [
        { match: "meal", text: "According to the Expense Reimbursement guide, the daily meal allowance for business trips is capped at $75 [Doc-2]." },
        { match: "*", text: "I am sorry, but the provided documentation does not contain the information required to answer your question." }
      ]
    },
    {
      id: "p2",
      title: "Project 2: Customer Support Copilot",
      description: "Dialog Guardrails & Escalation Tester. Test input filters and legal triggers.",
      systemPrompt: "You are a Retail Support Assistant. If client mentions 'sue' or 'lawyer', output [ESCALATE_TO_HUMAN]. If out of scope, output [OUT_OF_SCOPE]. Return policy: store credit within 30 days.",
      inputs: [
        { name: "message", label: "Customer Message", type: "text", default: "I want to sue you guys for this late delivery!" }
      ],
      mockResponses: [
        { match: "sue", text: "[ESCALATE_TO_HUMAN] I am placing you on hold while I connect you with our compliance supervisor." },
        { match: "lawyer", text: "[ESCALATE_TO_HUMAN] I am placing you on hold while I connect you with our compliance supervisor." },
        { match: "python", text: "[OUT_OF_SCOPE] I can only assist you with order status, returns, and store hours." },
        { match: "*", text: "We accept returns for store credit within 30 days of purchase. Please note that we do not issue cash refunds." }
      ]
    },
    {
      id: "p3",
      title: "Project 3: Insurance Claims Assistant",
      description: "Strict JSON Schema Extractor. Test extraction accuracy and JSON parsing.",
      systemPrompt: "You are a Claims Metadata Extractor. Output ONLY a valid JSON object matching the requested schema. No conversation. Schema:\n{\n  'policyholder': string,\n  'claim_type': 'Auto' | 'Home' | 'Life',\n  'loss_val': float\n}",
      inputs: [
        { name: "transcript", label: "Client Incident Statement", type: "textarea", default: "My name is Arthur Dent. On May 12, my car was rear-ended. The repair shop quoted $3,200." }
      ],
      mockResponses: [
        { match: "car", text: "{\n  \"policyholder\": \"Arthur Dent\",\n  \"claim_type\": \"Auto\",\n  \"loss_val\": 3200.0\n}" },
        { match: "*", text: "{\n  \"policyholder\": null,\n  \"claim_type\": \"Unclassified\",\n  \"loss_val\": 0.0\n}" }
      ]
    },
    {
      id: "p4",
      title: "Project 4: Sales Intelligence Copilot",
      description: "Dynamic Persona and LLM-as-a-Judge Scorecard Evaluation.",
      systemPrompt: "You are an Enterprise Sales Advisor. Tailor emails to the prospect's personality style.",
      inputs: [
        { name: "name", label: "Prospect Name", type: "text", default: "Douglas Adams" },
        { name: "persona", label: "Persona (Assertive | Analytical)", type: "text", default: "Assertive" },
        { name: "concern", label: "Primary Concern", type: "text", default: "Reducing cloud costs immediately" }
      ],
      mockResponses: [
        { match: "Assertive", text: "Draft: Hello Douglas, we cut server overhead by 30% without downtime. Let's schedule a brief 10-minute demo this Thursday at 2 PM.\n\nEvaluation Judge Output:\n{\n  \"tone_score\": 3,\n  \"concern_score\": 3,\n  \"length_compliance\": true\n}" },
        { match: "*", text: "Draft: Hi Douglas, our performance benchmarks indicate that implementing our automation cuts cloud costs by 28.4% on average. Are you available for a review next Tuesday?\n\nEvaluation Judge Output:\n{\n  \"tone_score\": 2,\n  \"concern_score\": 3,\n  \"length_compliance\": true\n}" }
      ]
    },
    {
      id: "p5",
      title: "Project 5: Enterprise AI Agent",
      description: "ReAct Agent Loop. Watch reasoning, action, and tool execution.",
      systemPrompt: "You are the IT Ops Agent. Follow the ReAct steps: Thought, Action, Observation. Tools: check_disk_space, clear_tmp_directory.",
      inputs: [
        { name: "alert", label: "System Warning Alert", type: "text", default: "CRITICAL_ALERT: Disk space on production server-01 exceeds 90% threshold." }
      ],
      mockResponses: [
        { match: "*", text: "Thought: Alert reports disk usage exceeds 90% threshold on server-01. I should check disk space.\nAction: check_disk_space('server-01')\nObservation: {\"disk_used_pct\": 94}\n\nThought: Usage is at 94%. I need to clear the /tmp directory to recover space.\nAction: clear_tmp_directory('server-01')\nObservation: {\"freed_bytes\": \"42GB\", \"new_disk_used_pct\": 65}\n\nThought: Disk usage is down to 65%. The alert is resolved.\nFinal Answer: Cleaned 42GB of temp logs on server-01. Usage reduced to 65%." }
      ]
    }
  ],
  quiz: [
    {
      question: "Which prompting technique forces an LLM to generate its intermediate logic steps, improving mathematical and logical reasoning accuracy?",
      options: [
        "Zero-Shot Prompting",
        "Chain-of-Thought (CoT) Prompting",
        "Role Prompting",
        "Positive Reinforcement"
      ],
      answer: 1,
      explanation: "Chain-of-Thought (CoT) prompting forces the model to generate its step-by-step reasoning steps before the final answer, which significantly increases accuracy on logical tasks."
    },
    {
      question: "What is the 'Lost in the Middle' phenomenon in LLM context windows?",
      options: [
        "The model forgetting its system instructions over time.",
        "The model paying the highest attention to the start and end of a prompt, and ignoring information in the middle.",
        "A tokenization error that drops characters in the middle of long strings.",
        "The model getting stuck in infinite agent execution loops."
      ],
      answer: 1,
      explanation: "LLMs pay the highest attention to information placed at the very beginning and very end of a prompt. Context or instructions in the middle are frequently missed or ignored."
    },
    {
      question: "Which semantic versioning update is appropriate for a prompt update that changes output format keys and breaks downstream parsing code?",
      options: [
        "Patch Update (e.g. v1.0.0 -> v1.0.1)",
        "Minor Update (e.g. v1.0.0 -> v1.1.0)",
        "Major Update (e.g. v1.0.0 -> v2.0.0)",
        "Build Update (e.g. v1.0.0 -> v1.0.0-beta)"
      ],
      answer: 2,
      explanation: "A major version increment (e.g., v1.x to v2.x) indicates breaking changes, such as modifying JSON keys, which require updating downstream application parsers."
    },
    {
      question: "In RAG prompt engineering, how do you prevent the LLM from answering queries when retrieved documents do not contain the answer?",
      options: [
        "Raise the temperature parameter to 1.0.",
        "Define strict out-of-bounds fallback instructions in the system prompt.",
        "Use a longer system prompt to overload the attention headers.",
        "Verify semantic distance manually before each API call."
      ],
      answer: 1,
      explanation: "Explicit grounding guidelines (e.g., 'If not found in the documents, reply with a set fallback statement') are the primary defense against factual hallucinations in RAG prompts."
    },
    {
      question: "What is the primary security risk of allowing unsanitized user inputs to be merged directly into prompt templates?",
      options: [
        "Prompt Injection",
        "Token Exhaustion",
        "Model Drift",
        "System Latency"
      ],
      answer: 0,
      explanation: "Prompt Injection occurs when a malicious user inputs commands that overwrite system instructions and hijack the model's behavior."
    }
  ]
};
