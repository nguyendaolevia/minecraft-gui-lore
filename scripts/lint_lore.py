#!/usr/bin/env python3
"""Static verifier for Minecraft GUI & Carried-Item names and lore.

Supports two profiles:
  --profile gui   (default): GUI menu tooltips (<=140px data target / 165px soft
                             ceiling, <=185px description, <=25% group balance,
                             <=35% cross-block band, <=14 lines).
  --profile item           : Carried/equipped items (disables cross-block 35%
                             band, checks <=120px item name for [item] chat/AH,
                             <=24 lore lines = name + 24 fits 1080p GUI Scale 4,
                             adds --vanilla-lines to vertical budget, flags GUI
                             menu CTAs on passive gear, allows <=2 deliberate
                             italic flavor lines).

Also checks: official Mojang Java 1.21.11 vanilla default bitmap widths
(uniform=false), WCAG contrast on #100010 (bans <3:1 readable text, bans &8 on
>3 words, flags 3.0-4.5:1 non-bold text), bold regions/data rows, scoped
MiniMessage bold/italic stacks, <newline>/<br>/\\n expansion, chunky block bars,
legacy &r resets, and Vietnamese UTF-8 mojibake heuristics.

Usage:
  python lint_lore.py <file.yml|file.txt> [options]
  python lint_lore.py --self-test

Exit codes:
  0 = pass (no ERROR; and no WARN when --strict is set)
  1 = lint failures found
  2 = invalid arguments, missing PyYAML, or unparseable YAML
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

FONT_PROFILE = "vanilla-1.21.11"

# Official Mojang Java 1.21.11 default.json bitmap/space advance widths (px,
# uniform=false, incl. 1px inter-glyph gap). Extracted directly from client.jar.
WIDTH_GROUPS: Dict[int, str] = {
    2: "!',.:;i|ị·",
    3: "`lìí•",
    4: ' "()*I[]t{}ỉÌÍỈỊ',
    5: "<>fkĩĨ●▌",
    6: (
        "#$%&+-/0123456789=?ABCDEFGHJKLMNOPQRSTUVWXYZ\\^_"
        "abcdeghjmnopqrsuvwxyz"
        "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệòóỏõọôồốổỗộùúủũụỳýỷỹỵ"
        "ÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÒÓỎÕỌÔỒỐỔỖỘÙÚỦŨỤỲÝỶỸỴ"
        "○♥⚡×◆◇♠♢♣♦"
    ),
    7: "@~đĐ✔✘«»–⏩▶",
    8: "ơờớởỡợưừứửữựƠỜỚỞỠỢƯỪỨỬỮỰ→⚔❤★❄⌛⏳◎☄☠⚓⛨",
    9: "—☀⛏",
}

VANILLA_WIDTHS: Dict[str, int] = {
    ch: width for width, chars in WIDTH_GROUPS.items() for ch in chars
}

# Unifont fallback advance widths (px) measured from the 1.21.11 asset unifont.zip
# (unifont_all_no_pua-17.0.01.hex) for glyphs NOT present in default.json bitmaps.
# Client bytecode gon$d$1.getAdvance returns (ink_columns / 2) + 1 (int division).
# Use --measure --unifont <zip> to measure a symbol that is not listed here.
UNIFONT_WIDTH_GROUPS: Dict[int, str] = {
    4: "◈⬥⬦☼⍟⊕◉◍▣►⬆⇧",
    6: "⛉⛊⛋⚘⬢⬡➶➹➚",
    7: "☘❖✶⛑⚙✠❦❧☙⋙⮞",
    8: "⛰✿❀✷✦✧✪✹✺❂❋❉✱✲✳✴✵✸❃❁✤✣✚✜⚜⚝✯⚚➾➽➼➻➺➤➲➠✨❇⬣",
    9: "⚒✰",
}

UNIFONT_WIDTHS: Dict[str, int] = {
    ch: width for width, chars in UNIFONT_WIDTH_GROUPS.items() for ch in chars
}

STAT_ICON_EXCLUDE = set("○•|-·")

# Resource-pack glyph tags (Nexo <glyph:id>) become one placeholder character with the
# house icon advance (item-lore.md §5.2: 7x7 art in an 8 px cell).
PACK_GLYPH_CHAR = ""
PACK_GLYPH_PX = 8


def glyph_width(ch: str) -> Optional[int]:
    """Advance width in px on vanilla 1.21.11: default bitmap first, then measured Unifont."""
    if ch == PACK_GLYPH_CHAR:
        return PACK_GLYPH_PX
    w = VANILLA_WIDTHS.get(ch)
    return w if w is not None else UNIFONT_WIDTHS.get(ch)


def measure_unifont_zip(path: str, chars: str) -> Dict[str, Optional[int]]:
    """Measure Unifont advance widths straight from a Minecraft unifont.zip (or hashed zip / .hex)."""
    import zipfile
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.endswith(".hex"))
            text = z.read(name).decode("ascii")
    else:
        text = Path(path).read_text(encoding="ascii")
    wanted = {ord(c) for c in chars}
    out: Dict[str, Optional[int]] = {c: None for c in chars}
    for line in text.splitlines():
        cp_hex, _, bits = line.partition(":")
        cp = int(cp_hex, 16)
        if cp not in wanted:
            continue
        cell = 8 if len(bits) == 32 else 16
        step = cell // 4
        rows = [int(bits[i * step:(i + 1) * step], 16) for i in range(16)]
        cols = [c for c in range(cell) if any((r >> (cell - 1 - c)) & 1 for r in rows)]
        out[chr(cp)] = ((max(cols) - min(cols) + 1) // 2 + 1) if cols else 0
    return out

# WCAG contrast reference on vanilla dark tooltip surface (#100010, ~94% alpha)
TOOLTIP_BG_RGB = (0x10, 0x00, 0x10)
DARK_GRAY_HEX = "#555555"

LEGACY_COLOR_HEX: Dict[str, str] = {
    "0": "#000000", "1": "#0000AA", "2": "#00AA00", "3": "#00AAAA",
    "4": "#AA0000", "5": "#AA00AA", "6": "#FFAA00", "7": "#AAAAAA",
    "8": "#555555", "9": "#5555FF", "a": "#55FF55", "b": "#55FFFF",
    "c": "#FF5555", "d": "#FF55FF", "e": "#FFFF55", "f": "#FFFFFF",
}

MM_COLOR_HEX: Dict[str, str] = {
    "black": "#000000", "dark_blue": "#0000AA", "dark_green": "#00AA00",
    "dark_aqua": "#00AAAA", "dark_red": "#AA0000", "dark_purple": "#AA00AA",
    "gold": "#FFAA00", "gray": "#AAAAAA", "grey": "#AAAAAA",
    "dark_gray": "#555555", "dark_grey": "#555555", "blue": "#5555FF",
    "green": "#55FF55", "aqua": "#55FFFF", "red": "#FF5555",
    "light_purple": "#FF55FF", "yellow": "#FFFF55", "white": "#FFFFFF",
}
MM_COLORS = set(MM_COLOR_HEX.keys())

MM_DECOR_BOLD = {"bold", "b"}
MM_DECOR_ITALIC = {"italic", "i", "em"}
MM_DECOR_OTHER = {"underlined", "u", "strikethrough", "st", "obfuscated", "obf"}
MM_DECOR_ALL = MM_DECOR_BOLD | MM_DECOR_ITALIC | MM_DECOR_OTHER
MM_NEWLINE_TAGS = {"newline", "br"}
MM_RESET_TAGS = {"reset", "r"}
MM_PARAM_PREFIXES = (
    "color:", "c:", "colour:", "gradient:", "transition:", "rainbow:",
    "font:", "shadow:", "hover:", "click:", "insertion:", "key:", "lang:",
    "translate:", "score:", "selector:", "nbt:", "pride:",
)
MM_BARE_STRUCTURAL = {
    "gradient", "transition", "rainbow", "color", "c", "colour",
    "font", "shadow", "hover", "click", "insertion", "pride",
}

LEGACY_HEX_X_RE = re.compile(r"[&§]x((?:[&§][0-9a-fA-F]){6})")
LEGACY_HEX_HASH_RE = re.compile(r"[&§](#[0-9a-fA-F]{6})")
BARE_HEX_RE = re.compile(r"(?<![A-Za-z0-9&§])(#[0-9a-fA-F]{6})")
LEGACY_CODE_RE = re.compile(r"[&§]([0-9a-fA-Fk-oK-OrR])")

# UTF-8 Vietnamese mis-decoded as Latin-1/Windows-1252.
# Excludes NBSP (U+00A0) so valid "Â\u00a0" / "Ã\u00a0" do not false-positive.
MOJIBAKE_RE = re.compile(r"(?:áº|á»|Ã[\xA1-\xBF]|Â[\xA1-\xBF]|Ä[\x80-\xBF]|Æ[\xB0\xAF\xA1]|â[\x80-\x9F])")

CHUNKY_BARS = set("▍▎▏▌▋▊▉█")
CTA_KEYWORDS = ("Chuột", "Nhấn", "Click", "→", "➟", "[Chưa")
ITEM_MENU_CTA_RE = re.compile(
    r"(?:Nhấn\s+để|Click\s+để|→\s*Chuột|➟|Chuột\s+(?:trái|phải)\s+để|\bChuột\s+(?:trái|phải)\s*:)",
    re.IGNORECASE,
)
ENCHANT_ROMAN_END_RE = re.compile(r"\s+(?:I|II|III|IV|V|VI|VII|VIII|IX|X)$")
SENTENCE_PUNCT_RE = re.compile(r"[.,!?]$")

# Pixel & balance budgets (Mojang Java 1.21.11)
DATA_PX_TARGET = 140
DATA_PX_WARN = 165
DESC_PX_WARN = 185
ITEM_NAME_PX_WARN = 120

GROUP_BALANCE_MAX_DELTA = 0.25
ITEM_STAT_BALANCE_MAX_DELTA = 0.35
TOOLTIP_BAND_MAX_DELTA = 0.35

CONTRAST_BANNED_MIN = 3.0
CONTRAST_TEXT_MIN = 4.5


def _configure_stdio_utf8() -> None:
    """Prevent UnicodeEncodeError on Windows cp1258/cp1252 consoles (M-10)."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _srgb_channel(v: int) -> float:
    s = v / 255.0
    return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4


