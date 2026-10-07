# Percy dynamic text ignore fixtures

Five production style pages for testing project level dynamic text intelli-ignore
(PPLT-6174 / PPLT-6133). Captured at **375 and 1280**.

Live: https://aryanmittal-bs.github.io/percy-dynamic-text-ignore-test/

| Snapshot | Page | Dynamic text it carries |
|---|---|---|
| 01 Northwind billing invoice | SaaS billing | prices, dates, email, phone, account id, counts, percentage, links |
| 02 Hallow and Co order confirmation | Ecommerce | order id, prices, delivery dates, time, tracking number, phone, email, typed search |
| 03 Meridian Air itinerary | Airline booking | dates, times, durations, flight numbers, fares, booking ref, ticket no, email, phone |
| 04 Pulse analytics overview | Metrics dashboard | counts, percentages, revenue, timestamps, date range, emails, run id, typed report name |
| 05 Relay helpdesk ticket | Support CRM | ticket id, SLA duration, timestamps, emails, phone, typed reply, order/build/session ids |

Between them the nine categories are all covered: dates, timestamps, phone
numbers, prices, email addresses, numbers, links, typed in text, custom text.

## Two variants

Every page exists as `-1` and `-2`. **Only the values differ.** Layout, copy,
labels, chart bar heights and the static control block are byte identical, and
the variant number appears only in `<title>`, which is not captured. So any diff
Percy reports outside the dynamic values is a bug in the ignore rules.

Each page carries a **static control block**. A diff reported inside that block
means a rule has over matched onto text it should not touch.

## Capturing

```
export PERCY_TOKEN=<project token>
npx percy snapshot snapshots-variant-1.yml   # baseline, approve it
npx percy snapshot snapshots-variant-2.yml   # changed values
```

Snapshot names are identical across the two files, so variant 2 compares against
the variant 1 baseline of the same name.

Static HTML only. No JavaScript, no external fonts, scripts, images or network calls.
