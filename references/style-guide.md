# Minecraft GUI Name & Lore Style Guide

Authoritative standard for player-facing Minecraft **GUI menu** names, lore, and
inventory titles. For **carried/equipped items** (weapons, tools, armor, charms,
materials), read [item-lore.md](item-lore.md) instead (sharing only §2.3 pixel
table, §3 typography/encoding safety, and §4.3 contrast table below).

Read alongside [pattern-library.md](pattern-library.md), [gallery.md](gallery.md),
and verify with [../scripts/lint_lore.py](../scripts/lint_lore.py).

## Contents

1. [Purpose & priority order](#1-purpose--priority-order)
2. [Decision-first hierarchy, pixel budget & vertical fit](#2-decision-first-hierarchy-pixel-budget--vertical-fit)
3. [Typography & Vietnamese safety](#3-typography--vietnamese-safety)
4. [Color system & WCAG contrast](#4-color-system--wcag-contrast)
5. [Spacing & inventory title contrast](#5-spacing--inventory-title-contrast)
6. [Carried & equipped items](#6-carried--equipped-items)
7. [Concrete serializer examples](#7-concrete-serializer-examples)
8. [Final checklist](#8-final-checklist)

---

## 1. Purpose & priority order

Make Minecraft GUI tooltips immediately scannable in **under 1 second**, visually
balanced, high-contrast, and consistent across peer buttons. When rules compete,
resolve in order:

1. **Hard plugin validators & data safety:** code-level checks (e.g., strict
   `<= 23` char rejection), placeholders, click semantics, encoding/BOM.
2. **Decision-first hierarchy & contrast:** critical status/price/requirement in
   the top 1–2 lines on action buttons; readable contrast (`>= 4.5:1` on
   `#100010`); one hue = one role per tooltip.
3. **Pixel balance & viewport fit:** Mojang 1.21.11 pixel budgets (`<= 140 px`
   data / `<= 185 px` description), group justification (`<= 25%`), width band
   (`<= 35%`), and vertical budget (`<= 14` lines).

---

## 2. Decision-first hierarchy, pixel budget & vertical fit

### 2.1 Decision-first ordering (1-second scan test)

Players sweep 6–10 slots per second and read only the top 2–3 lines first:

- **Decision buttons** *(buy, claim, upgrade, warp, unlock, locked slot)*: place
  **status, cost, or eligibility requirement in lines 1–2** directly under the
  name. Keep explanatory description to `<= 2` lines *below* decision facts (or
  omit when the title + stats already explain the slot).
- **Discovery / showcase buttons** *(feature hub, guide, mode overview)*:
  putting a 2-line description first is fine because there is no cost/gate.
- **1-second test:** cover everything from lore line 4 downward. Can a player
  immediately tell (1) what this is, (2) whether they can use/afford it, and
  (3) what happens on click? If not, move the decisive line up.

### 2.2 Bold by role, not by default

- **May be bold:** a short prominent item name; a short section label; a primary
  conversion CTA or badge of **`<= 4` words**.
- **Never bold:** descriptions, label/value data rows, requirement sentences,
  long lines, consecutive lore lines, or inventory titles by default (§5.2).
- Keep **at most ~2 bold regions per tooltip** (counted per contiguous bold
  span). Prefer position and color hierarchy before bold; peer slots share the
  same bold choice.

### 2.3 Pixel budgets & Mojang 1.21.11 default font table

Vietnamese uses more characters than English for the same phrase (`Left-click`
vs `Chuột trái`) and wide accented glyphs (`ư/ơ = 8 px`, `đ = 7 px`). Measure
line density by **rendered pixel budget** first, using character count only as a
quick reference — **never truncate natural Vietnamese phrases** (e.g. `Số dư hiện`,
`Shift + Trái`, `Chuột trái gia hạn`) merely to chase 23 characters! Rephrase
naturally (`Bạn đang có: 45 Xu`, `Shift + Chuột trái`) or accept a wider line
within pixel budget (unless a hard plugin-code validator enforces a strict cap).

| Tier | Applies to | Pixel budget (`vanilla-1.21.11`) | Char reference | Word ceiling |
| --- | --- | --- | --- | --- |
| **Data tier** | Names, label/value rows, rewards, costs, CTAs | **`<= 140 px`** *(preferred; warn `> 165 px`)* | ~23–27 VN chars | `<= 7` words |
| **Description tier** | Wrapped descriptions & guidance sentences | **`<= 185 px`** *(warn `> 185 px`)* | ~30–36 VN chars | `<= 9` words |

Count **visible NFC code points** after realistic placeholder expansion,
excluding formatting tags/codes (disclose unbounded placeholder ranges; never
truncate player names or numbers).

**Official Mojang Java 1.21.11 default bitmap/space advance widths (`uniform=false`, incl. 1 px gap):**

| Character class (Mojang Java 1.21.11) | Width (px) |
| --- | --- |
| `!`, `'`, `,`, `.`, `:`, `;`, `i`, `\|`, `ị`, `·` | `2 px` |
| `` ` ``, `l`, `ì`, `í`, `•` | `3 px` |
| space (` `), `"`, `(`, `)`, `*`, `I`, `[`, `]`, `t`, `{`, `}`, `ỉ`, `Ì`, `Í`, `Ỉ`, `Ị` | `4 px` |
| `<`, `>`, `f`, `k`, `ĩ`, `Ĩ`, `●` | `5 px` |
| Standard ASCII (`a..z`, `A..Z`, `0–9`), `à..ậ`, `è..ệ`, `ò..ộ`, `ù..ụ`, `ỳ..ỵ`, `○`, `♥` | `6 px` |
| `@`, `~`, `đ`, `Đ`, `✔`, `✘`, `«`, `»`, `–` | `7 px` |
| `ơ..ợ`, `ư..ự` (upper & lower), `→`, `⚔`, `❤`, `★`, `❄` | `8 px` |
| `—` | `9 px` |
| **Bold (`&l` / `<bold>`) modifier** | **`+1 px` per visible character** |

*(Glyphs outside the default bitmap — such as `➟`, `✦`, `➲`, or small-caps — fall
back to Unifont or a resource pack; treat their widths as unverified until
rendered in-client.)*

**Justification rules:**
- **Group justification (mandatory):** consecutive lines in one semantic group
  (wrapped descriptions, peer fact rows, multi-line guidance, including trailing
  lines) must stay within **`<= 25%` rendered pixel delta** (`lint_lore.py`
  warns strictly above `25%`). Never break inside tightly bound phrases (e.g.,
  never split `dành / cho` across two lines).
- **Whole-tooltip width band (GUI menus):** content blocks in one tooltip must
  stay within **`<= 35%` max-width divergence** (excluding short names, `H2`
  subtitles, section headers, badges, and compact single-line CTAs).
- **No space padding:** never pad with spaces to fake alignment (sole exception:
  render-verified `H4` centered title).

### 2.4 Vertical height budget (GUI Scale 3–4)

| GUI Tooltip type | Recommended rendered lore lines (incl. blanks) |
| --- | --- |
| Simple navigation / back / close button | `3–5` lines |
| Info, shop offer, warp, or action button | `6–10` lines |
| Dense detail panel (rank, upgrade, milestone) | `<= 14` lines (`lint_lore.py` warns above `14`) |

If a GUI panel exceeds `14` lines, split into sub-tabs or move secondary info to
a preview menu instead of clipping at GUI Scale 3–4.

---

## 3. Typography & Vietnamese safety

### 3.1 Inherited italics

Minecraft defaults item names and lore to italic. Disable explicitly unless
italics carry a deliberate flavor/quote role:
- **Adventure / Paper API:** `component.decoration(TextDecoration.ITALIC, false)`
- **MiniMessage:** prefix each line with `<!i>` (or `<i:false>`).
- **Legacy plugins:** check whether the plugin strips italics automatically;
  never mechanically prepend `&r` without verifying font-fallback behavior.

### 3.2 Tiny font, glyphs & provenance

- Keep values, costs, requirements, and CTAs in normal font. Tiny font is
  optional only for verified short secondary labels; **never mix normal and tiny
  fonts on the same row**, never strip Vietnamese diacritics to fit small-caps,
  and fall back to normal font whenever tiny support is unverified.
- **Arrow convention:** preserve the arrow proven in the target GUI. For new
  Non-Pack GUIs, default to `→` (`8 px`, in vanilla 1.21.11 bitmap); use `➟`
  only when verified on the target client.
- **Reference provenance:** never import mechanics, numbers, or commands from
  example templates as facts about the live server; always inspect real configs.

### 3.3 Vietnamese display failure triage & encoding safety

Classify before editing:
- **Mojibake** (`Luáº­t`, `CÃ i`) → encoding mismatch, not a font error.
- **Box / `?` / blank** → missing glyph in active font/pack.
- **Mixed typefaces / baselines** → font fallback (often triggered by `&r` or
  Unifont symbols).
- **Intact slanted text** → inherited item-meta italic.

Preserve original file encoding (UTF-8), BOM, and line endings. For remote
writes, back up exact bytes, upload with matching encoding, and reread before
reload. Never introduce unverified Unicode symbols, font tags, or `&r` resets
into a live GUI without same-surface render evidence.

---

## 4. Color system & WCAG contrast

### 4.1 Neutral base & single-role color discipline

- Default tooltip base is Minecraft gray (`&7` / `<gray>`, `8.8:1` on `#100010`),
  with `&f` / `<white>` selectively for clean values. Do not swap `&7` for
  slate/blue-gray unless standardized across the entire server. (Carried items
  never use this base: they follow the neutral-body + mood/rarity palette in
  [item-lore.md](item-lore.md) §3.)
- **Match accent saturation to menu mood & stakes:** use calmer/pastel accents
  for utility, settings, info, or cozy menus; use richer, higher-saturation
  jewel tones (Sat `70–90%`, Light `58–72%`, `>= 6:1` on `#100010`) for combat,
  bosses, high-tier rewards, and urgent warnings — while avoiding raw 100% RGB
  neon (`#FF0000`, `#00FF00`, `#FFFF00`) that strains the eyes.
- Highlight 1–2 scan anchors per informative block, then **return to `&7`** so
  trailing copy and punctuation stay neutral. Never color word-by-word.
- **One hue = one role per tooltip:** never assign the same color to two
  different meanings in one tooltip (e.g., never use gold simultaneously for
  expiring warning, Xu price, and CTA).
- **Distinguishable adjacent accents:** never place near-duplicate hues side by
  side (e.g., sky `#38BDF8` next to `aqua #55FFFF`, or `#FFD54F` next to
  `#FFE57F`) — at pixel size they blur together.
- **Separate `V1` resource colors from `V6` urgency colors:** record both tables
  in project docs so urgency amber/orange (e.g. `#FF9F43`) never collides with
  gold currency (`&e` / `#FFD54F`).

### 4.2 Color budget

For a multi-block GUI tooltip:
- **Neutral family:** `&7` base + `&f` emphasis + `#8C8CA0` for muted
  subtitles/flavor (`&8` only for brackets/dividers `<= 3` words).
- **1 primary accent:** item/card identity (a gradient counts as primary; max 1
  prominent gradient/item, never on long text).
- **1–2 supporting accents:** distinct semantic roles (e.g., action, value/cost,
  preview). Never exceed 2 supporting accents in one tooltip.
- **State colors:** available / warning / locked (reuse a supporting accent when
  the role overlaps; for long status lines, keep the label `&7` and color only
  the state/value). Server-wide `V1` resource colors on reward values do not
  count against the accent budget while labels stay `&7`.

### 4.3 WCAG contrast table on `#100010` tooltip surface

| Color | Ratio on `#100010` | Policy |
| --- | ---: | --- |
| `&1 #0000AA`, `#3F0A8D`, `&0 #000000` | `1.0–1.6:1` | **Banned** for text |
| `&4 #AA0000` | `2.6:1` | **Banned** for text (use `&c #FF5555` or `#F87171`) |
| `&8 #555555` (`dark_gray`) | `2.7:1` | **Brackets, dividers (`·`), borders, unfilled bar (`V4`) only**; banned on lines `> 3` words |
| `&5 #AA00AA` | `3.2:1` | Short bold tags only; prefer `#C084FC` / `#D946EF` |
| `&9 #5555FF` | `4.0:1` | Marginal; prefer `#6CA8FF` (`8.4:1`) |
| `#8C8CA0` (muted neutral) | `6.2:1` | **Recommended** for flavor lines & secondary subtitles (or `&7` in legacy-only) |
| `&7 #AAAAAA` | `8.8:1` | **Default base** for descriptions & labels |
| `#38BDF8`, `#A78BFA`, `#F472B6`, `#4ADE80`, `#FFD54F` | `7.5–13.5:1` | **Good** primary/supporting accents |

**Thresholds:** readable text **`>= 4.5:1`** · structural punctuation/brackets
**`>= 2.5:1`** · anything `< 3.0:1` is banned for readable text.

---

## 5. Spacing & inventory title contrast

### 5.1 Blank lines & tooltip structure

- Use a blank lore line **only** between genuinely independent groups (decision
  status/cost, description, rewards, CTA). Never isolate every line.
- Use [pattern-library.md](pattern-library.md) for reusable tooltip structures
  and [gallery.md](gallery.md) for lint-verified examples.

### 5.2 Inventory titles vs tooltips

- **Inventory title** sits on vanilla light gray (`#C6C6C6`) or a bright pack
  panel. Use **dark charcoal `#404040` (`6.1:1`), `#1F2937` (`8.6:1`), or `&0`**
  in **Title Case** — **avoid `&8`** (`4.4:1`, below AA threshold on `#C6C6C6`),
  no leading spaces, no ALL CAPS, no default `&l`.
- **Title width limit:** a 9-column chest header fits ~160 px; keep titles
  **`<= 150 px`** (~25–26 Vietnamese chars) so text never clips out of the frame.
- **Client advanced tooltips (`F3+H`):** ignore namespaced IDs and component
  counts when auditing plugin copy.

---

## 6. Carried & equipped items

Do **not** force weapons, tools, armor, charms, boss souls, or materials into
GUI menu rules (14-line cap, 35% band, decision-first CTA). Follow the dedicated
"ARPG gọn, bản dịu" guide in **[references/item-lore.md](item-lore.md)** and run
`scripts/lint_lore.py --profile item`.

---

## 7. Concrete serializer examples

Both examples below strictly pass `scripts/lint_lore.py --strict` (`0 error, 0
warn`), follow decision-first ordering, 1-hue-1-role, WCAG `>= 4.5:1`, and
action-colored CTAs.

### Example A — Paper / Adventure MiniMessage (Decision Button, Non-Pack OK)

```yaml
title: "<#1F2937>Kho Báu Biển Cả"
name: "<!i><#38BDF8>Hòm Báu Thủy Triều"
lore:
  - "<!i><#38BDF8>| <gray>Trạng thái: <green>Sẵn sàng"
  - "<!i><#38BDF8>| <gray>Phần thưởng: <white>3–5 vật phẩm"
  - ""
  - "<!i><gray>Chứa kho báu đại dương hiếm,"
  - "<!i><gray>mở lại sau mỗi <gold>24 giờ<gray> chơi."
  - ""
  - "<!i><gray>Chuột trái: <green>Nhận vật phẩm"
  - "<!i><gray>Chuột phải: <#38BDF8>Xem trước rương"
```

*(Roles: `#38BDF8` identity/preview, `<green>` ready/primary claim, `<gold>`
cooldown timer, `<white>` quantity — zero colliding hues!)*

### Example B — DeluxeMenus / Legacy + Hex (Shop Offer, Non-Pack OK)

```yaml
menu_title: '&#1F2937Cửa Hàng Danh Vọng'
display_name: '&#38BDF8Thẻ Mũ Câu Cá'
lore:
  - '&#8C8CA0Trang Phục · Mũ'
  - ''
  - '&#38BDF8| &7Giá đổi: &#FFD54F10 Danh Vọng'
  - '&#38BDF8| &7Bạn có: &#4ADE8014 Danh Vọng ✔'
  - ''
  - '&7Mở khóa trang phục đặc biệt'
  - '&7dành cho cần thủ kỳ cựu.'
  - ''
  - '&#4ADE80→ Nhấn để đổi ngay'
```

*(See [references/gallery.md](references/gallery.md) for all 14 role-specific
golden examples (`G1–G8` & `I1–I6`) verified with `lint_lore.py --strict`.)*

---

## 8. Final checklist (GUI Menu)

- [ ] **Surface & validator:** confirmed GUI Menu surface; target plugin's hard
      validators, placeholders, click semantics, and encoding/BOM are intact.
- [ ] **Decision-first (1-second test):** covering lore line 4+ still tells the
      player what this is, whether they can use/afford it, and what clicking does.
- [ ] **Pixel budget & natural Vietnamese:** data rows `<= 140 px` (`<= 7` words),
      descriptions `<= 185 px` (`<= 9` words), no chopped Vietnamese phrases, no
      broken phrase pairs (`dành / cho`).
- [ ] **Pixel balance & width band:** consecutive peer lines within `<= 25%`
      width delta; content blocks within `<= 35%` band; no space padding.
- [ ] **Vertical fit:** `3–5` (nav), `6–10` (standard), `<= 14` (dense panel).
- [ ] **WCAG contrast:** readable text `>= 4.5:1` on `#100010`; no `&1`/`&4`/
      `#3F0A8D`; no `&8` on lines `> 3` words; flavor/subtitle uses `#8C8CA0` or `&7`.
- [ ] **Single-role color budget:** `&7` base + 1 primary + 1–2 supporting
      accents; 1 hue = 1 role; no near-duplicate hues; `V6` urgency separate
      from `V1` resource colors.
- [ ] **Bold & non-italic:** `<!i>` / `ITALIC=false` applied; role-based bold
      only (`<= 4` words, `<= 2` spans, never on data rows or default titles).
- [ ] **Dynamic eligibility & guided locks:** requirement rows reflect player
      state (`✔` green / red missing count) when supported; locked buttons state
      what's missing and how to earn it.
- [ ] **CTA & bulk safety:** action phrase colored (not mouse label); bulk or
      irreversible actions preview total cost/consequences in the tooltip;
      warning color agrees with label semantics.
- [ ] **Pattern & glyph hygiene:** peers share one recipe from `gallery.md`,
      `<= 3` devices/tooltip, one marker per section (`○`, `•`, or thin `|`; no
      chunky `▍`), no unverified glyphs or blind `&r`.
- [ ] **Inventory title:** inventory title `#404040` or darker, Title Case,
      `<= 150 px`.
- [ ] **Terminology (`V0`):** consistent server currency/stat/number naming, no
      redundant units (`+20 Bụi Sao` under `Bụi Sao:`).
- [ ] **Strict lint run:** `python scripts/lint_lore.py <file> --strict` clean.
- [ ] **Render honesty:** verified in-game via screenshot, or unverified client
      rendering explicitly disclosed.

When two valid options tie, choose the one that is **clearer in 1 second,
higher-contrast, more natural in Vietnamese, and less decorated**.
