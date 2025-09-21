from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uuid, os
from pathlib import Path
from ai_pipeline import transcribe, detect_emotion, generate_story, translate_story

app = FastAPI(title="Artisan Aura API")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/process-audio")
async def process_audio(audio: UploadFile = File(...), languages: str = Form("es,fr,hi,ta,ar")):
    lang_list = [lang.strip() for lang in languages.split(",")]
    file_path = UPLOAD_DIR / f"{uuid.uuid4()}_{audio.filename}"
    with open(file_path, "wb") as f:
        f.write(await audio.read())

    try:
        transcript = transcribe(str(file_path))
        emotion = detect_emotion(transcript)
        story = generate_story(transcript, emotion)
        translations = translate_story(story, lang_list)
        return JSONResponse({
            "transcript": transcript,
            "emotion": emotion,
            "story": story,
            "translations": translations
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        os.remove(file_path)

@app.get("/")
def home():
    return {"message": "Welcome to Artisan Aura API 🌍"}
