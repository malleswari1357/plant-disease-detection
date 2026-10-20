import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2

# Dataset location
dataset_path = "dataset/PlantVillage"

# Image settings
IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Load training data
train_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Load validation data
validation_dataset = tf.keras.utils.image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

# Get class names
class_names = train_dataset.class_names
print("Classes:", class_names)

# Improve performance
AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.prefetch(buffer_size=AUTOTUNE)
validation_dataset = validation_dataset.prefetch(buffer_size=AUTOTUNE)

# Load MobileNetV2
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze the existing model
base_model.trainable = False

# Create our model
model = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Rescaling(1.0 / 127.5, offset=-1),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),
    layers.Dense(len(class_names), activation="softmax")
])

# Compile model
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Save the best model during training
checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "model/plant_disease_model.keras",
    save_best_only=True,
    monitor="val_accuracy",
    mode="max"
)

# Train
history = model.fit(
    train_dataset,
    validation_data=validation_dataset,
    epochs=10,
    callbacks=[checkpoint]
)

# Save final model
model.save("model/plant_disease_model.keras")

# Save class names
with open("model/class_names.txt", "w") as f:
    for name in class_names:
        f.write(name + "\n")

print("Training completed!")
print("Model saved successfully.")