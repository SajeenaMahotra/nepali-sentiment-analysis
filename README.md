# Sentiment Analysis of Code-Mixed Nepali-English Product Reviews

A machine learning system that classifies sentiment in Romanized Nepali-English ("Nepanglish") product reviews collected from Daraz Nepal. Built as an undergraduate thesis project at Softwarica College of IT and E-Commerce, in affiliation with Coventry University.

**Live demo:** https://nepali-sentiment-analysis.vercel.app/

## Overview

Reviews on Nepali e-commerce platforms are rarely written in clean, standard English. They mix Nepali and English mid-sentence, for example "yo product ekdam ramro cha but delivery slow thiyo." General sentiment analysis tools, built for monolingual English, are not designed to handle this kind of code-mixed text, and Nepali remains a low-resource language with little annotated data or tooling to fall back on.

This project builds and evaluates a sentiment classification pipeline on 4,343 real customer reviews scraped directly from Daraz Nepal, comparing three traditional machine learning classifiers trained on TF-IDF features:

| Model | Macro F1 |
|---|---|
| Logistic Regression | 0.65 |
| Support Vector Machine | 0.64 |
| Naive Bayes | 0.56 |

Sentiment labels were derived through weak labeling based on star ratings (4-5 stars as positive, 3 stars as neutral, 1-2 stars as negative), with a manual spot check used to assess label reliability. Positive and negative labels were found to be reliable, while only around 40 to 50 percent of neutral-labeled reviews were genuinely neutral in the text itself. This limitation is documented rather than hidden throughout the project.

## Features

- Custom preprocessing pipeline for Romanized Nepali-English text, including a hand-built list of roughly 247 Romanized Nepali stopwords
- TF-IDF feature extraction (unigrams and bigrams, min document frequency of 2, sublinear term frequency scaling)
- Three trained classifiers served together so predictions can be compared side by side
- Full-stack web application for live predictions
- Fully documented, reproducible notebook pipeline from data collection through evaluation

## Tech Stack

**Backend:** Flask, scikit-learn, joblib, deployed on Render
**Frontend:** Next.js, TypeScript, Tailwind CSS, shadcn/ui, deployed on Vercel
**Modeling and data processing:** Python, pandas, NumPy, scikit-learn, NLTK, Requests

## Project Structure

```
.
├── backend/               # Flask API serving the trained models
│   ├── app.py
│   └── requirements.txt
├── frontend/               # Next.js + TypeScript web app
│   └── src/
├── data/                   # Raw and processed review data
├── models/                 # Saved model artifacts (joblib)
├── notebooks/               # End-to-end pipeline, run in order
│   ├── 00_data_collection.ipynb
│   ├── 01_EDA.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_feature_extraction.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_test_evaluation.ipynb
├── src/                     # Reusable pipeline modules
│   ├── preprocess.py
│   ├── features.py
│   ├── models.py
│   └── evaluate.py
├── results/                 # Classification reports and generated plots
└── requirements.txt
```

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Notebooks

Run the notebooks in `notebooks/` in numerical order (00 through 05) to reproduce the full pipeline from data collection to evaluation.

## Known Limitations

- Neutral-class labels carry documented noise, since a 3-star rating does not always correspond to genuinely neutral review text.
- Nepali morphological negation (for example "chaina" or "thiyena," where negation is fused into the verb rather than expressed as a separate word) is not well captured by the current bigram-based features, and reviews using this pattern are more prone to misclassification.
- The dataset is drawn from a single platform, so results may not generalize to other Nepali marketplaces without further testing.
- The models are academic and exploratory, and are not intended for production or commercial deployment without further validation.

## Ethical Considerations

All data was collected from publicly visible Daraz Nepal review pages through the platform's own review API, with no login or access-control bypass involved. Only review text, star rating, and posting date were retained. Where display names appeared in the raw data, they were discarded and never used in the modeling or reporting process. Full ethical reasoning and a documented label-reliability check are included in the accompanying thesis.

## Author

Sajeena Mahotra

## License

This project is academic and non-commercial in nature. Please reach out before reusing the dataset or models for any other purpose.
