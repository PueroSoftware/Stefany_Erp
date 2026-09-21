UX/UI Design Guidelines for tienda-fabril

Color tokens (corporate palette):
- Primary: #1D1D1B
- Secondary: #465A56
- Tertiary: #6E807F
- Accent: #EADDCC
- Background: #F7F7F5

Typography
- Use system sans fonts (Arial/Inter as fallback). Maintain readable sizes: body 14–16px, headings 18–22px.
- Ensure high contrast: text on surfaces should have sufficient contrast against backgrounds.

UI Components (RN Web/Android)
- Buttons: rounded with subtle elevation; primary color as background; disabled state dimmed.
- Inputs: rounded with clear focus outline for accessibility; placeholder color muted.
- Selects/Enums: prefer chips or segmented controls for enums; use toggles for boolean-like states.
- Chips: visualize enum categories (Base, Aroma, Color, etc.) as chips to improve quick recognition.
- Layout: responsive flex layouts; two-column wireframe should adapt to tablet/phone widths.

Enum visual mapping (priority to clarity)
- Enums from the DB should map to intuitive UI controls (see ux/enums-ui-mapping.json).
- Use color accents to differentiate enum groups but maintain the corporate color tokens.
- Prefer progressive disclosure: show essential enums first; reveal detailed options on demand.

Accessibility
- Ensure semantic roles where possible; provide ARIA-like labels for web and accessibilityLabel for RN.
- Keyboard navigation support for web; ensure tab order is logical.

Cross-platform notes (React Native Web + Android)
- Use platform-specific selectors where needed; fall back to RN components for consistency.
- Abstract colors, typography, and spacing into tokens to keep a single source of truth.
- Test layouts on both web and mobile simulators to ensure spacing scales well.

Roadmap (next steps)
- Extend with a design system document, token file, and a starter RN web components library.
- Add sample screens (Login, Proveedores, Categoría de Materia, Materia Prima) implemented in React Native.
