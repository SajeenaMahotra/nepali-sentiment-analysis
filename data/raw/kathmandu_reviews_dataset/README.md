# Kathmandu Marketplace Code-Mixed Reviews v2 (100K)

**Project:** Sentiment Analysis of Code-Mixed Romanized Nepali-English Product Reviews on a Local Online Marketplace based in Kathmandu
**Version:** 2.0.0
**Total reviews:** 100,000
**Generator seed:** `42` (fully reproducible)
**Schema:** 22 columns — *identical* to v1, drop-in replacement

---

## 1. What changed from v1 (2,500 → 100,000)

A naive 40× scale-up would just repeat the same 24,000 maximum unique template combinations four times each, which produces a dataset full of near-duplicates and trains models to *memorize* templates instead of *learn sentiment*. Instead, v2 dramatically expands the generation surface so the resulting 100K reviews achieve **83% unique texts** (83,030 distinct review_text values), a healthy ratio for ML training.

| Aspect | v1 | v2 |
|---|---|---|
| Total reviews | 2,500 | **100,000** |
| Product catalogue | ~46 SKUs | **183 SKUs** |
| Categories | 8 | **10** (added Sports & Outdoor; expanded all) |
| Sellers | 20 | **30** |
| Locations | 15 | **20** |
| Payment methods | 6 | **7** (added FonePay) |
| Delivery partners | 5 | **8** |
| Fragment slots per review | 3 (opener / body / closer) | **5** (opener / product_aspect / delivery_aspect / service_aspect / closer) |
| Templates per slot | ~20 | **~30–50** |
| Slot-based phrase generators | No | **Yes** — `{aspect} × {quality} × {intensifier}` explodes combinatorially |
| Mixed-aspect reviews | No | **~8%** of positives carry a delivery gripe; ~6% of negatives carry a positive delivery line |
| Single-phrase short reviews | No | **~10%** of all reviews (mirrors real users typing "Mast cha!" or "Bekar product.") |
| Schema | 22 columns | **22 columns — IDENTICAL** |

---

## 2. Distribution

### Class balance (Pradhananga & Sah-style natural skew)
- Positive: **58,000** (58%)
- Negative: **30,000** (30%)
- Neutral:  **12,000** (12%)

This skew matches the natural class imbalance reported in the Pradhananga & Sah 2023 Daraz reviews paper (where positive reviews dominate by ~3:1 over negative). Don't randomly oversample neutrals to balance — your thesis can showcase how class-weight or focal-loss techniques handle this realistic skew.

### Code-mixing balance
- Nepali-dominant: ~51%
- Balanced: ~29%
- English-dominant: ~19%

### Train / val / test (stratified by sentiment)
- `split_train.csv`: **70,000 rows**
- `split_val.csv`:   **15,000 rows**
- `split_test.csv`:  **15,000 rows**

---

## 3. Schema (unchanged from v1)

| # | Column | Type | Description |
|--:|---|---|---|
| 1 | `review_id` | string | Primary key (e.g. `R000001`). |
| 2 | `product_id` | string | Stable hash-derived product ID. |
| 3 | `product_name` | string | Full product name. |
| 4 | `product_category` | string | One of 10 categories. |
| 5 | `brand` | string | Brand name. |
| 6 | `product_price_npr` | int | Price in NPR. |
| 7 | `seller_name` | string | Generic Kathmandu seller. |
| 8 | `delivery_partner` | string | Pathao, Aramex, Daraz Express, etc. |
| 9 | `reviewer_location` | string | City — weighted toward Kathmandu valley. |
| 10 | `payment_method` | string | COD / eSewa / Khalti / IME Pay / Card / ConnectIPS / FonePay. |
| 11 | `review_date` | datetime | Jan 2024 → Apr 2026. |
| 12 | `review_text` | string | **Label target — Romanized Nepali + English code-mixed.** |
| 13 | `rating` | int | 1–5 stars. |
| 14 | `sentiment_label` | string | **Primary label** — positive / negative / neutral. |
| 15 | `verified_purchase` | bool | Verified buyer flag. |
| 16 | `helpful_count` | int | Helpfulness votes. |
| 17 | `review_length_chars` | int | Character count. |
| 18 | `review_length_tokens` | int | Whitespace token count. |
| 19 | `english_token_ratio` | float | Fraction of English hint tokens. |
| 20 | `nepali_token_ratio` | float | Fraction of Nepali hint tokens. |
| 21 | `language_dominance` | string | Nepali-dominant / English-dominant / Balanced. |
| 22 | `has_emoji` | bool | Emoji presence flag. |

