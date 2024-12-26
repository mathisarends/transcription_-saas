import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class TranscriptionAnnotator:
    def __init__(self):
        self.openai = OpenAI()        

    def assign_speakers(self, transcription: str, context: str, speakers: dict) -> str:        
        system_prompt = (
            "Du bist ein Assistent, der Interviewtranskripte annotiert. "
            "Deine Aufgabe ist es, jedem Absatz im Transkript Sprecherlabels zuzuweisen (z. B. A, B). "
            "Antwort im folgenden Format:\n\n"
            "A: [Text des Interviewers]\nB: [Text des Experten]."
        )
            
        # Sprecherbeschreibungen als Teil des Benutzerprompts
        speaker_info = "\n".join([f"{key}: {value}" for key, value in speakers.items()])
        
        print(f"speaker_info {speaker_info}")
        
        user_prompt = (
            f"Das Thema des Interviews ist: {context}\n"
            f"Die folgenden Sprecher sind beteiligt:\n{speaker_info}\n\n"
            f"Hier ist das rohe Transkript:\n\n{transcription}\n\n"
            f"Bitte ordne jedem Absatz die entsprechenden Sprecherlabels zu."
        )

        # GPT-Ausgabe generieren
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )
        
        return response.choices[0].message.content
    
    def load_transcription_from_fs(self, filePath: str) -> str:
        """
        Lädt eine Transkriptionsdatei aus dem Dateisystem.

        :param filePath: Der Pfad zur Transkriptionsdatei.
        :return: Der Inhalt der Transkriptionsdatei als String.
        """
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"Die Datei {filePath} wurde nicht gefunden.")
        
        with open(filePath, "r", encoding="utf-8") as f:
            transcription = f.read()
        
        print(f"Transkription aus Datei geladen: {filePath}")
        return transcription


if __name__ == "__main__":
    transcriptionAnnotator = TranscriptionAnnotator()
    
    context = "Das Interview behandelt die historische Entwicklung der Anatomie und Zahnmedizin, einschließlich persönlicher Erfahrungen mit Präparierkursen und prägenden Persönlichkeiten."
    speakers = {
        "Interviewer": "Interviewer, der Fragen zur Geschichte der Anatomie und Zahnmedizin stellt.",
        "Experte": "Experte und Zeitzeuge, der über seine Erfahrungen in anatomischen Instituten und Präparierkursen berichtet."
    }
    # Transkription aus dem Dateisystem laden
    transcription_path = "./src/transcripts/interview_trimmed_transcript.txt"
    transcription = transcriptionAnnotator.load_transcription_from_fs(transcription_path)
    
    # Annotierte Transkription generieren
    annotated_transcription = transcriptionAnnotator.assign_speakers(transcription, context, speakers)
    print("Annotierte Transkription:\n", annotated_transcription)