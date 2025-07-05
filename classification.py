import json
import re
from langdetect import detect
from googletrans import Translator

translator = Translator()

def detect_language(text):
    """Detect the language using langdetect."""
    try:
        detected_lang = detect(text)
        print(text)
        print(detected_lang)
        return detected_lang if detected_lang in ["en", "ml"] else "en"  # Default to English if unknown
    except:
        return "en"

def translate_to_english(text, lang):
    """Translate non-English text to English before processing."""
    if lang != "en":
        try:
            print("1")
            translated_text = translator.translate(text, src=lang, dest="en").text
            print("2",translated_text)
            return translated_text
        except:
            return text  # Return original if translation fails
    return text

def classify_question_type(user_input):
    detected_lang = detect_language(user_input)
    user_input = translate_to_english(user_input, detected_lang)  # Translate if necessary

    # List of medical topics that should always be classified as "general"
    general_keywords = [
        "diet", "foods", "eat", "exercise", "angioplasty", "medication", "lifestyle",
        "recovery", "stress", "emotion", "mental health", "pain management", "walking",
        "blood pressure", "health", "treatment", "doctor", "nurse", "surgery"
    ]

    # Explicit indicators of **personalized** questions  
    personalized_patterns = [
        r"\bmy\b", r"\bme\b", r"\bmine\b", r"\bI\b",  
        r"\bshould I\b", r"\bcan I\b", r"\bdo I\b",  
        r"\bis my\b", r"\bam I\b", r"\bwill I\b",
        r"\bwhat is my\b", r"\bwhen should I\b", r"\bhow do I\b"
    ]

    # Implicit **commands** referring to user’s own medical details
    personal_command_patterns = [
        r"\bshow\b", r"\blist\b", r"\bgive\b", r"\bdisplay\b", r"\bschedule\b", r"\bappointment\b", r"\breport\b"
    ]

    user_input_lower = user_input.lower()

    # Ensure medical-related questions remain **general**
    contains_general_medical_topic = any(keyword in user_input_lower for keyword in general_keywords)

    # Check if the question explicitly contains personalization
    is_personalized = any(re.search(pattern, user_input_lower, re.IGNORECASE) for pattern in personalized_patterns)

    # Check if the question is a **command** requesting personal details
    contains_personal_command = any(re.search(pattern, user_input_lower, re.IGNORECASE) for pattern in personal_command_patterns)

    # Final classification
    if contains_personal_command:
        question_type = "personalized"
    elif contains_general_medical_topic:
        question_type = "general"
    elif is_personalized:
        question_type = "personalized"
    else:
        question_type = "general"

    # Return JSON response
    return json.dumps({"question_type": question_type, "lang": detected_lang})

# Test cases
print(classify_question_type("What foods should I eat after a robeoplastic?"))  
# Output: {"question_type": "general", "lang": "en"}

print(classify_question_type("What is the schedule of today"))  
# Output: {"question_type": "personalized", "lang": "en"}

print(classify_question_type("ഞാൻ അഞ്ജിയോപ്ലാസ്റ്റിക്കുശേഷം എന്ത് ഭക്ഷണം കഴിക്കണം?"))  
# (Malayalam: "What food should I eat after angioplasty?")  
# Output: {"question_type": "general", "lang": "ml"}
