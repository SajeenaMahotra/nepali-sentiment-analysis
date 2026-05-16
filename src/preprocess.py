import re
import pandas as pd

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

def preprocess_text(text):
    text = lowercase_text(text)
    text = remove_emojis(text)
    text = remove_urls(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_extra_whitespace(text)
    return text
