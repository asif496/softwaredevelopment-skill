# Design system guide (docs/DESIGN_SYSTEM.md)

The design system is the visual rulebook: colours, type, spacing and components. Without it an agent picks slightly different values on every screen, and by screen ten the app looks like it was built by ten people. With it, screen 20 matches screen 1.

Skip this doc for project types with no screens (api, cli, automation).

## Before writing

Read the PRD's users, screens and constraints. If the look isn't decided, ask for one of:

- a reference app or site they like, and what they like about it
- three adjectives (calm, dense, playful, serious...)
- a screenshot or brand colours
- light, dark or both; mobile-first or desktop-first

If they have a component library in mind, use it. Otherwise propose one that suits the stack and say why in a line.

## Sections

**Principles.** Three or four lines that settle arguments later: "one accent colour; everything else is neutral", "content first, lots of white space".

**Colour tokens.** A table of `Token | Light | Dark | Use for`. The usual set: `--bg`, `--surface`, `--text`, `--text-muted`, `--border`, `--accent`, `--accent-text`, `--success`, `--warning`, `--danger`. Give hex values for both themes even if v1 ships only one; adding dark mode later without tokens means touching every component. State the rule: components never hard-code a colour; they use the token.

**Typography.** Font and fallback stack, then a table of `Style | Size / line height | Weight` for H1, H2, H3, body, small. Four or five sizes are enough.

**Spacing, radius, shadow.** A fixed spacing scale (4, 8, 12, 16, 24, 32, 48, 64 and nothing else), a radius per element type, one or two shadow levels. A fixed scale is what makes layouts look aligned.

**Components.** Name the library, then for each component the allowed variants, sizes and every state: default, hover, focus, disabled, loading, error, empty. Cover at least buttons, inputs (where the label, helper and error text sit), cards, dialogs, toasts, navigation and empty states. The states an agent forgets are loading, error and empty, so spell those out.

**Layout.** Breakpoints, max content width, page padding, and whether it is mobile-first.

**Accessibility.** Text contrast at least 4.5:1 (3:1 for large text). Every interactive element reachable by keyboard with a visible focus ring. Tap targets at least 44x44 px. Inputs have labels, not just placeholders. Colour is never the only signal.

**Voice.** Short, friendly, specific. Buttons are verbs ("Save plan", not "Submit"). Give two or three example error messages in the house style.

## Self-check

- Dark values exist for every colour token.
- Check the contrast of text on background and accent-text on accent, in both themes, and adjust if under 4.5:1.
- Every component lists disabled, loading, error and empty states where they apply.
- Only one accent colour.
- The no-hard-coded-values rule is stated.
- Nothing here contradicts a screen or constraint in the PRD.

## Common mistakes

- Light mode only, with dark mode "later".
- Buttons defined but no input, error or empty states.
- Ten shades of grey with no rule for which to use.
- Vague principles ("modern and clean") that settle nothing.

## Setup after approval

A `/styleguide` page (dev only) that renders every token and component in every state. It is the fastest way to see whether the system is being followed.