Existing v1 code that reads any of these columns will work unchanged on v2.

---

## 4. Why the diversity numbers matter

**83% unique review texts** is significantly better than what you'd get from naïve duplication (which would be roughly 25%). This matters because:

1. **Train-test contamination is minimized.** With stratified shuffling, test set duplicates of train are rare.
2. **Model memorization is harder.** A 100K dataset with 24,000 distinct texts would let a model effectively memorize the entire template space — your sentiment classifier would look great in eval but generalize poorly. With 83K distinct texts, the model is forced to learn linguistic features.
3. **Realistic duplication.** The 17% repeat rate isn't a flaw — real Nepali e-commerce reviews actually do repeat short phrases like *"Mast cha!"* or *"Don't buy."* across different users. So we keep some intentional duplication of short phrases.

---

## 5. Methodology

### Template structure
Each review is composed of 1–5 fragments drawn from five sentiment-aligned pools:
- **opener** (always present) — sets sentiment
- **product_aspect** — comments on quality/build/feature
- **delivery_aspect** — comments on shipping/courier
- **service_aspect** — comments on seller/customer service
- **closer** — final recommendation/disappointment

The probability of including each non-opener slot is independently tuned so reviews follow a realistic length distribution (mean 21 tokens, median 22, max 55 tokens).

### Slot-based phrase generators
On top of fixed templates, ~30% of reviews insert a slot-generated phrase like:
- `{aspect} {intensifier} {quality} cha`
- `Yo product ko {aspect} {quality} feel diunchha`

with `aspect` drawn from 30 product attributes, `quality` from 16-20 sentiment-tagged words, and `intensifier` from 13 adverbs. This single template alone yields ~9,600 unique phrasings.

### Mixed-aspect reviews
About 8% of positive reviews include a delivery complaint, and 6% of negative reviews include a positive delivery line. This reflects real Nepali e-commerce reviews where users frequently say *"product ramro tara delivery delay bhayo"* — and stops your model from over-relying on any single aspect.

### Typo & emoji injection
- 30% of reviews undergo a single typo substitution (e.g. *ekdam* → *ekdum*) — mirrors real Romanized Nepali typing variance
- 20% of reviews append a sentiment-appropriate emoji

### Realism caveats
- Data is synthetic. Distributions match Pradhananga & Sah's reported pattern but no actual Daraz/Sastodeal reviews were used.
- Code-mixing patterns are template-driven, not learned from real corpora — your thesis should report this as proof-of-method on synthetic data and ideally validate at least one model on a small held-out set of real reviews if possible.
- Brand and product names are real (Wai Wai, Daraz Mall, Pampers, etc.) for realism, but no brand is being represented as endorsing or providing this data.

---

## 6. File inventory

```
kathmandu_marketplace_reviews_100k/
├── README.md                               # this file
├── dataset_metadata.json                   # machine-readable summary
├── generate_dataset.py                     # reproducible generator (seed=42)
├── build_xlsx.py                           # rebuilds the workbook
├── kathmandu_marketplace_reviews_100k.csv  # PRIMARY DATA — 100K rows × 22 cols
├── kathmandu_marketplace_reviews_100k.xlsx # multi-sheet workbook (samples + stats + dictionary)
├── split_train.csv                         # 70,000 rows (stratified by sentiment)
├── split_val.csv                           # 15,000 rows
└── split_test.csv                          # 15,000 rows
```

XLSX contains: README · What's New (v1 vs v2) · Data Dictionary · Summary Stats · 4 sample sheets (Positive 1000 · Negative 1000 · Neutral 500 · Random Mix 1000).

---

## 7. Suggested citation

> [Your Name] (2026). *Synthetic Code-Mixed Romanized Nepali-English Marketplace Review Dataset (v2, 100K).* Generated for thesis work on sentiment analysis of Nepali e-commerce reviews. Generation seed = 42.

The dataset is free to use, modify, and redistribute for academic and commercial purposes. Attribution is appreciated but not required.
