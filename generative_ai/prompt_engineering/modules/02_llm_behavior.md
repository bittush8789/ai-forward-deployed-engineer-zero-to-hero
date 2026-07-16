# Module 2: LLM Behavior Understanding

## 1. Industry Explanation
Large Language Models (LLMs) do not "read" or "understand" language in the human sense. They process text as sequence predictions over mathematical representations of word fragments called tokens. Consequently, their behavior is governed by probability distributions rather than logical rules. 

Understanding how LLMs interpret prompts requires looking at their inner mechanics: context window limitations, attention degradation (e.g., the "Lost in the Middle" phenomenon), tokenization quirks, and probabilistic generation risks. Designing reliable prompts requires shifting from human-centric writing to token-optimized instruction layouts.

## 2. Enterprise Use Cases
- **Contract Summarization**: Condensing multi-hundred-page legal agreements into core covenants without exceeding the context window or losing key details.
- **Enterprise Search Verification**: Analyzing structured corpus documents to verify if an incoming search result actually contains the answer, rather than hallucinating facts.
- **Data Extractor Agents**: Parsing logs, transaction trails, or configuration sheets to extract structured database fields.

## 3. Business Examples
An enterprise needs to extract lines items from a 50-page invoice document. 
- **The Tokenization Gotcha**: Numbers like `10,482.50` might get tokenized as `["10", ",", "48", "2", ".", "50"]`. If the prompt asks the model to "perform mathematical verification of sum totals," the token segmentation may lead to arithmetic inaccuracies because LLMs do not calculate mathematically; they predict tokens.
- **Correct Pattern**: Inject raw text parsing instructions, or extract variables into JSON and run a deterministic Python math verification script instead of asking the LLM to add numbers.

## 4. Common Failure Modes
- **Lost in the Middle**: Placing critical instructions or primary context data in the middle of a massive prompt. LLMs pay the highest attention to the very beginning and very end of prompts.
- **Over-reliance on Mathematical Logic**: Expecting the LLM to perform complex numeric calculations inside the context window.
- **Hallucination under Pressure**: When a prompt asks the LLM to answer a question but the answer is not in the provided text, the LLM often invents an answer to fulfill the instruction rather than saying "I don't know."

## 5. Governance Considerations
- **Risk Grading**: Model responses must be monitored for factual variance. Enterprise policies must mandate that LLMs never serve as the final authority on critical information (e.g., credit approvals, health diagnoses) without a human supervisor.
- **Stochastic Drift**: LLM behaviors change during updates. A prompt that works on a specific version of a model may behave differently when the cloud provider rolls out minor model updates.

## 6. Security Risks
- **Attention Overrides**: If the user injection is extremely long, the attention heads may focus entirely on user input, ignoring the core system guidelines defined at the top of the prompt.
- **PII Inference**: LLMs can combine unrelated fragments of context to infer private information that should have been redacted.

## 7. Best Practices
- **Anchor Key Instructions**: Place core commands, rules, and output schemas at the very bottom of the prompt context, close to the generation trigger.
- **Provide "Grounding" Flags**: Instruct the model to limit its answer space exclusively to a provided corpus (e.g., *"Use ONLY the facts inside the <context> tags. If not found, write 'NOT_FOUND'"*).
- **Format Numbers for Tokenizers**: Use spaces or structured tags around critical codes (like IDs or financial figures) to keep them from being fragmented during tokenization.

## 8. Evaluation Methods
- **Context Injection Testing**: Insert synthetic facts deep inside long prompts and measure if the model retrieves them successfully (Needle-in-a-Haystack tests).
- **Factual Grounding Scans**: Use semantic metrics (like RAGAS or G-Eval) to verify that generated sentences map directly to sentences in the context documents.

## 9. Production Considerations
- **Context Window Squeeze**: Larger context windows cost more money and increase latency. Prune irrelevant database rows or documents before passing them into the prompt.
- **Time-to-First-Token (TTFT)**: Long system prompts increase prefill calculation times. Cache system prompts using provider-level context caching techniques.

## 10. AI FDE Perspective
An AI FDE must balance context window usage against solution accuracy. When client stakeholders request analyzing entire PDF libraries in single prompts, the FDE should advise on breaking documents into indexed chunks, using a hybrid vector-semantic database retrieval layer, and passing only relevant context to the prompt.
