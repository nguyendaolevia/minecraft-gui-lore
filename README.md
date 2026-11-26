# Minecraft GUI & Item Lore Skill

Agent skill for designing, rewriting, reviewing, and verifying Minecraft Java
**GUI menu tooltips** and **carried/equipped item lore** (MMOItems, Nexo,
ItemsAdder, custom plugins).

## Contents

- `SKILL.md` — concise entrypoint with Step 0 surface classifier (`GUI Menu` vs
  `Carried Item` vs `Both`), priority order, workflow, and 12 non-negotiable rules.
- `references/style-guide.md` — authoritative GUI rules: decision-first ordering,
  Mojang 1.21.11 pixel budgets (`<= 140 px` data / `<= 185 px` desc), WCAG
  `#100010` contrast table, single-role color discipline, Vietnamese/encoding
  safety, light-panel title rules (`<= 150 px`), and 15-point GUI checklist.
- `references/pattern-library.md` — `[Non-Pack OK]` / `[Resource Pack]` /
  `[Unverified]` GUI patterns: `H1–H5`, `B1–B6` (`○`, `•`, thin `|`), `V0–V7`
  (term registry, resource colors, neutral `&8` progress bar, multi-state
  urgency, upgrade deltas), `C1–C5` (action-colored & card-accent CTAs, guided
  locks), and role recipe index.
- `references/item-lore.md` — item lore house style ("ARPG gọn — nền dịu, điểm
  nhấn có cảm xúc"): block skeleton, enchant-vs-tier placement (case A/B),
  neutral body + saturation scaling by rarity & mood (when to use pastel vs rich
  jewel/elemental accents), one highlight per block, trailing Non-Pack / leading
  Pack stat symbols, gem/set/skill grammar, bright durability, `Cúp` term
  registry, screen-based height (`<= 24`, tradeable `<= 19`), NBT lifecycle.
- `references/gallery.md` — golden gallery (`G1–G8` GUI + `I1–I6` Item) where
  every tooltip is strictly verified by `lint_lore.py --strict`.
- `scripts/lint_lore.py` — static verifier using official Mojang Java 1.21.11
  bitmap widths (`PyYAML` for YAML with exact line marks; `--plain` needs stdlib
  only), WCAG contrast checks, Windows UTF-8 console support, and `--profile
  gui|item` + `--vanilla-lines N` + `--tradeable` + `--allow-legacy-item`.
- `agents/openai.yaml` — interface metadata.

## Quick lint usage

```bash
python scripts/lint_lore.py path/to/menu.yml --strict
python scripts/lint_lore.py path/to/menu.yml --serializer barehex --strict
python scripts/lint_lore.py path/to/messages.yml --hard-max 23 --strict
python scripts/lint_lore.py path/to/items.yml --profile item --vanilla-lines 3 --strict
python scripts/lint_lore.py path/to/tradeable_items.yml --profile item --vanilla-lines 3 --tradeable --strict
python scripts/lint_lore.py --measure "⛏✿⛰✷" --unifont path/to/unifont.zip
python scripts/lint_lore.py --self-test
```

Exit codes: `0` = no errors (and no warnings with `--strict`), `1` = lint
failure, `2` = invalid arguments / YAML parse error. Requires Python 3.9+ and
`PyYAML` for YAML files (`--plain` works without PyYAML).
