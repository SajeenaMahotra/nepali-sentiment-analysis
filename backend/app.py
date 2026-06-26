from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

app = Flask(__name__)
CORS(app)

# Load models and vectorizer
vectorizer = joblib.load('../models/tfidf_vectorizer.pkl')
models = {
    'logistic_regression': joblib.load('../models/logistic_regression_model.pkl'),
    'svm': joblib.load('../models/svm_model.pkl'),
    'naive_bayes': joblib.load('../models/naive_bayes_model.pkl'),
}

NEPALI_STOPWORDS = [
    "cha", "chha", "chan", "chu", "tha", "thiyo", "ho", "hola", "hoina",
    "ni", "nai", "pani", "lai", "le", "ma", "ko", "ka", "ki", "ra", "ta",
    "tara", "ani", "yo", "tyo", "yो", "k", "ki", "kasari", "kina", "kun",
    "aba", "aaba", "ali", "ekdam", "dherai", "thikai", "bilkul", "purai",
    "gardai", "garxa", "garcha", "bhayo", "bhanne", "bhako", "gareko",
    "garne", "garnu", "dinu", "linu", "aunu", "jaanu", "basnu", "hunxa",
    "huxa", "huncha", "bhayena", "nagarne", "nagareko", "nabhako"
]

english_stopwords = set(stopwords.words('english'))
all_stopwords = english_stopwords.union(set(NEPALI_STOPWORDS))

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in all_stopwords]
    return ' '.join(tokens)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')
    model_name = data.get('model', 'logistic_regression')

    if not text.strip():
        return jsonify({'error': 'Empty text'}), 400

    if model_name not in models:
        return jsonify({'error': 'Invalid model'}), 400

    cleaned = preprocess(text)
    vectorized = vectorizer.transform([cleaned])
    prediction = models[model_name].predict(vectorized)[0]
    
    # LinearSVC doesn't support predict_proba
    if hasattr(models[model_name], 'predict_proba'):
        proba = models[model_name].predict_proba(vectorized)[0].tolist()
        classes = models[model_name].classes_.tolist()
        probabilities = dict(zip(classes, proba))
    else:
        # For LinearSVC, use decision function scores instead
        scores = models[model_name].decision_function(vectorized)[0].tolist()
        classes = models[model_name].classes_.tolist()
        probabilities = dict(zip(classes, scores))

    return jsonify({
        'sentiment': prediction,
        'probabilities': probabilities,
        'cleaned_text': cleaned
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)