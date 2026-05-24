import re
import nltk
import pandas as pd
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

english_stopwords = set(stopwords.words("english"))

nepali_roman_stopwords = {
    "cha", "chha", "thiyo", "ho", "hola", "bhayo", "garcha", "gareko",
    "huncha", "huna", "hunna", "bhayena", "rahecha", "raicha", "raheko",
    "ma", "ko", "ka", "ki", "lai", "bata", "sanga", "le", "pani",
    "ra", "ani", "tara", "ta", "ni", "nai", "chai", "mero", "timro",
    "usko", "hamro", "yo", "tyo", "uni", "hami", "tapai", "tapain",
    "hai", "la", "na", "ne", "nah", "yaar", "aba", "ali", "pachi",
}

all_stopwords = english_stopwords.union(nepali_roman_stopwords)

def lowercase_text(text):
    if pd.isna(text):
        return ""
    return str(text).lower()

def remove_emojis(text):
    return re.sub(r"[^\x00-\x7F]+", " ", text)

def remove_urls(text):
    return re.sub(r"http\S+|www\.\S+", "", text)

def remove_punctuation(text):
    return re.sub(r"[^\w\s]", " ", text)

def remove_numbers(text):
    return re.sub(r"\b\d+\b", "", text)

def remove_extra_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()

def remove_stopwords(text):
    tokens = text.split()
    filtered = [word for word in tokens if word not in all_stopwords]
    return " ".join(filtered)

def preprocess_text(text):
    text = lowercase_text(text)
    text = remove_emojis(text)
    text = remove_urls(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_extra_whitespace(text)
    text = remove_stopwords(text)
    return text
