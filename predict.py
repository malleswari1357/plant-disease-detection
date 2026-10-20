import tensorflow as tf
import numpy as np
from PIL import Image
from recommendations import get_recommendation

# Load the trained model
model = tf.keras.models.load_model("model/plant_disease_model.keras")

# Load class names
with open("model/class_names.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# Path of the test leaf image
image_path = "test_images/leaf.jpg"

# Open the image
image = Image.open(image_path).convert("RGB")

# Resize image
image = image.resize((224, 224))

# Convert image into an array
image_array = np.array(image)

# Add batch dimension
image_array = np.expand_dims(image_array, axis=0)

# Make prediction
prediction = model.predict(image_array)

# Find predicted class
predicted_index = np.argmax(prediction[0])
predicted_class = class_names[predicted_index]

# Get confidence
confidence = prediction[0][predicted_index] * 100

# Get recommendation
result = get_recommendation(predicted_class)

# Display result
print()
print("======================================")
print("     🌱 PLANT DISEASE DETECTION")
print("======================================")
print()

print("Disease detected :", result["disease"])
print("Confidence       :", round(confidence, 2), "%")
print("Cause            :", result["cause"])

print()
print("💡 RECOMMENDATIONS")
print("--------------------------------------")

for item in result["recommendation"]:
    print("•", item)

print()
print("======================================")