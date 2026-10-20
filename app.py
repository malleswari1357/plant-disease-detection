import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
from recommendations import get_recommendation

# Gemini
from google import genai
from dotenv import load_dotenv
import os
import time


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Plant Disease Detection",
    page_icon="🌱",
    layout="centered"
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(".env", override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
else:
    gemini_client = None


# ============================================================
# LOAD PLANT DISEASE MODEL
# ============================================================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "model/plant_disease_model.keras"
    )


model = load_model()


# ============================================================
# LOAD IMAGE CHECKING MODEL
# ============================================================

@st.cache_resource
def load_image_checker():

    return tf.keras.applications.MobileNetV2(
        weights="imagenet"
    )


image_checker = load_image_checker()


# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open("model/class_names.txt", "r") as f:
    class_names = [
        line.strip()
        for line in f.readlines()
    ]


# ============================================================
# CHECK WHETHER IMAGE IS A PLANT/LEAF
# ============================================================

def is_plant_image(image):

    image_resized = image.resize((224, 224))
    image_array = np.array(image_resized)

    # Convert RGB to HSV
    hsv = tf.image.rgb_to_hsv(
        image_array / 255.0
    ).numpy()

    hue = hsv[:, :, 0]
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    # Detect green plant-like pixels
    green_mask = (
        (hue > 0.20)
        & (hue < 0.50)
        & (saturation > 0.15)
        & (value > 0.15)
    )

    green_percentage = (
        np.sum(green_mask)
        / green_mask.size
    ) * 100

    # If enough green pixels are present,
    # accept the image as a possible plant/leaf.
    if green_percentage >= 5:
        return True

    # Also use ImageNet as a secondary check
    image_for_model = tf.keras.applications.mobilenet_v2.preprocess_input(
        image_array.astype(np.float32)
    )

    image_for_model = np.expand_dims(
        image_for_model,
        axis=0
    )

    predictions = image_checker.predict(
        image_for_model,
        verbose=0
    )

    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(
        predictions,
        top=10
    )[0]

    plant_words = [
        "leaf",
        "plant",
        "flower",
        "tree",
        "vine",
        "fern",
        "vegetable",
        "fruit",
        "corn",
        "potato",
        "tomato",
        "pepper",
        "cucumber",
        "broccoli",
        "cabbage",
        "mushroom"
    ]

    for _, label, confidence in decoded:

        label = label.lower()

        for word in plant_words:

            if word in label and confidence >= 0.05:
                return True

    return False


# ============================================================
# ESTIMATE AFFECTED AREA
# ============================================================

def estimate_disease_area(image):

    image_array = np.array(
        image.resize((224, 224))
    )

    # Convert RGB → HSV
    hsv = tf.image.rgb_to_hsv(
        image_array / 255.0
    ).numpy()

    hue = hsv[:, :, 0]
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    # Approximate green leaf pixels
    green_mask = (
        (hue > 0.20)
        & (hue < 0.45)
        & (saturation > 0.20)
        & (value > 0.20)
    )

    # Approximate unhealthy/damaged pixels
    damaged_mask = (
        (
            ((hue > 0.03) & (hue < 0.15))
            & (saturation > 0.25)
        )
        |
        (
            (value < 0.35)
            & (saturation > 0.15)
        )
        |
        (
            (hue > 0.10)
            & (hue < 0.20)
            & (saturation > 0.30)
            & (value > 0.30)
        )
    )

    leaf_pixels = np.sum(green_mask)

    damaged_pixels = np.sum(
        damaged_mask & green_mask
    )

    if leaf_pixels == 0:
        return 0

    percentage = (
        damaged_pixels / leaf_pixels
    ) * 100

    percentage = max(
        0,
        min(100, percentage)
    )

    return percentage


# ============================================================
# SEVERITY
# ============================================================

def get_severity(percentage):

    if percentage < 10:
        return "Low"

    elif percentage < 30:
        return "Moderate"

    elif percentage < 60:
        return "High"

    else:
        return "Severe"


# ============================================================
# TITLE
# ============================================================

st.title(
    "🌱 AI-Based Plant Disease Detection"
)

st.write(
    "Upload a plant leaf image and the AI will "
    "detect the possible disease and provide "
    "management recommendations."
)

st.divider()


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📷 Upload a leaf image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# ============================================================
# DETECTION
# ============================================================

current_detection = None


