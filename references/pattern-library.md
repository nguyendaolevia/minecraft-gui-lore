# Minecraft GUI Lore Pattern Library

Role-based tooltip patterns for Minecraft **GUI menus**. For carried/equipped
item lore, see [item-lore.md](item-lore.md). For complete lint-clean examples
of every role, see [gallery.md](gallery.md).

Compatibility tags:
- **`[Non-Pack OK]`** — verified in Mojang Java 1.21.11 default bitmap/space
  font without a custom resource pack.
- **`[Resource Pack]`** — requires custom pack glyphs/fonts (use fallback on
  Non-Pack servers).
- **`[Unverified]`** — falls back to Unifont in vanilla; verify in-client before
  shipping.

## Contents

1. [Choosing patterns](#1-choosing-patterns)
2. [Header patterns](#2-header-patterns)
3. [Body grouping patterns](#3-body-grouping-patterns)
4. [Value, registry & multi-state patterns](#4-value-registry--multi-state-patterns)
5. [Call-to-action patterns](#5-call-to-action-patterns)
6. [Recipes by item role](#6-recipes-by-item-role)
7. [Reference lessons: do not copy](#7-reference-lessons-do-not-copy)

---

## 1. Choosing patterns

- Pick by item role and decision priority, never by habit. Peer slots in one
  GUI share one recipe; variety comes from distinct roles.
- Stack **at most ~3 structural devices** per tooltip (e.g., bracketed name +
  thin-bar block + CTA).
- Use **one row marker per section** (`○`, `•`, or thin `|`); never mix markers
  in the same section and never use chunky block bars (`▍`, `▎`, `▌`).
- Keep simple navigation, filler, and back buttons compact (`3–5` lines).

---

## 2. Header patterns

### H1. Bracketed name `[Non-Pack OK]`

```text
<dark_gray>[<accent>Quà Đăng Nhập<dark_gray>]
```

- For selectable list entries: milestones, reward slots, upgrades. Dark gray
  `&8` is valid on the brackets (`2.7:1` structural punctuation); the title uses
  a readable accent (`>= 4.5:1`). Avoid combining with `H4`.

### H2. Name plus category subtitle `[Non-Pack OK]`

```text
<#38BDF8>Thuốc May Mắn I
<#8C8CA0>Thuốc Đào Mỏ
```

- Short 2–3 word metadata subtitle (`Thuốc Đào Mỏ`, `Trang Phục · Mũ`). Use
  `#8C8CA0` (`6.2:1`) or `&7` — **not `&8`** — so metadata stays comfortable to
  read. Never place requirements or costs here, and never fold `[Category]` onto
  the display-name line as an ad-hoc H1/H2 hybrid.

### H3. Rarity or state badge `[Resource Pack]` *(fallback `[Non-Pack OK]`)*

- Custom pack glyph plate placed under the name or at tooltip bottom (max 1 per
  tooltip). Non-Pack fallback: `<dark_gray>[<state_color>Đã Mở Khóa<dark_gray>]`.

### H4. Centered title `[Resource Pack]` *(conditional `[Non-Pack OK]`)*

- For wide detail panels whose body is visibly wider than the name. Requires
  pixel-computed leading space or negative-space font — sole exception to "no
  space padding", on the name line only, and **requires in-game render check**.

### H5. Icon prefix `[Resource Pack]`

- Custom pack icon before the name on showcase/mode selectors. Omit on Non-Pack.

---

## 3. Body grouping patterns

### B1. Bullet or thin-bar rows `[Non-Pack OK]`

```text
<gray>• Kim Cương: <aqua>25
<gray>• Chìa Khóa: <light_purple>x1

<#38BDF8>| <gray>Trạng thái: <green>Sẵn sàng
<#38BDF8>| <gray>Yêu cầu: <red>Cấp 45 <#8C8CA0>(bạn: 38)
```

- For short peer fact/reward/requirement lists (`<= 5` rows).
- Choose **one** marker per section:
  - **`|`** (`2 px`, vanilla bitmap): crisp, takes section/card accent color.
  - **`•`** (`3 px`, vanilla bitmap): compact neutral bullet; avoids `○` (`6 px`)
    looking like lowercase letter `o` at small pixel sizes.
  - **`○`** (`6 px`, vanilla bitmap): lighter open bullet for reward lists
    (verify visual clarity against lowercase `o` in-game).
- **Dynamic eligibility (`M-2`):** when the plugin supports conditional
  placeholders, color requirement values by player state (`<green>✔` when met,
  `<red>` + current value when unmet); otherwise keep neutral `&f`.

### B2. Accent vertical bar block `[Non-Pack OK]`

```text
<#A78BFA>Thông Tin
<#A78BFA>| <gray>Cấp hiện tại: <white>Lv.12<gray>/50
<#A78BFA>| <gray>Hiệu quả: <white>+26% <gray>→ <green>+28%
```

- Multi-section detail block where thin `|` takes its section header's color
  and binds rows + wrapped continuations into one clean block. Always use thin
  `|`, never chunky block bars (`▍`, `▎`, `▌`).

### B3. Section header `[Non-Pack OK]`

- Short Title Case label (`Thông Tin`, `Phần Thưởng`, `Nâng Cấp`) in section
  accent. May be bold (within 2-region budget) or verified tiny font, never both
  on a long label. Equivalent headers share identical styling.

### B4. Centered divider header `[Non-Pack OK]`

```text
<gold>——— <yellow>Tính Năng <gold>———
```

- Wide showcase/overview tooltips only; never on compact buttons. Keep both
  sides symmetric.

### B5. Arrow sub-header `[Unverified]` *(fallback `B3`)*

```text
<white>➲ <yellow>Thông Tin
```

- `➲` is **not** in Mojang 1.21.11's default bitmap (falls back to Unifont).
  Verify in-client before use, or use plain `B3`.

### B6. Plain label/value rows `[Non-Pack OK]`

- Labels and colons stay `&7`; values take semantic colors. Align label phrasing
  so peer rows stay within `<= 25%` width delta.

---

## 4. Value, registry & multi-state patterns

### V0. Server term & formatting registry `[Non-Pack OK]`

Record one canonical Vietnamese term & number format per server (never mix
English/Vietnamese or duplicate units):
- Currency & item names (`Xu`, `Bụi Sao`, `Đá Lapis`, `Cần thủ` instead of
  awkward `ngư thủ`; avoid mixing `HEAD`, `Coins`, `Common` unless explicitly
  adopted in server registry).
- Number separator (`75.000` **or** `75,000` — pick one server-wide).
- No redundant units: write `Sát thương: +28.5` (not `+28.5 ST`), `Bụi Sao: +20`
  (not `Bụi Sao: +20 Bụi Sao`), `Chí mạng: +12%` (not `+12% tỷ lệ`).

### V1. Resource color registry `[Non-Pack OK]`

- Assign one fixed color (`>= 4.5:1` on `#100010`) per currency, resource, key,
  or crate server-wide and record it in project docs.
- Registry colors mark values/quantities only (labels stay `&7`) and are exempt
  from the tooltip accent budget. **Never** reuse a `V1` currency color inside
  the `V6` urgency scale on the same tooltip.

### V2. Quantity notation `[Non-Pack OK]`

- Standardize one server-wide notation: suffix (`Chìa Phổ Thông x1`) or prefix
  (`3x Chìa Phổ Thông`).

### V3. Fixed-width timers `[Non-Pack OK]`

- Format live countdowns cleanly (`00h 29m 12s` or `02p 00s`) so width does not
  jitter. Label stays `&7`.

### V4. Progress bar `[Non-Pack OK]`

```text
<gray>Tiến độ: <dark_gray>[<green>|||||<dark_gray>:::::] <white>10<gray>/20
```

- Filled segment uses `<green>` (or accent); **unfilled segment uses `<dark_gray>`
  (`&8`), never `<red>`** (red signals error/danger, not normal progress).
- Always show absolute counts (`10/20`) alongside or instead of bare `%` so
  players immediately know how much remains.

### V5. Multicolor showcase list `[Non-Pack OK]`

- Distinct line colors are allowed **only** when each row names a feature whose
  color already identifies it elsewhere (its own icon/menu). Never use rainbow
  coloring for decoration.

### V6. Multi-state status & urgency shift `[Non-Pack OK]`

```text
<green>● Thẻ đang kích hoạt            # healthy (> 15d)
<#FF9F43>● Thẻ sắp hết hạn             # expiring soon (1..15d) — distinct from gold Xu!
<red>✘ Thẻ chưa kích hoạt              # inactive / blocked
```

- Keep the **exact same tooltip skeleton AND CTA phrasing** across active states
  (do not drop words like `"để"` between states!); change only the state marker
  (`●`, `✔`, `✘`), material, and state color, and swap the action CTA for a
  guided `C4` locked footer when blocked.
- Choose an urgency scale (`<green>` → orange `#FF9F43` → `<red>`) that **never
  collides** with `V1` currency colors (e.g., yellow/gold `Xu`) in the same card.

### V7. Upgrade delta & bulk cost preview `[Non-Pack OK]`

```text
<#A78BFA>| <gray>Hiệu quả: <white>+26% <gray>→ <green>+28%
<#A78BFA>| <gray>Nâng tối đa: <white>8 cấp <dark_gray>· <gold>21.000 Lapis
```

- Always show **current → next** (`+26% → +28%`) on upgrades so players know
  whether the value is a new total or an increment.
- Any bulk or irreversible action (`Shift + Chuột trái`) **must** preview total
  cost/levels in the tooltip or require an explicit confirmation step.

---

## 5. Call-to-action patterns

The CTA is the final block, separated by one blank line. Color the **action
phrase** as one cohesive unit — never color only the first word, and on
label-first CTAs color the **action**, not the mouse button label!

### C1. Arrow CTA `[Non-Pack OK]`

```text
<green>→ Chuột trái để mở
```

- Compact single action (`<= 5` words may use one solid action color). Default
  arrow is `→` (`8 px`, vanilla bitmap); use `➟` only when already standardized
  and glyph-verified on the target server.

### C2. Multi-click CTA `[Resource Pack]` *(Non-Pack fallback `[Non-Pack OK]`)*

```text
# Non-Pack (color the ACTION, keep mouse label neutral gray):
<gray>Chuột trái: <green>Nâng thêm 1 cấp
<gray>Shift + Chuột trái: <#38BDF8>Nâng tối đa

# Resource Pack:
<white>{mouse_icon} <gray>Nhấn để <green>nâng 1 cấp
<white>Shift + {mouse_icon} <gray>Nhấn để <#38BDF8>nâng tối đa
```

- Keeping `Chuột trái:` neutral `&7` lets the player's eye jump straight to the
  action phrase instead of stopping on the word "Chuột trái".

### C3. Emphasis CTA `[Non-Pack OK]`

- Bold **Title Case** CTA (`<= 4` words, e.g., `<green><bold>Nhận Ngay`) for a
  high-value conversion action (purchase, claim). Avoid ALL CAPS Vietnamese with
  stacked diacritics (`Ấ`, `Ệ`, `Ở`), which collide vertically in 10 px line
  height. Max 1 per tooltip, used sparingly.

### C4. Guided locked / unavailable footer `[Non-Pack OK]`

```text
<red>✘ Còn thiếu 54 Xu
<gray>Kiếm thêm tại <white>/nhiemvu
```

- Never leave a dead-end `[Chưa Đủ Xu]` label alone. Show the **exact shortage**
  (when placeholders permit) plus **one short next step** telling the player how
  to unlock or earn it (use real commands verified in server config).

### C5. Plain action line or Card-accent CTA `[Non-Pack OK]`

```text
<green>Nhấn để xem chi tiết
<#38BDF8>Nhấn để dịch chuyển           # matches card's primary accent
```

- In multi-card navigation/feature hubs (Warps, Fishing, Hub) where each card
  has its own distinct accent, a compact CTA may match that card's primary
  accent to keep each card visually unified. Reserve explicit green/red CTAs for
  transactions, confirmations, and blocked states.

---

## 6. Recipes by item role

Use this table as an index into **[references/gallery.md](gallery.md)**, which
contains a complete, `lint_lore.py --strict` verified tooltip for every role:

| Item role | Ordering | Patterns | Gallery ID |
| --- | --- | --- | --- |
| Navigation / back button | Plain | `C1` or `C5` | `G1` |
| Warp / hub card | Decision-first (`M-2`) | `B1 (\|)`, `C5` (card-accent) | `G2` |
| Daily / playtime reward | Decision-first | `H1`, `B1 (•)` + `V1`, `V3`, `C1`/`C4` | `G3` |
| Multi-state slot (pass/home/gacha) | Decision-first | `V6`, `C1`/`C4` | `G4` |
| Level / quest milestone | Decision-first | `H1`, `V4`, `B1 (○/•)` | `G5` |
| Shop offer / consumable | Decision-first | `H2`, `B1 (\|)` + `M-2`, `C1`/`C4` | `G6` |
| Upgrade / enchant entry | Decision-first | `H1`, `B3` + `B2 (\|)`, `V7`, `C2` | `G7` |
| Confirmation (destructive) | Decision-first | Consequence + warning CTA | `G8` |
| Carried / equipped gear | ARPG gọn (nền dịu, điểm nhấn theo cảm xúc) | See [item-lore.md](item-lore.md) | `I1–I6` |

---

## 7. Reference lessons: do not copy

- Never chop Vietnamese words (`Số dư hiện`, `Shift + Trái`) to chase 23 chars.
- Never let one color hold multiple meanings in one tooltip (e.g., gold for
  warning + currency + CTA).
- Never use `&8` (`2.7:1`) on sentences `> 3` words or flavor text; use
  `#8C8CA0` (`6.2:1`) or `&7`.
- Never color `Chuột trái:` while leaving the action phrase white on Non-Pack
  CTAs; color the action phrase.
- Never leave a blocked/locked state without telling the player what is missing
  or how to unlock it.
- Never color unfilled progress bar segments red; use `&8`.
- Never use chunky block bars (`▍`, `▎`, `▌`) as row markers; use thin `|`.
- Never pair a destructive/warning label with a positive block material (e.g.,
  red "Xác nhận xóa" on `LIME_WOOL` beside gray "Hủy" on `RED_WOOL`).
- Never leave an obviously uneven trailing line in a wrapped block or split
  tight phrases (`dành / cho`).
- Never use ALL CAPS Vietnamese CTAs with stacked diacritics or 5–6+ words.
- Never let metadata disagree with mechanics or include `F3+H` client lines.
