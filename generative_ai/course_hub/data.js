// Unified Database - Generative AI & LLM Academy Dashboard
const COURSE_DATA = {
  modules: [
    {
      id: "m1",
      title: "Module 1: LLM Fundamentals",
      summary: "Understand Transformer decoder architectures, BPE tokenization, context lengths, and pre-training datasets.",
      details: `
<h3>Key Concepts</h3>
<p>Large Language Models are based on the Transformer attention mechanism. They process natural language by converting inputs into numeric tokens and predicting subsequent tokens probabilistically.</p>
<h4>1. The Training Lifecycle</h4>
<ul>
  <li><strong>Pre-training:</strong> Training models on raw text datasets to learn grammar, vocabulary, and facts.</li>
  <li><strong>Supervised Fine-Tuning (SFT):</strong> Training the model on instruction-response pairs to teach it how to follow directions.</li>
  <li><strong>Alignment (RLHF/DPO):</strong> Refining models using human feedback to improve safety and helpfulness.</li>
</ul>
      `,
      fileLink: "../modules/01_llm_fundamentals.md"
    },
    {
      id: "m2",
      title: "Module 2: Embeddings",
      summary: "Explore high-dimensional vector representation models, semantic similarity metrics, and index generation.",
      details: `
<h3>Key Concepts</h3>
<p>Embeddings convert unstructured text strings into fixed-length numeric vectors. Semantic search engines compare these vectors to identify relevance, going beyond simple keyword matching.</p>
<h4>1. Mathematical Metrics</h4>
<ul>
  <li><strong>Cosine Similarity:</strong> Measuring the angle between vectors to compare semantic relevance.</li>
  <li><strong>Dot Product Similarity:</strong> Speeding up searches by multiplying normalized vector weights directly.</li>
</ul>
      `,
      fileLink: "../modules/02_embeddings.md"
    },
    {
      id: "m3",
      title: "Module 3: Retrieval-Augmented Generation (RAG)",
      summary: "Master chunking limits, hybrid index searches, reranker modules, and grounding checks.",
      details: `
<h3>Key Concepts</h3>
<p>RAG grounds model responses by retrieving facts from external databases, helping to prevent hallucinations and provide access to real-time information.</p>
<h4>1. Optimization Workflows</h4>
<p>Production RAG systems use a two-stage process: retrieving documents using hybrid vector-keyword searches, and applying cross-encoder rerankers to select the most relevant context chunks.</p>
      `,
      fileLink: "../modules/03_rag.md"
    },
    {
      id: "m4",
      title: "Module 4: Fine-Tuning",
      summary: "Learn full parameter training, supervised dataset format rules, and loss convergence.",
      details: `
<h3>Key Concepts</h3>
<p>Fine-tuning updates model weights to adapt its behavior to specialized tasks, domains, or vocabulary styles.</p>
<h4>1. Supervised Fine-Tuning (SFT)</h4>
<p>Formatting training examples into consistent JSONL structures containing system, user, and assistant roles to teach the model target outputs.</p>
      `,
      fileLink: "../modules/04_fine_tuning.md"
    },
    {
      id: "m5",
      title: "Module 5: LoRA",
      summary: "Explore Parameter-Efficient Fine-Tuning (PEFT) configurations, matrix decomposition, rank (r), and alpha scaling.",
      details: `
<h3>Key Concepts</h3>
<p>LoRA freezes base model weights and injects trainable rank decomposition matrices into the attention layers, reducing trainable parameters and training costs by up to 99%.</p>
<h4>1. Hyperparameter Settings</h4>
<ul>
  <li><strong>Rank (r):</strong> The rank of trainable adapters; use 8 or 16 for standard tasks, and 32 or 64 for complex domains.</li>
  <li><strong>Alpha (α):</strong> Scaling factor; usually configured as double the rank value to control adapter weights.</li>
</ul>
      `,
      fileLink: "../modules/05_lora.md"
    },
    {
      id: "m6",
      title: "Module 6: QLoRA",
      summary: "Master NF4 4-bit quantization math, double quantization storage, and low-memory training pipelines.",
      details: `
<h3>Key Concepts</h3>
<p>QLoRA combines 4-bit NormalFloat (NF4) quantization with 16-bit LoRA adapters, allowing developers to fine-tune large models on single, cost-effective GPUs.</p>
<h4>1. Double Quantization (DQ)</h4>
<p>Quantizing the quantization scale constants themselves to save an average of 0.37 bits per parameter, reducing memory footprints without loss in accuracy.</p>
      `,
      fileLink: "../modules/06_qlora.md"
    },
    {
      id: "m7",
      title: "Module 7: Function Calling",
      summary: "Analyze tool definition schemas, API extraction loops, validation states, and recovery workflows.",
      details: `
<h3>Key Concepts</h3>
<p>Function calling allows the LLM to output structured JSON arguments for external APIs, bridging the gap between text generation and external services.</p>
<h4>1. Execution Loops</h4>
<p>The host application validates model arguments, executes the requested APIs in a secure sandbox, and feeds the results back to the model's context.</p>
      `,
      fileLink: "../modules/07_function_calling.md"
    },
    {
      id: "m8",
      title: "Module 8: Structured Output",
      summary: "Verify schema adherence, enforce Pydantic formats, and build error-correction pipelines.",
      details: `
<h3>Key Concepts</h3>
<p>Structured output forces the model to conform strictly to JSON schemas, ensuring responses can be parsed and processed by downstream databases and APIs.</p>
<h4>1. guided Generation</h4>
<p>Using inference-level tools (like Outlines) to adjust token selection probabilities directly, ensuring outputs are always syntactically valid JSON.</p>
      `,
      fileLink: "../modules/08_structured_output.md"
    },
    {
      id: "m9",
      title: "Module 9: AI Agents",
      summary: "Deploy ReAct loops, state graph routing, multi-agent platforms, and state memory.",
      details: `
<h3>Key Concepts</h3>
<p>AI agents plan tasks, make decisions, select tools, and manage execution loops autonomously, transforming simple chat interfaces into active digital workers.</p>
<h4>1. Orchestration Frameworks</h4>
<p>Using state charts (like LangGraph) to define agent workflows as structured graphs, ensuring runs remain reliable and traceable.</p>
      `,
      fileLink: "../modules/09_ai_agents.md"
    }
  ],
  projects: [
    {
      id: "p1",
      title: "Project 1: Enterprise Knowledge Assistant",
      description: "Vector Index Search. Input raw text passages and query them to see Cosine Similarity matching scores.",
      systemPrompt: "Search Index Vocabulary: [remote, work, travel, expense, meal, laptop, monitor, equipment]\nModel calculates Cosine Similarity over unit-normalized bag-of-words vectors.",
      inputs: [
        { name: "query", label: "Semantic Search Query", type: "text", default: "What are the rules for travel meal expenses?" },
        { name: "corpus", label: "Policy Context Corpus", type: "textarea", default: "Doc 1: Remote work is capped at 2 days per week.\nDoc 2: Travel meal allowance is capped at $75 per day." }
      ],
      mockResponses: [
        { match: "meal", text: "Match Result [Cosine Similarity: 0.8165]\nDocument ID: Doc 2\nContent: Travel meal allowance is capped at $75 per day." },
        { match: "remote", text: "Match Result [Cosine Similarity: 0.7071]\nDocument ID: Doc 1\nContent: Remote work is capped at 2 days per week." },
        { match: "*", text: "Match Result [Cosine Similarity: 0.0000]\nNo relevant document matches found in vocabulary index." }
      ]
    },
    {
      id: "p2",
      title: "Project 2: Insurance Underwriting Copilot",
      description: "Function Calling JSON Validator. Simulates validation of generated parameters against schemas.",
      systemPrompt: "Tool: fetch_building_hazard_data(building_age: int, roof_material: str)\nConstraint: Allowed roof materials: ['wood', 'asphalt', 'tile', 'metal']. Output raw JSON.",
      inputs: [
        { name: "args", label: "Model Output Tool Arguments (JSON)", type: "textarea", default: '{"building_age": 66, "roof_material": "wood"}' }
      ],
      mockResponses: [
        { match: "wood", text: "[ARGUMENTS_VALIDATED]\nDatabase Record: { \"fire_risk_rating\": 4, \"structural_risk_rating\": 3 }\n\nStructured Underwriting Decision:\n{\n  \"underwriting_status\": \"DECLINE\",\n  \"scorecard\": { \"fire_score\": 4, \"structural_score\": 3 },\n  \"decision_rationale\": \"Property risk limits exceeded. Fire and structural hazard scores too high.\"\n}" },
        { match: "asphalt", text: "[ARGUMENTS_VALIDATED]\nDatabase Record: { \"fire_risk_rating\": 2, \"structural_risk_rating\": 1 }\n\nStructured Underwriting Decision:\n{\n  \"underwriting_status\": \"APPROVE\",\n  \"scorecard\": { \"fire_score\": 2, \"structural_score\": 1 },\n  \"decision_rationale\": \"Property risks lie within standard coverage guidelines.\"\n}" },
        { match: "*", text: "[VALIDATION ERROR] Invalid argument parameters. Ensure roof_material is one of ['wood', 'asphalt', 'tile', 'metal']." }
      ]
    },
    {
      id: "p3",
      title: "Project 3: Customer Support Copilot",
      description: "IT Service Agent execution chain. Verify state memory tracking during execution.",
      systemPrompt: "Agent Memory Schema: { customer_id: str, order_number: str, resolved: bool, log: list }\nTools: identify_customer, fetch_order_details.",
      inputs: [
        { name: "customer", label: "Customer Name", type: "text", default: "Fenchurch Kent" },
        { name: "order", label: "Order Number ID", type: "text", default: "ORD-104" }
      ],
      mockResponses: [
        { match: "*", text: "Thought: Verifying customer account logs...\nAction: identify_customer('Fenchurch Kent')\nObservation: Verified Customer ID: CUST-402\n\nThought: Customer is verified. Querying details for order ORD-104...\nAction: fetch_order_details('ORD-104')\nObservation: Found Item: Mechanical Keyboard, Status: IN_TRANSIT\n\nFinal Agent State Memory:\n{\n  \"customer_id\": \"CUST-402\",\n  \"order_number\": \"ORD-104\",\n  \"resolved\": true,\n  \"log\": [\n    \"Tool: identify_customer('Fenchurch Kent') -> CUST-402\",\n    \"Tool: fetch_order_details('ORD-104') -> IN_TRANSIT\"\n  ]\n}" }
      ]
    },
    {
      id: "p4",
      title: "Project 4: Legal Document Assistant",
      description: "Supervised Fine-Tuning dataset compiler. Preview generated JSONL instruction sets.",
      systemPrompt: "SFT Format: { messages: [ { role: 'system', content: str }, { role: 'user', content: str }, { role: 'assistant', content: JSON } ] }",
      inputs: [
        { name: "text", label: "Contract Extract Text", type: "textarea", default: "Governing Law: This agreement shall be governed by and construed in accordance with the laws of the State of Delaware." },
        { name: "law", label: "Target Governing Law", type: "text", default: "Delaware" },
        { name: "status", label: "Jurisdiction Status", type: "text", default: "STANDARD" }
      ],
      mockResponses: [
        { match: "*", text: "Generated SFT JSONL Training Entry:\n{\n  \"messages\": [\n    {\n      \"role\": \"system\",\n      \"content\": \"You are an expert Legal Auditor. Extract the governing law and jurisdiction status from the contract text.\"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"Extract details from: Governing Law: This agreement shall be governed by and construed in accordance with the laws of the State of Delaware.\"\n    },\n    {\n      \"role\": \"assistant\",\n      \"content\": \"{\\\"governing_law\\\": \\\"Delaware\\\", \\\"jurisdiction_status\\\": \\\"STANDARD\\\"}\"\n    }\n  ]\n}" }
      ]
    },
    {
      id: "p5",
      title: "Project 5: Enterprise Multi-Agent Platform",
      description: "State Routing Engine. Evaluates coordination between IT Diagnostic and Database Audit agents.",
      systemPrompt: "Router State Graph: USER -> ROUTER -> IT_DIAGNOSTIC or DB_AUDIT -> COMPLETED -> Final Summary Output.",
      inputs: [
        { name: "task", label: "Agent Task Assignment", type: "text", default: "Run diagnostic scans on the production server." }
      ],
      mockResponses: [
        { match: "server", text: "[ROUTER] Task mentions 'server'. Routing to: IT_DIAGNOSTIC_AGENT\n\n[IT_DIAGNOSTIC_AGENT] Running hardware diagnostic tools...\nObservation: CPU usage 45%, Storage usage 94% (CRITICAL).\n\n[ROUTER] Diagnostic scan finished. Routing back to ROUTER -> COMPLETED\n\nFinal Report:\nIT Diagnostic report complete. Server check: CPU usage 45%, Storage usage 94% (CRITICAL)." },
        { match: "user", text: "[ROUTER] Task mentions 'user'. Routing to: DB_AUDIT_AGENT\n\n[DB_AUDIT_AGENT] Running query checks over account logs...\nObservation: Found 3 failed logins for account admin-01 today.\n\n[ROUTER] Audit check finished. Routing back to ROUTER -> COMPLETED\n\nFinal Report:\nDB Audit query complete. Found 3 failed logins for account admin-01 today." },
        { match: "*", text: "[ROUTER] Unrecognized routing context. Task completed immediately. Output: I cannot determine the destination team for your query." }
      ]
    }
  ],
  quiz: [
    {
      question: "Which component of an enterprise LLM hosting pipeline is responsible for continuous batching and memory management using PagedAttention?",
      options: [
        "Inference engines like vLLM or Triton",
        "Orchestration frameworks like LangChain",
        "Vector databases like ChromaDB",
        "Log tracking systems like MLflow"
      ],
      answer: 0,
      explanation: "vLLM and Triton Inference Server implement key memory optimizations, such as continuous batching and PagedAttention, to maximize throughput and minimize latency."
    },
    {
      question: "What is the primary role of a Cross-Encoder Reranker model in a two-stage retrieval pipeline?",
      options: [
        "To generate vector embeddings for incoming queries",
        "To perform fast, initial document searches",
        "To evaluate relevance between queries and documents directly, improving top-K document relevance",
        "To quantize base weights to 4-bit precision"
      ],
      answer: 2,
      explanation: "Cross-Encoders evaluate the exact relationship between query and context strings, providing highly accurate relevance scores to select the best documents for the context window."
    },
    {
      question: "In LoRA PEFT training, what does the parameter Rank (r) configure?",
      options: [
        "The quantization precision of the base model weights",
        "The dimension size of the low-rank trainable weight matrices",
        "The learning rate multiplier of the optimizer state",
        "The sequence context window threshold"
      ],
      answer: 1,
      explanation: "The rank (r) determines the dimension size of the injected low-rank trainable weight matrices, directly balancing task adaptation capacity and trainable parameters."
    },
    {
      question: "Why does QLoRA utilize 4-bit NormalFloat (NF4) quantization over standard FP4 quantization?",
      options: [
        "FP4 requires double the GPU memory compared to NF4",
        "NF4 is mathematically designed for the normal distribution of neural weights, yielding higher model accuracy",
        "NF4 does not require dequantization during inference steps",
        "NF4 is only compatible with CPU training runs"
      ],
      answer: 1,
      explanation: "NF4 is a specialized data type designed for normally distributed model weights, resulting in significantly less accuracy loss than standard FP4."
    },
    {
      question: "What is the role of a state orchestrator (like LangGraph) in production AI Agent setups?",
      options: [
        "To compute embedding search vectors",
        "To write and compile SFT datasets",
        "To define agent workflows as structured graphs, ensuring reliable transitions and loops",
        "To compress model parameters to 8-bit precision"
      ],
      answer: 2,
      explanation: "State chart orchestrators like LangGraph manage agent runs as structured graphs, ensuring execution states, loops, and tools remain predictable and auditable."
    }
  ]
};