def _rel_luminance(rgb: Tuple[int, int, int]) -> float:
    return (
        0.2126 * _srgb_channel(rgb[0])
        + 0.7152 * _srgb_channel(rgb[1])
        + 0.0722 * _srgb_channel(rgb[2])
    )


_BG_LUM = _rel_luminance(TOOLTIP_BG_RGB)


def contrast_on_tooltip(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    rgb = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    lum = _rel_luminance(rgb)
    hi, lo = (lum, _BG_LUM) if lum >= _BG_LUM else (_BG_LUM, lum)
    return (hi + 0.05) / (lo + 0.05)


def _is_hex6(s: str) -> bool:
    return len(s) == 7 and s.startswith("#") and all(c in "0123456789abcdefABCDEF" for c in s[1:])


def _count_real_words(text: str) -> int:
    """Count whitespace-separated tokens that contain at least one letter or digit."""
    return sum(1 for tok in text.strip().split() if any(ch.isalnum() for ch in tok))


@dataclass
class LineMetrics:
    raw: str
    visible: str
    chars: int
    words: int
    pixels: int
    has_bold: bool
    bold_regions: int
    max_bold_span_words: int
    uses_mm: bool
    has_unprotected_mm_italic: bool
    has_explicit_italic: bool
    has_legacy_reset: bool
    has_mojibake: bool
    leading_space: bool
    unknown_glyphs: List[str] = field(default_factory=list)
    color_word_counts: Dict[str, int] = field(default_factory=dict)
    color_all_bold: Dict[str, bool] = field(default_factory=dict)
    used_legacy_colors: List[str] = field(default_factory=list)


@dataclass
class ScalarEntry:
    line_no: int
    text: str


@dataclass
class TooltipItem:
    item_id: str
    line_no: int
    name: Optional[ScalarEntry] = None
    lore: List[ScalarEntry] = field(default_factory=list)


@dataclass
class Finding:
    severity: str  # ERROR, WARN, INFO
    code: str
    item_id: str
    line_no: int
    message: str


def _scan_mm_tag(raw: str, start: int) -> Optional[Tuple[int, bool, str]]:
    """Scan a MiniMessage tag starting at '<', respecting single/double quotes and escapes."""
    n = len(raw)
    if start >= n or raw[start] != "<":
        return None
    i = start + 1
    in_quote: Optional[str] = None
    while i < n:
        ch = raw[i]
        if in_quote:
            if ch == "\\" and i + 1 < n:
                i += 2
                continue
            if ch == in_quote:
                in_quote = None
            i += 1
            continue
        if ch in ("'", '"'):
            in_quote = ch
            i += 1
            continue
        if ch == ">":
            body = raw[start + 1:i]
            if not body:
                return None
            closing = body.startswith("/")
            inner = body[1:] if closing else body
            return (i + 1, closing, inner)
        if ch == "<":
            return None
        i += 1
    return None


def _resolve_mm_color_token(token: str) -> Optional[str]:
    low = token.strip().lower()
    if low in MM_COLOR_HEX:
        return MM_COLOR_HEX[low]
    if _is_hex6(low):
        return low.upper()
    return None


def _classify_mm_tag(closing: bool, inner: str) -> Optional[Tuple[str, Any]]:
    """Return (kind, value) if inner is a known MiniMessage tag, else None.

    Kinds: 'newline', 'reset', 'bold', 'italic', 'color', 'other'
    """
    low = inner.strip().lower()
    if not low:
        return None
    head = low.split(":", 1)[0]
    arg = low.split(":", 1)[1] if ":" in low else None

    if low in MM_NEWLINE_TAGS and not closing:
        return ("newline", None)
    if low in MM_RESET_TAGS and not closing:
        return ("reset", None)
    if low in MM_COLOR_HEX:
        return ("color", (MM_COLOR_HEX[low], f"<{low}>"))
    if _is_hex6(low):
        return ("color", (low.upper(), None))

    if head in ("color", "c", "colour") and arg is not None:
        arg_low = arg.strip().lower()
        resolved = _resolve_mm_color_token(arg)
        if resolved:
            legacy_lbl = f"<{low}>" if arg_low in MM_COLOR_HEX else None
            return ("color", (resolved, legacy_lbl))
        return ("other", None)

    if head in ("gradient", "transition") and arg is not None:
        stops = []
        legacy_stop: Optional[str] = None
        for part in arg.split(":"):
            p_low = part.strip().lower()
            resolved = _resolve_mm_color_token(part)
            if resolved:
                stops.append(resolved)
                if p_low in MM_COLOR_HEX and legacy_stop is None:
                    legacy_stop = p_low
        if stops:
            # Conservative: pick lowest-contrast stop on #100010 so dark ends get caught
            worst = min(stops, key=contrast_on_tooltip)
            return ("color", (worst, f"<{legacy_stop}>" if legacy_stop else None))
        return ("other", None)

    # Negated decoration tags: <!b>, <!bold>, <!i>, <!italic>, <!em>, etc.
    if head.startswith("!") and head[1:] in MM_DECOR_ALL and arg is None:
        base = head[1:]
        if base in MM_DECOR_BOLD:
            return ("bold", False)
        if base in MM_DECOR_ITALIC:
            return ("italic", False)
        return ("other", None)

    # Decoration tags with optional :true/:false argument (e.g. <i:false>, <bold:true>)
    if head in MM_DECOR_ALL:
        if arg is None:
            val = True
        elif arg in ("true", "false"):
            val = (arg == "true")
        else:
            return None
        if head in MM_DECOR_BOLD:
            return ("bold", val)
        if head in MM_DECOR_ITALIC:
            return ("italic", val)
        return ("other", None)

    if any(low.startswith(p) for p in MM_PARAM_PREFIXES) or head in MM_BARE_STRUCTURAL:
        return ("other", None)

    # Resource-pack tags (Nexo): <glyph:id> renders one pack glyph; <shift:N> is spacing only
    if head == "glyph" and arg and not closing:
        return ("glyph", arg)
    if head == "shift" and not closing:
        return ("shift", None)

    return None


def _split_and_analyze_entry(
    raw: str,
    serializer: str = "auto",
) -> List[LineMetrics]:
    """Tokenize one raw scalar into one or more rendered LineMetrics (splitting on newline/br/\\n)."""
    allow_mm = serializer in ("auto", "minimessage")
    allow_legacy = serializer in ("auto", "legacy", "barehex")
    allow_barehex = serializer == "barehex"

    has_mojibake_all = bool(MOJIBAKE_RE.search(raw))
    has_legacy_reset_all = bool(re.search(r"[&§][rR]", raw)) if allow_legacy else False

    # Stack entries: (tag_head, prev_bold, prev_italic, prev_color, prev_legacy_lbl)
    mm_stack: List[Tuple[str, bool, Optional[bool], Optional[str], Optional[str]]] = []
    cur_bold = False
    cur_italic: Optional[bool] = None  # None = inherited default italic
    cur_color: Optional[str] = None
    cur_legacy_lbl: Optional[str] = None
    uses_mm_any = False

    # Each rendered line holds list of (char, bold, italic_state, color_hex, legacy_lbl)
    lines_tokens: List[List[Tuple[str, bool, Optional[bool], Optional[str], Optional[str]]]] = [[]]

    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]

        if ch == "\n":
            lines_tokens.append([])
            i += 1
            continue
        if ch == "\r":
            i += 1
            continue

        # Backslash escape in MiniMessage (e.g., \<bold> renders literal <bold>)
        if allow_mm and ch == "\\" and i + 1 < n and raw[i + 1] in ("<", "\\"):
            lines_tokens[-1].append((raw[i + 1], cur_bold, cur_italic, cur_color, cur_legacy_lbl))
            i += 2
            continue

        # MiniMessage tag
        if allow_mm and ch == "<":
            scanned = _scan_mm_tag(raw, i)
            if scanned is not None:
                end_pos, closing, inner = scanned
                classified = _classify_mm_tag(closing, inner)
                if classified is not None:
                    uses_mm_any = True
                    kind, val = classified
                    tag_head = inner.strip().lower().split(":", 1)[0]
                    if kind == "newline":
                        lines_tokens.append([])
                    elif kind == "glyph":
                        lines_tokens[-1].append((PACK_GLYPH_CHAR, cur_bold, cur_italic, cur_color, cur_legacy_lbl))
                    elif kind == "shift":
                        pass
                    elif kind == "reset":
                        mm_stack.clear()
                        cur_bold = False
                        cur_italic = None
                        cur_color = None
                        cur_legacy_lbl = None
                    elif closing:
                        matched_idx = None
                        for idx in range(len(mm_stack) - 1, -1, -1):
                            if mm_stack[idx][0] == tag_head:
                                matched_idx = idx
                                break
                        if matched_idx is not None:
                            _, prev_b, prev_i, prev_c, prev_leg = mm_stack[matched_idx]
                            del mm_stack[matched_idx:]
                            cur_bold = prev_b
                            cur_italic = prev_i
                            cur_color = prev_c
                            cur_legacy_lbl = prev_leg
                    else:
                        mm_stack.append((tag_head, cur_bold, cur_italic, cur_color, cur_legacy_lbl))
                        if kind == "bold" and val is not None:
                            cur_bold = bool(val)
                        elif kind == "italic" and val is not None:
                            cur_italic = bool(val)
                        elif kind == "color" and isinstance(val, tuple):
                            cur_color, cur_legacy_lbl = val
                    i = end_pos
                    continue

        # Legacy formatting codes (&x, &#RRGGBB, &0-f, &k-o, &r)
        if allow_legacy and ch in "&§":
            m = LEGACY_HEX_X_RE.match(raw, i)
            if m:
                digits = re.sub(r"[&§]", "", m.group(1))
                cur_color = "#" + digits.upper()
                cur_legacy_lbl = None
                cur_bold = False
                cur_italic = False if cur_italic is True else cur_italic
                i = m.end()
                continue
            m = LEGACY_HEX_HASH_RE.match(raw, i)
            if m:
                cur_color = m.group(1).upper()
                cur_legacy_lbl = None
                cur_bold = False
                cur_italic = False if cur_italic is True else cur_italic
                i = m.end()
                continue
            m = LEGACY_CODE_RE.match(raw, i)
            if m:
                code = m.group(1).lower()
                if code == "l":
                    cur_bold = True
                elif code == "o":
                    cur_italic = True
                elif code == "r":
                    cur_bold = False
                    cur_italic = None
                    cur_color = None
                    cur_legacy_lbl = None
                elif code in LEGACY_COLOR_HEX:
                    cur_color = LEGACY_COLOR_HEX[code]
                    cur_legacy_lbl = f"&{code}"
                    cur_bold = False
                    cur_italic = False if cur_italic is True else cur_italic
                i = m.end()
                continue

        # Bare #RRGGBB (only when serializer == "barehex")
        if allow_barehex and ch == "#":
            m = BARE_HEX_RE.match(raw, i)
            if m:
                cur_color = m.group(1).upper()
                cur_legacy_lbl = None
                cur_bold = False
                i = m.end()
                continue

        lines_tokens[-1].append((ch, cur_bold, cur_italic, cur_color, cur_legacy_lbl))
        i += 1

    results: List[LineMetrics] = []
    for tokens in lines_tokens:
        # Rebuild NFC-normalized clusters while preserving style per cluster
        clusters: List[Tuple[str, bool, Optional[bool], Optional[str], Optional[str]]] = []
        for ch, b, it_st, col, leg in tokens:
            if unicodedata.combining(ch) and clusters:
                prev_ch, prev_b, prev_it, prev_col, prev_leg = clusters[-1]
                clusters[-1] = (unicodedata.normalize("NFC", prev_ch + ch), prev_b or b, prev_it, prev_col, prev_leg)
            else:
                clusters.append((unicodedata.normalize("NFC", ch), b, it_st, col, leg))

        vis = unicodedata.normalize("NFC", "".join(c for c, _, _, _, _ in clusters))
        leading_space = vis.startswith(" ") and vis.strip() != ""
        words = _count_real_words(vis)

        px = 0
        has_bold = False
        bold_regions = 0
        in_bold_region = False
        current_bold_buf: List[str] = []
        max_bold_span_words = 0
        unprotected_mm_italic = False
        explicit_italic = False
        unknown_glyphs: List[str] = []
        used_legacy_colors: List[str] = []

        # Per-color word counts & bold flags (alphanumeric words only; ignores brackets/bars)
        color_word_counts: Dict[str, int] = {}
        color_all_bold: Dict[str, bool] = {}
        cur_word_colors: Dict[str, bool] = {}  # color -> all_bold within current word

        def _flush_word() -> None:
            if not cur_word_colors:
                return
            for col_hex, word_is_bold in cur_word_colors.items():
                color_word_counts[col_hex] = color_word_counts.get(col_hex, 0) + 1
                color_all_bold[col_hex] = color_all_bold.get(col_hex, True) and word_is_bold
            cur_word_colors.clear()

        for ch, is_b, it_st, col, leg in clusters:
            w = VANILLA_WIDTHS.get(ch)
            if w is None and ch == PACK_GLYPH_CHAR:
                w = PACK_GLYPH_PX
            elif w is None:
                if ch not in unknown_glyphs and not ch.isspace():
                    unknown_glyphs.append(ch)
                w = UNIFONT_WIDTHS.get(ch, 6)
            if is_b and ch != " ":
                w += 1
                has_bold = True
            px += w

            if is_b:
                if not in_bold_region and not ch.isspace():
                    bold_regions += 1
                    in_bold_region = True
                if in_bold_region:
                    current_bold_buf.append(ch)
            else:
                if in_bold_region:
                    span_words = _count_real_words("".join(current_bold_buf))
                    if span_words > max_bold_span_words:
                        max_bold_span_words = span_words
                    current_bold_buf.clear()
                    in_bold_region = False

            if not ch.isspace():
                if it_st is True:
                    explicit_italic = True
                elif uses_mm_any and it_st is None:
                    unprotected_mm_italic = True

                if leg is not None and leg not in used_legacy_colors:
                    used_legacy_colors.append(leg)

                if ch.isalnum() and col is not None:
                    cur_word_colors[col] = cur_word_colors.get(col, True) and is_b
            else:
                _flush_word()

        _flush_word()

        if in_bold_region:
            span_words = _count_real_words("".join(current_bold_buf))
            if span_words > max_bold_span_words:
                max_bold_span_words = span_words

        results.append(LineMetrics(
            raw=raw,
            visible=vis,
            chars=len(vis),
            words=words,
            pixels=px,
            has_bold=has_bold,
            bold_regions=bold_regions,
            max_bold_span_words=max_bold_span_words,
            uses_mm=uses_mm_any,
            has_unprotected_mm_italic=unprotected_mm_italic,
            has_explicit_italic=explicit_italic,
            has_legacy_reset=has_legacy_reset_all,
            has_mojibake=has_mojibake_all,
            leading_space=leading_space,
            unknown_glyphs=unknown_glyphs,
            color_word_counts=color_word_counts,
            color_all_bold=color_all_bold,
            used_legacy_colors=used_legacy_colors,
        ))

    return results


