# Minecraft GUI Design Agent Skill

Codex skill for designing, reviewing, and rewriting Minecraft inventory GUI
item names, lore, tooltips, labels, and player-facing menu text.

The skill focuses on:

- concise GUI copy with a preferred 23-character target for data lines and a
  wider description tier when justification needs it;
- mandatory visual justification for related lore lines and whole-tooltip width harmony;
- role-based pattern library (headers, grouping, value colors, CTAs) chosen by context;
- bold by role rather than by default;
- normal/tiny font roles with verified Vietnamese glyph support;
- readable Vietnamese text and encoding safety;
- controlled color roles for Minecraft tooltip surfaces;
- non-italic item metadata by default;
- practical checks for glyph support, resource-pack fonts, and visual balance.

## Contents

- `SKILL.md` - skill entrypoint and workflow.
- `references/style-guide.md` - required GUI name and lore style guide.
- `references/pattern-library.md` - optional layout patterns and role recipes.
- `agents/openai.yaml` - Codex/OpenAI interface metadata.

## Install

Install or copy this folder into your Codex skills directory, then use:

```text
Use $minecraft-gui-lore to design or revise this Minecraft GUI name and lore.
```

Read `references/style-guide.md` before editing live GUI configs.
