import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from model import load_data, train_model, predict_delay


st.set_page_config(page_title="Flight Delay Predictor")

st.title("Flight Delay Prediction")

# Load dataset
df = load_data()

# Train model
model = train_model(df)

# Sidebar input
distance = st.sidebar.slider(
    "Distance (km)",
    int(df.distance_km.min()),
    int(df.distance_km.max()),
    1500
)

# Prediction
delay = predict_delay(model, distance)

st.subheader("Predicted Arrival Delay")

st.success(f"{delay:.2f} minutes")

# Visualization
st.subheader("Distance vs Arrival Delay")

fig, ax = plt.subplots()

ax.scatter(df["distance_km"], df["arrival_delay_min"], alpha=0.5)

x_range = np.linspace(df.distance_km.min(), df.distance_km.max(), 100)

y_range = model.predict(
    x_range.reshape(-1,1)
)

ax.plot(x_range, y_range)

ax.set_xlabel("Distance (km)")
ax.set_ylabel("Arrival Delay (minutes)")

st.pyplot(fig)