if uploaded_file is not None:

    image = Image.open(
        uploaded_file
    ).convert("RGB")

    st.image(
        image,
        caption="Uploaded Image",
        width="stretch"
    )

    # --------------------------------------------------------
    # CHECK PLANT IMAGE
    # --------------------------------------------------------

    with st.spinner(
        "Checking whether this is a plant image..."
    ):

        plant_check = is_plant_image(
            image
        )

    if not plant_check:

        st.error(
            "❌ This does not appear to be a plant/leaf image."
        )

        st.info(
            "Please upload a clear photo of a plant leaf."
        )

        st.stop()

    # --------------------------------------------------------
    # DISEASE PREDICTION
    # --------------------------------------------------------

    resized_image = image.resize(
        (224, 224)
    )

    image_array = np.array(
        resized_image
    )

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    with st.spinner(
        "🔍 Detecting plant disease..."
    ):

        prediction = model.predict(
            image_array,
            verbose=0
        )

    predicted_index = np.argmax(
        prediction[0]
    )

    predicted_class = class_names[
        predicted_index
    ]

    confidence = (
        prediction[0][predicted_index]
        * 100
    )

    result = get_recommendation(
        predicted_class
    )

    # --------------------------------------------------------
    # DISEASE AREA
    # --------------------------------------------------------

    affected_area = estimate_disease_area(
        image
    )

    severity = get_severity(
        affected_area
    )

    # --------------------------------------------------------
    # SAVE CURRENT DETECTION
    # --------------------------------------------------------

    current_detection = {
        "disease": result["disease"],
        "confidence": confidence,
        "cause": result["cause"],
        "affected_area": affected_area,
        "severity": severity,
        "recommendations": result["recommendation"]
    }

    # --------------------------------------------------------
    # DISPLAY RESULT
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔍 Detection Result"
    )

    st.success(
        f"🌿 Disease: {result['disease']}"
    )

    st.metric(
        "Disease Confidence",
        f"{confidence:.2f}%"
    )

    st.info(
        f"🦠 Cause: {result['cause']}"
    )

    st.subheader(
        "📊 Estimated Disease Severity"
    )

    st.metric(
        "Estimated Affected Area",
        f"{affected_area:.2f}%"
    )

    if severity == "Low":

        st.success(
            f"Severity: {severity}"
        )

    elif severity == "Moderate":

        st.warning(
            f"Severity: {severity}"
        )

    else:

        st.error(
            f"Severity: {severity}"
        )

    st.caption(
        "Note: Affected-area percentage is an approximate "
        "image-based estimate, not a laboratory measurement."
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    st.subheader(
        "💡 Recommendations"
    )

    for recommendation in result[
        "recommendation"
    ]:

        st.write(
            f"• {recommendation}"
        )


# ============================================================
# CHATBOT
# ============================================================

st.divider()

st.header(
    "🤖 Plant Health AI Assistant"
)

st.write(
    "Ask questions about plant diseases, "
    "prevention, watering, treatment, symptoms, "
    "and plant care."
)


# ============================================================
# CHAT HISTORY
# ============================================================

if "chat_messages" not in st.session_state:

    st.session_state.chat_messages = []


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================

for message in st.session_state.chat_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_question = st.chat_input(
    "🌱 Ask anything about plants..."
)


if user_question:

    # --------------------------------------------------------
    # SAVE USER MESSAGE
    # --------------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):

        st.markdown(
            user_question
        )

    # --------------------------------------------------------
    # CHECK GEMINI KEY
    # --------------------------------------------------------

    if gemini_client is None:

        answer = (
            "❌ Gemini API key was not found.\n\n"
            "Please check your `.env` file."
        )

    else:

        # ----------------------------------------------------
        # SYSTEM INSTRUCTION
        # ----------------------------------------------------

        system_instruction = """
You are a Plant Health AI Assistant.

Your job is to answer questions about:

- plant diseases
- crop diseases
- symptoms
- causes
- prevention
- treatment and management
- watering
- fertilizers
- soil
- plant care
- healthy plant growth

Give simple, practical answers that a college student
or farmer can understand.

If a disease has already been detected in the application,
use that information when it is relevant.

Do not claim that an AI diagnosis is 100% certain.

For serious crop problems, recommend consulting a
local agricultural expert.

Do not make dangerous chemical recommendations.
If pesticides or fungicides are discussed, advise following
the product label and locally approved agricultural guidance.
"""

        # ----------------------------------------------------
        # CURRENT DETECTION CONTEXT
        # ----------------------------------------------------

        detection_context = ""

        if current_detection is not None:

            detection_context = f"""
CURRENT IMAGE DETECTION:

Disease:
{current_detection["disease"]}

Disease confidence:
{current_detection["confidence"]:.2f}%

Cause:
{current_detection["cause"]}

Estimated affected area:
{current_detection["affected_area"]:.2f}%

Estimated severity:
{current_detection["severity"]}

Recommendations:
{", ".join(current_detection["recommendations"])}
"""

        # ----------------------------------------------------
        # CONVERSATION
        # ----------------------------------------------------

        conversation = ""

        for message in st.session_state.chat_messages:

            conversation += (
                f"{message['role'].upper()}: "
                f"{message['content']}\n"
            )

        # ----------------------------------------------------
        # GEMINI REQUEST WITH RETRY + FALLBACK
        # ----------------------------------------------------

        answer = None

        models_to_try = [
            "gemini-3.8-flash",
            "gemini-3.5-flash-lite"
        ]

        for model_name in models_to_try:

            for attempt in range(3):

                try:

                    response = gemini_client.models.generate_content(

                        model=model_name,

                        contents=(
                            system_instruction
                            + "\n\n"
                            + detection_context
                            + "\n\n"
                            + conversation
                        )
                    )

                    answer = response.text

                    break

                except Exception as error:

                    error_text = str(error)

                    # Retry temporary server errors
                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                        or "429" in error_text
                    ):

                        time.sleep(
                            2 ** attempt
                        )

                        continue

                    # For other errors, move to fallback model
                    break

            if answer:

                break

        # ----------------------------------------------------
        # FINAL ERROR MESSAGE
        # ----------------------------------------------------

        if answer is None:

            answer = """
❌ Gemini is temporarily unavailable.

Your plant disease detection system is still working correctly.

The AI chatbot could not get a response from Google's Gemini service right now.

Please try your question again later.
"""

    # --------------------------------------------------------
    # DISPLAY ANSWER
    # --------------------------------------------------------

    with st.chat_message(
        "assistant"
    ):

        st.markdown(
            answer
        )

    # --------------------------------------------------------
    # SAVE ANSWER
    # --------------------------------------------------------

    st.session_state.chat_messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌱 AI-Based Plant Disease Detection and "
    "Recommendation System"
)

st.caption(
    "The AI provides preliminary information. "
    "For serious crop problems, consult a qualified "
    "agricultural expert."
)