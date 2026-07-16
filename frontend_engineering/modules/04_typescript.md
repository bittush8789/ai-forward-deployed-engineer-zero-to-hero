# 04 TypeScript

## Industry Explanation
TypeScript has become the de‑facto standard for large‑scale front‑end codebases. It adds static typing to JavaScript, enabling early error detection, clearer APIs, and better IDE support—crucial for enterprise teams maintaining thousands of components and integrating AI services.

## Enterprise Architecture
In enterprise projects, TS source is compiled to ES6+ bundles via build pipelines (Webpack, Vite, esbuild). Monorepos (Nx, Turborepo) allow sharing type definitions across micro‑frontends and backend services, ensuring contract consistency between UI and AI APIs.

## Business Use Cases
- AI‑driven SaaS dashboards where typed data models prevent runtime crashes.
- Multi‑tenant platforms with per‑tenant feature flags typed via discriminated unions.
- Complex form handling for AI prompt engineering tools.

## Production Design
- Use `tsconfig.json` with `strict: true`, `noImplicitAny`, and `paths` aliases for shared modules.
- Generate declaration files (`.d.ts`) for shared SDKs (LLM client libraries).
- Integrate type‑checked GraphQL or OpenAPI client generators.

## Common Failure Modes
- Over‑using `any` undermines type safety.
- Mismatched type definitions between front‑end and backend leading to runtime API errors.
- Slow incremental builds due to large `node_modules`.

## Optimization Strategies
- Enable `isolatedModules` and `incremental` for faster compilation.
- Leverage `esbuild` or `swc` for high‑speed transpilation.
- Use path mapping to avoid deep relative imports.

## Security Considerations
- Types alone don’t secure data; always validate inputs on the server.
- Avoid exposing secret keys in client‑side config—keep them out of compiled bundles.

## Accessibility Considerations
- Type definitions for ARIA props (e.g., `aria-label?: string`) help ensure accessibility is not omitted.
- Use strict `enum` types for keyboard navigation states.

## Best Practices
- Adopt `interface` for component props and `type` for union types.
- Prefer immutable data structures (`ReadonlyArray`, `Readonly<T>`).
- Enforce lint rules (`@typescript-eslint/strict-boolean-expressions`).

## AI FDE Perspective
Front‑end engineers expose typed SDKs for AI services, enabling consumers to catch mismatched request shapes at compile time, improving reliability of LLM integrations.

### Code Example: Typed AI Chat Client
```ts
// src/api/chatClient.ts
import type { ChatMessage, ChatResponse } from "./types";

export async function sendMessage(messages: ChatMessage[]): Promise<ChatResponse> {
  const resp = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });
  if (!resp.ok) throw new Error(`Chat API error: ${resp.status}`);
  return resp.json();
}
```

```ts
// src/api/types.ts
export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatResponse {
  id: string;
  created: number;
  choices: Array<{ index: number; message: ChatMessage }>; 
}
```
