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

Read [references/pattern-library.md](references/pattern-library.md) when
designing or restyling a tooltip that needs more than a plain name and one
action line. It lists header, grouping, value, and CTA patterns with the
situations each fits, plus role-based recipes.

## Workflow

1. Inspect the target plugin, configuration format, existing GUI style, audience,
   placeholders, supported text serializer, file encoding, resource-pack font
   providers, and actual background behind each text surface. Treat inventory
   titles and item tooltips separately.
2. Preserve functional placeholders, click semantics, permissions, and config
   syntax while changing only player-facing text unless broader changes are
   requested.
3. Draft the semantic content before adding colors or decoration. Identify the
   item's role, then choose compact lore for a simple action or a recipe from
   the pattern library when the player needs distinct information, rewards, and
   requirements. Items with the same role share one recipe; vary patterns by
   role, never randomly, and never spam one pattern across every slot. Rephrase
   a visibly long line with shorter, equally clear wording before splitting it
   or compensating with layout.
4. Prefer about 23 visible Unicode characters or fewer per item display name or
   data-tier lore line (labels, values, rewards, prices, CTAs); this is a
   density target, not a hard cap. Wrapped description paragraphs may extend to
   about 32–36 characters when that yields a better justified block. Count
   spaces, decoration, and expanded placeholders, excluding formatting syntax;
   normalize Vietnamese to NFC. Keep seven displayed words as the emergency
   ceiling for data-tier lines (about nine for description lines). Rephrase
   first, then wrap naturally. Review commands, click hints, values, and
   realistic placeholder expansions; do not truncate meaningful data to hit 23.
5. Mandatory: visually justify consecutive lore lines belonging to the same
   semantic group, including wrapped continuations and requirement sentences.
   Rephrase and reflow until their rendered widths are balanced, including the
   final line. This takes priority over the 23-character target. Then check the
   whole tooltip: all blocks must sit in one width band, so a block of
   36-character lines must not be followed by a block of 20-character lines.
   Equal character counts are not proof; do not pad text with spaces to imitate
   justification.
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
9. Choose normal or tiny font by information role, not by alternating lines.
   Keep names, values, rewards, requirements, and instructions readable in normal
   font; optionally use verified tiny font for short secondary section labels.
   Follow the reference's font-role guidance and normal-font fallback. Add bold,
   Unicode, hex colors, or a gradient only with a clear purpose and contrast.
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

- Treat 23 visible Unicode characters as a preferred density target, not a hard
  rejection threshold. A justified, meaningful line may be longer.
- Never exceed seven displayed words on a name or data-tier line, or about nine
  on a description-tier line.
- Never accept visibly uneven consecutive related lore lines merely because
  each fits the character target. Justification within each group is mandatory.
- Never let content blocks in one tooltip diverge sharply in width; the whole
  tooltip must read as one even shape.
- Never use `&l` by default or on descriptions, data rows, long lines, or
  consecutive lines. Bold is allowed by role for a short name, section label,
  CTA, or badge (about four words or fewer), at most about two regions per
  tooltip.
- Never apply one layout pattern to every slot or stack more than about three
  structural devices in one tooltip.
- Never add `&l` to an inventory title by default. Title boldness must be
  explicitly requested, already established by that exact menu style, or verified
  as readable on the real title background.
- Never leave item name or lore italic merely because the renderer inherited
  Minecraft's default item-meta style.
- Never assume that 23 characters produce equal pixel width; inspect the
  proportional Minecraft font and balance neighboring lines visually.
- Never force short section labels to match the width of data rows, or add
  headers and blank lines to a simple button merely to fit a segmented template.
- Never use tiny font to replace rewriting and visual justification or to hide
  a requirement. Do not use unverified small-cap substitutions for Vietnamese.
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
