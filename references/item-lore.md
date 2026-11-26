# Minecraft Carried & Equipped Item Lore Guide

Dedicated standard for **persistent, player-held items**: weapons, pickaxes,
tools, armor, charms, boss souls, consumables, materials, cosmetics, and event
collectibles (MMOItems, Nexo, ItemsAdder, custom item plugins).

House style: **"ARPG gọn — nền dịu, điểm nhấn có cảm xúc"** (clean ARPG with a
calm neutral body and purposeful accent saturation). A short positional
skeleton, calm neutral body text (`#A9A6B4` / `#ECE9F2` / `#8A8597`), one
highlight per block, and **intentional color saturation** matched to item
rarity, material, and mood — pastel/soft where calm, rich jewel/elemental tones
where powerful or fierce, never flat pastel everywhere and never raw RGB neon.
Gallery `I1–I6` in [gallery.md](gallery.md) are the canonical renders of this
standard.

Item lore is **fundamentally different** from GUI menu lore:
- Persisted in item NBT/DataComponents (template changes need migration/RevID
  via `minecraft-custom-item-safety`).
- Inspected in inventory comparisons, `[item]` chat, Auction House and trades,
  next to vanilla enchant/attribute rows.
- GUI menu limits **do not apply**: no 14-line cap, no 35% cross-block width
  band, no decision-first CTA, no `&7` legacy base.

Shared technical rules still come from [style-guide.md](style-guide.md): Mojang
1.21.11 pixel table (§2.3), Vietnamese/encoding & italic safety (§3), WCAG
contrast on `#100010` (§4.3). Lint with `scripts/lint_lore.py --profile item`.

## Contents

