# UI Design

## Design System
- **Library**: {{shadcn/ui | Material | custom}}
- **Tokens**: spacing, color, typography defined in {{path}}
- **Accessibility target**: WCAG 2.2 AA (NFR-USA-01)

## Screen Inventory

| ID    | Screen              | Purpose                        | Entry points           | Related UC |
|-------|---------------------|--------------------------------|------------------------|------------|
| S-01  | Landing             | Pitch + signup CTA             | `/`                    | UC-001     |
| S-02  | Sign up             | Create account                 | Landing CTA            | UC-001     |
| S-03  | Verify email        | Confirmation / resend          | Email link             | UC-001     |
| S-04  | Login               | Authenticate                   | Any protected route    | UC-002     |
| S-05  | Dashboard           | Post-login home                | After login            | {{...}}    |

## States per Screen

Each interactive screen must define:

- **Default / empty**
- **Loading**
- **Error** (user-recoverable vs. not)
- **Success**
- **Disabled / permission-denied**

## Navigation Map

```
Landing ─▶ Sign up ─▶ Verify email ─▶ Dashboard
   ▲                                      │
   └──────────── Logout ◀─────────────────┘
```

## Responsive Breakpoints

| Name   | Width      |
|--------|------------|
| mobile | < 640 px   |
| tablet | 640–1024   |
| desktop| > 1024     |

## Interaction Rules

- Primary action buttons: right-aligned in modals
- Destructive actions: require explicit confirm (no single-click deletes)
- Form validation: inline on blur; summary on submit
- Empty states: always include a next action
- Loading: skeleton for > 300ms; spinner only for indeterminate waits

## Mockups

Link to Figma / design files: {{URL}}
