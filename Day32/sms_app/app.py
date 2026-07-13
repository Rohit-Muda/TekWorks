import os
import pickle
import re
from pathlib import Path

import pandas as pd
import streamlit as st
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "spam_model.keras"
TOKENIZER_PATH = BASE_DIR / "tokenizer.pkl"
DATASET_PATH = BASE_DIR / "spam.csv"

MAX_WORDS = 5000
MAX_LEN = 50


@st.cache_resource
def load_saved_model():
    return load_model(MODEL_PATH)


@st.cache_resource
def load_saved_tokenizer():
    with TOKENIZER_PATH.open("rb") as file:
        return pickle.load(file)


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def train_model():
    df = pd.read_csv(DATASET_PATH, encoding="latin-1")
    df = df[["v1", "v2"]]
    df.columns = ["label", "text"]
    df["label"] = df["label"].map({"ham": 0, "spam": 1})
    df["text"] = df["text"].apply(clean_text)

    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(df["text"])
    sequences = tokenizer.texts_to_sequences(df["text"])
    x = pad_sequences(sequences, maxlen=MAX_LEN, padding="post")
    y = df["label"]

    with TOKENIZER_PATH.open("wb") as file:
        pickle.dump(tokenizer, file)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    model = Sequential(
        [
            Embedding(input_dim=MAX_WORDS, output_dim=128, input_length=MAX_LEN),
            SimpleRNN(128),
            Dense(32, activation="relu"),
            Dense(1, activation="sigmoid"),
        ]
    )

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(x_train, y_train, validation_split=0.2, epochs=25, batch_size=32, verbose=0)
    model.save(MODEL_PATH)

    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    predictions = (model.predict(x_test, verbose=0) > 0.5).astype(int)

    return {
        "accuracy": accuracy,
        "loss": loss,
        "classification_report": classification_report(y_test, predictions),
        "confusion_matrix": confusion_matrix(y_test, predictions),
    }


def predict_sms(message):
    model = load_saved_model()
    tokenizer = load_saved_tokenizer()
    message = clean_text(message)
    sequence = tokenizer.texts_to_sequences([message])
    sequence = pad_sequences(sequence, maxlen=MAX_LEN, padding="post")
    probability = model.predict(sequence, verbose=0)[0][0]
    if probability > 0.5:
        return "spam", probability
    return "ham", 1 - probability


st.set_page_config(page_title="SMS Spam Detection", page_icon="📩", layout="centered")
st.title("SMS Spam Detection using RNN")
st.write("Many-to-One RNN")

if not DATASET_PATH.exists():
    st.error(f"Dataset not found at {DATASET_PATH}")
    st.stop()

if not MODEL_PATH.exists():
    st.warning("Model not found. Training a new spam classifier...")
    with st.spinner("Training model. Please wait..."):
        train_stats = train_model()
    st.success("Training completed!")
else:
    train_stats = None

message = st.text_area("Enter SMS message")
if st.button("Predict"):
    if not message.strip():
        st.warning("Please enter a message.")
    else:
        prediction, probability = predict_sms(message)
        if prediction == "spam":
            st.error("Prediction: SPAM 🚨")
        else:
            st.success("Prediction: HAM ✅")
        st.write("Confidence:", round(probability * 100, 2), "%")

if train_stats is not None:
    st.subheader("Training Summary")
    st.write(f"Accuracy: {train_stats['accuracy']:.2%}")
    st.text(train_stats["classification_report"])
    st.text(str(train_stats["confusion_matrix"]))
