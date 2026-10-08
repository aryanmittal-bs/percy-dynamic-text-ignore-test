# Dynamic text ignore fixture

One long production style page for testing Percy's project level
**dynamic text intelli-ignore** (PPLT-6174 / PPLT-6133).

Live: https://aryanmittal-bs.github.io/percy-dynamic-text-ignore-test/
Source: `index.html`, a single self contained file.

About 6,174px tall at 1280 and 11,277px at 375.

## The values change on every load

No editing needed between captures. A small inline script rewrites every
`data-dyn` value on each page load, so every capture differs from the last one
on its own.

What it guarantees:

- **Same character length, every time.** Digits are swapped for digits, month
  and weekday names for ones of equal length, words for words of equal length.
  If no equal length word exists the original is kept. 184 of the 185 values are
  exactly length preserving.
- **Same page height, every time.** Verified across 8 loads: 6,174px at 1280 and
  11,277px at 375, every single load. Nothing reflows. The only difference
  between two captures is which characters are drawn.
- **Repeated values stay consistent.** Every place that showed the same invoice
  id still shows the same new id, so the page reads as one coherent document.
- **Nothing outside `data-dyn` is touched.** Verified across 6 loads: every
  heading, label, table header, button, pill and hint is byte identical, and so
  are the chart bar heights and the static control block.

The one exception is the long textarea, which picks from a pool of four written
messages of slightly different lengths. It sits in a fixed height box, so it
does not affect layout.

`?static=1` turns randomising off and gives you the values written in the HTML.

## What is on the page

| Attribute | Rule it targets | Example | Count |
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

Values sit at a mixed type scale, from 12px captions up to the 52px hero amount,
so each rule is tested at more than one text size.

## Two things that never change

- **Chart bar heights** are structure, not data. A changing bar height would be
  a genuine layout diff that no text rule will ignore.
- **The static control block** near the foot of the page. A diff reported inside
  it means a rule has over matched and is suppressing or shifting content it was
  never meant to touch.

## Capturing

```
export PERCY_TOKEN=<project token>
npx percy snapshot snapshots.yml
```

Run it twice. The first build is the baseline, approve it, then run it again and
the values will already be different. One snapshot, captured at 375 and 1280.
