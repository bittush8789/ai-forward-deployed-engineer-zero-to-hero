# 07 Tailwind CSS

## Industry Explanation
Tailwind CSS has become the de‑facto utility‑first framework for building fast, consistent UI at scale. Enterprises adopt it to enforce design‑system tokens, reduce CSS debt, and accelerate development across large teams.

## Enterprise Architecture
- Tailwind is integrated into the build pipeline (PostCSS, Vite, Webpack) and compiled to a single CSS bundle delivered via CDN.
- Design tokens (colors, spacing, typography) are defined in `tailwind.config.js` and shared across micro‑frontends.
- Utility classes prevent cascade conflicts, enabling independent feature teams.

## Business Use Cases
- SaaS admin dashboards with customizable themes per client.
- AI product portals where UI needs rapid iteration and A/B testing.
- Internal tooling platforms that require strict brand compliance.

## Production Design
- Use `purge`/`content` paths to remove unused utilities for smallest bundle size.
- Enable JIT mode for on‑the‑fly class generation.
- Adopt a component library (e.g., `@tailwindcss/forms`, `@tailwindcss/typography`).

## Common Failure Modes
- Over‑reliance on arbitrary utility values leading to design drift.
- Missing purge configuration causing bloated CSS.
- Inconsistent naming when mixing Tailwind with custom CSS.

## Optimization Strategies
- Leverage `@apply` in component CSS for reusable patterns.
- Configure `darkMode: "class"` and use `prefers-color-scheme`.
- Use `extract` to generate utility‑only CSS for critical above‑the‑fold components.

## Security Considerations
- Tailwind does not introduce XSS, but avoid injecting arbitrary class strings from user input.
- CSP `style-src` can safely allow Tailwind‑generated stylesheet URLs.

## Accessibility Considerations
- Use Tailwind’s accessible form utilities (`@tailwindcss/forms`).
- Ensure sufficient color contrast with the `contrast` plugin or custom palette.
- Add focus-visible utilities (`focus-visible:outline-none`).

## Best Practices
- Keep design tokens centralized in `tailwind.config.js`.
- Use component‑level CSS files with `@apply` to avoid long class strings.
- Enforce linting with `stylelint-config-tailwindcss`.

## AI FDE Perspective
Front‑end engineers must expose a Tailwind‑driven theming API that can be updated at runtime based on AI‑generated brand palettes, while keeping the compiled bundle minimal.

### Code Example: Tailwind Config & Button Component
```js
// tailwind.config.js
module.exports = {
  content: ["./src/**/*.tsx", "./public/index.html"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#1E40AF", // brand primary
        accent: "#2563EB",
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
```
```tsx
// src/components/Button.tsx
export function Button({ children, onClick }: { children: React.ReactNode; onClick?: () => void }) {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-primary text-white rounded hover:bg-accent focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary"
    >
      {children}
    </button>
  );
}
```
