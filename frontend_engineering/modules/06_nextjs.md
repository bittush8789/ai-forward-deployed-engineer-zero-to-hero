# 06 Next.js

## Industry Explanation
Next.js is the premier framework for building production‑grade, server‑rendered React applications. Enterprises adopt it for its hybrid rendering model (SSR, SSG, ISR), built‑in routing, and edge‑runtime support—crucial for SEO‑friendly AI product pages and low‑latency dashboards.

## Enterprise Architecture
- Deploy Next.js on Vercel, Netlify, or custom edge platforms (AWS CloudFront, Cloudflare Workers).
- Use monorepos to share UI components and TypeScript types across micro‑frontends.
- Leverage Incremental Static Regeneration (ISR) for dynamic AI content that updates without full rebuilds.

## Business Use Cases
- AI SaaS landing pages with server‑rendered SEO metadata.
- Real‑time AI analytics dashboards that pre‑render static reports.
- Multi‑tenant portals where each tenant gets a statically generated homepage but live chat components via API routes.

## Production Design
- Enable `image` optimization for AI‑generated visualizations.
- Use `getServerSideProps` for authenticated AI API calls.
- Implement API routes as thin wrappers around backend AI services (e.g., `/api/chat`).
- Deploy with CI/CD pipelines that run `next build` and perform lint/tests.

## Common Failure Modes
- Over‑using `getServerSideProps` causing server overload.
- Misconfigured caching headers leading to stale AI responses.
- Large bundle sizes from unoptimized third‑party libraries.

## Optimization Strategies
- Use dynamic imports for heavy AI widgets.
- Enable `next/script` with `strategy="lazyOnload"` for third‑party scripts.
- Apply `webpackBundleAnalyzer` to prune unused code.

## Security Considerations
- Store API keys in server‑only environment variables (`process.env`).
- Set CSP and `X-Content-Type-Options` headers via `next.config.js`.
- Rate‑limit API routes that proxy LLM calls.

## Accessibility Considerations
- Use Next.js built‑in `Head` component for accessible page titles and meta.
- Ensure all interactive components have keyboard support.
- Provide ARIA live regions for streaming AI outputs.

## Best Practices
- Keep pages small; extract UI into reusable components.
- Write end‑to‑end tests with Playwright.
- Use `next-seo` for managing SEO metadata.

## AI FDE Perspective
Front‑end engineers expose server‑side endpoints that abstract LLM throttling, logging, and auditing, while the UI consumes them via typed hooks for a seamless AI experience.

### Code Example: API Route for AI Chat (TypeScript)
```ts
// pages/api/chat.ts
import type { NextApiRequest, NextApiResponse } from "next";
import { sendMessage } from "../../../src/api/chatClient";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();
  const { messages } = req.body;
  try {
    const response = await sendMessage(messages);
    res.status(200).json(response);
  } catch (e) {
    console.error(e);
    res.status(500).json({ error: "AI service error" });
  }
}
```

```tsx
// pages/chat.tsx
import { ChatBox } from "../components/ChatBox";
export default function ChatPage() {
  return (
    <main className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">AI Assistant</h1>
      <ChatBox />
    </main>
  );
}
```
