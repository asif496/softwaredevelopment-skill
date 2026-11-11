# Design system: {{APP_NAME}}
Status: draft | Last updated: {{DATE}}

## Principles
- <Principle that settles an argument, e.g. "one accent colour; everything else is neutral">

## Colour tokens
| Token | Light | Dark | Use for |
|---|---|---|---|
| --bg | <hex> | <hex> | Page background |
| --surface | <hex> | <hex> | Cards, dialogs |
| --text | <hex> | <hex> | Body text |
| --text-muted | <hex> | <hex> | Secondary text |
| --border | <hex> | <hex> | Dividers, input borders |
| --accent | <hex> | <hex> | Primary buttons, links |
| --accent-text | <hex> | <hex> | Text on accent |
| --success | <hex> | <hex> | Success states |
| --danger | <hex> | <hex> | Errors, destructive actions |

Rule: components never hard-code a colour. They use the token.

## Typography
Font: <font>, <fallback stack>

| Style | Size / line height | Weight |
|---|---|---|
| H1 | <px / px> | <weight> |
| H2 | <px / px> | <weight> |
| Body | <px / px> | <weight> |
| Small | <px / px> | <weight> |

## Spacing, radius, shadow
- Spacing scale: <4, 8, 12, 16, 24, 32, 48, 64>. Nothing else.
- Radius: <px per element type>
- Shadow: <levels and where each is used>

## Components
Library: <library>

- Button: variants <list>; sizes <list>; states default, hover, focus, disabled, loading.
- Input: label above, helper text below, error text below in --danger; states default, focus, disabled, error.
- Card: <padding, radius, border>
- Empty state: <what it contains, e.g. one sentence + one primary button>
- <Other components: dialog, toast, navigation>

## Layout
- Breakpoints: <values>
- Max content width: <px>. <Mobile-first or desktop-first>.

## Accessibility
- Text contrast at least 4.5:1.
- Every interactive element is reachable by keyboard and has a visible focus ring.
- Tap targets at least 44x44 px.

## Voice
<Tone in a few words.> Buttons are verbs.

## Open questions
- [ ] <question>