def analyze_line(raw: str, serializer: str = "auto") -> LineMetrics:
    """Analyze a single rendered line (returns first line if raw contains newlines)."""
    return _split_and_analyze_entry(raw, serializer=serializer)[0]


# --- Line-tracking YAML loader (PyYAML) ---

@dataclass
class _LocatedScalar:
    value: Any
    line: int


@dataclass
class _LocatedMapping:
    items: List[Tuple[_LocatedScalar, Any]]
    line: int


@dataclass
class _LocatedSequence:
    items: List[Any]
    line: int


def _load_yaml_located(text: str) -> Any:
    if yaml is None:
        raise RuntimeError(
            "PyYAML is required to parse YAML files cleanly. Install PyYAML or pass --plain."
        )

    class _LocLoader(yaml.SafeLoader):
        pass

    def _construct_scalar(loader: Any, node: Any) -> _LocatedScalar:
        return _LocatedScalar(loader.construct_scalar(node), node.start_mark.line + 1)

    def _construct_mapping(loader: Any, node: Any) -> _LocatedMapping:
        loader.flatten_mapping(node)
        pairs: List[Tuple[_LocatedScalar, Any]] = []
        for k_node, v_node in node.value:
            k_obj = loader.construct_object(k_node, deep=True)
            v_obj = loader.construct_object(v_node, deep=True)
            if not isinstance(k_obj, _LocatedScalar):
                k_obj = _LocatedScalar(str(k_obj), k_node.start_mark.line + 1)
            pairs.append((k_obj, v_obj))
        return _LocatedMapping(pairs, node.start_mark.line + 1)

    def _construct_sequence(loader: Any, node: Any) -> _LocatedSequence:
        seq = [loader.construct_object(child, deep=True) for child in node.value]
        return _LocatedSequence(seq, node.start_mark.line + 1)

    for tag in (
        "tag:yaml.org,2002:str",
        "tag:yaml.org,2002:int",
        "tag:yaml.org,2002:float",
        "tag:yaml.org,2002:bool",
        "tag:yaml.org,2002:null",
        "tag:yaml.org,2002:timestamp",
    ):
        _LocLoader.add_constructor(tag, _construct_scalar)
    _LocLoader.add_constructor("tag:yaml.org,2002:map", _construct_mapping)
    _LocLoader.add_constructor("tag:yaml.org,2002:seq", _construct_sequence)

    return yaml.load(text, Loader=_LocLoader)


def _extract_lore_entries(node: Any) -> List[ScalarEntry]:
    if isinstance(node, _LocatedSequence):
        out: List[ScalarEntry] = []
        for elem in node.items:
            if isinstance(elem, _LocatedScalar):
                out.append(ScalarEntry(elem.line, "" if elem.value is None else str(elem.value)))
        return out
    if isinstance(node, _LocatedScalar) and isinstance(node.value, str):
        return [ScalarEntry(node.line, node.value)]
    return []


