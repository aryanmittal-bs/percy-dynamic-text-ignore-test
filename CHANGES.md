# Changed variant: what was altered

Baseline commit for this page: run `git log --oneline -- index.html` and take the
commit before "Changed variant". `git show <baseline>:index.html` recovers it.

## 1. Value only, 175 places

Every `data-dyn` value on the page was replaced with a different value of the
same kind. Dates moved from Jan 2025 to Mar 2026, prices roughly tripled, the
domain moved from northwind.co to northwind.io, ids were reissued, and so on.

**Expected: ignored**, because only the text changed and the rule for that kind
is enabled.

## 2. Value AND presentation, 10 places

These ten also had their font size and/or colour changed, so the pixels differ
for a reason that is not just the text.

| # | Rule | Where on the page | Value change | Presentation change |
|---|---|---|---|---|
| S1 | Prices | Hero, amount due | $1,240.00 to $3,815.42 | 52px to **64px**, dark ink to **red** |
| S2 | Dates | Hero, "Due ..." line | 9 February 2025 to 26 April 2026 | 15px to **22px**, bold, **red** |
| S3 | Custom text | Hero, invoice id | INV-2025-0418 to INV-2026-0973 | 24px to **32px**, **indigo** |
| S4 | Email addresses | Hero, billing contact | sam.carter@northwind.co to s.carter@northwind.io | 19px to **25px**, **green** |
| S5 | Phone numbers | Hero, account phone | (855) 807-0572 to (415) 236-1188 | 19px to **25px**, **indigo** |
| S6 | Numbers | KPI card, snapshots | 48,210 to 1,205,774 | **green** (size unchanged) |
| S7 | Timestamps | Chart footer, last refreshed | 14:05 to 09:41 | 13px to **20px**, **red** |
| S8 | Typed-in text | Nav search box | "invoice overage march" to "renewal credit april" | 17px to **21px**, **red** |
| S9 | Links | Footer, first product link | northwind.co/builds to northwind.io/dashboards | 15px to **21px**, bold, **red** |
| S10 | Prices | Invoice total due | $1,240.00 to $3,815.42 | 34px to **44px**, **red** |

**Expected: still reported.** A dynamic text rule is meant to forgive the value,
not a restyle. If these come back ignored, the rule is matching on the element
rather than on the text difference, and it will hide real regressions.

## 3. Deliberately NOT changed

- **Chart bar heights** are byte identical. Verified with a diff.
- **The static control block** is byte identical. Verified with a diff.
- Every heading, label, table header and section title is untouched.

So any diff reported in those places is the rules over matching.

Page height at 1280 went from 6,174px to 6,243px, which is the ten enlarged
elements pushing their rows slightly taller. That is expected, and it is part of
what makes group 2 a real visual change rather than a text swap.
