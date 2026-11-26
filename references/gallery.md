# Golden Tooltip Gallery (`G1–G8` & `I1–I6`)

Complete, production-ready Vietnamese examples matching every role in
[pattern-library.md §6](pattern-library.md#6-recipes-by-item-role) and
[item-lore.md](item-lore.md). Start from the closest role below instead of
improvising from shorthand pattern codes.

- Every GUI example (`G1–G8`) passes `scripts/lint_lore.py --profile gui --strict`
  with **0 errors, 0 warnings**.
- Every Item example (`I1–I6`) passes `scripts/lint_lore.py --profile item --strict`
  with **0 errors, 0 warnings**.
- GUI examples use `[Non-Pack OK]` Mojang Java 1.21.11 bitmap glyphs; Non-Pack
  Item examples (`I1–I5`) use the neutral-body + mood/rarity palette from
  [item-lore.md](item-lore.md) with trailing BMP stat symbols (`Tốc đào: +45 ⛏`)
  so labels align flush-left, plus 6 px bitmap gem sockets `◆ ◇`; Pack example
  `I6` uses leading 8 px Nexo `<glyph:id>` icons. All keep WCAG `>= 4.5:1`
  readable contrast on `#100010` and single-role color discipline.
- *(Client render note: verified statically via Mojang 1.21.11 glyph metrics and
  WCAG contrast; confirm final feel with an in-game screenshot at GUI Scale 3–4.)*

---

## Part 1 — GUI Menu Examples (`--profile gui --strict`)

### G1. Navigation / Back button
*Role: compact 3-line navigation / back button tooltip.*

```yaml
nav_back:
  material: ARROW
  display_name: "<!i><#F87171>Quay Lại"
  lore:
    - "<!i><gray>Trở về menu chính."
    - ""
    - "<!i><#F87171>→ Nhấn để quay lại"
```

### G2. Warp / Hub card (Decision-first + Dynamic eligibility + Card-accent CTA)
*Role: puts requirement & boss in lines 1–2 (`M-2` unmet red + `#8C8CA0` current value; swaps to `<green>Cấp 45 ✔` when met), thin `|` and `C5` CTA match card accent `#38BDF8` without colliding with `aqua`.*

```yaml
warp_darkwater:
  material: PRISMARINE_SHARD
  display_name: "<!i><#38BDF8>Động Huyền Thủy"
  lore:
    - "<!i><#38BDF8>| <gray>Yêu cầu: <red>Cấp 45 <#8C8CA0>(bạn: 38)"
    - "<!i><#38BDF8>| <gray>Trùm giữ cửa: <white>Thủy Quái"
    - ""
    - "<!i><gray>Hang ngầm sâu dưới đáy biển,"
    - "<!i><gray>nơi rơi ngọc biển hiếm nhất."
    - ""
    - "<!i><#38BDF8>→ Nhấn để dịch chuyển"
```

### G3. Daily / Playtime reward (`H1`, `•`, `V1`, `V3`, `C1`)
*Role: decision status + fixed timer (`V3`) on top, `•` (`3 px`) reward rows using `V1` resource colors (`#FFD54F` Xu, `#A78BFA` Chìa Sử Thi), distinct from `#38BDF8` title and `<green>` claim CTA.*

```yaml
daily_reward_ready:
  material: CHEST_MINECART
  display_name: "<!i><dark_gray>[<#38BDF8>Quà Điểm Danh<dark_gray>]"
  lore:
    - "<!i><gray>Trạng thái: <green>Sẵn sàng nhận"
    - "<!i><gray>Làm mới sau: <white>08h 14m 05s"
    - ""
    - "<!i><gray>• Tiền thưởng: <#FFD54F>5.000 Xu"
    - "<!i><gray>• Chìa kho báu: <#A78BFA>Chìa Sử Thi x1"
    - ""
    - "<!i><green>→ Chuột trái để nhận quà"
```

### G4. Multi-state slot (`V6` + `C4` guided lock)
*Role: identical skeleton and CTA wording across active states (`N-6`); urgency scale `<green>` → orange `#FF9F43` → `<red>` stays strictly separate from `#FFD54F` Xu (`H-2`); locked state gives exact shortage + `/nhiemvu` (`M-3`).*

```yaml
pass_healthy:
  material: LIME_DYE
  display_name: "<!i><green>Thẻ Tháng BoxMine"
  lore:
    - "<!i><green>● Thẻ đang kích hoạt"
    - "<!i><gray>Còn lại: <white>22 ngày 04 giờ"
    - ""
    - "<!i><gray>Phí gia hạn thẻ: <#FFD54F>99 Xu"
    - "<!i><gray>Cộng thêm: <white>30 ngày / lần"
    - ""
    - "<!i><green>→ Chuột trái để gia hạn"

pass_expiring:
  material: ORANGE_DYE
  display_name: "<!i><#FF9F43>Thẻ Tháng BoxMine"
  lore:
    - "<!i><#FF9F43>● Thẻ sắp hết hạn"
    - "<!i><gray>Còn lại: <#FF9F43>04 ngày 02 giờ"
    - ""
    - "<!i><gray>Phí gia hạn thẻ: <#FFD54F>99 Xu"
    - "<!i><gray>Cộng thêm: <white>30 ngày / lần"
    - ""
    - "<!i><#FF9F43>→ Chuột trái để gia hạn"

pass_locked:
  material: GRAY_DYE
  display_name: "<!i><red>Thẻ Tháng BoxMine"
  lore:
    - "<!i><red>✘ Thẻ chưa kích hoạt"
    - "<!i><gray>Phí kích hoạt: <#FFD54F>99 Xu"
    - "<!i><gray>Bạn đang có: <red>45 Xu"
    - ""
    - "<!i><red>✘ Còn thiếu 54 Xu để mở"
    - "<!i><gray>Kiếm thêm tại <white>/nhiemvu"
```

### G5. Level / Quest milestone (`H1`, neutral `&8` `V4` bar + `10/20`)
*Role: neutral `<dark_gray>` unfilled bar (`M-4`) paired with absolute `10/20` and clean Vietnamese terms (`V0`, no redundant units).*

```yaml
milestone_20:
  material: NETHER_STAR
  display_name: "<!i><dark_gray>[<#38BDF8>Mốc Nhiệm Vụ 20<dark_gray>]"
  lore:
    - "<!i><gray>Tiến độ: <dark_gray>[<green>|||||<dark_gray>:::::] <white>10<gray>/20"
    - "<!i><gray>Còn cần: <white>10 nhiệm vụ nữa"
    - ""
    - "<!i><#38BDF8>Phần Thưởng"
    - "<!i><gray>• Tiền thưởng: <#FFD54F>25.000 Xu"
    - "<!i><gray>• Chìa Phổ Thông: <#A78BFA>x2"
    - "<!i><gray>• Bụi Sao rèn đồ: <#F472B6>+20"
    - ""
    - "<!i><red>✘ Chưa đạt đủ mốc 20"
    - "<!i><gray>Xem nhiệm vụ tại <white>/nhiemvu"
```

### G6. Shop offer / Consumable (`H2`, Decision-first + Dynamic balance `M-2`)
*Role: `H2` subtitle in `#8C8CA0` (`6.2:1`, never `&8`), price & live player balance in lines 2–3 before effect description, action-colored CTA.*

```yaml
shop_lucky_potion:
  material: POTION
  display_name: "<!i><#38BDF8>Thuốc May Mắn I"
  lore:
    - "<!i><#8C8CA0>Thuốc Đào Mỏ"
    - ""
    - "<!i><#38BDF8>| <gray>Giá vật phẩm: <#FFD54F>12.000 Xu"
    - "<!i><#38BDF8>| <gray>Bạn đang có: <green>35.000 Xu ✔"
    - ""
    - "<!i><gray>Tăng <white>+15%<gray> tỷ lệ rơi quặng hiếm"
    - "<!i><gray>trong <white>10 phút<gray> đào mỏ liên tục."
    - ""
    - "<!i><green>→ Chuột trái để mua ngay"
```

### G7. Upgrade / Enchant entry (`H1`, `B3` + `B2 |`, `V7` delta + bulk preview, `C2`)
*Role: `V7` delta (`+26% → +28%`) removes total-vs-increment ambiguity, `Tối đa 8 cấp: 21.000 Lapis` previews bulk cost (`M-8`), and `C2` colors the actions instead of mouse labels (`M-1`) without chopping `Shift + Chuột trái` (`H-1`).*

```yaml
enchant_fortune:
  material: ENCHANTED_BOOK
  display_name: "<!i><dark_gray>[<#A78BFA>Gia Tài Quặng<dark_gray>]"
  lore:
    - "<!i><#A78BFA>Nâng Cấp"
    - "<!i><#A78BFA>| <gray>Cấp hiện tại: <white>Lv.12<gray>/50"
    - "<!i><#A78BFA>| <gray>Hiệu quả: <white>+26% <gray>→ <green>+28%"
    - "<!i><#A78BFA>| <gray>Giá 1 cấp: <#FFD54F>2.500 Lapis"
    - "<!i><#A78BFA>| <gray>Tối đa 8 cấp: <#FFD54F>21.000 Lapis"
    - ""
    - "<!i><gray>Tăng mạnh lượng quặng rơi ra"
    - "<!i><gray>khi khai thác ở mọi khu mỏ."
    - ""
    - "<!i><gray>Chuột trái: <green>Nâng thêm 1 cấp"
    - "<!i><gray>Shift + Chuột trái: <#38BDF8>Nâng tối đa"
```

### G8. Destructive confirmation pair
*Role: destructive confirm vs safe cancel tooltip copy with explicit consequence and matching warning color.*

```yaml
confirm_delete_home:
  material: RED_CONCRETE
  display_name: "<!i><red><bold>Xác Nhận Xóa Nhà"
  lore:
    - "<!i><gray>Mục tiêu: <white>Nhà Mỏ Chính"
    - "<!i><gray>Hậu quả: <red>Không thể hoàn tác"
    - ""
    - "<!i><red>→ Nhấn để xóa vĩnh viễn"

cancel_delete_home:
  material: GRAY_CONCRETE
  display_name: "<!i><white>Hủy Và Quay Lại"
  lore:
    - "<!i><gray>Giữ nguyên vị trí nhà hiện tại"
    - "<!i><gray>và quay lại danh sách cũ."
    - ""
    - "<!i><gray>→ Nhấn để hủy thao tác"
```

---

## Part 2 — Carried & Equipped Item Examples (`--profile item --strict`)

House style **"ARPG gọn — nền dịu, điểm nhấn có cảm xúc"** from
[item-lore.md](item-lore.md): calm neutral body (`#A9A6B4` / `#ECE9F2` /
`#8A8597`), saturation escalated by rarity & item mood (softer on low tiers,
rich jewel/elemental accents on epic/boss/endgame gear, never raw RGB neon),
line 2 `Nhóm · Hạng`, trailing symbols on Non-Pack core stats, gems as their
own block, `Tên kỹ năng · Trigger`, one highlight per block, bright durability.

### I1. Material / Boss drop (3–5 lines)
*Role: rarity, crafting use and drop source; clean medium blue (`Hiếm`), no symbols, no footer needed.*

```yaml
item_kryon_crystal:
  material: AMETHYST_SHARD
  display_name: "<!i><#6CA8F8>Tinh Thể Kryon"
  lore:
    - "<!i><#A9A6B4>Nguyên liệu <#5E596B>· <#6CA8F8>Hiếm"
    - ""
    - "<!i><#A9A6B4>Dùng để: <#ECE9F2>Rèn giáp và cúp băng"
    - "<!i><#A9A6B4>Nguồn rơi: <#ECE9F2>Trùm Kryon"
```

### I2. Pickaxe with gems, set bonus and skill (canonical, 19 lines)
*Role: rich amethyst `Sử Thi` (`#B878FF`) and crisp utility icons over a calm neutral body (soulbound; 19 lore lines inside the 24-line 1080p GUI Scale 4 screen budget). Tradeable variants keep `lore + vanilla <= 19` (`--tradeable`).*

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

Low-durability state swaps only the durability row:
`"<!i><#A9A6B4>Độ bền: <#FF5C5C>86<#8A8597>/1.561 <#FF5C5C>· Cần sửa"`.

### I3. Boss weapon (13 lines + vanilla rows)
*Role: themed glacial-ice name (`#38BDF8`) paired with `Sử Thi` (`#B878FF`) tier line and rich combat icons (`#FF5C5C / #E879F9 / #FACC15`), showing how combat/elemental gear carries stronger saturation than utility items.*

```yaml
item_frost_blade:
  material: DIAMOND_SWORD
  item_flags: [HIDE_ATTRIBUTES]   # 1.21.5+: tooltip_display hides attribute_modifiers
  display_name: "<!i><#38BDF8>Hàn Băng Kiếm <#ECE9F2>+5"
  lore:
    - "<!i><#A9A6B4>Vũ khí <#5E596B>· <#B878FF>Sử Thi"
    - ""
    - "<!i><#A9A6B4>Sát thương: <#ECE9F2>+28.5 <#FF5C5C>⚔"
    - "<!i><#A9A6B4>Chí mạng: <#ECE9F2>+12% <#E879F9>✷"
    - "<!i><#A9A6B4>Tốc đánh: <#ECE9F2>1.6/giây <#FACC15>⚡"
    - ""
    - "<!i><#38BDF8>Bão Băng Giam Cầm <#8A8597>· Chuột phải"
    - "<!i><#A9A6B4>Triệu hồi bão băng quanh bạn,"
    - "<!i><#A9A6B4>đóng băng kẻ địch <#ECE9F2>2 giây<#A9A6B4>."
    - "<!i><#8A8597>Hồi chiêu: 14 giây"
    - ""
    - "<!i><italic><#8A8597>Rèn từ lõi tim Hàn Băng Vương."
    - "<!i><#8A8597>Rơi từ Hàn Băng Vương · Gắn hồn"
```

### I4. Enchants in lore, tier on top (`item-lore.md` §2.1 case A)
*Role: vanilla enchant rows hidden, enchants re-rendered by lore in calm neutral tones. Tier line stays on line 2, then one blank line, then the enchant block.*

```yaml
item_cup_tinh_thach_ench:
  material: NETHERITE_PICKAXE
  item_flags: [HIDE_ENCHANTS, HIDE_ATTRIBUTES]   # 1.21.5+: tooltip_display hides enchantments & attribute_modifiers
  display_name: "<!i><#B878FF>Cúp Tinh Thạch <#ECE9F2>+3"
  lore:
    - "<!i><#A9A6B4>Công cụ <#5E596B>· <#B878FF>Sử Thi"
    - ""
    - "<!i><#A9A6B4>Hiệu Suất <#ECE9F2>V"
    - "<!i><#A9A6B4>Gia Tài <#ECE9F2>III"
    - "<!i><#A9A6B4>Chậm Hỏng <#ECE9F2>III"
    - ""
    - "<!i><#A9A6B4>Tốc đào: <#ECE9F2>+45 <#F5B942>⛏"
    - "<!i><#A9A6B4>May mắn: <#ECE9F2>+12% <#34D399>✿"
    - "<!i><#A9A6B4>Độ cứng: <#ECE9F2>Bậc 4 <#93B4DC>⛰"
    - ""
    - "<!i><#38BDF8>Bùng Nổ Quặng <#8A8597>· Chuột phải"
    - "<!i><#A9A6B4>Đào khối 3x3 trong <#ECE9F2>5 giây<#A9A6B4>."
    - "<!i><#8A8597>Hồi chiêu: 60 giây"
    - ""
    - "<!i><#A9A6B4>Độ bền: <#ECE9F2>1.250<#8A8597>/1.561"
    - "<!i><#8A8597>Gắn hồn · Không thể giao dịch"
```

### I5. Vanilla enchants visible, tier at the bottom (`item-lore.md` §2.1 case B)
*Role: real enchant rows stay visible and the game draws them right under the
name, so the tier line moves to the very last line. Hiding `attribute_modifiers`
ensures `Công cụ · Hiếm` is genuinely the bottom line instead of sitting above
`"Khi ở tay chính:"`. Lore opens with a blank line so stats do not touch the
enchant rows. Lint with `--profile item --vanilla-lines 3 --strict`.*

```yaml
item_cup_lam_quang:
  material: DIAMOND_PICKAXE
  item_flags: [HIDE_ATTRIBUTES]   # 1.21.5+: tooltip_display hides attribute_modifiers so tier stays truly last
  enchantments: {efficiency: 5, fortune: 3, unbreaking: 3}   # syntax varies by plugin
  display_name: "<!i><#6CA8F8>Cúp Lam Quang"
  lore:
    - ""
    - "<!i><#A9A6B4>Tốc đào: <#ECE9F2>+30 <#F5B942>⛏"
    - "<!i><#A9A6B4>May mắn: <#ECE9F2>+8% <#34D399>✿"
    - "<!i><#A9A6B4>Độ cứng: <#ECE9F2>Bậc 3 <#93B4DC>⛰"
    - ""
    - "<!i><#A9A6B4>Độ bền: <#ECE9F2>1.480<#8A8597>/1.561"
    - ""
    - "<!i><#A9A6B4>Công cụ <#5E596B>· <#6CA8F8>Hiếm"
```

Rendered order in game (with `attribute_modifiers` hidden): `Cúp Lam Quang` →
`Hiệu suất V` / `Gia tài III` / `Chậm hỏng III` (vanilla gray, `vi_vn` client;
`Efficiency V` / `Fortune III` / `Unbreaking III` on `en_us`) → blank → stats →
durability → blank → `Công cụ · Hiếm`.

### I6. Pack version of I2 (Nexo / Resource Pack, `item-lore.md` §5.2)
*Role: same 19-line skeleton, colors and order as `I2`. Fixed-width 8 px pixel
stat icons sit leading before labels, gem sockets and rarity word become pack
glyphs, and the frame comes from a per-rarity `tooltip_style`. `<#FFFFFF>` before
each glyph guards against tint inheritance on raw PUA/non-Nexo setups. Glyph ids
and the component key are examples; verify them against your installed pack plugin.*

```yaml
item_cup_tinh_thach_pack:
  material: NETHERITE_PICKAXE
  item_flags: [HIDE_ATTRIBUTES]   # 1.21.5+: tooltip_display hides attribute_modifiers
  # component: tooltip_style = myserver:rarity_su_thi  (sprites tooltip/rarity_su_thi_background + _frame)
  display_name: "<!i><#B878FF>Cúp Tinh Thạch <#ECE9F2>+3"
  lore:
    - "<!i><#A9A6B4>Công cụ <#5E596B>· <#FFFFFF><glyph:rarity_su_thi>"
    - ""
    - "<!i><#FFFFFF><glyph:stat_dao> <#A9A6B4>Tốc đào: <#ECE9F2>+45"
    - "<!i><#FFFFFF><glyph:stat_luck> <#A9A6B4>May mắn: <#ECE9F2>+12%"
    - "<!i><#FFFFFF><glyph:stat_hard> <#A9A6B4>Độ cứng: <#ECE9F2>Bậc 4"
    - ""
    - "<!i><#A9A6B4>Ngọc khảm: <#FFFFFF><glyph:gem_luc> <glyph:gem_lam> <glyph:gem_empty>"
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
