# Minecraft GUI Name & Lore Style Guide

## Contents

1. [Purpose](#1-purpose)
2. [Hard requirements](#2-hard-requirements)
3. [Typography and decoration](#3-typography-and-decoration)
4. [Color system](#4-color-system)
5. [Spacing](#5-spacing)
6. [Implementation constraints](#6-implementation-constraints)
7. [Surface contrast](#7-surface-contrast)
8. [Design sequence](#8-design-sequence)
9. [Example](#9-example)
10. [Final checklist](#10-final-checklist)

## 1. Purpose

Make Minecraft GUI names and lore:

- Concise and easy to scan.
- Visually balanced across lines.
- Clear in information hierarchy.
- Distinctive without becoming noisy.
- Consistent across items with the same role.

## 2. Hard requirements

### 2.1 Do not overuse bold

- Do not use `&l` as the default format.
- Do not bold an entire name or several consecutive lore lines.
- Consider bold only for a short word or phrase that genuinely requires extra
  emphasis.
- Prefer wording, line position, and color hierarchy before bold.

### 2.2 Balance visible character length

- Keep seven displayed words as an emergency ceiling, not the main target.
- For descriptive lore, aim for roughly 25 visible characters per line.
- Within one descriptive group, keep neighboring lines within about two visible
  characters when natural phrasing allows.
- Shorten long copy or split it at a natural phrase boundary.
- Keep closely related words together.
- Evaluate the rendered value of placeholders, not only their short config token.
- Do not use decorative characters or unusual tokenization to evade the limit.
- Treat dynamic placeholders, command examples, and click instructions as
  exceptions: keep them clear and intact, then balance visually as much as the
  functional text permits.
- Do not split a short click instruction into separate label and action lines
  merely to satisfy the descriptive-line target. If the combined action line is
  the longest natural unit, keep it whole and balance nearby lore around that
  line's visual width.
- Click, command, placeholder, and value lines may exceed the descriptive target
  by roughly five visible characters when splitting would look awkward or weaken
  the interaction rhythm.

Word count alone is insufficient. A seven-word line with short words can be
fine, while a six-word line with long Vietnamese words may feel too wide.
Minecraft also uses proportional glyph widths, so character count is still a
proxy; screenshots remain the best evidence.

### 2.3 Balance the layout visually

- Keep neighboring lines reasonably balanced in rendered pixel width.
- Within the same semantic group, aim for neighboring lines to differ by no more
  than roughly 20–25% in rendered width when accurate wording permits.
- Across the whole tooltip, avoid an isolated line shorter than roughly two-thirds
  of the longest line unless that difference creates an intentional hierarchy.
- Avoid placing one very long line among several very short lines unless it
  creates a deliberate hierarchy.
- Keep the same structural pattern for items with the same function.
- Do not insert spaces to force both edges into alignment.

Minecraft tooltips do not support true justified alignment. Interpret “justify”
as visual balance after rendering.

The percentage targets are review heuristics, not a reason to distort meaning.
Prefer rewriting or moving a phrase over adding filler words or spaces.

Before changing spacing, font, or decoration, look for a shorter phrase with the
same meaning. Rephrase at the semantic level first. For example, when the menu
context already establishes that rewards are items, `xem trước vật phẩm` is
clearer and easier to balance than `xem trước phần thưởng`.

## 3. Typography and decoration

### 3.1 Inherited italics

- Item names and lore may inherit Minecraft's italic item-meta style even when
  the MiniMessage or legacy source contains no italic tag.
- Explicitly set `TextDecoration.ITALIC` to `false` on Adventure components, or
  use the serializer's verified non-italic equivalent.
- Keep italics only for a deliberate role such as a quotation or flavor text.
- Do not use italics across names, descriptions, statuses, and instructions by
  default; the slant reduces Vietnamese readability and makes width balancing
  less predictable.

### 3.2 Tiny font

- Use tiny font selectively for labels, classifications, or secondary metadata.
- Do not use it for primary instructions or information that must be read quickly.
- Verify Vietnamese diacritics, punctuation, and symbols against the active
  resource pack.
- Fall back to normal text when a glyph is missing or hard to read.

### 3.3 Unicode

- Use Unicode selectively for bullets, separators, arrows, or a deliberate accent.
- Assign each symbol a clear role.
- Reuse one coherent symbol set across the GUI.
- Do not surround short text with multiple decorative symbols.
- Verify every glyph in the actual client and resource pack.

### 3.4 Vietnamese encoding and font safety

Classify the visible failure before editing:

- Mojibake such as `Luáº­t` indicates an encoding mismatch, not a missing font.
- A box, replacement mark, or blank character indicates a missing glyph.
- Mixed typefaces, baselines, or character sizes indicate font fallback.
- Slanted text with intact glyphs indicates inherited italic styling.

Preserve the target file's encoding, BOM, and newline convention when it already
renders Vietnamese correctly. For SFTP or other remote edits, retain the original
bytes as a backup, upload using the same encoding, then reread and decode the live
file before reload.

Do not introduce decorative symbols, font tags, or reset codes such as legacy
`&r` merely because they are valid syntax. A reset may change component styling
or font fallback in the target plugin. Require a screenshot or direct in-client
render from the same GUI surface before adding them. Without render evidence,
reuse only symbols and style codes already proven in that GUI.

## 4. Color system

### 4.1 Color only meaningful phrases

Use Minecraft gray (`&7`, `<gray>`, or the serializer-equivalent named color)
as the default base for tooltip copy. Use Minecraft white (`&f`, `<white>`) only
when a phrase needs stronger neutral emphasis. Do not silently replace this base
with a slate, blue-gray, or pale-blue hex merely because it looks neutral in a
palette tool.

Neutral dominance does not mean removing useful color. Each semantic block
should retain a clear focal phrase when the content contains something worth
scanning. Ordinary descriptions, explanations, and interaction labels should
normally remain gray around that focal phrase. Reserve accent color for:

- Item or feature names.
- Values, quantities, prices, or rewards.
- Rarity and state.
- The action a player should take.

Do not switch color word by word. A player should immediately distinguish primary
content from supporting copy.

Return to the base color after a mid-line accent so the remaining punctuation or
copy does not inherit the accent unintentionally.

Do not turn an entire informative paragraph into plain `&7` when it contains
scan-worthy keywords. Highlight one or two semantic anchors per block, such as a
system name, destination, resource, action, value, or future availability state,
then return to neutral gray for the surrounding explanation. This keeps the text
readable while giving players something to lock onto at a glance.

### 4.2 Color statuses by information, not line length

- For a longer status sentence, keep the label and connective words gray.
- Color only the state keyword or dynamic value such as duration, price,
  quantity, percentage, or player-facing result.
- A whole sentence may use a state color only when it is a compact status phrase
  of roughly four or five words and the solid color reads like one badge.
- Never let a placeholder cause the colored region to expand across unrelated
  explanatory text.

Example:

```text
<gray>Có thể nhận lại sau: <gold>{remaining}
<gray>Trạng thái: <green>Sẵn sàng nhận
```

### 4.3 Use a restrained color budget

For a multi-block item tooltip, default to:

- One neutral family for most text, usually gray plus white.
- One primary accent for item identity or the dominant information.
- One or two supporting accents for distinct concepts such as positive action,
  time/value, preview, or recovery.
- Contextual state colors for available, warning, locked, or error; reuse a
  supporting accent where its role already matches instead of adding another
  color.

A gradient counts as the primary accent. Do not assign a different color to each
line. Supporting accents must repeat by meaning, not by position. If the tooltip
feels colorful before the reader notices its hierarchy, reduce the palette.

Avoid the opposite failure as well: repeating one accent for every highlighted
phrase can make a long tooltip visually flat. Do not highlight every keyword
only with the item's display-name color when a secondary action, value, warning,
or future-state color would make the tooltip more harmonious. In a tooltip with
several blocks, place two or three accent anchors across identity/description,
state/value, and interaction when those blocks contain genuinely distinct
information.

### 4.4 Give colors explicit roles

Define a small palette for each GUI:

- **Base:** normal descriptive content.
- **Primary accent:** the most important information.
- **Supporting accent 1:** positive action, recovery, or confirmation.
- **Supporting accent 2:** time, value, preview, or attention.
- **State:** success, warning, error, locked, or unavailable.

Do not introduce a color that has no distinct semantic role. Reuse the same role
mapping across related items.

### 4.5 Hex colors

- Use hex colors when the Minecraft default palette is too restrictive.
- Prefer gentle, comfortable colors with sufficient contrast.
- Check adjacent colors for harmony and distinguishability.
- Judge the colors against the real tooltip background.
- Confirm the plugin, server version, and serializer syntax before applying hex.

### 4.6 Gradients

- Use a gradient for a special name, phrase, or lore line only when it communicates
  rarity, quality, or deliberate emphasis.
- Avoid multiple gradients beside each other in one item.
- Avoid gradients over long text.
- Default to no more than one prominent gradient region per item.
- Preserve a clear hierarchy between the gradient and surrounding copy.

## 5. Spacing

- Insert a blank lore line only between genuinely independent content groups,
  such as description, statistics, and interaction instructions.
- Do not separate sentences that express the same idea.
- Do not turn every lore line into an isolated block.
- Use the same spacing model for items with the same role.

Excessive spacing makes the tooltip feel fragmented rather than organized.

### 5.1 Optional compact click hints

For a button with one short, obvious action, consider a compact single-line hint
such as:

```text
&#6DD770 ➟ Dịch chuyển &7[Chuột Trái]
```

Treat this as an option, not a required template for every button. It works best
when:

- The button has only one relevant click action.
- The action needs no price, warning, requirement, or confirmation.
- Neighboring items with the same role use the same interaction pattern.

Prefer a label-first instruction such as
`&#6DD770Chuột trái: &fDịch chuyển` when the item supports multiple click types,
the action is costly or destructive, or the player needs conditions explained
before clicking. Preserve the serializer and established GUI style, and verify
that the arrow and Vietnamese glyphs render in the active client/resource pack.

## 6. Implementation constraints

Determine the supported text format before writing formatting codes. Possible
systems include legacy ampersand codes, section-sign codes, plugin-specific hex,
MiniMessage, JSON components, or custom resource-pack font tags.

Do not silently convert between formats. Preserve:

- YAML quoting and indentation.
- Placeholders and conditional tokens.
- Escaping rules.
- Click behavior and functional metadata.
- Existing serializer conventions.

Hex, gradients, and tiny fonts are capabilities, not universal guarantees.
Static source inspection cannot confirm glyph coverage, pixel width, tooltip
background contrast, or final gradient appearance.

When generating Adventure item components, explicitly clear inherited italics:

```java
component.decoration(TextDecoration.ITALIC, false);
```

Apply this to both display names and every lore component. Do not assume that
MiniMessage text without `<italic>` renders upright in item metadata.

Client advanced tooltips can append namespaced item IDs, component counts, and
component icons below plugin lore. Identify these lines before changing plugin
copy; they are not controlled by the GUI lore configuration.

## 7. Surface contrast

Inventory titles and item tooltips can sit on different backgrounds:

- Inventory titles may render on a bright white or light-gray panel supplied by
  a resource pack. Prefer a dark neutral title unless the actual panel proves a
  light accent readable.
- Do not add `&l` to an inventory title by default. Use title boldness only when
  the user explicitly asks for it, when that exact menu style already establishes
  it, or when a same-surface render proves it improves readability.
- Item tooltip text normally renders on a very dark translucent background.
  Light neutral text and restrained accents work better there.

Never select one palette from hex codes alone and reuse it on both surfaces.
Inspect the actual screenshot or client. A pastel cyan/lavender title that works
on a dark tooltip can become unreadable on a white inventory header.

## 8. Design sequence

1. Identify each text surface and its real background.
2. Determine the meaning and player action.
3. Write the shortest accurate copy; rephrase long wording before styling.
4. Split at natural phrase boundaries.
5. Keep descriptive lore near 25 visible characters per line.
6. Keep neighboring descriptive lines within roughly two visible characters when
   natural phrasing allows.
7. Assign Minecraft gray/white as the neutral base, one primary accent, and at
   most two supporting accents with stable semantic roles.
8. Disable inherited italics for item metadata.
9. Add optional decoration only with a clear purpose.
10. Render and inspect in Minecraft when possible.

## 9. Example

The tags below describe color roles conceptually. Convert them only to syntax
supported by the target project.

```text
Inventory title on a light panel:
<dark-neutral>Kho Báu</dark-neutral>

Item name:
<neutral>Hòm Báu <accent>Thủy Triều</accent></neutral>

Lore:
<gray>Chứa <primary>vật phẩm đại dương</primary></gray>
<gray>Nhận lại sau <value>24 giờ</value></gray>

<positive>Chuột trái:</positive> <white>nhận vật phẩm</white>
<attention>Chuột phải:</attention> <white>xem trước vật phẩm</white>
```

This example keeps each line below seven words, uses one gradient region, gives
the emphasized reward phrase a semantic role, and reserves the blank line for a
real boundary before the interaction instruction.

## 10. Final checklist

- [ ] Descriptive lore lines sit near 25 visible characters when practical.
- [ ] Neighboring descriptive lines differ by no more than about two visible
      characters when natural phrasing allows.
- [ ] Click instructions remain whole when splitting would make the tooltip look
      awkward; the longest natural action line is used as a balancing anchor.
- [ ] Every rendered line stays under the seven-word emergency ceiling.
- [ ] Placeholder expansion does not break the line limit.
- [ ] `&l` is absent or used only for a justified short emphasis.
- [ ] Inventory titles are not bolded by default.
- [ ] Item names and lore explicitly render non-italic unless intentional.
- [ ] Lines are balanced by visual width, not merely word count.
- [ ] Neighboring lines in one group stay near the 20–25% width target.
- [ ] Line breaks preserve natural meaning.
- [ ] Needlessly long wording was rephrased before layout or decoration changes.
- [ ] Neutral gray or white carries most ordinary copy.
- [ ] Tooltip base uses Minecraft gray (`&7`/`<gray>`) unless a verified design
      reason requires another neutral.
- [ ] Each informative block has a meaningful focal phrase when appropriate;
      neutral styling has not made the tooltip visually flat.
- [ ] Long status lines color only the keyword or dynamic value, not the entire
      sentence.
- [ ] A multi-block tooltip uses one primary accent plus no more than two
      supporting accents by default.
- [ ] Supporting accents have stable roles and create useful color rhythm rather
      than random variety.
- [ ] Distinct semantic blocks are not all highlighted with one monotonous color
      when another role-based accent would improve scanning.
- [ ] Accent colors mark only important content.
- [ ] Every color has a defined role.
- [ ] Hex colors remain gentle, readable, and supported.
- [ ] Any gradient is purposeful and does not dominate the tooltip.
- [ ] Tiny-font and Unicode glyphs render correctly.
- [ ] Vietnamese text failures were classified as encoding, missing glyph,
      fallback font, or inherited styling before editing.
- [ ] The original encoding, BOM, and newline convention were preserved.
- [ ] No new Unicode symbol, font tag, or reset code was added without a
      same-surface render check.
- [ ] Blank lines separate independent content groups only.
- [ ] Related items share the same structure and palette.
- [ ] Inventory-title contrast was checked separately from tooltip contrast.
- [ ] Client debug or advanced-tooltip lines were not mistaken for plugin lore.
- [ ] The tooltip was rendered in Minecraft, or the lack of visual verification
      is explicitly disclosed.

When two options are otherwise valid, prefer the one that is easier to read,
shorter, more consistent, and less decorated.
