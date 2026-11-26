---
name: minecraft-gui-lore
description: Design, rewrite, review, and implement player-facing names, tooltips, and item lore for Minecraft Java servers. Covers both GUI Menu Lore (buttons, shops, warps, quests, milestones, confirmations) and Carried/Equipped Item Lore (weapons, tools, armor, charms, materials, MMOItems/Nexo/ItemsAdder) with Mojang 1.21.11 pixel metrics, WCAG contrast, Vietnamese safety, and static linting.
---

# Minecraft GUI & Item Lore

Create concise, high-contrast, visually balanced Minecraft GUI tooltips and
carried-item tooltips with clear 1-second scannability and verified rendering
safety.

## Step 0 — Classify the surface (mandatory before reading details)

| Surface | Read | Linter profile |
| --- | --- | --- |
| **GUI Menu / Button** (rebuilt each open: hub, shop, warp, quest, milestone, confirm) | [references/style-guide.md](references/style-guide.md), [references/pattern-library.md](references/pattern-library.md), [references/gallery.md](references/gallery.md) | `scripts/lint_lore.py <file>` (`--profile gui`) |
| **Carried / Equipped Item** (persisted in NBT: weapon, tool, armor, charm, material, event item) | [references/item-lore.md](references/item-lore.md) + shared technical rules (§2.3, §3, §4.3) in [references/style-guide.md](references/style-guide.md) + [references/gallery.md](references/gallery.md) | `scripts/lint_lore.py <file> --profile item` |
| **Both** (e.g., shop GUI selling real gear) | Follow `item-lore.md` for the product's persistent lore; follow `style-guide.md` + `pattern-library.md` for the menu wrapper/price/CTA lines | Lint menu & item templates separately |

*(For persistent item NBT/RevID migration, also follow `minecraft-custom-item-safety`.)*

## Priority order (GUI Menu)

1. **Technical & safety constraints:** hard code-level validators in the target
   plugin (e.g., strict `<= 23`-char reject rules), functional placeholders,
   click semantics, YAML syntax, and Vietnamese encoding safety.
2. **Decision-first hierarchy & contrast:** 1-second scannability (status/price/
   requirement in lines 1–2 on decision buttons), WCAG contrast (`>= 4.5:1` for
   readable text on `#100010`), and single-role color discipline.
3. **Pixel balance & viewport fit:** pixel budgets (`<= 140 px` data tier,
   `<= 185 px` description tier; never truncate Vietnamese phrases to hit a
   character count), group justification (`<= 25%`), width band (`<= 35%`), and
   vertical height (`<= 14` lines).

*(Item Lore uses its own house style "ARPG gọn — nền dịu, điểm nhấn có cảm xúc":
calm neutral body with purposeful saturation matched to rarity & item mood, fixed
block skeleton, enchant-dependent tier line, and a screen-based height limit,
all defined in [references/item-lore.md](references/item-lore.md).)*

## Reference map

| File | Role |
| --- | --- |
| [references/style-guide.md](references/style-guide.md) | Authoritative GUI rules: pixel budget & Mojang 1.21.11 width table, vertical budget, WCAG `#100010` contrast table, 1-hue-1-role colors, decision-first layout, Vietnamese/encoding safety, title rules, and final checklist. |
| [references/pattern-library.md](references/pattern-library.md) | Role-based GUI lore patterns tagged `[Non-Pack OK]` / `[Resource Pack]` / `[Unverified]`: `H1–H5`, `B1–B6` (`○`, `•`, thin `|`), `V0–V7` (term registry, resource colors, multi-state urgency, delta rows), `C1–C5` (action-colored & card-accent CTAs, guided locks), recipes, and anti-patterns. |
| [references/item-lore.md](references/item-lore.md) | User-approved item lore house style (MMOItems, Nexo, ItemsAdder, custom plugins): block skeleton, enchant-vs-tier placement (case A/B), neutral body + purposeful saturation by rarity & mood (pastel vs rich jewel/elemental, no raw RGB neon), one highlight per block, trailing Non-Pack / leading Pack stat symbols, gem/set/skill grammar, bright durability footer, `Cúp` term registry, screen-based height (`<= 24` lore+vanilla, `<= 19` if tradeable), vanilla/AH/chat coexistence, NBT lifecycle. |
| [references/gallery.md](references/gallery.md) | Golden gallery of complete, `lint_lore.py --strict` verified Vietnamese tooltips for every GUI and Item role. Start here instead of improvising from shorthand codes. |
| [scripts/lint_lore.py](scripts/lint_lore.py) | Static verifier (`--profile gui\|item`, `--tradeable`, `--allow-legacy-item`, `--serializer auto\|minimessage\|legacy\|barehex`, `--hard-max N`, `--vanilla-lines N`, `--api-non-italic`, `--strict`, `--self-test`, `--measure CHARS [--unifont unifont.zip]`); warns `STAT_ICON_WIDTH` on mixed-width stat symbols. |

## Workflow

1. **Classify & inspect:** determine GUI Menu vs Carried Item vs Both; check
   plugin serializer, Non-Pack vs Pack setup, hard code validators, project term
   & color registries (`V0`/`V1`), encoding/BOM/newlines, and real backgrounds.
