import joblib
import nltk



def predict_class_level(text):
    tokens = nltk.word_tokenize(text)
    preprocessed_text = " ".join(tokens)
    loaded_classifier = joblib.load('text_classifier_model.joblib')
    loaded_vectorizer = joblib.load('text_vectorizer.joblib')
    input_vector = loaded_vectorizer.transform([preprocessed_text])
    predicted_security_level = loaded_classifier.predict(input_vector)
    print(predicted_security_level)