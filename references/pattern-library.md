# Minecraft GUI Lore Pattern Library

Optional layout patterns distilled from tooltips the user considers easy on the
eye. Each pattern is a tool for a specific situation, not a template for every
item. Read this together with `style-guide.md`; the style guide's justification,
width, contrast, encoding, and render-verification rules still apply.

## Contents

1. [Choosing patterns](#1-choosing-patterns)
2. [Header patterns](#2-header-patterns)
3. [Body grouping patterns](#3-body-grouping-patterns)
4. [Value and color-identity patterns](#4-value-and-color-identity-patterns)
5. [Call-to-action patterns](#5-call-to-action-patterns)
6. [Recipes by item role](#6-recipes-by-item-role)
7. [Reference lessons: do not copy](#7-reference-lessons-do-not-copy)

## 1. Choosing patterns

- Choose by the item's role and the shape of its information, never by habit.
  Repeating one pattern on every slot makes a GUI monotonous; mixing patterns
  randomly makes it incoherent.
- Within one GUI, items with the same role share one recipe. Variety should come
  from different roles (navigation, reward, upgrade, collectible), not from
  restyling peers.
- Use at most about three structural devices in one tooltip, for example a
  bracketed name, an accent bar block, and a CTA. Do not stack subtitle, badge,
  centered dividers, bars, bullets, and a progress bar in one item.
- Keep one row marker per section. A header marker (arrow, bar, divider) may
  pair with one row marker (bullet or bar); do not mix bullets and bars inside
  the same section.
- Simple navigation, filler, and back buttons stay compact even when richer
  items in the same GUI use segmented layouts.
- The target server supports hex/MiniMessage and resource-pack fonts. Each
  glyph, tiny font, or badge still needs Vietnamese and same-surface render
  verification; every pattern below lists a plain-text fallback.

## 2. Header patterns

### H1. Bracketed name

```text
<dark_gray>[<accent>Quà Đăng Nhập<dark_gray>]
```

- Use for interactive entries in a list: milestones, reward slots, feature
  buttons, upgrade entries. The brackets signal "selectable entry".
- Brackets use a dark or neutral tone; the name carries the accent.
- Avoid on physical items whose identity is rarity-driven, and do not combine
  with a centered title.

### H2. Name plus category subtitle

```text
<accent>Thuốc May Mắn I
<dark_gray>Thuốc Đào Mỏ
```

- A short second line naming the item's type or system: `Thú Cưng`, `Menu`,
  `Tiền Tệ`. Keep it to about three words.
- Uppercase or tiny font is allowed here only when the Vietnamese uppercase
  diacritics render correctly; otherwise use Title Case in normal font.
- Dark gray is acceptable because this is metadata. Never place decision-critical
  information in the subtitle.

### H3. Rarity or state badge

- A resource-pack glyph badge such as a rarity plate or an `Đã Mở Khóa` pill,
  placed under the name or at the bottom of the lore.
- Use for collectibles, cosmetics, titles, and unlockable upgrades where rarity
  or state is a primary property.
- Fallback without a verified glyph: `<gray>[<rarity_color>Phổ Thông<gray>]`.
- One badge per tooltip.

### H4. Centered title

- Use for wide detail tooltips such as an enchant upgrade panel or a level
  milestone, where the body is visibly wider than the name.
- Centering requires pixel-computed leading space or a negative-space font. This
  is the only accepted exception to "no space padding", and only for the name
  line, with render verification. Without it, keep the name left-aligned.

### H5. Icon prefix

- A small resource-pack icon before the name, for showcase entries such as a
  server or mode selector. Requires a verified glyph; omit it otherwise.

## 3. Body grouping patterns

### B1. Circle-bullet rows

```text
<gray>○ Kim Cương: <aqua>25
<gray>○ Rusty Key: <light_purple>x1
```

- For short lists of peer facts or rewards, up to about five rows. Light visual
  weight; works well in compact reward and status tooltips.
- Bullet stays neutral gray; labels gray; values use semantic colors.

### B2. Accent vertical bar block

```text
<accent>Thông Tin
<accent>▍ <gray>Thời gian: <white>120s
<accent>▍ <gray>Bậc thuốc: <white>1
```

- For multi-section detail tooltips (information, upgrades, rewards). The bar
  colors the section and visually binds wrapped lines into one block.
- The bar uses the section header's color. Use the same bar glyph for every
  section; change bar color between sections only when the sections have
  distinct roles.
- A wrapped continuation keeps the bar, because the bar marks the block rather
  than a new entry. Justify the wrapped lines as one group.

### B3. Section header

- A short Title Case label in the section's accent: `Thông Tin`, `Phần Thưởng`,
  `Nâng Cấp`, `Mô Tả`. It may be bold (see bold criteria in the style guide) or
  verified tiny uppercase, never both on a long label.
- Equivalent headers use identical styling across related items.

### B4. Centered divider header

```text
<gold>——— <yellow>Tính Năng <gold>———
```

- For overview or showcase tooltips only, such as a mode selector listing
  features. It needs a wide, harmonious body; never use it in compact buttons.
- Verify the dash glyph width and keep both sides symmetric.

### B5. Arrow sub-header

```text
<white>➲ <yellow>Thông Tin
```

- A lighter alternative to B3 when the tooltip has one information section.
  Pair it with B1 rows.

### B6. Label/value rows

- Labels and connectors stay gray; only the value takes a semantic color.
- Align label wording so peer rows in one section have similar widths.

## 4. Value and color-identity patterns

### V1. Resource color registry

- Assign one fixed color to each currency, resource, key, and box type, and
  reuse it across every GUI on the server, for example diamonds in aqua, gold
  currency in gold, keys in lavender.
- Record the registry in the project, such as a palette note or config comment,
  before applying it widely; follow an existing registry when one exists.
- Registry colors mark values and quantities, not labels. They count as value
  colors rather than extra accents, so a reward list may show several resource
  colors while labels stay neutral. Do not reuse a registry color for an
  unrelated role in the same GUI.

### V2. Quantity notation

- Pick one notation per server, either a suffix (`Rusty Key: x1`) or a prefix
  (`3x Grind Key`), and keep it consistent. The quantity takes the value color.

### V3. Timers and counters

- Use a fixed-width format such as `00h 29m 12s` so a live countdown does not
  make the line jitter in width.
- Color by meaning: elapsed time and remaining time may use different value
  colors, while the label stays gray.

### V4. Progress bar

- A glyph bar plus percentage for milestones and quests:
  `<gray>Tiến độ: <dark_gray>[<red>::::::::<dark_gray>] <green>(0.0%)`.
- Requires verified glyph widths; the percentage follows state colors.

### V5. Multicolor showcase list

- Coloring each line differently is allowed only when every entry is a distinct
  feature whose color already identifies it elsewhere (its own menu or icon).
  Otherwise use one list color. Never use rainbow coloring merely for liveliness.

## 5. Call-to-action patterns

The CTA is normally the last plugin line, separated from the body by one blank
line. Color the CTA phrase as one unit: do not color only the first word.

### C1. Arrow CTA

```text
<green>→ Chuột phải để mở
```

- For one obvious action. A compact phrase (about five words or fewer) may be a
  single solid color.

### C2. Mouse-glyph CTA

```text
<white>{mouse_icon} <gray>Click để <aqua>nâng cấp
<white>Shift + {mouse_icon} <gray>Click để <aqua>nâng nhiều cấp
```

- For items with several click types. Use the label-first structure, with the
  action keyword colored. `{mouse_icon}` stands for a verified resource-pack
  glyph; vanilla fonts do not render emoji mouse icons. Fallback: `[Chuột trái]`.

### C3. Emphasis CTA

- A bold, optionally uppercase CTA of about four words or fewer for the primary
  conversion action of a high-value item: obtain, purchase, claim.
- At most one per tooltip and rare across the GUI. Vietnamese uppercase must keep
  its diacritics.

### C4. Locked or unavailable footer

```text
<red>[Chưa Mở Khóa]
```

- Replaces the action CTA when the action is blocked. Use the state color; put
  the requirement above it when the player needs it to decide.

### C5. Plain action line

```text
<green>Nhấn để xem nâng cấp
```

- A full-sentence action in the positive action color, for items that open a
  detail view.

## 6. Recipes by item role

These are starting points. Omit absent fields and adapt to the GUI.

| Item role | Header | Body | Footer |
| --- | --- | --- | --- |
| Navigation or back button | Plain name | None or one line | C1 |
| Daily or playtime reward slot | H1 | B1 rows with V1, timer V3 | C1/C5 or C4 |
| Consumable or potion | H2 | Short description, B3 + B2 info | C5, storage row |
| Upgrade or enchant entry | H1 or H4 | Description, B5/B3 + B1/B2, price | C2, optional H3 |
| Collectible, cosmetic, title | H1 + H3 | B3 sections + B2 | Optional C1 |
| Level milestone | H4 with state | B2 information + rewards, V4 | C4 or claim CTA |
| Currency or info item | H2 | B2 info, balance row | C3 |
| Mode or server selector | H5 | Description, B4 sections | C1 |

## 7. Reference lessons: do not copy

- A wrapped paragraph whose last line is far shorter than the others is
  unfinished, even in an otherwise attractive tooltip.
- A long ALL CAPS Vietnamese CTA such as a six-word instruction is hard to read;
  keep emphasis CTAs to about four words.
- Coloring only the first word of a CTA weakens it; color the action as a unit.
- Displayed data must match the mechanic. A mining-speed enchant labeled with a
  movement category is a content error, not a styling choice.
- Dense English paragraphs of four or more lines in a bar block do not transfer
  well to Vietnamese; prefer two or three justified lines.
- Dark-gray footer text is acceptable for metadata, never for requirements.
- Mixing English and Vietnamese inside one item name should follow an
  established server naming convention, not appear ad hoc.
- Client advanced-tooltip lines (namespaced IDs, component counts) in reference
  screenshots are not part of the design.
