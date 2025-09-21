import torch
from faster_whisper import WhisperModel
from transformers import pipeline
from deep_translator import GoogleTranslator

def get_whisper_model():
    return WhisperModel("openai/whisper-small", device="cuda" if torch.cuda.is_available() else "cpu")

def get_emotion_classifier():
    return pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

def transcribe(audio_path: str) -> str:
    model = get_whisper_model()
    segments, _ = model.transcribe(audio_path)
    return ''.join(seg.text for seg in segments).strip()

def detect_emotion(text: str) -> str:
    classifier = get_emotion_classifier()
    results = classifier(text)
    return max(results[0], key=lambda x: x['score'])['label']

def generate_story(transcript: str, emotion: str) -> str:
    return f"""
I speak with {emotion.lower()} in my heart.
{transcript}

This craft is not just work — it’s my family’s breath, passed through thread and time.
"""

def translate_story(story: str, languages: list) -> dict:
    translations = {}
    for lang in languages:
        try:
            translated = GoogleTranslator(source='en', target=lang).translate(story)
            translations[lang] = translated
        except Exception as e:
            translations[lang] = f"[Translation failed: {str(e)}]"
    return translations
