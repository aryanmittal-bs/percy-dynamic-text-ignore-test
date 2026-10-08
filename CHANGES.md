# Changed variant: text only

Reverted to the exact page captured in build #8 and changed **only the text**.

- No style attribute added anywhere. Verified: `grep -c 'data-dyn="[a-z]*" style='` returns 0.
- CSS block, static control block and chart bar heights are **byte identical** to the build #8 page.
- **Every replacement is the same character length as the value it replaces.** 146 mappings, all length preserving.
- Result: the file is the same byte count as the build #8 page, and the rendered
  page height is identical at both widths, 6,174px at 1280 and 11,227px at 375.
  Nothing reflows. The only thing that moved is which characters are drawn.

185 values changed across all nine categories. A few examples:

| Rule | Before | After |
|---|---|---|
| Dates | 10 Jan 2025 | 27 Mar 2026 |
| Timestamps | 00:48:22 | 02:13:07 |
| Phone numbers | (855) 807-0572 | (415) 236-1188 |
| Prices | $1,240.00 | $3,815.42 |
| Email addresses | sam.carter@northwind.co | sam.carter@northgate.io |
| Numbers | 48,210 | 71,935 |
| Links | northwind.co/builds | northgate.io/charts |
| Typed-in text | invoice overage march | renewal credits april |
| Custom text | INV-2025-0418 | INV-2026-0973 |

With every rule enabled this page should come back with no differences at all.

Anything reported is either a rule that is not matching that format, or a rule
over matching, and the static control block tells the two apart: a diff inside
that block is over matching.
