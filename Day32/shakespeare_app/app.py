import os
import pickle
from pathlib import Path

import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, Embedding, Input, SimpleRNN
from tensorflow.keras.models import Sequential, load_model

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "char_rnn_many_to_many.keras"
VOCAB_PATH = BASE_DIR / "char_vocab.pkl"
DATASET_PATH = BASE_DIR / "tiny-shakespeare.txt"

SEQ_LEN = 80
STEP_SIZE = 3
EMBED_DIM = 64
RNN_UNITS = 128
BATCH_SIZE = 64
EPOCHS = 8
TRAIN_SPLIT = 0.9


@st.cache_resource
def load_saved_model():
    return load_model(MODEL_PATH)


@st.cache_resource
def load_saved_vocab():
    with VOCAB_PATH.open("rb") as file:
        return pickle.load(file)


def load_text():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return file.read()


def build_vocabulary(text):
    characters = sorted(set(text))
    char_to_idx = {char: index for index, char in enumerate(characters)}
    idx_to_char = characters
    return char_to_idx, idx_to_char


def encode_text(text, char_to_idx):
    return np.array([char_to_idx[char] for char in text], dtype=np.int32)


def split_input_target(chunk):
    return chunk[:, :-1], chunk[:, 1:]


def make_sequence_dataset(encoded_text, shuffle):
    if len(encoded_text) <= SEQ_LEN + 1:
        raise ValueError("Dataset is too short for the configured sequence length.")

    dataset = tf.keras.utils.timeseries_dataset_from_array(
        data=encoded_text,
        targets=None,
        sequence_length=SEQ_LEN + 1,
        sequence_stride=STEP_SIZE,
        sampling_rate=1,
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
    )

    dataset = dataset.map(split_input_target, num_parallel_calls=tf.data.AUTOTUNE)
    return dataset.prefetch(tf.data.AUTOTUNE)


def build_model(vocab_size):
    model = Sequential(
        [
            Input(shape=(SEQ_LEN,)),
            Embedding(input_dim=vocab_size, output_dim=EMBED_DIM),
            SimpleRNN(RNN_UNITS, return_sequences=True),
            Dense(vocab_size, activation="softmax"),
        ]
    )

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def train_model():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"{DATASET_PATH} was not found.")

    text = load_text()
    char_to_idx, idx_to_char = build_vocabulary(text)
    encoded_text = encode_text(text, char_to_idx)

    split_index = int(len(encoded_text) * TRAIN_SPLIT)
    train_encoded = encoded_text[:split_index]
    val_encoded = encoded_text[split_index:]

    train_dataset = make_sequence_dataset(train_encoded, shuffle=True)
    val_dataset = make_sequence_dataset(val_encoded, shuffle=False)

    with VOCAB_PATH.open("wb") as file:
        pickle.dump(
            {
                "char_to_idx": char_to_idx,
                "idx_to_char": idx_to_char,
                "vocab_size": len(idx_to_char),
            },
            file,
        )

    model = build_model(len(idx_to_char))
    callbacks = [EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True)]

    history = model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1,
    )

    model.save(MODEL_PATH)
    validation_loss, validation_accuracy = model.evaluate(val_dataset, verbose=0)

    load_saved_model.clear()
    load_saved_vocab.clear()

    return {
        "history": history.history,
        "validation_loss": validation_loss,
        "validation_accuracy": validation_accuracy,
        "vocab_size": len(idx_to_char),
        "dataset_size": len(encoded_text),
    }


def sample_next_index(probabilities, temperature):
    probabilities = np.asarray(probabilities).astype("float64")
    probabilities = np.maximum(probabilities, 1e-8)

    scaled = np.log(probabilities) / max(temperature, 0.1)
    scaled = np.exp(scaled - np.max(scaled))
    scaled = scaled / np.sum(scaled)

    return int(np.random.choice(len(scaled), p=scaled))


def generate_text(seed_text, length, temperature):
    model = load_saved_model()
    vocab = load_saved_vocab()

    char_to_idx = vocab["char_to_idx"]
    idx_to_char = vocab["idx_to_char"]
    pad_index = char_to_idx.get(" ", 0)

    if not seed_text:
        seed_text = "ROMEO:\n"

    generated_indices = [char_to_idx.get(char, pad_index) for char in seed_text]

    for _ in range(length):
        window = generated_indices[-SEQ_LEN:]
        padded = np.full((SEQ_LEN,), pad_index, dtype=np.int32)
        padded[-len(window):] = window
        predictions = model.predict(padded[np.newaxis, :], verbose=0)
        next_index = sample_next_index(predictions[0, -1], temperature)
        generated_indices.append(next_index)

    return "".join(idx_to_char[index] for index in generated_indices)


st.set_page_config(page_title="Shakespeare Character Generator", page_icon="🎭", layout="centered")
st.title("Character-Level Text Generation using RNN")
st.write("Many-to-Many RNN")
st.caption("The model learns a next-character sequence at every time step.")

if not DATASET_PATH.exists():
    st.error(f"Dataset not found at {DATASET_PATH}")
    st.stop()

training_stats = None

if not MODEL_PATH.exists() or not VOCAB_PATH.exists():
    st.warning("Saved model not found. Training a new many-to-many RNN...")
    with st.spinner("Training model. Please wait..."):
        training_stats = train_model()
    st.success("Training completed!")

st.subheader("Generate Text")
seed_text = st.text_area("Enter seed text", value="ROMEO:\n", height=180)
generation_length = st.slider("Characters to generate", min_value=50, max_value=500, value=250, step=25)
temperature = st.slider("Temperature", min_value=0.2, max_value=1.5, value=0.8, step=0.1)

if st.button("Generate"):
    generated_text = generate_text(seed_text=seed_text, length=generation_length, temperature=temperature)
    st.text_area("Generated output", value=generated_text, height=320)

if st.button("Retrain Model"):
    with st.spinner("Retraining model. Please wait..."):
        training_stats = train_model()
    st.success("Model retrained successfully!")

if training_stats is not None:
    st.info(
        "Vocabulary size: "
        f"{training_stats['vocab_size']} | Characters used: {training_stats['dataset_size']} | "
        f"Validation accuracy: {training_stats['validation_accuracy']:.2%}"
    )
