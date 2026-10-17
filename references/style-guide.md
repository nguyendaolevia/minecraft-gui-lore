# Minecraft GUI Name & Lore Style Guide

## Contents

1. [Purpose](#1-purpose)
2. [Copy and layout standards](#2-copy-and-layout-standards)
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

## 2. Copy and layout standards

### 2.1 Use bold by role, not by default

Bold is neither banned nor a default. Decide by the role of the text:

- **May be bold:** a short, prominent item name; a short section label; a
  primary CTA or badge of about four words or fewer.
- **Never bold:** descriptions, label/value data rows, long lines, requirement
  sentences, or several consecutive lore lines.
- Keep at most about two bold regions per tooltip. If the tooltip already has
  enough focal points from color and structure, skip bold.
- Equivalent elements across related items share the same bold decision.
- Prefer wording, line position, and color hierarchy first; bold is the last
  emphasis layer. Inventory titles follow the separate rule in section 7.

### 2.2 Balance visible character length

- Prefer about 23 visible Unicode characters or fewer per item display name and
  lore line, including spaces and decoration. This is a priority density target,
  not an absolute cap. Exceed it when needed to preserve clear meaning, natural
  phrasing, or the mandatory visual justification of related lore lines.
- Do not count legacy color codes, hex prefixes, MiniMessage tags, or other
  non-rendered formatting syntax. Normalize text to NFC and count Unicode code
  points rather than UTF-16 units.
- Count placeholders after expansion. Inspect realistic long values and reflow
  the group if needed; do not truncate names or meaningful data merely to hit 23.
  If expansion cannot be bounded, disclose the unverified layout range.
- Priority order: mandatory visual justification first, then the 23-character
  density target.
- Two length tiers:
  - **Data tier** — names, label/value rows, rewards, prices, CTAs: about 23
    characters, seven displayed words as the emergency ceiling.
  - **Description tier** — wrapped descriptive paragraphs: may extend to about
    32–36 characters (about nine displayed Vietnamese words) when that produces
    a better justified, more natural block than breaking at 23.
- Keep seven displayed words as a secondary emergency ceiling for the data tier,
  not the main measurement.
- Within one descriptive group, keep neighboring lines within about two visible
  characters when natural phrasing allows.
- Shorten long copy or split it at a natural phrase boundary.
- Keep closely related words together.
- Do not distort words or add decoration to manipulate the character count.
- Commands, click instructions, values, and placeholders share the same preferred
  target and the same allowance for clear meaning and balanced layout.

The 23-character target guides density, not exact pixel width. Minecraft uses a
proportional font, so two lines with equal character counts can still render at
different widths. Screenshots remain the best evidence for final alignment.

### 2.3 Mandatory visual justification of related lore

- Consecutive lore lines in the same semantic group must be visually justified:
  balanced in rendered width with a consistent left edge. This includes related
  fact rows, wrapped descriptions, requirement sentences, and their final lines.
- Rephrase or redistribute phrases across the whole group until it reads evenly.
  An obviously uneven group is unfinished even if every line is within 23
  characters. Prefer a natural line above 23 over a forced break that unbalances
  the group; preserve meaning and the secondary word ceiling.
- Within the same semantic group, aim for neighboring lines to differ by no more
  than roughly 20–25% in rendered width when accurate wording permits.
- Across the whole tooltip, avoid an isolated line shorter than roughly two-thirds
  of the longest line unless that difference creates an intentional hierarchy.
- Avoid placing one very long line among several very short lines unless it
  creates a deliberate hierarchy.
- Keep the same structural pattern for items with the same function.
- Do not insert spaces to force both edges into alignment. The only exception
  is a render-verified centered name line (`pattern-library.md`, H4).

Standard tooltip lore has no paragraph-justification setting. Here, mandatory
"justify align" means visual justification through wording and line breaks,
verified after rendering, rather than automatic expansion of spaces. Exact equal
pixel widths are not assumed. Without a render, report alignment as unverified.

The percentage targets are review heuristics, not a reason to distort meaning.
Prefer rewriting or moving a phrase over adding filler words or spaces.
Compare consecutive related lines within their own block. A separate short
section label or item name need not match the width of data rows. A requirement
footer is a separate group, but its own related lines still require justification.
Recheck pixel balance when mixing normal and tiny fonts.

Before changing spacing, font, or decoration, look for a shorter phrase with the
same meaning. Rephrase at the semantic level first. For example, when the menu
context already establishes that rewards are items, `xem trước vật phẩm` is
clearer and easier to balance than `xem trước phần thưởng`.

### 2.4 Whole-tooltip width harmony

Justifying each group is not enough; the final tooltip must look even as a
whole.

- Choose one width band for the tooltip and keep every content block near it.
  A description block of 36-character lines followed by a data block of
  20-character lines is unbalanced and unfinished.
- When the description must be wide, enrich or rephrase the data rows (fuller
  labels, value context) or narrow the description so blocks meet in the middle.
  When the data is short, wrap the description narrower rather than stretching
  it to 36.
- Short section labels, a short name, and a compact CTA may sit below the band;
  data and description blocks may not diverge sharply from each other.
- Exceeding 23 characters is acceptable only when the resulting whole tooltip
  is visibly more even and readable. Judge the full render, not single lines.

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

Choose the font by the role and reading priority of the content:

| Content role | Default | Optional variation |
| --- | --- | --- |
| Item name | Normal | Existing verified identity font |
| Short secondary section label | Normal | Tiny when clear and supported |
| Labels, values, stats, rewards | Normal | Tiny only for genuinely secondary metadata |
| Requirements, prices, warnings, click instructions | Normal | Keep decision-critical content immediately readable |

- Normal font throughout is valid. Mixed typography is an option, not a quota;
  a useful combination is tiny section labels above normal data rows.
- Give equivalent headings the same treatment across related items. Do not
  alternate fonts line by line or split a label/value row between sizes without
  same-surface evidence that the baseline and hierarchy remain clear.
- Tiny font may come from a resource-pack provider or Unicode substitutions;
  these have different glyph coverage. Do not assume that a small-cap converter
  supports Vietnamese, or remove accents to make a label fit its character set.
- Verify Vietnamese diacritics, punctuation, baseline, and contrast in the actual
  tooltip at the intended GUI scale. If support or readability is unverified,
  retain the established font; if tiny text fails, use normal font.
- Apply the same preferred 23-character target in either font. Font choice must
  serve information hierarchy; shrinking text does not replace mandatory visual
  justification, and fewer pixels do not make a requirement secondary.
- Distinguish a lore section label from an inventory title. Short uppercase lore
  labels can be a deliberate verified style, but normal Vietnamese labels are a
  readable default; tiny font does not require uppercase text. Inventory titles
  follow the separate Title Case rule in section 7.

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
<gray>Còn lại: <gold>{remaining}
<gray>Trạng thái: <green>Sẵn sàng
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

A gradient counts as the primary accent. Colors from a server-wide resource
color registry (see `pattern-library.md`, V1) mark resource values and do not
count against the accent budget, provided labels stay neutral. Do not assign a
different color to each line. Supporting accents must repeat by meaning, not by position. If the tooltip
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

For richer header, grouping, value, and CTA patterns (bracketed names, category
subtitles, accent bars, resource color registry, mouse-glyph CTAs, role-based
recipes), read [pattern-library.md](pattern-library.md). Choose patterns by item
role; do not apply one pattern to every slot.

### 5.1 Optional segmented information lore

Use this pattern for items with several distinct questions to answer, such as
where an ore occurs, what it drops, and which tool is required. The ore references
work through hierarchy and repeated structure, not through a mandatory number of
sections or exact colors.

- Start with the normal-font item name. Add a short label only when it helps
  identify a genuine group; do not repeat information already clear from context.
- Group related facts into short label/value rows. Keep labels gray and emphasize
  values by semantic role, such as location, rarity, quantity, or state.
- Give rewards their own block when they are distinct from the item's properties.
  Use an established bullet consistently for peer entries; a wrapped continuation
  is still the same entry and does not need another bullet or space padding.
- Separate independent groups with one blank line. A single compact action can
  use the click-hint pattern without section headings or extra blocks.
- Keep requirements in a clear normal-font line or footer with the decisive tool
  or condition highlighted. Do not copy a reference's low-contrast dark footer
  merely because its placement looks attractive. For a costly or blocked action,
  place its condition before the action or reward when needed for the decision.
- Reuse the structure for items with the same role, while omitting absent fields
  and empty sections. Avoid importing reference mechanics or values as facts
  about the target server.

Example of visible copy (all lines are within 23 characters):

```text
Quặng Orichalcum

Thông tin
- Độ cao: -32 đến 32
- Thế giới: Overworld
- Độ hiếm: Hiếm

Nhận được
- Thỏi Orichalcum

Cần cuốc Mythril
hoặc cấp cao hơn.
```

The values illustrate layout, not verified server mechanics. `Thông tin` and
`Nhận được` may use tiny font only with verified Vietnamese support; all other
lines use normal font. Render labels and connective text in gray, with selected
values in white or existing semantic accents. The hyphen is an example marker,
not authorization to add an unverified glyph to a live GUI. This is visible copy,
not serializer syntax; apply the target plugin's verified font and color format.
This copy has not been rendered in the target client; its group justification
must still be checked against the active font, including the requirement footer.

### 5.2 Optional compact click hints

For a button with one short, obvious action, consider a compact single-line hint
such as:

```text
&#6DD770➟ Đi tới &7[Chuột trái]
```

Treat this as an option, not a required template for every button. It works best
when:

- The button has only one relevant click action.
- The action needs no price, warning, requirement, or confirmation.
- Neighboring items with the same role use the same interaction pattern.

Prefer a label-first instruction such as
`&#6DD770Chuột trái: &fĐi tới` when the item supports multiple click types,
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
- Use Title Case for inventory/menu titles, with no leading spaces and no ALL
  CAPS. Lore section labels are a separate surface, as described in section 3.2.
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
2. Determine the meaning, player action, and item role; pick a recipe from
   `pattern-library.md` that fits the role.
3. Write the shortest accurate copy; rephrase long wording before styling.
4. Split at natural phrase boundaries.
5. Prefer about 23 visible Unicode characters per name or lore line; allow longer
   lines when clarity, natural phrasing, or group justification calls for it.
6. Visually justify all consecutive related lore lines, including final lines,
   by rephrasing and reflowing; verify pixel widths rather than just counts.
   Then check that all blocks share one width band across the whole tooltip.
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

<positive>Chuột trái:</positive> <white>nhận đồ</white>
<attention>Chuột phải:</attention> <white>xem trước</white>
```

This example keeps each line within the preferred character target and secondary
word ceiling, gives the emphasized reward phrase a semantic role, and reserves
the blank line for a real boundary before the interaction instruction. The tags
are conceptual; final group justification remains unverified without a render.

## 10. Final checklist

- [ ] Names and lore use 23 visible characters as the preferred density target;
      longer lines serve clear meaning, natural phrasing, or group justification.
- [ ] Formatting syntax is excluded and placeholder expansions are included in
      the visible-character count.
- [ ] Neighboring descriptive lines differ by no more than about two visible
      characters when natural phrasing allows.
- [ ] Click instructions are concise and split naturally where useful, without
      treating 23 characters as an absolute cap.
- [ ] Data-tier lines stay under the seven-word emergency ceiling; description
      lines beyond 23 characters (up to about 32–36) are justified as a group.
- [ ] The whole tooltip sits in one width band; description and data blocks do
      not diverge sharply.
- [ ] Patterns were chosen by item role; peers share one recipe and no tooltip
      stacks more than about three structural devices.
- [ ] Realistic placeholder expansions preserve readability and group layout;
      any unverified expansion range is disclosed.
- [ ] Bold appears only on a short name, section label, CTA, or badge, in at most
      about two regions per tooltip, and never on descriptions or data rows.
- [ ] Inventory titles are not bolded by default.
- [ ] Item names and lore explicitly render non-italic unless intentional.
- [ ] All consecutive related lore lines, including final continuations, meet
      mandatory visual justification; render evidence or its absence is stated.
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
- [ ] Keyword highlights are not all forced into the item display-name color when
      a harmonious supporting color would improve scanning.
- [ ] Distinct semantic blocks are not all highlighted with one monotonous color
      when another role-based accent would improve scanning.
- [ ] Accent colors mark only important content.
- [ ] Every color has a defined role.
- [ ] Hex colors remain gentle, readable, and supported.
- [ ] Any gradient is purposeful and does not dominate the tooltip.
- [ ] Tiny-font and Unicode glyphs render correctly.
- [ ] Font choice follows information priority; tiny labels are optional, and
      requirements, values, and actions remain readable in normal font.
- [ ] Compact or segmented structure matches the amount of information; empty
      sections, redundant headings, and unnecessary blank lines are absent.
- [ ] Width comparisons apply to peer lines, not to short labels versus data.
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
