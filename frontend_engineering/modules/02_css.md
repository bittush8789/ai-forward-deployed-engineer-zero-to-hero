# 02 CSS

## Industry Explanation
CSS powers the visual language of enterprise web applications—from data‑heavy SaaS dashboards to AI product UIs. Modern teams treat CSS as a first‑class asset, leveraging design systems, theming, and performance‑focused tooling to ensure consistency at scale.

## Enterprise Architecture
In large organisations, CSS is compiled via build pipelines (PostCSS, Webpack, Vite) and served from CDNs. Scoped styling approaches (CSS Modules, BEM, utility‑first Tailwind) prevent style leakage across micro‑frontends.

## Business Use Cases
- Real‑time analytics dashboards with complex grid layouts
- AI‑driven reporting portals requiring dark‑mode theming
- Multi‑tenant SaaS platforms with brandable UI skins

## Production Design
Adopt a modular architecture: base resets, design tokens, component libraries. Use CSS Grid for complex data tables, Flexbox for responsive cards, and media queries for breakpoints. Minify and purge unused styles in CI.

## Common Failure Modes
- Global CSS conflicts causing layout breaks across teams
- Over‑specific selectors leading to maintenance pain
- Unoptimized selectors causing repaint/reflow performance hits

## Optimization Strategies
- Use CSS variables for theming and runtime token updates
- Enable `prefers-color-scheme` media queries for dark mode
- Leverage critical CSS extraction for above‑the‑fold content

## Security Considerations
Prevent CSS‑based attacks (e.g., CSS injection) by sanitizing any dynamic style values. Enforce CSP `style-src` to restrict inline styles.

## Accessibility Considerations
- Ensure sufficient color contrast (WCAG 2.1 AA)
- Provide focus indicators and avoid hidden content via `display:none` for assistive tech
- Use `:focus-visible` for keyboard navigation cues

## Best Practices
- Follow a design‑system token hierarchy (color, spacing, typography)
- Prefer utility‑first or component‑scoped styles over deep nesting
- Run stylelint in CI to enforce conventions

## AI FDE Perspective
Front‑end engineers must expose style hooks for AI‑generated theming (e.g., dynamic brand palettes) while maintaining performance and security across deployments.
