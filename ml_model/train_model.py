import json
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from preprocess import clean_text
# import pickle 

# Sample data format: [{"text": "leaked info here", "label": 1}, ...]
with open('ml_model/sample_data.json', 'r') as f:
    data = json.load(f)

texts = [clean_text(item['text']) for item in data]
# texts = [item['text'] for item in data]
labels = [item['label'] for item in data]

vectorizer = TfidfVectorizer(max_features=3000)
# vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

y = labels
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=500)
model = LogisticRegression()
model.fit(X_train, y_train)
# model.fit(X, labels)

# Save model and vectorizer
#with open('ml_model/vectorizer.pkl', 'wb') as f:
#   pickle.dump(vectorizer, f)
#with open('ml_model/model.pkl', 'wb') as f:
#    pickle.dump(model, f)
    
joblib.dump(model, 'ml_model/leak_predictor.pkl')
joblib.dump(vectorizer, 'ml_model/tfidf_vectorizer.pkl')

print(classification_report(y_test, model.predict(X_test)))
