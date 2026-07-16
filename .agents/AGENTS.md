# Profile README Design Guidelines

Any future updates or additions to this repository's profile page must follow these design guidelines:

1. **Beautify README Standards**:
   - Take active inspiration from [beautify-github-readme](https://github.com/oil-oil/beautify-github-readme).
   - Treat SVGs as the visual layer and Markdown as the content/story layer.
   - Maintain a cohesive visual story tailored to the "Android Artist" theme (Android slate, Kotlin violet, and Compose blue-green accents).

2. **Asset Design & Spacing**:
   - Keep the design of visual cards in `assets/` clean and spacious.
   - Prevent text/line congestion. Ensure generous margins and line heights (e.g. at least 20px-24px for descriptions, and clear separation between descriptions and action badges).
   - Use dynamic colors/theme support via `@media (prefers-color-scheme: dark)` inside SVGs so they render correctly on both light and dark GitHub backgrounds.

3. **Section Dividers**:
   - Prefer the custom gradient [divider.svg](file:///Users/deardhruv/Dhruv/work/dhruv/dhruv-git/DearDhruv/assets/divider.svg) over standard markdown line elements (`---`) to separate sections cleanly.