def parse_yaml_tooltips(text: str) -> List[TooltipItem]:
    """Extract all GUI/item tooltips from valid YAML with exact line numbers and full paths."""
    root = _load_yaml_located(text)
    items: List[TooltipItem] = []
    if root is None:
        return items

    item_hints = {
        "material", "type", "slot", "slots", "icon", "item", "item-id",
        "amount", "click_commands", "left_click_commands", "view_requirement",
        "cost", "commands",
    }

    def walk(node: Any, path: List[str]) -> None:
        if isinstance(node, _LocatedMapping):
            kv_lower: Dict[str, Tuple[_LocatedScalar, Any]] = {}
            for k_loc, v_node in node.items:
                k_str = str(k_loc.value)
                kv_lower[k_str.lower()] = (k_loc, v_node)

            name_entry: Optional[ScalarEntry] = None
            for nk in ("display_name", "display-name", "name"):
                if nk in kv_lower and isinstance(kv_lower[nk][1], _LocatedScalar):
                    val = kv_lower[nk][1].value
                    if isinstance(val, str):
                        if nk != "name" or "lore" in kv_lower or (set(kv_lower.keys()) & item_hints):
                            name_entry = ScalarEntry(kv_lower[nk][1].line, val)
                            break

            lore_entries: List[ScalarEntry] = []
            if "lore" in kv_lower:
                lore_entries = _extract_lore_entries(kv_lower["lore"][1])

            if (name_entry and name_entry.text.strip()) or lore_entries:
                label = ".".join(path) if path else "root"
                start_ln = name_entry.line_no if name_entry else (lore_entries[0].line_no if lore_entries else node.line)
                items.append(TooltipItem(item_id=label, line_no=start_ln, name=name_entry, lore=lore_entries))

            paired_prefixes = set()
            for lk in kv_lower:
                if lk.endswith("-lore"):
                    paired_prefixes.add(lk[:-5])
            for pref in sorted(paired_prefixes):
                p_name: Optional[ScalarEntry] = None
                if f"{pref}-name" in kv_lower and isinstance(kv_lower[f"{pref}-name"][1], _LocatedScalar):
                    v = kv_lower[f"{pref}-name"][1].value
                    if isinstance(v, str):
                        p_name = ScalarEntry(kv_lower[f"{pref}-name"][1].line, v)
                p_lore = _extract_lore_entries(kv_lower[f"{pref}-lore"][1])
                if (p_name and p_name.text.strip()) or p_lore:
                    label = ".".join(path + [pref]) if path else pref
                    start_ln = p_name.line_no if p_name else p_lore[0].line_no
                    items.append(TooltipItem(item_id=label, line_no=start_ln, name=p_name, lore=p_lore))

            for k_loc, v_node in node.items:
                if isinstance(v_node, (_LocatedMapping, _LocatedSequence)):
                    walk(v_node, path + [str(k_loc.value)])
        elif isinstance(node, _LocatedSequence):
            for idx, child in enumerate(node.items):
                if isinstance(child, (_LocatedMapping, _LocatedSequence)):
                    walk(child, path + [f"[{idx}]"])

    walk(root, [])
    return items


def parse_plain_tooltips(text: str) -> List[TooltipItem]:
    lines = text.splitlines()
    if not lines:
        return []
    name = ScalarEntry(1, lines[0])
    lore = [ScalarEntry(idx, ln) for idx, ln in enumerate(lines[1:], 2)]
    return [TooltipItem(item_id="snippet", line_no=1, name=name, lore=lore)]


def is_data_line(vis: str) -> bool:
    s = vis.strip()
    if not s:
        return True
    if any(s.startswith(p) for p in ("○", "●", "•", "|", "▍", "→", "➟", "✔", "✘", "+", "-", "[")):
        return True
    if _is_skill_header_row(s):
        return True
    if ":" in s or "Chuột" in s or "Nhấn" in s or "Click" in s:
        return True
    return False


def is_label_value_row(vis: str) -> bool:
    """Detect data rows where bold is forbidden (e.g., 'Giá: 100', '| Cấp: 5'), excluding CTAs."""
    s = vis.strip()
    if not s or any(k in s for k in CTA_KEYWORDS):
        return False
    if s.startswith(("○", "•", "|", "-")):
        return True
    if ":" in s:
        left, right = s.split(":", 1)
        if left.strip() and right.strip():
            return True
    return False


SKILL_TRIGGERS = ("Chuột phải", "Shift + Chuột phải", "Shift + F", "Shift +", "Khi đánh trúng",
                  "Khi đánh", "Khi bị đánh", "Bị động")


def _is_skill_header_row(vis: str) -> bool:
    """Skill header in either order: 'Name · Trigger' or 'Trigger · Name' (item-lore.md §6)."""
    s = vis.strip()
    if "·" not in s:
        return False
    parts = [p.strip() for p in s.split("·") if p.strip()]
    if len(parts) < 2:
        return False
    return any(parts[0].startswith(p) or parts[-1].startswith(p) for p in SKILL_TRIGGERS)


def _is_enchant_block(group: List[Tuple[int, int, LineMetrics]]) -> bool:
    """Detect Case A enchant blocks (1/line or 2/line '·' separated) so varied lengths don't trigger prose GROUP_BALANCE."""
    if len(group) < 2:
        return False
    has_roman = False
    for _, _, m in group:
        vis = m.visible.strip()
        if not vis or m.has_explicit_italic or ":" in vis or SENTENCE_PUNCT_RE.search(vis):
            return False
        segs = [seg.strip() for seg in vis.split("·") if seg.strip()]
        if any(ENCHANT_ROMAN_END_RE.search(seg) for seg in segs):
            has_roman = True
    return has_roman


def _check_contrast(
    findings: List[Finding],
    iid: str,
    lno: int,
    label: str,
    m: LineMetrics,
    is_item: bool = False,
) -> None:
    """Enforce WCAG contrast rules on #100010 tooltip background."""
    dg_hint = "use #8A8597 (Muted) or #5E596B (Separator)" if is_item else "use #8C8CA0 or &7"
    for col_hex, w_count in m.color_word_counts.items():
        if w_count <= 0:
            continue
        ratio = contrast_on_tooltip(col_hex)
        if col_hex == DARK_GRAY_HEX:
            if w_count > 3:
                findings.append(Finding(
                    "WARN", "DARK_GRAY_TEXT", iid, lno,
                    f"{label}: &8/#555555 ({ratio:.1f}:1 on #100010) used on {w_count} words (> 3); {dg_hint} ('{m.visible}')",
                ))
        elif ratio < CONTRAST_BANNED_MIN:
            findings.append(Finding(
                "WARN", "CONTRAST_BANNED", iid, lno,
                f"{label}: color {col_hex} has {ratio:.1f}:1 contrast on #100010 (< 3.0:1 banned for text) ('{m.visible}')",
            ))
        elif ratio < CONTRAST_TEXT_MIN:
            # Allow short bold tags (<= 2 words) such as &5&lBOSS per style-guide §4.3
            if not (m.color_all_bold.get(col_hex, False) and w_count <= 2):
                findings.append(Finding(
                    "WARN", "CONTRAST_LOW", iid, lno,
                    f"{label}: color {col_hex} has {ratio:.1f}:1 contrast on #100010 (< 4.5:1 AA threshold) ('{m.visible}')",
                ))


