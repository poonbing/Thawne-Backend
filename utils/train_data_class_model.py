import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from utils.example_data import example_data, file_data
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
import random


nltk.download('stopwords')
nltk.download('punkt')
vectorizer = CountVectorizer()
classifier = MultinomialNB()

def preprocess_text_samples(text_samples):
    preprocessed_texts = [preprocess_text(text) for text in text_samples]
    return preprocessed_texts

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text.replace('_',' '))
    tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

def shuffle_dictionary(dictionary):
    shuffled_keys = list(dictionary.keys())
    random.shuffle(shuffled_keys)
    shuffled_dict = {key: dictionary[key] for key in shuffled_keys}
    return shuffled_dict


text_samples = list(example_data.keys())
security_levels = list(example_data.values())
X_train, X_test, y_train, y_test = train_test_split(
    text_samples, security_levels, test_size=0.2, random_state=42, shuffle=True, stratify=security_levels
)
X_train_preprocessed = preprocess_text_samples(X_train)
X_test_preprocessed = preprocess_text_samples(X_test)
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train_preprocessed)
X_test_vectorized = vectorizer.transform(X_test_preprocessed)
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)
y_pred = classifier.predict(X_test_vectorized)
joblib.dump(classifier, 'text_classifier_model.joblib')
joblib.dump(vectorizer, 'text_vectorizer.joblib')
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='weighted', zero_division=0))
print("Recall:", recall_score(y_test, y_pred, average='weighted', zero_division=0))
print("F1 Score:", f1_score(y_test, y_pred, average='weighted', zero_division=0))

file_data = shuffle_dictionary(file_data)

text_samples = list(file_data.keys())
security_levels = list(file_data.values())
X_train, X_test, y_train, y_test = train_test_split(
    text_samples, security_levels, test_size=0.2, random_state=42, shuffle=True, stratify=security_levels
)
X_train_preprocessed = preprocess_text_samples(X_train)
X_test_preprocessed = preprocess_text_samples(X_test)
vectorizer = CountVectorizer()
X_train_vectorized = vectorizer.fit_transform(X_train_preprocessed)
X_test_vectorized = vectorizer.transform(X_test_preprocessed)
classifier = MultinomialNB()
classifier.fit(X_train_vectorized, y_train)
y_pred = classifier.predict(X_test_vectorized)
joblib.dump(classifier, 'filename_classifier_model.joblib')
joblib.dump(vectorizer, 'filename_vectorizer.joblib')
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average='weighted', zero_division=0))
print("Recall:", recall_score(y_test, y_pred, average='weighted', zero_division=0))
print("F1 Score:", f1_score(y_test, y_pred, average='weighted', zero_division=0))