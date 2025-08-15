# AGENTS.md

## Build, Lint, and Test

- **svelte5-mandiri**:
  - Dev: `npm run dev` (or `pnpm run dev`)
  - Build: `npm run build`
  - Type/lint: `npm run check`
  - Single test: No formal suite; use `npm run check` or test manually.
- **friendly-snippets**:
  - Lint: `npx prettier --write <file>`
  - Single test: Open in VSCode and check for errors.
- **rocket-test (Rust)**:
  - Test: `cargo test` (in `rocket-test/rocket-test`)
  - Single test: `cargo test <test_name>`
- **Other projects**: See each subproject’s README or package.json for test commands.

## Code Style Guidelines

- **Imports**: Use ES modules; group external before internal.
- **Formatting**: Use Prettier. JSON: 4 spaces. JS/TS: 4 spaces. Prettier: `singleQuote: true`, `trailingComma: all`, `printWidth: 100-110`.
- **Types**: Use TypeScript where possible. Prefer explicit types.
- **Naming**: camelCase (vars/fns), PascalCase (components/classes), kebab-case (files).
- **Error Handling**: Use try/catch for async; validate JSON; handle Svelte errors gracefully; always log unexpected errors.
- **Docs**: Update `README.md`/`API_ENDPOINTS.md` for new features or API changes.
- **Dependencies**: Keep up to date; run `npm audit` regularly.
- **CI/Formatting**: JSON files are auto-formatted in CI with Prettier (`--tab-width 4 --parser json --write **/*.json`).

## Agentic Best Practices

- Follow these conventions for all code, automation, and PRs.
- If you find new style or lint rules (Cursor/Copilot), add them here.
- Be explicit in error handling and type usage. Prefer clarity over brevity.
- On every update, check for `.cursor/rules/` and `.github/copilot-instructions.md` and summarize their rules here.

*This file is for agentic coding agents. Adhere strictly to these guidelines for consistency and maintainability.*