def lint_tooltip(
    item: TooltipItem,
    hard_max: Optional[int] = None,
    max_lines: Optional[int] = None,
    serializer: str = "auto",
    api_non_italic: bool = False,
    profile: str = "gui",
    vanilla_lines: int = 0,
    tradeable: bool = False,
    allow_legacy_item: bool = False,
) -> List[Finding]:
    findings: List[Finding] = []
    iid = item.item_id
    is_item = (profile == "item")
    # item: name + 24 lore/vanilla rows ~= 25 rendered lines (1080p GUI Scale 4; 19 if tradeable for 5 AH rows, item-lore.md §8)
    default_item_max = 19 if tradeable else 24
    effective_max_lines = max_lines if max_lines is not None else (default_item_max if is_item else 14)

    # Expand name and lore entries into actual rendered lines
    rendered_name: List[Tuple[int, LineMetrics]] = []
    if item.name is not None:
        for m in _split_and_analyze_entry(item.name.text, serializer=serializer):
            rendered_name.append((item.name.line_no, m))

    rendered_lore: List[Tuple[int, int, LineMetrics]] = []  # (render_idx, yaml_line, metrics)
    r_idx = 0
    for entry in item.lore:
        for m in _split_and_analyze_entry(entry.text, serializer=serializer):
            r_idx += 1
            rendered_lore.append((r_idx, entry.line_no, m))

    all_rows: List[Tuple[str, int, LineMetrics]] = []
    for ln, m in rendered_name:
        all_rows.append(("name", ln, m))
    for ri, ln, m in rendered_lore:
        all_rows.append((f"lore[{ri}]", ln, m))

    # 1. Per-line checks
    bold_lore_indices: List[Tuple[int, int]] = []
    total_bold_regions = 0
    explicit_italic_lines: List[int] = []

    for label, lno, m in all_rows:
        if m.has_mojibake:
            findings.append(Finding("WARN", "MOJIBAKE", iid, lno, f"{label}: possible UTF-8 mojibake -> '{m.visible}'"))
        if m.has_legacy_reset:
            findings.append(Finding("INFO", "LEGACY_RESET", iid, lno, f"{label}: contains &r; verify it does not break font fallback"))
        if any(ch in CHUNKY_BARS for ch in m.visible):
            findings.append(Finding("WARN", "THICK_BAR", iid, lno, f"{label}: chunky block bar found; prefer thin '|' instead ('{m.visible}')"))

        if m.uses_mm and not api_non_italic and m.visible.strip():
            if m.has_unprotected_mm_italic:
                findings.append(Finding("WARN", "MM_ITALIC", iid, lno, f"{label}: MiniMessage text without active <!i>/<i:false> may inherit italic"))
            elif m.has_explicit_italic:
                if is_item:
                    explicit_italic_lines.append(lno)
                else:
                    findings.append(Finding("WARN", "MM_ITALIC", iid, lno, f"{label}: explicit MiniMessage italic active; keep only for deliberate flavor/quotes"))
        elif is_item and m.has_explicit_italic and m.visible.strip():
            explicit_italic_lines.append(lno)

        if m.leading_space:
            findings.append(Finding("INFO", "LEADING_SPACE", iid, lno, f"{label}: leading visible space -> '{m.visible}'"))
        if m.unknown_glyphs:
            glyphs = "".join(m.unknown_glyphs)
            measured = [g for g in m.unknown_glyphs if g in UNIFONT_WIDTHS]
            unmeasured = "".join(g for g in m.unknown_glyphs if g not in UNIFONT_WIDTHS)
            note = " (Unifont fallback, measured " + " ".join(f"{g}={UNIFONT_WIDTHS[g]}px" for g in measured) + ")" if measured else ""
            if unmeasured:
                note += f"; unmeasured '{unmeasured}' (Unifont/pack width unverified)"
            findings.append(Finding("INFO", "UNVERIFIED_GLYPH", iid, lno, f"{label}: glyph(s) '{glyphs}' outside {FONT_PROFILE} default bitmap{note}"))

        if not m.visible.strip():
            continue

        _check_contrast(findings, iid, lno, label, m, is_item=is_item)

        # Item-specific soft palette, name & CTA checks
        if is_item:
            if not allow_legacy_item and m.used_legacy_colors:
                cols = ", ".join(m.used_legacy_colors)
                findings.append(Finding(
                    "WARN", "ITEM_LEGACY_COLOR", iid, lno,
                    f"{label}: vanilla legacy color ({cols}) disallowed in item lore; use soft hex palette (item-lore.md §3) ('{m.visible}')",
                ))
            if label == "name" and m.pixels > ITEM_NAME_PX_WARN:
                findings.append(Finding(
                    "WARN", "ITEM_NAME_WIDE", iid, lno,
                    f"name: {m.pixels}px > {ITEM_NAME_PX_WARN}px [item] chat/AH readability budget ('{m.visible}')",
                ))
            if label.startswith("lore[") and ITEM_MENU_CTA_RE.search(m.visible):
                findings.append(Finding(
                    "WARN", "PASSIVE_ITEM_CTA", iid, lno,
                    f"{label}: GUI menu CTA phrase on carried item; use skill trigger grammar or omit ('{m.visible}')",
                ))

        # Pixel & hard-char density checks
        data_tier = (label == "name") or is_data_line(m.visible)
        word_cap = 7 if data_tier else 9

        if hard_max is not None and m.chars > hard_max:
            findings.append(Finding("ERROR", "HARD_MAX_CHARS", iid, lno, f"{label}: {m.chars} NFC chars > hard cap {hard_max} ('{m.visible}')"))
        elif data_tier and m.pixels > DATA_PX_WARN:
            findings.append(Finding("WARN", "PIXEL_BUDGET", iid, lno, f"{label}: {m.pixels}px ({m.chars} chars) > {DATA_PX_WARN}px data soft ceiling ('{m.visible}')"))
        elif data_tier and m.pixels > DATA_PX_TARGET:
            findings.append(Finding("INFO", "PIXEL_TARGET", iid, lno, f"{label}: {m.pixels}px ({m.chars} chars) > {DATA_PX_TARGET}px preferred target ('{m.visible}')"))
        elif not data_tier and m.pixels > DESC_PX_WARN:
            findings.append(Finding("WARN", "PIXEL_BUDGET", iid, lno, f"{label}: {m.pixels}px ({m.chars} chars) > {DESC_PX_WARN}px description ceiling ('{m.visible}')"))

        if m.words > word_cap:
            findings.append(Finding("WARN", "WORD_CEILING", iid, lno, f"{label}: {m.words} words > {word_cap} ceiling ('{m.visible}')"))

        if m.has_bold:
            total_bold_regions += m.bold_regions
            if m.max_bold_span_words > 4:
                findings.append(Finding("WARN", "BOLD_LONG", iid, lno, f"{label}: bold spans {m.max_bold_span_words} words (> 4) ('{m.visible}')"))
            if label.startswith("lore["):
                ri = int(label[5:-1])
                bold_lore_indices.append((ri, lno))
                if is_label_value_row(m.visible):
                    findings.append(Finding("WARN", "BOLD_DATA_ROW", iid, lno, f"{label}: bold on label/value data row is disallowed ('{m.visible}')"))

    if is_item and len(explicit_italic_lines) > 2:
        findings.append(Finding(
            "WARN", "FLAVOR_LONG", iid, explicit_italic_lines[2],
            f"{len(explicit_italic_lines)} explicit italic lines (> 2 max flavor budget for item lore)",
        ))

    if total_bold_regions > 2:
        findings.append(Finding("WARN", "BOLD_BUDGET", iid, item.line_no, f"{total_bold_regions} bold regions (> ~2 max per tooltip)"))
    for (a_idx, a_ln), (b_idx, _) in zip(bold_lore_indices, bold_lore_indices[1:]):
        if b_idx == a_idx + 1:
            findings.append(Finding("WARN", "BOLD_CONSECUTIVE", iid, a_ln, f"consecutive bold lore lines lore[{a_idx}] & lore[{b_idx}]"))
            break

    # 2. Vertical height budget (rendered lore lines + optional vanilla enchant/attribute rows)
    total_lines = len(rendered_lore) + max(0, vanilla_lines)
    if total_lines > effective_max_lines:
        last_ln = rendered_lore[-1][1] if rendered_lore else item.line_no
        if vanilla_lines > 0:
            msg = f"{len(rendered_lore)} lore + {vanilla_lines} vanilla = {total_lines} lines > {effective_max_lines} budget"
        else:
            msg = f"{len(rendered_lore)} rendered lore lines > {effective_max_lines} budget"
        findings.append(Finding("WARN", "VERTICAL_HEIGHT", iid, last_ln, msg))

    # 3. Group visual justification & GUI whole-tooltip band
    groups: List[List[Tuple[int, int, LineMetrics]]] = []
    cur_group: List[Tuple[int, int, LineMetrics]] = []
    for ri, ln, m in rendered_lore:
        if not m.visible.strip():
            if cur_group:
                groups.append(cur_group)
                cur_group = []
        else:
            cur_group.append((ri, ln, m))
    if cur_group:
        groups.append(cur_group)

    block_max_px: List[Tuple[int, int]] = []
    for g_idx, g in enumerate(groups):
        if is_item:
            # Equal-width stat symbols (item-lore.md §5.1): Minecraft has no tab stops,
            # so icons of different advance widths make the label column ragged.
            icon_rows: List[Tuple[int, str, Optional[int]]] = []
            for _ri, _lno, _m in g:
                _s = _m.visible.strip()
                if (len(_s) >= 3 and _s[1] == " " and _s[0] not in STAT_ICON_EXCLUDE
                        and not _s[0].isalnum() and is_label_value_row(_s[2:])):
                    icon_rows.append((_lno, _s[0], glyph_width(_s[0])))
            if len(icon_rows) >= 2:
                unmeasured_icons = "".join(dict.fromkeys(ic for _, ic, w in icon_rows if w is None))
                widths_seen = {w for _, _, w in icon_rows if w is not None}
                if len(widths_seen) > 1:
                    desc = ", ".join(f"{ic}={w}px" for _, ic, w in icon_rows if w is not None)
                    findings.append(Finding(
                        "WARN", "STAT_ICON_WIDTH", iid, icon_rows[0][0],
                        f"stat symbols differ in width ({desc}); use one width (8 px set in item-lore.md §5.1)",
                    ))
                if unmeasured_icons:
                    findings.append(Finding(
                        "INFO", "STAT_ICON_UNMEASURED", iid, icon_rows[0][0],
                        f"stat symbol(s) '{unmeasured_icons}' have no measured width; run --measure with --unifont",
                    ))

            # Skip Case A enchant blocks (varied enchant names / odd last row in 2-per-line layout)
            if _is_enchant_block(g):
                continue

            # Separate italic flavor runs (<=25%), non-italic prose runs (<=25%), and peer stat rows (<=35%)
            italic_run: List[Tuple[int, int, LineMetrics]] = []
            prose_run: List[Tuple[int, int, LineMetrics]] = []
            stat_run: List[Tuple[int, int, LineMetrics]] = []

            def _check_run(run: List[Tuple[int, int, LineMetrics]], limit: float, kind_lbl: str) -> None:
                if len(run) < 2:
                    return
                widths = [m.pixels for _, _, m in run]
                w_min, w_max = min(widths), max(widths)
                if w_max > 0:
                    delta = (w_max - w_min) / w_max
                    if delta > limit:
                        desc = ", ".join(f"L{ri}={m.pixels}px" for ri, _, m in run)
                        findings.append(Finding(
                            "WARN", "GROUP_BALANCE", iid, run[0][1],
                            f"uneven {kind_lbl} width ({delta*100:.1f}% > {int(limit*100)}%): {desc}",
                        ))

            for entry_row in g:
                vis = entry_row[2].visible
                if _is_skill_header_row(vis):
                    _check_run(italic_run, GROUP_BALANCE_MAX_DELTA, "flavor")
                    _check_run(prose_run, GROUP_BALANCE_MAX_DELTA, "prose")
                    _check_run(stat_run, ITEM_STAT_BALANCE_MAX_DELTA, "stat")
                    italic_run, prose_run, stat_run = [], [], []
                elif is_label_value_row(vis):
                    _check_run(italic_run, GROUP_BALANCE_MAX_DELTA, "flavor")
                    _check_run(prose_run, GROUP_BALANCE_MAX_DELTA, "prose")
                    italic_run, prose_run = [], []
                    stat_run.append(entry_row)
                elif entry_row[2].has_explicit_italic:
                    _check_run(prose_run, GROUP_BALANCE_MAX_DELTA, "prose")
                    _check_run(stat_run, ITEM_STAT_BALANCE_MAX_DELTA, "stat")
                    prose_run, stat_run = [], []
                    italic_run.append(entry_row)
                else:
                    _check_run(italic_run, GROUP_BALANCE_MAX_DELTA, "flavor")
                    _check_run(stat_run, ITEM_STAT_BALANCE_MAX_DELTA, "stat")
                    italic_run, stat_run = [], []
                    prose_run.append(entry_row)
            _check_run(italic_run, GROUP_BALANCE_MAX_DELTA, "flavor")
            _check_run(prose_run, GROUP_BALANCE_MAX_DELTA, "prose")
            _check_run(stat_run, ITEM_STAT_BALANCE_MAX_DELTA, "stat")
        else:
            peer_lines = g
            if len(g) >= 2 and g[0][2].chars <= 14 and not is_data_line(g[0][2].visible) and is_data_line(g[1][2].visible):
                peer_lines = g[1:]
            if len(peer_lines) >= 2:
                widths = [m.pixels for _, _, m in peer_lines]
                w_min, w_max = min(widths), max(widths)
                if w_max > 0:
                    delta = (w_max - w_min) / w_max
                    if delta > GROUP_BALANCE_MAX_DELTA:
                        desc = ", ".join(f"L{ri}={m.pixels}px" for ri, _, m in peer_lines)
                        findings.append(Finding("WARN", "GROUP_BALANCE", iid, peer_lines[0][1], f"uneven group width ({delta*100:.1f}% > 25%): {desc}"))
            if g:
                first_m = g[0][2]
                is_h2_subtitle = (g_idx == 0 and len(g) == 1 and first_m.words <= 3 and first_m.chars <= 18)
                is_single_badge = (len(g) == 1 and first_m.visible.strip().startswith("[") and first_m.visible.strip().endswith("]"))
                is_single_cta = (len(g) == 1 and any(k in first_m.visible for k in CTA_KEYWORDS))
                if not (is_h2_subtitle or is_single_badge or is_single_cta):
                    block_max_px.append((g[0][1], max(m.pixels for _, _, m in g)))

    if not is_item and len(block_max_px) >= 2:
        b_min = min(px for _, px in block_max_px)
        b_max = max(px for _, px in block_max_px)
        if b_max > 0 and (b_max - b_min) / b_max > TOOLTIP_BAND_MAX_DELTA:
            delta_b = (b_max - b_min) / b_max * 100
            findings.append(Finding("WARN", "TOOLTIP_BAND", iid, block_max_px[0][0], f"blocks diverge in width ({delta_b:.1f}% > 35%): narrowest={b_min}px vs widest={b_max}px"))

    return findings


