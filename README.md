# Dynamic text ignore fixture

One long production style page for testing Percy's project level
**dynamic text intelli-ignore** (PPLT-6174 / PPLT-6133).

Live: https://aryanmittal-bs.github.io/percy-dynamic-text-ignore-test/
Source: `index.html`, a single self contained file. No JavaScript, no external
fonts, scripts, images or network calls.

About 6,200px tall at 1280 and 11,000px at 375, so it exercises a real scroll
length rather than one screenful.

## How to edit it

Every value the ignore rules should match is tagged with `data-dyn`:

| Attribute | Rule it targets | Example in the page | Count |
|---|---|---|---|
| `data-dyn="date"` | Dates | 10 Jan 2025, 2025-01-10, 01/10/2025, Friday, 10 January 2025 | 40 |
| `data-dyn="time"` | Timestamps | 00:48:22, 14:05, 2:05 PM, 00:00:04.218 | 23 |
| `data-dyn="phone"` | Phone numbers | (855) 807-0572, +44 20 7946 0318, +91 98200 12345 | 12 |
| `data-dyn="price"` | Prices | $1,240.00, $0.012, -$99.00 | 23 |
| `data-dyn="email"` | Email addresses | sam.carter@northwind.co | 15 |
| `data-dyn="number"` | Numbers | 48,210, 64%, 3 of 20, 6 of 24 results | 34 |
| `data-dyn="link"` | Links shown as text | northwind.co/builds, https://status.northwind.co | 20 |
| `data-dyn="typed"` | Typed-in text | input and textarea values | 8 |
| `data-dyn="custom"` | Custom text | INV-2025-0418, build-7f3a91, sess_8812ab44, ACC-77F3A91B | 20 |

195 tagged values in total. Find one kind with:

```
grep -n 'data-dyn="date"' index.html
```

The values sit at a **deliberately mixed type scale**, from 12px captions up to
the 52px hero amount, so each rule is tested at more than one text size.

## Making a changed variant

Copy `index.html`, change the **values only**. Do not touch labels, headings,
layout, the chart bar heights or the static control block. If you change any of
those you get diffs that have nothing to do with the ignore rules.

Two things on the page are deliberately NOT dynamic:

- **Chart bar heights** are structure, not data. A changing bar height is a
  genuine layout diff that no text rule will ignore.
- **The static control block** near the foot of the page is identical in every
  variant. A diff reported inside it means a rule has over matched and is
  suppressing or shifting content it was never meant to touch.

## Capturing

```
export PERCY_TOKEN=<project token>
npx percy snapshot snapshots.yml
```

Give the baseline and the changed capture the same snapshot name so they compare.
