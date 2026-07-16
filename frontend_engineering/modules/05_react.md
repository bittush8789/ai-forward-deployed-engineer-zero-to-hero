# 05 React

## Industry Explanation
React dominates modern enterprise front‑ends due to its component‑driven model, virtual DOM performance, and ecosystem of state‑management libraries. Large SaaS products (e.g., Shopify, Slack) rely on React for reusable UI blocks and rapid feature delivery.

## Enterprise Architecture
React apps are typically built as a monorepo of shared component libraries (Storybook, Bit) and deployed via CI/CD pipelines to CDNs. Server‑side rendering (SSR) with frameworks like Next.js or Remix improves SEO for AI product landing pages.

## Business Use Cases
- AI‑driven chat assistants embedded in customer‑support portals.
- Real‑time analytics dashboards visualising model metrics.
- Multi‑tenant SaaS admin consoles with role‑based UI components.

## Production Design
- Use functional components with hooks.
- Leverage TypeScript for prop typing.
- Adopt a design‑system (e.g., Radix UI + Tailwind) for consistency.
- Implement code‑splitting with `React.lazy` and `Suspense`.

## Common Failure Modes
- Over‑rendering leading to UI jank.
- Memory leaks from stale subscriptions.
- Prop‑drilling causing brittle component hierarchies.

## Optimization Strategies
- Memoize heavy components with `React.memo`.
- Use `useCallback`/`useMemo` for stable references.
- Enable automatic static optimization in Next.js.

## Security Considerations
- Sanitize any HTML injected into component props.
- Enforce CSP and avoid `dangerouslySetInnerHTML` unless absolutely necessary.
- Store API keys in server‑only environment variables.

## Accessibility Considerations
- Use semantic HTML elements (`<button>`, `<nav>`).
- Add ARIA roles and live regions for dynamic AI responses.
- Ensure focus is managed correctly after modal dialogs.

## Best Practices
- Keep components small and focused (single responsibility).
- Write unit tests with React Testing Library and end‑to‑end tests with Cypress.
- Use ESLint rules `react-hooks/exhaustive-deps`.

## AI FDE Perspective
Front‑end engineers must expose clean hooks for AI services – e.g., a `useChatStream` hook that abstracts token streaming, retries, and error handling while keeping the UI responsive.

### Code Example: AI Chat Component
```tsx
import { useState, useEffect, useRef } from "react";
import { sendMessage } from "../api/chatClient";

interface Message { role: "user" | "assistant"; content: string; }

export function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const abortRef = useRef<AbortController | null>(null);

  const handleSend = async () => {
    const userMsg: Message = { role: "user", content: input };
    setMessages((m) => [...m, userMsg]);
    setInput("");
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    try {
      const resp = await sendMessage([...messages, userMsg]);
      setMessages((m) => [...m, { role: "assistant", content: resp.choices[0].message.content }]);
    } catch (e) {
      console.error(e);
      setMessages((m) => [...m, { role: "assistant", content: "Error communicating with AI service." }]);
    }
  };

  return (
    <div className="flex flex-col h-full p-4">
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role === "assistant" ? "bg-gray-100 p-2 rounded" : "bg-blue-100 p-2 rounded self-end"}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border rounded p-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          aria-label="Chat input"
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}
```
