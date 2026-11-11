# Design system: StudyPlan
Status: approved | Last updated: 2026-11-11

## Principles
- Calm: lots of white space, one accent colour, no decoration.
- Content first: the task list is the interface.
- Thumb-friendly: every primary action is reachable on a phone held in one hand.

## Colour tokens
| Token | Light | Dark | Use for |
|---|---|---|---|
| --bg | #FFFFFF | #0B1120 | Page background |
| --surface | #F8FAFC | #111827 | Cards, dialogs |
| --text | #0F172A | #F1F5F9 | Body text |
| --text-muted | #475569 | #94A3B8 | Secondary text, helper text |
| --border | #E2E8F0 | #1F2937 | Dividers, input borders |
| --accent | #4F46E5 | #818CF8 | Primary buttons, links, focus ring |
| --accent-text | #FFFFFF | #0B1120 | Text on accent |
| --success | #15803D | #4ADE80 | Completed tasks |
| --danger | #B91C1C | #F87171 | Errors, the "Overdue" label, delete |

Rule: components never hard-code a colour. They use the token.

## Typography
Font: Inter, system-ui, sans-serif

| Style | Size / line height | Weight |
|---|---|---|
| H1 | 28 / 36 px | 700 |
| H2 | 20 / 28 px | 600 |
| Body | 16 / 24 px | 400 |
| Small | 14 / 20 px | 400 |

## Spacing, radius, shadow
- Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64 px. Nothing else.
- Radius: 8 px for inputs and buttons, 12 px for cards, 16 px for dialogs.
- Shadow: one level (0 1px 2px rgba(0,0,0,0.06)), cards only.

## Components
Library: shadcn/ui

- Button: variants primary, secondary, ghost, destructive; sizes sm (32 px) and md (44 px); states default, hover, focus, disabled, loading (spinner replaces the label and the width doesn't change).
- Input: label above, helper text below, error text below in --danger; states default, focus, disabled, error.
- Checkbox (task): 24 px box inside a 44 px tap area; done tasks get --text-muted and a strikethrough.
- Card: --surface, 16 px padding, 12 px radius, 1 px --border.
- Dialog: used for delete confirmation only; the destructive button is on the right.
- Toast: bottom centre, 4 seconds, one at a time.
- Empty state: one sentence and one primary button.
- Loading: skeleton rows in the shape of the list; never a blank screen.

## Layout
- Breakpoints: 640, 768, 1024 px. Mobile-first.
- Max content width: 720 px, centred. Page padding 16 px on phones, 24 px from 768 px.

## Accessibility
- Text contrast at least 4.5:1 in both themes.
- Every interactive element is reachable by keyboard and has a visible 2 px --accent focus ring.
- Tap targets at least 44x44 px.
- Inputs have visible labels; the "Overdue" state is text, not colour alone.

## Voice
Short, friendly, specific. Buttons are verbs: "Save plan", not "Submit". Errors say what to do: "Title is required".

## Open questions
None.