2. **Preserve behavior:** keep placeholders, click actions, permissions, and
   YAML quoting intact unless asked to change mechanics.
3. **Draft meaning decision-first:** write natural Vietnamese first (never chop
   words to chase a character count). Put decision data (status, cost,
   eligibility) in lines 1–2 on action buttons; match a role from `gallery.md`.
4. **Balance pixels & height:** check Mojang 1.21.11 pixel budgets (`<= 140 px`
   data / `<= 185 px` description), group balance (`<= 25%`), and vertical height.
5. **Style with contrast & discipline:** GUI menus use `&7`/`<gray>` base,
   readable contrast (`>= 4.5:1`, `#8C8CA0` for flavor/subtitles, never `&8` on
   `> 3` words), 1 hue = 1 role per tooltip, role-based bold only, explicit
   non-italic (`<!i>` / `ITALIC=false`), thin `|` / `○` / `•` only (no chunky
   bars `▍`). Carried items keep a calm neutral body (`#A9A6B4`/`#ECE9F2`/`#8A8597`)
   and scale accent saturation by rarity & mood — pastel for low-tier/cozy/utility,
   rich jewel/elemental tones for epic+/combat/boss/alerts, never raw RGB neon or
   vanilla legacy colors (`item-lore.md` §3, §5).
6. **Verify before reporting:** run `python scripts/lint_lore.py <file> --strict`
   (with `--profile item --vanilla-lines <N>` for gear, plus `--tradeable` for
   tradeable gear; `--hard-max 23` if plugin enforces a hard cap). Treat in-game
   screenshots as final authority; disclose clearly when client rendering was
   not verified.

## Non-negotiable rules

1. **Hard plugin validators win** over soft pixel/length targets.
2. **Never truncate natural Vietnamese** (`Số dư hiện`, `Shift + Trái`) to hit
   23 characters; rephrase cleanly or accept a wider line within pixel budget.
3. **Decision-first on action buttons:** status, cost, or requirement belongs in
   lines 1–2 before description (pass the 1-second top-3-lines test).
4. **One hue = one role per tooltip:** never overload one color for warning,
   currency, and CTA; separate `V6` urgency colors from `V1` resource colors.
5. **Enforce contrast (`>= 4.5:1` text):** ban `&1`, `&4`, `&0`, and `< 3:1`
   hex on readable text; ban `&8` on lines longer than 3 words; use `#404040` or
   darker (`<= 150 px`) for light-panel inventory titles.
6. **Enforce balance & height:** `<= 25%` pixel delta inside groups; `<= 35%`
   width band across GUI content blocks (disabled on `--profile item`); `<= 14`
   lines for GUI panels; items are limited by the screen (`<= 24` lore + vanilla
   rows, `<= 19` for tradeable gear to leave AH headroom); no chunky bars (`▍`).
7. **Control bold & italics:** disable inherited italics (`<!i>` / `ITALIC=false`);
   bold by role only (`<= 4` words, max ~2 regions/tooltip, never on data rows,
   descriptions, consecutive lines, or default inventory titles).
8. **Protect Vietnamese & encoding:** triage defects (mojibake vs missing glyph
   vs fallback vs italic), preserve encoding/BOM/newlines, never invent
   unverified glyphs or blind `&r`.
9. **Keep destructive & bulk actions explicit:** bulk or irreversible actions
   must show total cost/consequences in the tooltip (or route through a
   confirmation step), and warning colors must match label semantics.
10. **Never claim visual verification without an in-game screenshot.**
11. **Item tier line follows vanilla above-lore components:** tier
    (`Nhóm · Hạng`) sits on line 2 with the enchant block one blank line below
    when above-lore vanilla rows (`enchantments`, `stored_enchantments`, `trim`,
    `dyed_color`, `potion_contents`) are hidden or absent (Case A); when any of
    those vanilla rows remain visible (drawn under the name), the tier line must
    move to the bottom and below-lore `attribute_modifiers`/`unbreakable` should
    be hidden when lore already displays stats (Case B, `item-lore.md` §2.1).
12. **Stat symbol placement:** on Non-Pack servers, place colored Unicode stat
    symbols **after** the value (`Tốc đào: +45 ⛏`, BMP characters only — no
    `U+1Fxxx` emoji) so every stat label aligns flush-left without fighting
    mixed Unicode glyph widths (`item-lore.md` §5.1). On Pack servers using
    fixed-width pixel glyphs (or if a server explicitly chooses leading Unicode
    icons), every leading symbol in a stat block must share one advance width
    (checked by `STAT_ICON_WIDTH` and `lint_lore.py --measure`, §5.2).

## Review output

When reviewing existing GUI or item text:

- Cite exact `file:line` violations and separate plugin lore from `F3+H` debug
  lines.
- Flag unverified glyphs, placeholder expansions, contrast risks, and layout
  inconsistencies.
- Supply ready-to-use, `lint_lore.py`-verified replacement copy preserving
  functional syntax.
- Explain only decisions that materially improve 1-second scannability or UX.