def run_self_test() -> int:
    _configure_stdio_utf8()

    # 1. Clean MiniMessage GUI tooltip -> 0 ERROR, 0 WARN
    good_yaml = """
items:
  sample_good:
    display_name: "<!i><#38BDF8>Hòm Báu Thủy Triều"
    lore:
      - "<!i><#38BDF8>| <gray>Trạng thái: <green>Sẵn sàng"
      - "<!i><#38BDF8>| <gray>Phần thưởng: <white>3–5 vật phẩm"
      - ""
      - "<!i><gray>Chứa kho báu đại dương hiếm,"
      - "<!i><gray>mở lại sau mỗi <gold>24 giờ<gray> chơi."
      - ""
      - "<!i><gray>Chuột trái: <green>Nhận vật phẩm"
      - "<!i><gray>Chuột phải: <#38BDF8>Xem trước rương"
"""
    good_items = parse_yaml_tooltips(good_yaml)
    assert len(good_items) == 1
    good_f = lint_tooltip(good_items[0], hard_max=None, max_lines=14)
    assert not [f for f in good_f if f.severity in ("ERROR", "WARN")], f"Unexpected on good sample: {good_f}"

    # 2. GLR-01 + GLR-09: double-quoted keys, inline comments, flow list, block scalar, exact line numbers
    tricky_yaml = (
        'menus:\n'
        '  shop:\n'
        '    "reward":\n'
        '      "display_name": "' + 'A' * 24 + '"\n'
        '      "lore": # comment\n'
        '        - "' + 'B' * 30 + '"\n'
        '    flow_item:\n'
        '      display_name: "Flow"\n'
        '      lore: ["' + 'C' * 26 + '"]\n'
        '    block_item:\n'
        '      display_name: >-\n'
        '        ' + 'D' * 25 + '\n'
        '      lore:\n'
        '        - |-\n'
        '          ' + 'E' * 25 + '\n'
        '        - "' + 'F' * 25 + '"\n'
    )
    tricky = parse_yaml_tooltips(tricky_yaml)
    assert len(tricky) == 3, f"Expected 3 tricky items, got {len(tricky)}"
    assert tricky[0].item_id == "menus.shop.reward"
    f0 = lint_tooltip(tricky[0], hard_max=23, max_lines=14)
    hard_lines = {f.line_no for f in f0 if f.code == "HARD_MAX_CHARS"}
    assert hard_lines == {4, 6}, f"Expected exact lines {{4, 6}}, got {hard_lines}"
    assert any(f.code == "HARD_MAX_CHARS" for f in lint_tooltip(tricky[1], hard_max=23, max_lines=14))
    assert len([f for f in lint_tooltip(tricky[2], hard_max=23, max_lines=14) if f.code == "HARD_MAX_CHARS"]) == 3

    # 3. GLR-02: Official Mojang 1.21.11 Vietnamese pixel widths
    expected_px = {"i": 2, "ì": 3, "í": 3, "ỉ": 4, "ĩ": 5, "ị": 2, "đ": 7, "ư": 8, "ơ": 8, "→": 8, "✔": 7, "✘": 7}
    for ch, want in expected_px.items():
        got = analyze_line(ch).pixels
        assert got == want, f"Mojang 1.21.11 width mismatch for {ch!r}: got {got}, want {want}"
    assert analyze_line("ĩĩĩĩ").pixels == 20
    assert analyze_line("&7&lKryon").pixels == analyze_line("&7Kryon").pixels + 5

    # 4. GLR-03: MiniMessage gradient phase, quoted hover, alias <i:false>, escape, bare hex isolation
    assert analyze_line("<!i><gradient:#ff0000:#0000ff:0.5>ABC</gradient>").visible == "ABC"
    assert analyze_line("<!i><hover:show_text:'<red>Mô tả'>ABC</hover>").visible == "ABC"
    m_alias = analyze_line("<i:false>ABC")
    assert m_alias.visible == "ABC" and not m_alias.has_unprotected_mm_italic
    m_esc = analyze_line(r"<!i>\<bold>ABC")
    assert m_esc.visible == "<bold>ABC" and not m_esc.has_bold
    assert analyze_line("Mã #ABCDEF", serializer="auto").visible == "Mã #ABCDEF"
    assert analyze_line("#ffd54fĐiểm", serializer="barehex").visible == "Điểm"
    assert analyze_line("<!i><gray>Chào <player>!").visible == "Chào <player>!"

    # 5. GLR-04: Nested bold stack & scoped italic check
    assert analyze_line("<!i><bold>A<bold>B</bold>C</bold>").pixels == 21
    assert analyze_line("<!i><bold>A<!bold>B</!bold>C</bold>").pixels == 20
    for bad_it in ("<gray>ABC<!i>D", "<italic>ABC</italic><!i>D", "<!i><italic>ABC</italic>"):
        f_it = lint_tooltip(TooltipItem("it", 1, None, [ScalarEntry(1, bad_it)]), None, 14)
        assert any(f.code == "MM_ITALIC" for f in f_it), f"Missed MM_ITALIC on {bad_it!r}"

    # 6. GLR-05: <newline>/<br> splits into rendered lines for vertical height
    f_nl = lint_tooltip(TooltipItem("nl", 1, None, [ScalarEntry(1, "<!i><gray>A" + "<newline>B" * 14)]), None, 14)
    assert any(f.code == "VERTICAL_HEIGHT" for f in f_nl), "Missed VERTICAL_HEIGHT on <newline> chain"

    # 7. GLR-06: Exact 25% group balance & 35% whole-tooltip band
    f_gb = lint_tooltip(TooltipItem("gb", 1, None, [ScalarEntry(1, "A" * 15), ScalarEntry(2, "A" * 11)]), None, 14)
    assert any(f.code == "GROUP_BALANCE" for f in f_gb), "Missed 26.7% GROUP_BALANCE"
    f_tb = lint_tooltip(TooltipItem("tb", 1, None, [
        ScalarEntry(1, "A" * 30), ScalarEntry(2, "A" * 30), ScalarEntry(3, ""),
        ScalarEntry(4, "B" * 18), ScalarEntry(5, "B" * 18),
    ]), None, 14)
    assert any(f.code == "TOOLTIP_BAND" for f in f_tb), "Missed 30 vs 18 TOOLTIP_BAND"

    # 8. GLR-07: Mojibake warns on real mojibake, ignores valid Vietnamese + NBSP
    assert analyze_line("Luáº­t").has_mojibake
    assert not analyze_line("Chữ Â\u00a0trong tiếng Việt").has_mojibake
    assert not analyze_line("Chữ Ã\u00a0trong bảng chữ").has_mojibake
    f_mj = lint_tooltip(TooltipItem("mj", 1, None, [ScalarEntry(1, "&7Luáº­t")]), None, 14)
    assert any(f.code == "MOJIBAKE" and f.severity == "WARN" for f in f_mj)

    # 9. GLR-08 + THICK_BAR: Bold regions & bold on data row & chunky bar
    f_b3 = lint_tooltip(TooltipItem("b3", 1, None, [ScalarEntry(1, "&lA&7 &lB&7 &lC")]), None, 14)
    assert any(f.code == "BOLD_BUDGET" for f in f_b3), "Missed 3 bold regions on 1 line"
    f_bd = lint_tooltip(TooltipItem("bd", 1, None, [ScalarEntry(1, "&lGiá: 100")]), None, 14)
    assert any(f.code == "BOLD_DATA_ROW" for f in f_bd), "Missed bold on data row"
    f_tb2 = lint_tooltip(TooltipItem("tb2", 1, None, [ScalarEntry(1, "&a▍ &7Thanh dày")]), None, 14)
    assert any(f.code == "THICK_BAR" for f in f_tb2), "Missed THICK_BAR"

    # 10. H-3: WCAG contrast checks on #100010 (banned <3:1, &8 >3 words, low 3-4.5:1, valid #8C8CA0 & &8 brackets)
    assert any(f.code == "CONTRAST_BANNED" for f in lint_tooltip(TooltipItem("c1", 1, None, [ScalarEntry(1, "&4Lỗi nghiêm trọng")])))
    assert any(f.code == "CONTRAST_BANNED" for f in lint_tooltip(TooltipItem("c2", 1, None, [ScalarEntry(1, "<!i><#3F0A8D>Bóng tối cổ đại")])))
    assert any(f.code == "CONTRAST_BANNED" for f in lint_tooltip(TooltipItem("c3", 1, None, [ScalarEntry(1, "<!i><gradient:#3F0A8D:#C084FC>Kiếm Tối</gradient>")])))
    assert any(f.code == "DARK_GRAY_TEXT" for f in lint_tooltip(TooltipItem("c4", 1, None, [ScalarEntry(1, "<!i><dark_gray>Rèn từ lõi tim băng giá cổ")])))
    assert any(f.code == "CONTRAST_LOW" for f in lint_tooltip(TooltipItem("c5", 1, None, [ScalarEntry(1, "<!i><blue>Hạng Hiếm")])))
    # Valid: &8 brackets/bar, &5&l short bold tag, #8C8CA0 flavor
    f_ok_c = lint_tooltip(TooltipItem("cok", 1, ScalarEntry(1, "<!i><dark_gray>[<#FFD54F>Mốc 20<dark_gray>]"), [
        ScalarEntry(2, "<!i><gray>Tiến độ: <dark_gray>[<green>|||||<dark_gray>:::::] <white>10<gray>/20"),
        ScalarEntry(3, "<!i><#8C8CA0>Phụ đề dễ đọc hơn sáu chấm hai"),
    ]))
    assert not [f for f in f_ok_c if f.code in ("CONTRAST_BANNED", "DARK_GRAY_TEXT", "CONTRAST_LOW")], f"False contrast warn: {f_ok_c}"
    f_ok_p = lint_tooltip(TooltipItem("cp", 1, ScalarEntry(1, "&5&lBOSS"), []))
    assert not [f for f in f_ok_p if f.code == "CONTRAST_LOW"], f"False warn on short bold &5: {f_ok_p}"

    # 11. Item profile (--profile item): ARPG soft palette, 24/19 tradeable cap, Case A enchants, footer italic split, triggers, legacy ban, CTAs
    good_item_yaml = """
items:
  frost_blade:
    display_name: "<!i><#C3A3F5>Hàn Băng Kiếm <#E8E4EE>+5"
    lore:
      - "<!i><#A9A6B4>Vũ khí <#5E596B>· <#C3A3F5>Sử Thi"
      - ""
      - "<!i><#A9A6B4>Sát thương: <#E8E4EE>+28.5 <#EE9A8A>⚔"
      - "<!i><#A9A6B4>Chí mạng: <#E8E4EE>+12% <#E8B4D8>✷"
      - "<!i><#A9A6B4>Tốc đánh: <#E8E4EE>1.6/giây <#B9E08F>⚡"
      - ""
      - "<!i><#8CC8E8>Bão Băng Giam Cầm <#8A8597>· Chuột phải"
      - "<!i><#A9A6B4>Triệu hồi bão băng quanh bạn,"
      - "<!i><#A9A6B4>đóng băng kẻ địch <#E8E4EE>2 giây<#A9A6B4>."
      - "<!i><#8A8597>Hồi chiêu: 14 giây"
      - ""
      - "<!i><italic><#8A8597>Rèn từ lõi tim Hàn Băng Vương."
      - "<!i><#8A8597>Gắn hồn"
"""
    it_good = parse_yaml_tooltips(good_item_yaml)[0]
    f_item_ok = lint_tooltip(it_good, profile="item", vanilla_lines=3)
    assert not [f for f in f_item_ok if f.severity in ("ERROR", "WARN")], f"Unexpected on good item: {f_item_ok}"
    # Vanilla lines pushing over 24 (soulbound) and 19 (--tradeable)
    f_item_tall = lint_tooltip(it_good, profile="item", vanilla_lines=12)
    assert any(f.code == "VERTICAL_HEIGHT" for f in f_item_tall), "Missed --vanilla-lines VERTICAL_HEIGHT (25 > 24)"
    f_trade_tall = lint_tooltip(it_good, profile="item", vanilla_lines=7, tradeable=True)
    assert any(f.code == "VERTICAL_HEIGHT" for f in f_trade_tall), "Missed --tradeable VERTICAL_HEIGHT (20 > 19)"
    # F-03: Case A enchant blocks (varied 1/line & 5 enchants 2/line) must not false-positive GROUP_BALANCE
    f_ench_1 = lint_tooltip(TooltipItem("e1", 1, ScalarEntry(1, "<!i><#C3A3F5>Cúp Tinh Thạch"), [
        ScalarEntry(2, "<!i><#A9A6B4>Gia Tài <#E8E4EE>III"),
        ScalarEntry(3, "<!i><#A9A6B4>Mềm Mại <#E8E4EE>I"),
        ScalarEntry(4, "<!i><#A9A6B4>Lời Nguyền Biến Mất"),
    ]), profile="item")
    assert not [f for f in f_ench_1 if f.code == "GROUP_BALANCE"], f"False GROUP_BALANCE on 1/line enchants: {f_ench_1}"
    f_ench_5 = lint_tooltip(TooltipItem("e5", 1, ScalarEntry(1, "<!i><#C3A3F5>Cúp Tinh Thạch"), [
        ScalarEntry(2, "<!i><#A9A6B4>Hiệu Suất <#E8E4EE>V <#5E596B>· <#A9A6B4>Gia Tài <#E8E4EE>III"),
        ScalarEntry(3, "<!i><#A9A6B4>Chậm Hỏng <#E8E4EE>III <#5E596B>· <#A9A6B4>Tu Sửa <#E8E4EE>I"),
        ScalarEntry(4, "<!i><#A9A6B4>Mềm Mại <#E8E4EE>I"),
    ]), profile="item")
    assert not [f for f in f_ench_5 if f.code == "GROUP_BALANCE"], f"False GROUP_BALANCE on 5-enchant 2/line: {f_ench_5}"
    # F-03: Uneven 2-line italic flavor still warns, while italic flavor + short non-italic footer passes (verified in it_good above)
    f_flav_uneven = lint_tooltip(TooltipItem("fl", 1, ScalarEntry(1, "<!i><#C3A3F5>Nhẫn Băng"), [
        ScalarEntry(2, "<!i><italic><#8A8597>Rèn từ lõi tim Hàn Băng Vương cổ đại,"),
        ScalarEntry(3, "<!i><italic><#8A8597>chưa ai giữ nổi."),
    ]), profile="item")
    assert any(f.code == "GROUP_BALANCE" for f in f_flav_uneven), "Missed uneven 2-line italic flavor"
    # F-03 & F-06: Shift + Q trigger & consistent data_tier across Chuột phải vs Bị động
    f_shift_q = lint_tooltip(TooltipItem("sk_q", 1, ScalarEntry(1, "<!i><#C3A3F5>Cúp Tinh Thạch"), [
        ScalarEntry(2, "<!i><#8CC8E8>Bùng Nổ Quặng Cực Mạnh <#8A8597>· Shift + Q"),
        ScalarEntry(3, "<!i><#A9A6B4>Đào khối 3x3."),
    ]), profile="item")
    assert not [f for f in f_shift_q if f.code == "GROUP_BALANCE"], f"Shift + Q skill header grouped as prose: {f_shift_q}"
    assert is_data_line("Bão Băng Giam Cầm · Bị động") and is_data_line("Bão Băng Giam Cầm · Chuột phải")
    # F-06: Legacy colors banned on item (unless allow_legacy_item), plus 'Chuột trái:' caught as PASSIVE_ITEM_CTA
    f_item_bad = lint_tooltip(
        TooltipItem("bad_gear", 1, ScalarEntry(1, "<!i><#C3A3F5>Thần Kiếm Hủy Diệt Cổ Đại Cấp Năm"), [
            ScalarEntry(2, "<!i><gray>Chuột trái: <#E8E4EE>Đánh thường"),
        ]),
        profile="item",
    )
    assert any(f.code == "ITEM_NAME_WIDE" for f in f_item_bad), "Missed ITEM_NAME_WIDE"
    assert any(f.code == "PASSIVE_ITEM_CTA" for f in f_item_bad), "Missed PASSIVE_ITEM_CTA on 'Chuột trái:'"
    assert any(f.code == "ITEM_LEGACY_COLOR" for f in f_item_bad), "Missed ITEM_LEGACY_COLOR on <gray>"
    f_item_allow_leg = lint_tooltip(TooltipItem("ok_leg", 1, ScalarEntry(1, "&dKiếm"), [ScalarEntry(2, "&7Vũ khí")]),
                                    profile="item", allow_legacy_item=True)
    assert not [f for f in f_item_allow_leg if f.code == "ITEM_LEGACY_COLOR"], "allow_legacy_item failed to suppress"

    # 11b. Stat symbol widths: Non-Pack trailing icons pass freely; leading icons must share one width (item-lore.md §5.1-5.2)
    assert glyph_width("⛏") == 9 and glyph_width("⚔") == 8 and glyph_width("⛨") == 8 and glyph_width("◆") == 6 and glyph_width("☘") == 7 and glyph_width("◈") == 4
    trailing = lint_tooltip(TooltipItem("icons_trailing", 1, ScalarEntry(1, "<!i><#C3A3F5>Cúp Thử"), [
        ScalarEntry(2, "<!i><#A9A6B4>Tốc đào: <#E8E4EE>+45 <#E3C48A>⛏"),
        ScalarEntry(3, "<!i><#A9A6B4>May mắn: <#E8E4EE>+12% <#9FD3A8>☘"),
        ScalarEntry(4, "<!i><#A9A6B4>Độ cứng: <#E8E4EE>Bậc 4 <#A9BCD6>⛰"),
    ]), profile="item")
    assert not [f for f in trailing if f.severity in ("ERROR", "WARN")], f"Unexpected warn on trailing icons: {trailing}"
    ragged = lint_tooltip(TooltipItem("icons_bad", 1, ScalarEntry(1, "<!i><#C3A3F5>Cúp Thử"), [
        ScalarEntry(2, "<!i><#E3C48A>⛏ <#A9A6B4>Tốc đào: <#E8E4EE>+45"),
        ScalarEntry(3, "<!i><#9FD3A8>☘ <#A9A6B4>May mắn: <#E8E4EE>+12%"),
        ScalarEntry(4, "<!i><#A9BCD6>◈ <#A9A6B4>Độ cứng: <#E8E4EE>Bậc 4"),
    ]), profile="item")
    assert any(f.code == "STAT_ICON_WIDTH" for f in ragged), f"Missed STAT_ICON_WIDTH: {ragged}"
    even = lint_tooltip(TooltipItem("icons_ok", 1, ScalarEntry(1, "<!i><#C3A3F5>Kiếm Thử"), [
        ScalarEntry(2, "<!i><#EE9A8A>⚔ <#A9A6B4>Sát thương: <#E8E4EE>+28.5"),
        ScalarEntry(3, "<!i><#E8B4D8>✷ <#A9A6B4>Chí mạng: <#E8E4EE>+12%"),
        ScalarEntry(4, "<!i><#B9E08F>➾ <#A9A6B4>Tốc đánh: <#E8E4EE>1.6/giây"),
    ]), profile="item")
    assert not [f for f in even if f.code in ("STAT_ICON_WIDTH", "STAT_ICON_UNMEASURED")], f"False STAT_ICON warn: {even}"
    # Nexo pack glyphs (<glyph:id>) count as one 8 px icon, not as visible tag text
    pack = lint_tooltip(TooltipItem("icons_pack", 1, ScalarEntry(1, "<!i><#C3A3F5>Cúp Thử"), [
        ScalarEntry(2, "<!i><#FFFFFF><glyph:stat_dao> <#A9A6B4>Tốc đào: <#E8E4EE>+45"),
        ScalarEntry(3, "<!i><#FFFFFF><glyph:stat_luck> <#A9A6B4>May mắn: <#E8E4EE>+12%"),
    ]), profile="item")
    assert not [f for f in pack if f.severity in ("ERROR", "WARN")], f"Pack glyph rows flagged: {pack}"
    assert analyze_line("<glyph:stat_dao> Tốc").pixels == 8 + 4 + 6 * 3, "pack glyph = 8 px + space 4 + 'Tốc' 18"

    # 12. M-10: Vietnamese stdout sanity (must not raise UnicodeEncodeError on Windows cp1258)
    print("SELF-TEST PASS: all 12 suites (clean, GLR-01..09, THICK_BAR, WCAG, item-profile ARPG, tiếng Việt UTF-8) verified.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    _configure_stdio_utf8()

    ap = argparse.ArgumentParser(description="Lint Minecraft GUI & Carried-Item names and lore.")
    ap.add_argument("target", nargs="?", help="YAML or plain-text file to lint")
    ap.add_argument("--profile", choices=("gui", "item"), default="gui",
                    help="Tooltip surface profile: gui (default) or item (carried/equipped gear)")
    ap.add_argument("--hard-max", type=int, default=None, help="Enforce hard visible NFC character cap (e.g. 23)")
    ap.add_argument("--max-lines", type=int, default=None,
                    help="Vertical rendered lore line budget (default: 14 for gui, 24 for item, 19 with --tradeable)")
    ap.add_argument("--vanilla-lines", type=int, default=0,
                    help="Extra vanilla enchant/attribute rows to include in vertical height check (default: 0)")
    ap.add_argument("--tradeable", action="store_true",
                    help="Item profile: enforce <= 19 lore+vanilla lines (reserves 5 AH/trade rows out of 24)")
    ap.add_argument("--allow-legacy-item", action="store_true",
                    help="Item profile: allow vanilla legacy colors (&7/<gray>/etc.) when overriding soft hex registry")
    ap.add_argument("--serializer", choices=("auto", "minimessage", "legacy", "barehex"), default="auto",
                    help="Formatting syntax profile (default: auto; use barehex for #RRGGBB-without-& plugins)")
    ap.add_argument("--api-non-italic", action="store_true",
                    help="Suppress MM_ITALIC when target plugin clears italics in Java API")
    ap.add_argument("--strict", action="store_true", help="Exit 1 on warnings as well as errors")
    ap.add_argument("--plain", action="store_true", help="Treat file as plain snippet (line 1 = name, rest = lore)")
    ap.add_argument("--self-test", action="store_true", help="Run built-in linter self-tests")
    ap.add_argument("--measure", metavar="CHARS", default=None,
                    help="Print the vanilla 1.21.11 advance width of each character and exit")
    ap.add_argument("--unifont", metavar="PATH", default=None,
                    help="With --measure: Minecraft unifont.zip (or .hex) to measure symbols missing from the built-in table")
    args = ap.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if args.measure:
        live = measure_unifont_zip(args.unifont, args.measure) if args.unifont else {}
        for ch in dict.fromkeys(args.measure):
            if ch.isspace():
                continue
            if ch in VANILLA_WIDTHS:
                src, w = "default bitmap", VANILLA_WIDTHS[ch]
            elif live.get(ch) is not None:
                src, w = "unifont.zip", live[ch]
            elif ch in UNIFONT_WIDTHS:
                src, w = "unifont (built-in table)", UNIFONT_WIDTHS[ch]
            else:
                src, w = "unmeasured", None
            print(f"U+{ord(ch):04X} {ch}  {w if w is not None else '?'} px  [{src}]")
        return 0
    if not args.target:
        ap.error("Provide a file path or --self-test")

    p = Path(args.target)
    try:
        text = p.read_text(encoding="utf-8")
        items = parse_plain_tooltips(text) if args.plain else parse_yaml_tooltips(text)
    except Exception as exc:
        print(f"PARSE ERROR ({p.name}): {exc}", file=sys.stderr)
        return 2

    total_err = 0
    total_warn = 0
    total_info = 0
    print(f"Scanned {p.name} [{FONT_PROFILE}, profile={args.profile}, serializer={args.serializer}]: {len(items)} tooltip(s)")
    if not items:
        print("  [NOTE ] No GUI/item tooltips matched standard item/lore keys in this file.")
    for it in items:
        fs = lint_tooltip(
            it,
            hard_max=args.hard_max,
            max_lines=args.max_lines,
            serializer=args.serializer,
            api_non_italic=args.api_non_italic,
            profile=args.profile,
            vanilla_lines=args.vanilla_lines,
            tradeable=args.tradeable,
            allow_legacy_item=args.allow_legacy_item,
        )
        for f in fs:
            if f.severity == "ERROR":
                total_err += 1
            elif f.severity == "WARN":
                total_warn += 1
            else:
                total_info += 1
            print(f"  [{f.severity:5}] {f.item_id} (L{f.line_no}) {f.code}: {f.message}")

    print(f"Summary: {total_err} error(s), {total_warn} warning(s), {total_info} info(s)")
    if total_err > 0 or (args.strict and total_warn > 0):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
