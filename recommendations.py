recommendations = {

    "Pepper__bell___Bacterial_spot": {
        "disease": "Pepper Bell Bacterial Spot",
        "cause": "Bacterial infection",
        "recommendation": [
            "Remove and safely dispose of severely affected leaves.",
            "Avoid watering the leaves from above.",
            "Keep enough space between plants for good air circulation.",
            "Use clean tools when working with plants.",
            "Use locally recommended disease-management products if necessary."
        ]
    },

    "Pepper__bell___healthy": {
        "disease": "Pepper Bell Healthy",
        "cause": "No visible disease detected",
        "recommendation": [
            "Continue regular plant care.",
            "Provide adequate sunlight and water.",
            "Monitor leaves regularly for early signs of disease.",
            "Keep the growing area clean."
        ]
    },

    "Potato___Early_blight": {
        "disease": "Potato Early Blight",
        "cause": "Fungal disease",
        "recommendation": [
            "Remove severely affected leaves.",
            "Avoid overhead watering.",
            "Improve air circulation around plants.",
            "Remove infected plant debris from the growing area.",
            "Follow locally recommended fungicide guidance when necessary."
        ]
    },

    "Potato___Late_blight": {
        "disease": "Potato Late Blight",
        "cause": "Disease caused by a fungus-like pathogen",
        "recommendation": [
            "Remove and dispose of severely infected plant material.",
            "Avoid keeping leaves wet for long periods.",
            "Improve air circulation between plants.",
            "Remove infected crop debris.",
            "Seek local agricultural guidance for appropriate disease-management products."
        ]
    },

    "Potato___healthy": {
        "disease": "Potato Healthy",
        "cause": "No visible disease detected",
        "recommendation": [
            "Continue regular plant care.",
            "Provide suitable water and sunlight.",
            "Monitor the leaves regularly.",
            "Keep the field or garden clean."
        ]
    },

    "Tomato_Bacterial_spot": {
        "disease": "Tomato Bacterial Spot",
        "cause": "Bacterial infection",
        "recommendation": [
            "Remove severely affected leaves.",
            "Avoid working with plants when they are wet.",
            "Avoid overhead irrigation.",
            "Maintain good spacing and air circulation.",
            "Follow local agricultural recommendations for disease management."
        ]
    },

    "Tomato_Early_blight": {
        "disease": "Tomato Early Blight",
        "cause": "Fungal disease",
        "recommendation": [
            "Remove severely affected leaves.",
            "Avoid overhead watering.",
            "Improve air circulation around the plant.",
            "Remove infected leaves and plant debris.",
            "Use locally recommended disease-management products when necessary."
        ]
    },

    "Tomato_Late_blight": {
        "disease": "Tomato Late Blight",
        "cause": "Disease caused by a fungus-like pathogen",
        "recommendation": [
            "Remove severely infected plant material.",
            "Avoid prolonged leaf wetness.",
            "Improve air circulation.",
            "Remove infected plant debris.",
            "Seek local agricultural guidance for appropriate management."
        ]
    },

    "Tomato_Leaf_Mold": {
        "disease": "Tomato Leaf Mold",
        "cause": "Fungal disease",
        "recommendation": [
            "Improve ventilation around the plants.",
            "Avoid excessive moisture on leaves.",
            "Remove severely affected leaves.",
            "Avoid overcrowding plants.",
            "Follow local recommendations for disease management if the problem continues."
        ]
    },

    "Tomato_Septoria_leaf_spot": {
        "disease": "Tomato Septoria Leaf Spot",
        "cause": "Fungal disease",
        "recommendation": [
            "Remove affected lower leaves.",
            "Avoid overhead watering.",
            "Improve air circulation.",
            "Remove infected plant debris.",
            "Follow locally recommended disease-management practices."
        ]
    },

    "Tomato_Spider_mites_Two_spotted_spider_mite": {
        "disease": "Tomato Spider Mites",
        "cause": "Spider mite infestation",
        "recommendation": [
            "Inspect the undersides of leaves regularly.",
            "Remove heavily affected leaves when appropriate.",
            "Keep plants adequately watered and reduce plant stress.",
            "Encourage beneficial insects where possible.",
            "Use locally recommended mite-management methods if infestation is severe."
        ]
    },

    "Tomato__Target_Spot": {
        "disease": "Tomato Target Spot",
        "cause": "Fungal disease",
        "recommendation": [
            "Remove severely affected leaves.",
            "Avoid overhead watering.",
            "Improve air circulation.",
            "Remove infected plant debris.",
            "Follow local agricultural guidance for disease management."
        ]
    },

    "Tomato__Tomato_YellowLeaf__Curl_Virus": {
        "disease": "Tomato Yellow Leaf Curl Virus",
        "cause": "Viral disease commonly associated with whitefly transmission",
        "recommendation": [
            "Remove severely infected plants where appropriate.",
            "Monitor and manage whitefly populations.",
            "Remove weeds that may harbor pests.",
            "Use healthy planting material.",
            "Follow local agricultural guidance for virus and vector management."
        ]
    },

    "Tomato__Tomato_mosaic_virus": {
        "disease": "Tomato Mosaic Virus",
        "cause": "Viral disease",
        "recommendation": [
            "Remove severely infected plants where appropriate.",
            "Keep tools and hands clean when handling plants.",
            "Avoid using infected plant material for propagation.",
            "Remove infected plant debris.",
            "Use healthy planting material."
        ]
    },

    "Tomato_healthy": {
        "disease": "Tomato Healthy",
        "cause": "No visible disease detected",
        "recommendation": [
            "Continue regular plant care.",
            "Provide suitable sunlight and water.",
            "Monitor leaves regularly.",
            "Keep the growing area clean.",
            "Check plants regularly for early signs of pests or disease."
        ]
    }
}


def get_recommendation(predicted_class):
    return recommendations.get(
        predicted_class,
        {
            "disease": predicted_class,
            "cause": "Information not available",
            "recommendation": [
                "Consult a local agricultural expert for further diagnosis."
            ]
        }
    )