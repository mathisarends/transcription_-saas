import os
from collections import defaultdict
from dotenv import load_dotenv
from pyannote.audio import Pipeline


# .env-Datei laden
load_dotenv()

# Hugging Face Token abrufen
hf_token = os.getenv("HF_TOKEN")


pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=hf_token)


diarization = pipeline("./src/interview_trimmed.wav", num_speakers=2)

print("Sprecher-Diarisation abgeschlossen. Ergebnisse:")
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    
    
speaker_durations = defaultdict(float)

for turn, _, speaker in diarization.itertracks(yield_label=True):
    duration = turn.end - turn.start
    speaker_durations[speaker] += duration

for speaker, total_duration in speaker_durations.items():
    print(f"Sprecher {speaker} hat insgesamt {total_duration:.1f} Sekunden gesprochen.")