import { useState } from 'react';
import axios from 'axios';

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [result, setResult] = useState<any>(null);
  let mediaRecorder: MediaRecorder | null = null;
  const chunks: BlobPart[] = [];

  const startRecording = () => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
      mediaRecorder = new MediaRecorder(stream);
      mediaRecorder.start();
      setIsRecording(true);

      mediaRecorder.ondataavailable = e => chunks.push(e.data);
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const file = new File([blob], "voice.webm", { type: 'audio/webm' });

        const formData = new FormData();
        formData.append('audio', file);
        formData.append('languages', "es,fr,hi,ta,ar");

        const res = await axios.post("http://127.0.0.1:8000/process-audio", formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setResult(res.data);
      };
    });
  };

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop();
      setIsRecording(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold">🎙️ Artisan Aura</h1>
      <button
        onClick={isRecording ? stopRecording : startRecording}
        className={`px-4 py-2 mt-4 rounded ${isRecording ? 'bg-red-500' : 'bg-green-500'} text-white`}
      >
        {isRecording ? "Stop Recording" : "Start Recording"}
      </button>

      {result && (
        <div className="mt-6">
          <h2>Detected Emotion: {result.emotion}</h2>
          <p><b>Story:</b> {result.story}</p>
          <h3 className="mt-4">Translations</h3>
          <ul>
            {Object.entries(result.translations || {}).map(([lang, text]) => (
              <li key={lang}><b>{lang}:</b> {String(text)}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
