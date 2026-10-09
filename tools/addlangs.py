# -*- coding: utf-8 -*-
"""regex-common.html: add the remaining scripts as samples 7 to 13, and pin
every sample to a fixed suffix length so only the characters change."""
import io, re, sys

p = 'regex-common.html'
s = io.open(p, encoding='utf-8').read()

def dedupe(t):
    seen, out = set(), []
    for c in t:
        if c not in seen:
            seen.add(c); out.append(c)
    return "".join(out)

# key, label, colour name, hex, glow rgba, font stack, size, mobile size, fixed length, pool
NEW = [
    ("ja", "Japanese", "mint", "#7cf0c4", "124,240,196",
     '"Noto Sans JP","Hiragino Sans","Yu Gothic","Meiryo",sans-serif', 44, 27, 8,
     "大阪府梅田中央区東京都新宿役所名古屋横浜神戸札幌福岡仙台京奈良広島金沢静岡"),
    ("ko", "Korean", "pink", "#ff8ad4", "255,138,212",
     '"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif', 42, 26, 9,
     "부산광역시해운대서울특별강남구인천공항경기도제주세종대전광주울산수원성남"),
    ("hi", "Hindi", "periwinkle", "#8ab6ff", "138,182,255",
     '"Noto Sans Devanagari","Kohinoor Devanagari","Mangal",sans-serif', 40, 25, 10,
     "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"),
    ("te", "Telugu", "pale yellow", "#ffe066", "255,224,102",
     '"Noto Sans Telugu","Kohinoor Telugu","Gautami",sans-serif', 38, 24, 11,
     "కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలవశషసహ"),
    ("kn", "Kannada", "violet", "#b388ff", "179,136,255",
     '"Noto Sans Kannada","Kohinoor Kannada","Tunga",sans-serif', 36, 23, 12,
     "ಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲವಶಷಸಹ"),
    ("ar", "Arabic, right to left", "aqua", "#4dffd8", "77,255,216",
     '"Noto Sans Arabic","Geeza Pro","Segoe UI",sans-serif', 42, 26, 13,
     "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"),
    ("th", "Thai", "coral", "#ff9f7a", "255,159,122",
     '"Noto Sans Thai","Thonburi","Leelawadee UI",sans-serif', 40, 25, 14,
     "กขคงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"),
]
NEW = [t[:9] + (dedupe(t[9]),) for t in NEW]

for t in NEW:
    pool = t[9]
    if any(ord(c) > 0xFFFF for c in pool):
        print("ERROR: %s pool has a non BMP char" % t[0]); sys.exit(1)
    if len(pool) < 20:
        print("ERROR: %s pool only %d chars" % (t[0], len(pool))); sys.exit(1)

# ---- 1. widen the font link to cover every script ----
old = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@700&display=swap">'
assert s.count(old) == 1
s = s.replace(old, '<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
    '?family=Noto+Sans+SC:wght@700'
    '&family=Noto+Sans+JP:wght@700'
    '&family=Noto+Sans+KR:wght@700'
    '&family=Noto+Sans+Devanagari:wght@700'
    '&family=Noto+Sans+Telugu:wght@700'
    '&family=Noto+Sans+Kannada:wght@700'
    '&family=Noto+Sans+Arabic:wght@700'
    '&family=Noto+Sans+Thai:wght@700'
    '&display=swap">')

# ---- 2. pin every existing sample to one fixed length ----
FIXED = {1: 6, 2: 12, 3: 24, 4: 40, 5: 46, 6: 10}
for idx, n in FIXED.items():
    m = re.search(r'(<div class="sample s%d">.*?</div>\s*</div>)' % idx, s, re.S)
    assert m, "sample %d not found" % idx
    block = m.group(1)
    nb = re.sub(r'data-min="\d+" data-max="\d+"', 'data-min="%d" data-max="%d"' % (n, n), block)
    nb = re.sub(r'(<b class="len">)\d+(</b>)', r'\g<1>%d\g<2>' % n, nb)
    assert nb != block, "sample %d unchanged" % idx
    s = s.replace(block, nb)

# ---- 3. colour tokens ----
old = '  --amber:#ffa94d;'
assert s.count(old) == 1
s = s.replace(old, old + "\n" + "\n".join(
    "  --%s:%s;" % (t[0], t[3]) for t in NEW))

# ---- 4. per sample styles, appended after the Chinese one ----
old = """.s6 .val{
  font-family:"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-size:46px;line-height:1.3;font-weight:700;
  color:var(--amber);text-shadow:0 0 20px rgba(255,169,77,.40);
}"""
assert s.count(old) == 1
css = []
for i, t in enumerate(NEW, start=7):
    key, label, cname, hexv, glow, font, size, msize, n, pool = t
    css.append(""".s%d .val{
  font-family:%s;
  font-size:%dpx;line-height:1.3;font-weight:700;
  color:var(--%s);text-shadow:0 0 18px rgba(%s,.38);
}""" % (i, font, size, key, glow))
s = s.replace(old, old + "\n" + "\n".join(css))

# ---- 5. responsive sizes ----
old = '  .s6 .val{font-size:28px}'
assert s.count(old) == 1
s = s.replace(old, old + "\n" + "\n".join(
    "  .s%d .val{font-size:%dpx}" % (i, t[8]) for i, t in enumerate(NEW, start=7)))

# ---- 6. the new samples, appended after sample 6 ----
m = re.search(r'(<div class="sample s6">.*?</div>\s*</div>)', s, re.S)
assert m
blocks = []
for i, t in enumerate(NEW, start=7):
    key, label, cname, hexv, glow, font, size, msize, n, pool = t
    fallback = pool[:n]
    assert len(fallback) == n
    blocks.append("""    <div class="sample s%d">
      <div class="tag">Sample %d &middot; %s &middot; %s</div>
      <span class="val" data-rx data-min="%d" data-max="%d" data-chars="%s" lang="%s">common-%s</span>
      <div class="meta">suffix length <b class="len">%d</b> of 50</div>
    </div>""" % (i, i, cname, label, n, n, pool, key, fallback, n))
s = s.replace(m.group(1), m.group(1) + "\n\n" + "\n\n".join(blocks))

# ---- 7. header comment, not rendered ----
old = "  Six samples. Each keeps its OWN fixed font, size, weight, style and colour\n  on every load. Only the TEXT and its LENGTH change."
assert s.count(old) == 1
s = s.replace(old,
  "  Thirteen samples. Each keeps its OWN fixed font, size, weight, style and\n"
  "  colour, and its OWN fixed suffix LENGTH, on every load. Only the characters\n"
  "  change.")
old = "  Sample 6  amber     Chinese, Simplified Han"
assert s.count(old) == 1
s = s.replace(old, old + "\n" + "\n".join(
    "  Sample %-2d %-9s %s" % (i, t[2], t[1]) for i, t in enumerate(NEW, start=7)))
old = """  Suffix lengths are drawn from different bands so short and long cases are
  both on the page every time, including the 1 and 50 character boundaries."""
assert s.count(old) == 1
s = s.replace(old,
  "  Each sample has a fixed suffix length, from 6 up to 46, so short and long\n"
  "  cases are both on the page while no single value ever changes length.")

io.open(p, 'w', encoding='utf-8').write(s)
print("done: 13 samples, fixed lengths %s" % (
    sorted(list(FIXED.values()) + [t[8] for t in NEW])))
