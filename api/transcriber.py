import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class Transcriber:
    def __init__(self):
        self.openai = OpenAI()

    def transcribe(self, filePath: str, save_in_fs=True) -> dict:
        """
        Transkribiert die angegebene Audiodatei mit OpenAI Whisper und gibt Zeitstempel zurück.
        """
        audio_file = open(filePath, "rb")
        transcription = self.openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="json"
        )
        
        print("transcription", transcription)

        if save_in_fs:
            self.save_transcript_in_fs(filePath, transcription)

        return transcription
    
    def save_transcript_in_fs(self, filePath: str, transcription: dict):
        """
        Speichert das Transkript mit Zeitstempeln als Datei im Dateisystem.

        :param filePath: Der Pfad zur ursprünglichen Audiodatei.
        :param transcription: Das Transkript als JSON-Objekt.
        """
        output_dir = "./src/transcripts"
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.basename(filePath)
        transcript_file = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_transcript.json")

        # Transkript im JSON-Format speichern
        with open(transcript_file, "w", encoding="utf-8") as f:
            import json
            json.dump(transcription, f, indent=4, ensure_ascii=False)

        print(f"Transkript mit Zeitstempeln gespeichert unter: {transcript_file}")

# TODO: hierfür kann man eventuell auch besser die WhisperAPI benutzen die Open Source ist mit entsprechenden Zeitstempeln
# Lösung kann dann mit pyannote kombiniert werden um die Sprecher richtig zu klassifzieren
if __name__ == "__main__":
    transcriber = Transcriber()
    
    transcription = transcriber.transcribe("./src/interview_trimmed.mp3", save_in_fs=False)

    # Ausgabe der Transkriptionssegmente mit Zeitstempeln
    for segment in transcription.get("segments", []):
        print(f"Start: {segment['start']}s, Ende: {segment['end']}s, Text: {segment['text']}")