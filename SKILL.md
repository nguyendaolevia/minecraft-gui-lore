---
name: minecraft-gui-lore
description: Design, rewrite, review, and implement player-facing names and lore for Minecraft server inventory GUIs and menu configuration files. Use when Codex works on GUI item names, lore, tooltips, buttons, rewards, status text, line wrapping, legacy or hex colors, gradients, tiny fonts, Unicode decoration, placeholders, or visual consistency in Minecraft plugins and resource packs.
---

# Minecraft GUI Name & Lore

Create concise, readable, visually balanced Minecraft GUI text with controlled
emphasis, neutral color support, and verified contrast on the actual UI surface.

## Required reference

Read [references/style-guide.md](references/style-guide.md) completely before
creating, rewriting, reviewing, or implementing any GUI name or lore. Treat it
as the authoritative default standard.

## Workflow

1. Inspect the target plugin, configuration format, existing GUI style, audience,
   placeholders, supported text serializer, file encoding, resource-pack font
   providers, and actual background behind each text surface. Treat inventory
   titles and item tooltips separately.
2. Preserve functional placeholders, click semantics, permissions, and config
   syntax while changing only player-facing text unless broader changes are
   requested.
3. Draft the semantic content before adding colors or decoration. Rephrase a
   visibly long line with shorter, equally clear wording before splitting it or
   compensating with layout.
4. Wrap each visible line at a natural phrase boundary. Keep seven displayed
   words as an emergency ceiling, but prefer around 25 visible characters per
   descriptive lore line. Within one descriptive group, keep neighboring lines
   within roughly two visible characters when natural Vietnamese phrasing allows.
   Treat dynamic placeholders, command examples, and click instructions as
   exceptions that must stay readable and semantically intact. Do not split a
   click instruction merely to satisfy the descriptive-line target; if the
   action line is the longest natural unit, keep it whole and balance nearby
   lore around that visual anchor.
5. Balance neighboring lines by rendered visual width, not word count alone. Do
   not pad text with spaces to imitate true justification.
6. Make Minecraft gray (`&7`, `<gray>`, or the serializer-equivalent named
   color) the default tooltip base. Use white (`&f`/`<white>`) selectively.
   For a multi-block tooltip, use one primary accent plus one or two supporting
   accents with stable roles. Do not rely only on the display-name color for
   every highlighted keyword; combine it with one or two harmonious supporting
   colors for actions, values, warnings, or future-state notes. Distribute them
   across meaningful focal points so the tooltip has color rhythm without
   becoming random. Do not leave an information-heavy description entirely
   neutral when it contains clear scan keywords such as feature names, resources,
   destinations, actions, values, or player systems.
7. For a button with one short, obvious action, consider the optional compact
   click-hint pattern in the reference guide. Do not apply it mechanically to
   every button.
8. Explicitly disable inherited italics for item names and lore unless italics
   have a deliberate semantic role. Check serializer tags and component
   decorations because Minecraft item metadata may default to italic. Do not
   mechanically add legacy `&r`: first verify its effect in the target plugin
   because a reset can alter component styling or font fallback.
9. Add bold, tiny font, Unicode, hex colors, or a gradient only when each choice
   has a clear purpose and enough contrast on the real background.
10. Match the user's requested output format. When editing files, preserve the
   serializer and quoting style already used by the project.
11. Before changing Vietnamese text, classify any existing display failure as
   encoding corruption, a missing glyph, resource-pack font fallback, or
   inherited styling. Preserve the original file encoding, BOM, and newline
   convention. Do not introduce a new Unicode decoration or font/reset code
   without evidence that it renders correctly on the same client surface.
12. Render in Minecraft when possible. Treat a supplied screenshot as
   authoritative evidence for contrast, balance, color density, and inherited
   styling. Otherwise perform static checks and state
   clearly that glyph support, pixel balance, and final color appearance remain
   unverified.

## Non-negotiable checks

- Never exceed seven displayed words on one name or lore line.
- Never treat the seven-word limit as sufficient. For descriptive lore, aim near
  25 visible characters per line and keep neighboring lines within about two
  visible characters where the language allows.
- Never split a short click instruction into label and action lines when the
  combined line reads better. Click, command, placeholder, and value lines may
  exceed the descriptive target by roughly five visible characters, and should
  become the balancing anchor when they are the longest natural line.
- Never use `&l` as a default style or across whole blocks.
- Never add `&l` to an inventory title by default. Title boldness must be
  explicitly requested, already established by that exact menu style, or verified
  as readable on the real title background.
- Never leave item name or lore italic merely because the renderer inherited
  Minecraft's default item-meta style.
- Never assume that seven words guarantee a short line; inspect pixel width.
- Never keep a needlessly long phrase when a shorter, equally clear expression
  would improve balance; rephrase before adding spaces, decoration, or more
  lines.
- Never reuse a tooltip palette for an inventory title without checking the
  title-panel background; a light title needs dark text.
- Never assume hex, gradient, tiny-font, or Unicode support without checking the
  plugin, serializer, client, and resource pack.
- Never diagnose a Vietnamese display problem as a generic “font error” from
  source text alone. Distinguish mojibake, missing glyphs, font fallback, and
  inherited styling before editing.
- Never add a new Unicode symbol, `&r`, font tag, or reset code to a live GUI
  without same-surface render evidence. Without that evidence, preserve the
  known-good symbol and style-code set already used by the target GUI.
- Never rewrite a working Vietnamese config through a different encoding, BOM,
  or newline convention. Byte-verify remote uploads by decoding and rereading
  the result with the original encoding.
- Never color every word independently.
- Never force every highlight into the same accent when the tooltip contains
  distinct concepts such as identity, positive action, and time/value. Use up
  to two supporting accents with explicit reusable roles.
- Never highlight every keyword with only the item's display-name color when a
  secondary action/value/warning color would make the tooltip more harmonious
  and easier to scan.
- Never let accents dominate the tooltip; neutral gray and white should carry
  ordinary descriptions and instructions.
- Never make an entire descriptive paragraph `&7` when it contains meaningful
  keywords players need to scan quickly. Highlight a small number of semantic
  anchors while keeping the surrounding copy neutral.
- Never substitute a blue-gray or pastel slate hex for the requested Minecraft
  gray base without a verified visual reason.
- Never color a long status sentence uniformly. Keep its label and connective
  copy gray, then color the state keyword, value, duration, price, or quantity.
  A whole-line state color is acceptable only for a compact phrase of roughly
  four or five words.
- Never add blank lines without a genuine boundary between content groups.
- Never claim visual verification if the result was not rendered.

## Review output

When reviewing existing GUI text:

- Identify concrete violations and ambiguous rendering assumptions.
- Distinguish plugin-authored lore from client debug or advanced-tooltip metadata.
- Propose corrected text rather than only describing problems.
- Keep unchanged functional syntax intact.
- Explain only the design decisions that materially affect readability or
  hierarchy.
