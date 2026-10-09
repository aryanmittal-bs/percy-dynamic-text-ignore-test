# -*- coding: utf-8 -*-
"""Builds common-languages.html.

Nine scripts, three values each at 5, 7 and 8 code points after `common-`.
The values in the HTML are the fallback; an inline script rewrites every one of
them on each page load, picking from that script's own character pool and
keeping the code point count exactly.
"""
import json, sys

# key, display name, script note, lang attr, css class, fallback values, char pool
LANGS = [
    ("en", "English", "Latin", "en", "latn",
     {5: "Leeds", 7: "Bristol", 8: "Coventry"},
     "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"),

    ("zh", "Chinese", "Simplified Han", "zh-Hans", "cjk-sc",
     {5: "上海市浦东", 7: "上海市浦东新区", 8: "上海市浦东新区张"},
     "上海市浦东新区张北京朝阳中国广州深圳天津重庆南京杭州成都武汉西安长沙青岛大连"),

    ("ja", "Japanese", "Kanji and Kana", "ja", "cjk-jp",
     {5: "大阪府梅田", 7: "大阪府梅田中央", 8: "大阪府梅田中央区"},
     "大阪府梅田中央区東京都新宿役所名古屋横浜神戸札幌福岡仙台京奈良広島金沢静岡"),

    ("ko", "Korean", "Hangul", "ko", "cjk-kr",
     {5: "부산광역시", 7: "부산광역시해운", 8: "부산광역시해운대"},
     "부산광역시해운대서울특별강남구인천공항경기도제주세종대전광주울산수원성남"),

    ("hi", "Hindi", "Devanagari", "hi", "deva",
     {5: "टठडढत", 7: "टठडढतथद", 8: "टठडढतथदध"},
     "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"),

    ("te", "Telugu", "Telugu", "te", "telu",
     {5: "టఠడఢత", 7: "టఠడఢతథద", 8: "టఠడఢతథదధ"},
     "కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలవశషసహ"),

    ("kn", "Kannada", "Kannada", "kn", "knda",
     {5: "ಟಠಡಢತ", 7: "ಟಠಡಢತಥದ", 8: "ಟಠಡಢತಥದಧ"},
     "ಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಲವಶಷಸಹ"),

    ("ar", "Arabic", "Arabic, right to left", "ar", "arab",
     {5: "رزسشص", 7: "رزسشصضط", 8: "رزسشصضطظ"},
     "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"),

    ("th", "Thai", "Thai", "th", "thai",
     {5: "ดตถทธ", 7: "ดตถทธนบ", 8: "ดตถทธนบป"},
     "กขคงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"),
]

# ---- checks: fallback lengths, and every pool char must be one code point ----
# dedupe each pool in place, preserving order, so no character is weighted twice
_d = []
for t in LANGS:
    seen, out = set(), []
    for c in t[6]:
        if c not in seen:
            seen.add(c); out.append(c)
    _d.append(t[:6] + ("".join(out),))
LANGS = _d

errs = []
for key, _, _, _, _, vals, pool in LANGS:
    for n, s in vals.items():
        if len(s) != n:
            errs.append("%s fallback %d is %d code points: %r" % (key, n, len(s), s))
    for c in pool:
        if ord(c) > 0xFFFF:
            errs.append("%s pool char %r is outside the BMP, JS length would count it twice" % (key, c))
    if len(pool) < 20:
        errs.append("%s pool only has %d chars" % (key, len(pool)))
if errs:
    for e in errs:
        print("ERROR:", e)
    sys.exit(1)
print("checks passed: %d scripts, %d values, pools %s" % (
    len(LANGS), sum(len(v) for _, _, _, _, _, v, _ in LANGS),
    ", ".join("%s=%d" % (k, len(p)) for k, _, _, _, _, _, p in LANGS)))

POOLS_JS = json.dumps({k: p for k, _, _, _, _, _, p in LANGS}, ensure_ascii=False)

FONTS = ("https://fonts.googleapis.com/css2"
         "?family=Noto+Sans+SC:wght@700"
         "&family=Noto+Sans+JP:wght@700"
         "&family=Noto+Sans+KR:wght@700"
         "&family=Noto+Sans+Devanagari:wght@700"
         "&family=Noto+Sans+Telugu:wght@700"
         "&family=Noto+Sans+Kannada:wght@700"
         "&family=Noto+Sans+Arabic:wght@700"
         "&family=Noto+Sans+Thai:wght@700"
         "&display=swap")

