# -*- coding: utf-8 -*-
"""Builds common-languages.html. Every value is verified to be exactly
5, 7 or 8 Unicode code points after the `common-` prefix."""
import sys

# CJK and Hangul: real place names, one code point per visible character.
# The alphabetic scripts use standalone letters with no combining marks, so the
# code point count and what you see on screen are the same thing.
LANGS = [
    ("Chinese", "Simplified Han", "zh-Hans", "cjk-sc", {
        5: "上海市浦东",
        7: "上海市浦东新区",
        8: "上海市浦东新区张",
    }),
    ("Japanese", "Kanji and Kana", "ja", "cjk-jp", {
        5: "大阪府梅田",
        7: "大阪府梅田中央",
        8: "大阪府梅田中央区",
    }),
    ("Korean", "Hangul", "ko", "cjk-kr", {
        5: "부산광역시",
        7: "부산광역시해운",
        8: "부산광역시해운대",
    }),
    ("Hindi", "Devanagari", "hi", "deva", {
        5: "टठडढत",
        7: "टठडढतथद",
        8: "टठडढतथदध",
    }),
    ("Telugu", "Telugu", "te", "telu", {
        5: "టఠడఢత",
        7: "టఠడఢతథద",
        8: "టఠడఢతథదధ",
    }),
    ("Kannada", "Kannada", "kn", "knda", {
        5: "ಟಠಡಢತ",
        7: "ಟಠಡಢತಥದ",
        8: "ಟಠಡಢತಥದಧ",
    }),
    ("Arabic", "Arabic, right to left", "ar", "arab", {
        5: "رزسشص",
        7: "رزسشصضط",
        8: "رزسشصضطظ",
    }),
    ("Thai", "Thai", "th", "thai", {
        5: "ดตถทธ",
        7: "ดตถทธนบ",
        8: "ดตถทธนบป",
    }),
]

# verify every string is exactly the length it claims
bad = [(n, k, s, len(s)) for n, _, _, _, d in LANGS for k, s in d.items() if len(s) != k]
if bad:
    for b in bad:
        print("LENGTH MISMATCH", b)
    sys.exit(1)
print("all %d values verified" % sum(len(d) for _, _, _, _, d in LANGS))

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
.val .pre{font-family:"Arial Black","Helvetica Neue",Helvetica,Arial,sans-serif;font-weight:900}

.cjk-sc .val{font-family:"Noto Sans SC","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif}
.cjk-jp .val{font-family:"Noto Sans JP","Hiragino Sans","Yu Gothic","Meiryo",sans-serif}
.cjk-kr .val{font-family:"Noto Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif}
.deva   .val{font-family:"Noto Sans Devanagari","Kohinoor Devanagari","Mangal",sans-serif}
.telu   .val{font-family:"Noto Sans Telugu","Kohinoor Telugu","Gautami",sans-serif}
.knda   .val{font-family:"Noto Sans Kannada","Kohinoor Kannada","Tunga",sans-serif}
.arab   .val{font-family:"Noto Sans Arabic","Geeza Pro","Segoe UI",sans-serif}
.thai   .val{font-family:"Noto Sans Thai","Thonburi","Leelawadee UI",sans-serif}

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
}
"""

CONTROL = """  <div class="control">
    <p><b>Static control block.</b> Identical in every capture of this page. A difference
    reported inside this block means the rule has over matched and is touching content it
    was never meant to.</p>
    <p>Reference line: the quick brown fox jumps over the lazy dog, 0123456789.
    Nothing here matches the rule.</p>
  </div>"""

blocks = []
for name, script, lang, cls, vals in LANGS:
    rows = []
    for n in (5, 7, 8):
        s = vals[n]
        rows.append(
            '      <div class="row">\n'
            '        <div class="n">%d chars</div>\n'
            '        <p class="val" data-lang="%s" data-len="%d" lang="%s">'
            '<span class="pre">common-</span><span class="sfx">%s</span></p>\n'
            '      </div>' % (n, lang, n, lang, s))
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
  Eight scripts, three values each, at 5, 7 and 8 characters after `common-`.
  Every value is verified to be exactly that many Unicode code points, which is
  what `.` counts in a Python regex.

  Chinese, Japanese and Korean use real place names, one code point per visible
  character. The alphabetic scripts use standalone letters with no combining
  marks, so what you count on screen is what the regex counts. Mixing in vowel
  signs would make the two disagree and muddy the test.

  Each suffix lives in its own <span class="sfx"> so the characters can be
  swapped or reordered later without touching anything else.

  Fonts are pulled from Google Noto so the scripts render the same wherever the
  page is captured, rather than depending on what the capture machine happens to
  have installed.
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
    Eight scripts, three values each, at 5, 7 and 8 characters after the prefix.
    Every value matches the rule and sits well inside the 50 character bound.
  </p>

%s

%s

</div>

</body>
</html>
""" % (FONTS, CSS, "\n\n".join(blocks), CONTROL)

open("common-languages.html", "w", encoding="utf-8").write(html)
print("written: common-languages.html  (%d values)" % sum(len(d) for _, _, _, _, d in LANGS))
