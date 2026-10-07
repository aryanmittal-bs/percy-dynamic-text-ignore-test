# Percy dynamic-text ignore test pages

Static fixtures for **PPLT-6133 / PPLT-6174** — dynamic text intelli-ignore at project level.

Live: https://aryanmittal-bs.github.io/percy-dynamic-text-ignore-test/

## How it works

Every page exists in two variants. Between variant 1 and variant 2 **only the dynamic
values change** — layout, wording, fonts and the static control block are identical.

So for each rule:

- rule **ON**  → the comparison should be **0% diff**
- rule **OFF** → the same comparison should be **flagged**

That difference is the whole test. One page per category, so a rule can be proven in
isolation without another category's values muddying the result.

## Pages

| Page | Covers |
|---|---|
| `dates` | long form, numeric slash, ISO, month-name-first, short year, weekday |
| `timestamps` | duration, 24h, 12h, with seconds, milliseconds |
| `phone-numbers` | US bracketed/dashed/dotted, international, India mobile |
| `prices` | USD, EUR, GBP, INR, JPY, negative |
| `email-addresses` | simple, dotted, plus-addressed, subdomain, long local part |
| `numbers` | result counts, integers, decimals, percentages, grouped, ranges |
| `links` | bare path, full scheme, query string, docs link, deep path |
| `typed-in-text` | values inside real `<input>` fields |
| `custom-text` | order ids, build ids, ticket refs, tokens, batch labels (for regex rules) |
| `mixed-all-types` | several categories on one page, for testing rules together |
| `negative-control` | a **genuine** visual change next to a dynamic value |

### The negative control matters

`negative-control` changes a badge's colour and wording between variants. With every
rule switched on, Percy **must still flag it**. If that page ever reports 0%, the ignore
rules are swallowing real changes — which is the failure mode worth catching.

## Capturing

```bash
export PERCY_TOKEN=<project write token>

# baseline
npx percy snapshot snapshots-variant-1.yml

# then the comparison, same snapshot names
npx percy snapshot snapshots-variant-2.yml
```

No JavaScript and no external assets, so captures are deterministic.
