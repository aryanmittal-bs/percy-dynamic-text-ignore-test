# Percy dynamic-text intelli-ignore fixtures

Static pages for testing project-level dynamic text ignore (PPLT-6133 / PPLT-6174).

Live: https://aryanmittal-bs.github.io/percy-dynamic-text-ignore-test/

## Structure

**Five mixed pages** carry all nine dynamic-text types in different layouts
(dashboard, invoice, profile, report, feed), so the rules are exercised together
the way a real page would.

**Four focused pages** carry only a named subset, so one rule can be proven
without another rule's values muddying the result. Page 06 is dates, timestamps
and phone numbers only.

**One negative control** puts a genuine visual change (a badge that changes
colour and wording) next to dynamic values. With every rule switched on, Percy
must still report this page as changed. If it goes to 0%, the rules are
swallowing real regressions.

## Types covered

dates, timestamps, phone numbers, prices, email addresses, numbers, links,
typed-in text (input values), custom text (order/build/session/batch ids).

## Two variants

Every page exists as `-1` and `-2`. Only the **values** differ. Layout, wording,
headings, static control block and footer are byte-identical, and the variant
number appears only in `<title>`, which is not captured. So any diff Percy
reports outside the dynamic values is a bug in the ignore rules.

Each page also carries a **static control block**. A diff reported inside that
block means an ignore rule has over-matched.

## Capturing

```
export PERCY_TOKEN=<project token>
npx percy snapshot snapshots-variant-1.yml   # baselines
npx percy snapshot snapshots-variant-2.yml   # changed values
```

Snapshot names are identical across the two files, so variant 2 compares against
the variant 1 baseline of the same name.

| Page | | |
|---|---|---|
| 01 Mixed - Account dashboard | [variant 1](mixed-dashboard-1.html) | [variant 2](mixed-dashboard-2.html) |
| 02 Mixed - Invoice | [variant 1](mixed-invoice-1.html) | [variant 2](mixed-invoice-2.html) |
| 03 Mixed - User profile | [variant 1](mixed-profile-1.html) | [variant 2](mixed-profile-2.html) |
| 04 Mixed - Build report | [variant 1](mixed-report-1.html) | [variant 2](mixed-report-2.html) |
| 05 Mixed - Activity feed | [variant 1](mixed-feed-1.html) | [variant 2](mixed-feed-2.html) |
| 06 Focus - Dates, timestamps, phones | [variant 1](focus-dates-timestamps-phones-1.html) | [variant 2](focus-dates-timestamps-phones-2.html) |
| 07 Focus - Prices and numbers | [variant 1](focus-prices-numbers-1.html) | [variant 2](focus-prices-numbers-2.html) |
| 08 Focus - Emails and links | [variant 1](focus-emails-links-1.html) | [variant 2](focus-emails-links-2.html) |
| 09 Focus - Typed-in and custom text | [variant 1](focus-typed-custom-1.html) | [variant 2](focus-typed-custom-2.html) |
| 10 Negative control | [variant 1](negative-control-1.html) | [variant 2](negative-control-2.html) |

No JavaScript, no external assets, no network calls.