CSS = """
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0;background:#ffffff;color:#0f1115;
  font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1180px;margin:0 auto;padding:56px 40px 90px}

h1{font-size:38px;line-height:1.1;letter-spacing:-.03em;margin:0 0 10px;font-weight:800}
.rule{
  display:inline-block;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-size:19px;color:#1f2937;background:#f1f3f6;border:1px solid #dce0e6;
  border-radius:9px;padding:7px 14px;margin:4px 0 8px;
}
.lede{color:#5b6472;font-size:16px;max-width:76ch;margin:0 0 10px}

.lang{margin-top:44px;padding-top:26px;border-top:2px solid #eceff3}
.lang:first-of-type{border-top:0}
.lang h2{
  font-size:13px;font-weight:800;letter-spacing:.16em;text-transform:uppercase;
  color:#8b94a3;margin:0 0 20px;
}
.lang h2 span{color:#c3c9d2;font-weight:700;letter-spacing:.1em}

.row{display:flex;align-items:baseline;gap:22px;padding:12px 0}
.n{
  flex:none;width:112px;font-size:12px;font-weight:800;letter-spacing:.1em;
  text-transform:uppercase;color:#9aa3b0;
}
.val{
  margin:0;font-size:54px;line-height:1.28;font-weight:700;letter-spacing:-.01em;
  color:#0f1115;word-break:break-all;overflow-wrap:anywhere;
}
.latn   .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,sans-serif}

/* one element means the strut now comes from Arial Black, so each script's
   line box is pinned back to the height the two element version produced */
.cjk-sc .val{line-height:72.11px}
.cjk-jp .val{line-height:72.11px}
.cjk-kr .val{line-height:72.11px}
.deva   .val{line-height:77.11px}
.telu   .val{line-height:79.11px}
.knda   .val{line-height:82.11px}
.arab   .val{line-height:73.11px}
.thai   .val{line-height:73.11px}
.cjk-sc .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
.cjk-jp .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans JP","Hiragino Sans","Yu Gothic","Meiryo",sans-serif}
.cjk-kr .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif}
.deva   .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans Devanagari","Kohinoor Devanagari","Mangal",sans-serif}
.telu   .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans Telugu","Kohinoor Telugu","Gautami",sans-serif}
.knda   .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans Kannada","Kohinoor Kannada","Tunga",sans-serif}
.arab   .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans Arabic","Geeza Pro","Segoe UI",sans-serif}
.thai   .val{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,"Noto Sans Thai","Thonburi","Leelawadee UI",sans-serif}

.control{
  margin-top:64px;background:#f1f3f6;border:1px dashed #c3c9d2;
  border-radius:12px;padding:20px 24px;max-width:900px;
}
.control p{margin:0 0 8px;font-size:13.5px;color:#5b6472}
.control p:last-child{margin:0}
.control b{color:#0f1115}

@media (max-width:820px){
  .wrap{padding:32px 18px 64px}
  h1{font-size:28px}
  .row{flex-direction:column;gap:4px;padding:10px 0}
  .n{width:auto}
  .val{font-size:34px}
  .cjk-sc .val{line-height:45.52px}
  .cjk-jp .val{line-height:45.52px}
  .cjk-kr .val{line-height:45.52px}
  .deva   .val{line-height:48.52px}
  .telu   .val{line-height:49.52px}
  .knda   .val{line-height:51.52px}
  .arab   .val{line-height:45.52px}
  .thai   .val{line-height:45.52px}
}
"""

CONTROL = """  <div class="control">
    <p><b>Static control block.</b> Identical in every capture of this page. A difference
    reported inside this block means the rule has over matched and is touching content it
    was never meant to.</p>
    <p>Reference line: the quick brown fox jumps over the lazy dog, 0123456789.
    Nothing here matches the rule.</p>
  </div>"""

SCRIPT = """<script>
(function () {
  if (/[?&]static=1/.test(location.search)) return;
  var POOLS = %s;
  var els = document.querySelectorAll('.sfx'), i, el, pool, n, s, j;
  for (i = 0; i < els.length; i++) {
    el = els[i];
    pool = POOLS[el.getAttribute('data-pool')];
    n = parseInt(el.getAttribute('data-len'), 10);
    if (!pool || !n) continue;
    s = '';
    for (j = 0; j < n; j++) s += pool.charAt(Math.floor(Math.random() * pool.length));
    el.textContent = 'common-' + s;
  }
})();
</script>""" % POOLS_JS

blocks = []
for key, name, script, lang, cls, vals, pool in LANGS:
    rows = []
    for n in (5, 7, 8):
        rows.append(
            '      <div class="row">\n'
            '        <div class="n">%d chars</div>\n'
            '        <p class="val sfx" lang="%s" data-pool="%s" data-len="%d">'
            'common-%s</p>\n'
            '      </div>' % (n, lang, key, n, vals[n]))
    blocks.append(
        '    <section class="lang %s">\n'
        '      <h2>%s <span>&middot; %s</span></h2>\n%s\n    </section>'
        % (cls, name, script, "\n".join(rows)))

html = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>common- in other scripts</title>
<!--
  ============================================================================
  NON LATIN SCRIPT FIXTURE   for the custom text rule  common-.{1,50}$
  ============================================================================
  Nine scripts, three values each, at 5, 7 and 8 characters after `common-`.

  Every suffix is regenerated on each page load from that script's own
  character pool, and always to the exact code point count written in
  data-len. So a fresh capture always differs from the last one, and the
  length never moves.

  Only the suffixes change. Headings, labels, the 5/7/8 markers, fonts, sizes
  and the static control block are identical on every load.

  Each pool holds single code point characters with no combining marks, so the
  count you see on screen is the count the regex sees. Mixing in vowel signs
  would make the two disagree and muddy the test.

  Fonts come from Google Noto so the scripts render the same wherever the page
  is captured, rather than depending on what the capture machine has installed.

  ?static=1 switches randomising off and shows the values written in the HTML.
  ============================================================================
-->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="%s">
<style>%s</style>
</head>
<body>

<div class="wrap">

  <h1>common- in other scripts</h1>
  <div class="rule">common-.{1,50}$</div>
  <p class="lede">
    Nine scripts, three values each, at 5, 7 and 8 characters after the prefix.
    Every value matches the rule and sits well inside the 50 character bound.
    The characters change on every load, the lengths never do.
  </p>

%s

%s

</div>

%s

</body>
</html>
""" % (FONTS, CSS, "\n\n".join(blocks), CONTROL, SCRIPT)

open("common-languages.html", "w", encoding="utf-8").write(html)
print("written: common-languages.html")