1. [Priority order](#1-priority-order)
2. [Block skeleton & spacing](#2-block-skeleton--spacing)
3. [Palette, saturation & mood discipline](#3-palette-saturation--mood-discipline)
4. [Identity line, rarity & term registry](#4-identity-line-rarity--term-registry)
5. [Stats & stat symbols](#5-stats--stat-symbols)
6. [Gems, set bonus & skills](#6-gems-set-bonus--skills)
7. [Footer: flavor, durability, binding, origin](#7-footer-flavor-durability-binding-origin)
8. [Height: the screen is the limit](#8-height-the-screen-is-the-limit)
9. [Vanilla rows, plugin templates, chat & AH](#9-vanilla-rows-plugin-templates-chat--ah)
10. [NBT lifecycle](#10-nbt-lifecycle)
11. [Canonical example](#11-canonical-example)
12. [Item Lore checklist](#12-item-lore-checklist)

---

## 1. Priority order

1. **Data/NBT integrity & template compatibility:** never touch Item ID, Ability
   ID, Presentation ID or Pack ID; edit shared templates (`lore-format.yml`)
   instead of hand-patching single items.
2. **Truthful mechanics & positional scanning:** numbers and triggers match the
   real code; peer items keep the identical block and stat order so players
   compare two pickaxes by glancing at the same row.
3. **Calm hierarchy:** soft palette, one highlight per block, symbols only on
   core stats, readable contrast (`>= 4.5:1` for text on `#100010`).
4. **Fit:** whole tooltip stays on screen (§8); pixel balance only **inside**
   a block (`<= 25%`).

---

## 2. Block skeleton & spacing

Fixed order. Omit blocks the item does not have; **never reorder** between peer
items. Exactly **one blank line between blocks**, none inside a block.

| # | Block | Content |
| --- | --- | --- |
| 1 | **Identity** | Name (rarity color) + optional `+N` upgrade level; line 2 `Nhóm · Hạng` (tier line; position depends on enchants, §2.1) |
| 2 | **Enchants** | Real and custom enchants, right after the tier line |
| 3 | **Requirements** *(optional)* | Level/class gate, colored by player state when the plugin supports it |
| 4 | **Core stats** | 2–5 label/value rows, fixed order per item class, one symbol each |
| 5 | **Gems / modifiers** | `Ngọc khảm: ◆ ◆ ◇` and other player-installed parts |
| 6 | **Set bonus** | `Bộ <Tên> (k/n)` + one line per tier |
| 7 | **Skill** | `Tên kỹ năng · Trigger` + 1–2 effect lines + cooldown/cost row |
| 8 | **Footer** | Flavor (`<= 2` lines) → durability → binding / origin / expiry |

Why gems are their own block: stats are the item's base power; gems are what the
player installs and can still be empty. Glued to the stat rows, a gem line reads
as a fourth stat missing its symbol.

### 2.1 Enchants & vanilla components decide where the tier line goes (mandatory)

In Mojang Java 1.21.x (`ItemStack.addDetailsToTooltip`), several vanilla
components render **directly under the name, above all lore** — notably
`minecraft:enchantments`, `minecraft:stored_enchantments` (Enchanted Books),
`minecraft:trim` (Armor Trims), `minecraft:dyed_color`, and
`minecraft:potion_contents`. Meanwhile `minecraft:attribute_modifiers`
(`"Khi ở tay chính:"`) and `minecraft:unbreakable` (`"Không phá được"`) render
**below lore**. Because of this, the tier line (`Nhóm · Hạng`) has exactly two
legal positions:

| Case | When | Layout |
| --- | --- | --- |
| **A: tier on top** | All above-lore vanilla rows are hidden (`tooltip_display.hidden_components` on 1.21.5+ / `HIDE_ENCHANTS`, `HIDE_ADDITIONAL_TOOLTIP`, etc.) or absent | Name → `Nhóm · Hạng` → blank → enchant block → blank → stats… |
| **B: tier at the bottom** | `enchantments`, `stored_enchantments` (Enchanted Books), or other above-lore vanilla rows stay visible | Name → *(vanilla rows)* → blank → stats… → footer → blank → `Nhóm · Hạng` as the **last line** |

- **Never** leave the tier line under visible vanilla rows (enchants/trim
  sandwiched between name and tier), and never show it twice.
- **Hide below-lore components for true bottom placement (Case B):** because
  `attribute_modifiers` and `unbreakable` render **below** `lore`, gear that
  already displays its stats in lore must hide `attribute_modifiers` (and
  `unbreakable` if replaced by lore) via `tooltip_display.hidden_components` /
  `HIDE_ATTRIBUTES` so `Nhóm · Hạng` is genuinely the last line of the tooltip.
  If vanilla attributes are intentionally kept visible, `Nhóm · Hạng` sits at
  the bottom of the lore block (directly above `"Khi ở tay chính:"`).
- **Enchanted Books (`stored_enchantments`):** hiding `"enchantments"` /
  `HIDE_ENCHANTS` does **not** hide enchantments on an `ENCHANTED_BOOK`. On
  1.21.5+ hide `"stored_enchantments"` in `tooltip_display.hidden_components`
  (legacy: `HIDE_ADDITIONAL_TOOLTIP`), or treat the book as Case B.
- **Hybrid items (visible vanilla enchants + plugin custom enchants in lore):**
  under Case B, place custom enchant rows (MMOItems / EcoEnchants /
  ExcellentEnchants) at the very top of `lore` with **no leading blank line** so
  all enchants read as one continuous block, followed by one blank line before
  stats.
- **Anvil/Grindstone sync guard (Case A):** only use Case A on player-enchantable
  gear when the plugin dynamically re-renders lore after enchanting/anvil/
  grindstone events (or enchanting is disabled); otherwise hidden real enchants
  will silently drift from static lore.
- Lore in pure Case B (no custom lore enchants) starts with one blank line so
  the stats do not touch the vanilla enchant rows.
- Vanilla enchant rows keep vanilla gray and follow the client's language. Pick
  one case per item family and keep it server-wide (all pickaxes A, or all
  pickaxes B), so players always find the tier in the same place.

Enchant block grammar (case A): one enchant per line, name in Label, level in
Value, Roman numerals as vanilla does. With more than 4 enchants, put two per
line separated by a Separator `·`.

```text
<#A9A6B4>Hiệu Suất <#E8E4EE>V
<#A9A6B4>Gia Tài <#E8E4EE>III
<#A9A6B4>Chậm Hỏng <#E8E4EE>III
```

**Enchant names (user decision 2026-11-26):** lore-rendered enchants use the
official Mojang `vi_vn.json` names in Title Case (`Hiệu Suất`, `Gia Tài`,
`Chậm Hỏng`, `Độ Mềm Mại`, `Tu Sửa`, `Sắc Bén`), so they match what Vietnamese
clients show at the enchanting table, the anvil and in Case B. Community names
(`Bền Vững`, `Mềm Mại`) are allowed only on a server that uses Case A for the
whole gear line and records them in its `V0` term registry.

---

## 3. Palette, saturation & mood discipline

**Do not use vanilla legacy colors** (`&a #55FF55`, `&b #55FFFF`, `&e #FFFF55`,
`&7 #AAAAAA`, `&8 #555555`…) or **raw 100%-channel RGB neon** (`#FF0000`,
`#00FF00`, `#0000FF`, `#FFFF00`, `#FF00FF`) in item lore: they vibrate on
`#100010` and look cheap.

At the same time, **do not flatten every item into washed-out pastel**. Keep
80% of the tooltip (labels, values, enchants, flavor) **calm & neutral**, then
**scale saturation intentionally** by rarity, item theme, and emotion so a
volcanic endgame sword feels fierce while a cozy starter charm feels gentle.

### 3.1 When to use Pastel vs Rich/Vibrant accents

| Register | Saturation / Lightness | Use when | Avoid when |
| --- | --- | --- | --- |
| **Calm Neutral** | Sat `5–12%`, Light `55–93%` | Body text: labels (`#A9A6B4`), values (`#ECE9F2`), muted/flavor (`#8A8597`), separators (`#5E596B`) | Never for major focal identity on rare+ gear |
| **Soft / Pastel** | Sat `35–55%`, Light `72–82%` | Low tiers (`Thường`/`Khá`), cozy/farming/healing/support items, cosmetics, starter tools, utility sub-stats | Endgame weapons, boss drops, fire/lava/void themes, urgent warnings (feels weak/washed-out) |
| **Rich / Vibrant** *(Jewel & Elemental)* | Sat `70–90%`, Light `58–72%` | High tiers (`Sử Thi`/`Huyền Thoại`/`Thần Thoại`), combat weapons, elemental/boss themes (fire, frost, void, venom), active skills, combat stat icons, low-durability/error alerts | Spreading across full sentences or every line (keep strictly to the 1 highlight per block) |
| **Raw RGB Neon** *(Banned)* | Sat `100%`, pure primary (`#FF0000`, `#00FF00`, `#FFFF00`) | **Never** — causes eye strain and visual clash | Always replace with Rich/Vibrant equivalents (`#FF5C5C`, `#4ADE80`, `#FACC15`) |

### 3.2 Base structural & status palette (WCAG measured on `#100010`)

| Role | Hex | Legacy hex | Contrast | Used for |
| --- | --- | --- | ---: | --- |
| Label | `#A9A6B4` | `&#A9A6B4` | 8.5:1 | Stat labels, effect text, `Nhóm` (always calm) |
| Value | `#ECE9F2` | `&#ECE9F2` | 17.0:1 | Numbers, `+N`, key words inside effects (clean crisp white-lilac) |
| Muted | `#8A8597` | `&#8A8597` | 5.7:1 | Cooldown, inactive set tier, flavor, binding, `/max` |
| Separator | `#5E596B` | `&#5E596B` | 3.0:1 | Only `·` and empty socket `◇`, never words |
| Ability | `#38BDF8` *(or theme)* | `&#38BDF8` | 9.5:1 | Skill name only (may shift to `#FF7A2F` fire, `#C084FC` void, `#34D399` nature) |
| Active | `#4ADE80` | `&#4ADE80` | 11.7:1 | Active set-bonus tier, requirement met (clear positive signal) |
| Currency | `#F5C451` | `&#F5C451` | 12.5:1 | Prices (AH/shop wrappers), never stats |
| Negative | `#FF5C5C` | `&#FF5C5C` | 6.7:1 | Low durability (`Cần sửa`), unmet requirement, expiring (urgent red, never weak pink) |

### 3.3 Rarity scale (saturation escalates with prestige)

Low tiers stay softer so high tiers visibly "light up" with jewel richness:

| Hạng | Register | Hex | Contrast |
| --- | --- | --- | ---: |
| Thường | Neutral | `#E4E2EC` | 15.9:1 |
| Khá | Soft | `#86D993` | 12.0:1 |
| Hiếm | Clean medium | `#6CA8F8` | 8.4:1 |
| Sử Thi | Rich amethyst | `#B878FF` | 7.0:1 |
| Huyền Thoại | Rich gold-amber | `#F5A623` | 10.1:1 |
| Thần Thoại | Rich ruby-rose | `#FF5C8A` | 6.9:1 |

### 3.4 Elemental & mood name palettes (optional for themed / boss / endgame gear)

By default, item names use the rarity color. For signature elemental, boss, or
endgame gear, the **name** (and skill title) may take its theme color while line
2 (`Nhóm · Hạng`) holds the canonical rarity color — keeping both emotional
identity and instant rarity readability:

| Theme / Mood | Primary Hex | Contrast | Optional 2-tone Gradient (highest tier only) | Feel |
| --- | --- | ---: | --- | --- |
| Lửa / Dung Nham / Nether | `#FF7A2F` | 7.9:1 | `#FF5C38` → `#FFB347` | Fierce, molten, aggressive |
| Băng / Thủy / Vương Quyền | `#38BDF8` / `#60A5FA` | 9.5:1 / 8.0:1 | `#38BDF8` → `#A5F3FC` | Glacial, sharp, regal |
| Huyết / Chiến Đấu / Boss | `#FF5C5C` | 6.7:1 | `#FF4D6D` → `#FF9A8B` | Lethal, high-stakes |
| Độc / Rừng / Ngọc Lục Bảo | `#34D399` | 10.6:1 | `#10B981` → `#86EFAC` | Venomous or vibrant nature |
| Hư Không / Ám Ảnh / Ma Pháp | `#C084FC` | 7.7:1 | `#A855F7` → `#F0ABFC` | Arcane, mysterious |
| Ấm Áp / Nông Trại / Hỗ Trợ | `#9FD3A8` / `#E6CF8F` | 12.2:1 / 13.3:1 | *(Keep solid pastel — no gradient needed)* | Relaxed, cozy, approachable |

Gradients: highest tier / signature centerpiece gear only, **name only**,
between two harmonious tones (both `>= 6.5:1` on `#100010`).

**Highlight budget: one per block.** Because 80% of the tooltip stays neutral,
rich highlights look crisp and deliberate instead of noisy.

| Block | The one highlight |
| --- | --- |
| Identity | Rarity or theme color on name; rarity color on the rarity word |
| Enchants | None: name Label, level Value |
| Core stats | The stat symbol (values stay `#ECE9F2`, never colored) |
| Gems | Gem colors |
| Set bonus | The active tier line (`#4ADE80`) |
| Skill | Skill name (Ability `#38BDF8` or item's theme accent) |
| Footer | Durability value (bright `#ECE9F2`, `#FF5C5C` when low) |

---

## 4. Identity line, rarity & term registry

- **Name:** rarity color by default, or the item's elemental/mood theme color
  (§3.4) for signature boss/endgame gear while line 2 holds the rarity color.
  Upgrade level follows as ` +3` in Value color, no brackets. Keep names `<= ~120 px` (about 20 characters) because `[item]` chat
  and AH show the name inline. No per-stat upgrade deltas such as `(+6)` in the
  tooltip; show those in the upgrade menu.
- **Line 2:** `<Nhóm> · <Hạng>`: group in Label, `·` in Separator, rarity word
  in rarity color.
  - Group vocabulary: `Công cụ`, `Vũ khí`, `Giáp`, `Phụ kiện`, `Tiêu hao`,
    `Nguyên liệu`, `Trang phục`, `Sự kiện` *(use `Sự kiện` only for pure event
    tickets/tokens/keepsakes that do not fit the other 7 groups; event weapons
    or armor keep `Vũ khí`/`Giáp` and put the event name in the footer)*.
  - **Never repeat a word from the name** (`Cúp Tinh Thạch` / `Cúp · Sử Thi` is
    wrong; use `Công cụ · Sử Thi`). The group line also covers names without a
    type word (`Băng Tâm` → `Vũ khí · Hiếm`).
- **Tier line position:** fixed by §2.1. Line 2 when enchants are rendered by
  lore or absent (case A); last line when vanilla enchant rows are visible
  (case B). Never color-only: new and color-blind players need the word.
- **Rarity ≠ origin:** Boss / Event / Season is origin and goes to the footer.
- **Term registry** (Vietnamese community terms):

| Item | Use | Never |
| --- | --- | --- |
| Pickaxe | `Cúp` | `Cuốc` |
| Sword / axe / bow | `Kiếm` / `Rìu` / `Cung` | English names |
| Helmet / chestplate / leggings / boots | `Mũ` / `Áo` / `Quần` / `Giày` | `HEAD`, `Helmet` |

Record server-specific stat and currency names in the project registry
(`pattern-library.md` `V0`) and reuse them exactly.

---

## 5. Stats & stat symbols

- Row grammar:
  - **Non-Pack servers (default):** `<Label>: <Value> <symbol>` (label `#A9A6B4`,
    value `#E8E4EE`, colored symbol after a single space — e.g.
    `<#A9A6B4>Tốc đào: <#E8E4EE>+45 <#E3C48A>⛏`). Placing Unicode symbols after
    the value keeps every stat label flush-left with zero ragged alignment, so
    servers do not have to fight mixed Unicode widths.
  - **Pack servers (§5.2):** `<#FFFFFF><glyph:stat_id> <#A9A6B4><Label>: <#E8E4EE><Value>`
    (leading pixel icon, since custom pack icons share one fixed advance).
- Explicit sign `+`/`−`; never repeat the unit or stat name in the value
  (`+28.5`, not `+28.5 ST`). Roll ranges use an en dash (`12–18`).
- Fixed stat order per class:
  - **Pickaxe:** Tốc đào → May mắn → Độ cứng
  - **Sword:** Sát thương → Chí mạng → Tốc đánh
  - **Armor:** Phòng thủ → Máu
- **Symbols on core stat rows only.** No symbols on identity, set bonus, skill,
  cooldown, durability, binding or flavor lines; that is where tooltips start
  to feel busy.
- Same stat = same symbol and color across the whole server.

### 5.1 Non-Pack Unicode symbols & verified 1.21.11 widths

Because Minecraft has no tab stops, **Non-Pack servers put Unicode stat symbols
at the end of the stat line** (`Tốc đào: +45 ⛏`). That keeps the left label
column straight even when symbols have different advances (e.g., `⛏` 9 px vs
`⚡` 6 px vs `✿` 8 px).

- Use **BMP characters only** (`<= U+FFFF`). Avoid `U+1Fxxx` emoji-plane
  symbols (`💥`, `🍀`, `🔥`) because some YAML pipelines and plugins mangle
  surrogate pairs or render fallback boxes.
- Recommended Non-Pack stat symbol registry (sources & widths verified directly
  in `minecraft-1.21.11-client.jar` `default.json` → `nonlatin_european.png`
  and `unifont.zip` 17.0.01):

| Stat | Symbol | Source (Java 1.21.11) | Advance | Color (Rich / Calm) |
| --- | --- | --- | ---: | --- |
| Tốc đào | `⛏` | Default bitmap (`nonlatin_european.png`) | 9 px | `#F5B942` (warm amber) |
| May mắn / Gia tài | `✿` or `☘` | Unifont | 8 / 7 px | `#34D399` (emerald) |
| Độ cứng | `⛰` | Unifont | 8 px | `#93B4DC` (slate-steel) |
| Nổ lan / Phá khối | `✹` | Unifont | 8 px | `#FF6B4A` (ember orange) |
| Sát thương | `⚔` | Default bitmap (`nonlatin_european.png`) | 8 px | `#FF5C5C` (combat crimson) |
| Chí mạng / ST Boss | `✷` or `☠` | Unifont / Default bitmap | 8 / 8 px | `#E879F9` (vivid magenta) |
| Tốc đánh / Tốc chạy | `⚡` or `➾` | Default bitmap / Unifont | 6 / 8 px | `#FACC15` (electric gold) |
| Phòng thủ | `⛨` or `⬣` | Default bitmap / Unifont | 8 / 8 px | `#7DD3FC` (sky shield) |
| Máu | `❤` | Default bitmap (`nonlatin_european.png`) | 8 px | `#FB7185` (vital rose-red) |
| Kinh nghiệm | `✦` | Unifont | 8 px | `#A3E635` (fresh lime) |

- **If a Non-Pack server still chooses leading Unicode icons** before stat
  labels (`<symbol> <Label>: <Value>`), every leading symbol in that stat block
  **must share the same advance width** (e.g., all 8 px: bitmap `⚔ ❤ ⛨ ☠ ⌛ ★ ❄`
  or Unifont `✿ ⛰ ✷ ➾ ⬣ ✦ ✹`). Check with
  `python scripts/lint_lore.py --measure "CHARS" --unifont <path to unifont.zip>`;
  `lint_lore.py` warns `STAT_ICON_WIDTH` whenever leading stat symbols mix
  widths.
- Gem sockets `◆ ◇` are both default bitmap **6 px**, so the socket row stays
  even. Multiplication sign `×` (`U+00D7`, default bitmap 6 px) and ASCII `x`
  (`3x3`, 6 px) have the same advance; ASCII `x` is safest across custom fonts.
- Unifont strokes are thinner than default bitmap strokes; check mixed pairs
  on an in-game screenshot. Bedrock/GeyserMC clients use their own font and may
  differ.

### 5.2 Pack servers (Nexo / ItemsAdder)

A pack server keeps the exact same skeleton, text colors, enchant cases,
durability rule and height. It swaps only three things (canonical render:
`gallery.md` `I6`):

1. **Leading pixel icons instead of trailing Unifont symbols.** Stat icons and
   gem sockets become bitmap glyphs. Every icon PNG is 7×7 art in an 8 px
   advance (the 1 px gap included), drawn in the registry color, with one shared
   `height` and `ascent` so the baseline matches text. Nexo `<glyph:id>` renders
   white by default unless `:colorable`/`:c` is used; adding `<#FFFFFF>` before
   raw PUA/non-Nexo glyphs prevents lore's default dark-purple tint. Use Nexo's
   `<shift:N>` only for deliberate per-pixel offsets.
2. **Rarity frame via `tooltip_style`** (1.21.2+): one style per rarity, each
   needing two sprites, `textures/gui/sprites/tooltip/<style>_background.png`
   and `<style>_frame.png` (with `.png.mcmeta` `nine_slice` metadata if scaled).
   Frame color = rarity color. Re-check text contrast on the new background
   (target `>= 4.5:1` as on `#100010`).
3. **Rarity pill glyph** replaces the colored rarity word on the tier line
   (`Công cụ · [Sử Thi]`); the line keeps its Case A/B position.

Asset checklist per pack: 3 pickaxe stat icons + 5 combat stat icons (one per
registry entry), gem icons per gem color + 1 empty socket, 6 rarity pills,
6 tooltip styles. Glyph ids in `I6` (`stat_dao`, `gem_empty`, `rarity_su_thi`…)
are examples: keep the server's real ids and verify tag syntax against the
installed Nexo version.

- Players without the pack see missing-glyph boxes, so pack-only lore requires
  a forced resource pack. Never rely on Unifont symbols for column alignment on
  a pack server.

---

## 6. Gems, set bonus & skills

**Gems:** one row `Ngọc khảm: ◆ ◆ ◇`. Filled sockets take the gem's color, empty
`◇` takes Separator. Gem effects are already folded into the stat values, so no
per-gem effect lines and no `(2/3)` count.

**Set bonus:**
```text
<#A9A6B4>Bộ Tinh Thạch <#8A8597>(2/4)
<#8FD9A8>2 món: +10% tốc đào
<#8A8597>4 món: +1 cấp Gia Tài
```
Active tier = whole line Active; inactive = whole line Muted. No `✔`/`✘`.

**Skill:**
```text
<#8CC8E8>Bùng Nổ Quặng <#8A8597>· Chuột phải
<#A9A6B4>Đào khối 3x3 trong <#E8E4EE>5 giây<#A9A6B4>.
<#8A8597>Hồi chiêu: 60 giây
```
- Name first (Ability color), trigger after `·` in Muted.
- Trigger vocabulary: `Chuột phải`, `Shift + Chuột phải`, `Shift + F`,
  `Khi đánh trúng`, `Khi bị đánh`, `Bị động`.
- 1–2 effect lines, key numbers in Value. Cooldown/cost on its own Muted row
  with a colon.
- One trigger per skill, and it must match the real mechanic. Never put menu
  CTAs (`Nhấn để…`, `Chuột trái:`) on gear.

---

## 7. Footer: flavor, durability, binding, origin

No blank lines inside the footer. Order: flavor → durability → binding/origin/expiry.

- **Flavor:** `<= 2` lines, italic, Muted. No world names (`Mine2`), commands or
  mechanic numbers. Proper names use Sino-Vietnamese canon (`Hàn Băng Vương`).
- **Durability:** its own line, always bright, because it asks the player to do
  something (repair):
  - Normal: `<#A9A6B4>Độ bền: <#ECE9F2>1.250<#8A8597>/1.561`
  - Low (`<= 10%`, or the project threshold):
    `<#A9A6B4>Độ bền: <#FF5C5C>86<#8A8597>/1.561 <#FF5C5C>· Cần sửa`
- **Binding / origin / expiry** (Muted unless urgent):
  - `Gắn hồn · Không thể giao dịch`
  - `Rơi từ Hàn Băng Vương · Gắn hồn`
  - `Sự kiện Halloween 2026` (always include the year)
  - `Hết hạn: 30/11/2026` (value turns Negative inside the last 24 h)

---

## 8. Height: the screen is the limit

No fixed category cap. The real limit is the screen. On 1080p, GUI Scale 4 fits
about **25 rendered lines** (name included) and GUI Scale 3 about 34. Overflow
gets clipped.

| Item | Typical length | Rule |
| --- | --- | --- |
| Material / drop | 3–5 lines | Identity · `Dùng để:` · `Nguồn rơi:` |
| Consumable / charm | 4–8 lines | Identity · effect + duration · cooldown |
| Tool / weapon / armor | 10–20 lines | Full skeleton as needed |
| Soulbound endgame gear | up to 24 lines (lore + vanilla) | Cannot be listed on AH |
| **Tradeable gear** | **lore + vanilla rows <= 19** | AH/trade adds ~5 rows; total must stay <= 24 |

- Count vanilla enchant/attribute rows too (`--vanilla-lines N`). For tradeable
  gear pass `--tradeable` (sets budget to `19`) or add 5 via `--vanilla-lines N+5`.
- The first 5 lines must answer: what is it, how rare/strong, can I use it.
- Balance pixel width only **inside** a block (`<= 25%`); never stretch stat
  rows to match a wide skill line.

---

## 9. Vanilla rows, plugin templates, chat & AH

- Real enchantments, `stored_enchantments` (Enchanted Books), `trim`,
  `dyed_color`, and `potion_contents` render **above** lore; vanilla attributes
  (`"Khi ở tay chính:"` in official `vi_vn.json`) and `unbreakable`
  (`"Không phá được"`) render **below**. All visible vanilla rows count toward
  height. Visible above-lore rows force the tier line to the bottom (§2.1 case B).
- Hide `attribute_modifiers` (`HIDE_ATTRIBUTES`) only when lore shows every
  relevant stat; hide `enchantments` (`HIDE_ENCHANTS`) or `stored_enchantments`
  only when lore re-displays them. On 1.21.5+, hide components explicitly via
  `tooltip_display.hidden_components` (`"enchantments"`, `"stored_enchantments"`,
  `"trim"`, `"dyed_color"`, `"potion_contents"`, `"attribute_modifiers"`,
  `"unbreakable"`).
- MMOItems / ItemsAdder / custom item plugins: change the shared template, not
  single items. Nexo / pack servers may use `tooltip_style` per rarity; re-check
  contrast on that background.
- Serializer: keep the plugin's format. MiniMessage uses `<#RRGGBB>`, legacy
  hex uses `&#RRGGBB`; never convert silently. Always disable inherited italics
  (`<!i>` / `ITALIC=false`).

---

## 10. NBT lifecycle

- Changing the format does not rewrite items already in inventories or vaults.
  Plan RevID/migration through `minecraft-custom-item-safety`.
- Dynamic rows (durability, kills, upgrade level, owner) use fixed formats
  (`1.250/1.561`, Vietnamese `.` thousands separator) so the tooltip does not
  jump around.

---

## 11. Canonical example

Approved render (`gallery.md` `I2`): 19 lore lines, passes
`lint_lore.py --profile item --strict`.

```yaml
item_cup_tinh_thach:
  material: NETHERITE_PICKAXE
  item_flags: [HIDE_ATTRIBUTES]   # 1.21.5+: tooltip_display hides attribute_modifiers
  display_name: "<!i><#B878FF>Cúp Tinh Thạch <#ECE9F2>+3"
  lore:
    - "<!i><#A9A6B4>Công cụ <#5E596B>· <#B878FF>Sử Thi"
    - ""
    - "<!i><#A9A6B4>Tốc đào: <#ECE9F2>+45 <#F5B942>⛏"
    - "<!i><#A9A6B4>May mắn: <#ECE9F2>+12% <#34D399>✿"
    - "<!i><#A9A6B4>Độ cứng: <#ECE9F2>Bậc 4 <#93B4DC>⛰"
    - ""
    - "<!i><#A9A6B4>Ngọc khảm: <#34D399>◆ <#38BDF8>◆ <#5E596B>◇"
    - ""
    - "<!i><#A9A6B4>Bộ Tinh Thạch <#8A8597>(2/4)"
    - "<!i><#4ADE80>2 món: +10% tốc đào"
    - "<!i><#8A8597>4 món: +1 cấp Gia Tài"
    - ""
    - "<!i><#38BDF8>Bùng Nổ Quặng <#8A8597>· Chuột phải"
    - "<!i><#A9A6B4>Đào khối 3x3 trong <#ECE9F2>5 giây<#A9A6B4>."
    - "<!i><#8A8597>Hồi chiêu: 60 giây"
    - ""
    - "<!i><italic><#8A8597>Rèn ở lò sâu nhất Mỏ Rùa."
    - "<!i><#A9A6B4>Độ bền: <#ECE9F2>1.250<#8A8597>/1.561"
    - "<!i><#8A8597>Gắn hồn · Không thể giao dịch"
```

Legacy-hex plugins write the same lines with `&#RRGGBB` (for example
`'&#A9A6B4Công cụ &#5E596B· &#C3A3F5Sử Thi'`).

---

## 12. Item Lore checklist

- [ ] **Safety:** shared template edited; IDs untouched; migration noted for
      existing items.
- [ ] **Skeleton:** blocks in §2 order, one blank line between blocks, peer
      items share block and stat order.
- [ ] **Identity:** name in rarity color (`+N` in Value); tier line is
      `Nhóm · Hạng` with no word repeated from the name; name `<= 120 px`.
- [ ] **Enchants & tier:** case A (above-lore vanilla rows hidden or absent;
      Anvil sync verified if player-enchantable) = tier on line 2, blank, enchant
      block; case B (vanilla `enchantments`/`stored_enchantments`/`trim` visible)
      = tier is the last line (`attribute_modifiers`/`unbreakable` hidden if stats
      are in lore) and pure Case B lore opens with a blank line. Same case for the
      whole item family.
- [ ] **Palette & mood:** neutral body (`#A9A6B4`/`#ECE9F2`/`#8A8597`) + intentional
      accent saturation matched to rarity/theme (§3.1–§3.4); no vanilla legacy
      colors or raw 100% RGB neon; `#5E596B` only on `·`/`◇`.
- [ ] **Highlights:** exactly one highlight per block; stat values not colored.
- [ ] **Symbols:** only on core stat rows, from the registry, render-checked in
      game before server-wide use.
- [ ] **Gems & set:** gems in their own block, no per-gem lines; set tiers as
      whole-line Active/Muted, no `✔`/`✘`.
- [ ] **Skill:** `Tên · Trigger`, 1–2 effect lines, `Hồi chiêu:` row, mechanic
      matches the code, no menu CTA.
- [ ] **Footer:** flavor `<= 2` lines without meta leaks; durability bright and
      red when low; binding/origin/expiry muted.
- [ ] **Terms:** `Cúp` (never `Cuốc`), group vocabulary, registry stat names,
      `.` thousands separator.
- [ ] **Height:** lore + vanilla `<= 24`; tradeable gear `<= 19` (AH headroom).
- [ ] **Lint:** `python scripts/lint_lore.py <file> --profile item
      --vanilla-lines <N> [--tradeable] --strict` clean; in-game render disclosed
      if not done.
