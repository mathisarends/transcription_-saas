import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class Transcriber:
    def __init__(self):
        self.openai = OpenAI()

    def transcribe(self, filePath: str) -> str:
        """
        Transkribiert die angegebene Audiodatei mit OpenAI Whisper.
        """
        audio_file = open(filePath, "rb")
        transcription = self.openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        
        self.save_transcript_in_fs(filePath, transcription.text)
        
        return transcription.text
    
    def save_transcript_in_fs(self, filePath: str, transcript: str):
        """
        Speichert das gegebene Transkript als Datei im Dateisystem.

        :param filePath: Der Pfad zur ursprünglichen Audiodatei.
        :param transcript: Das Transkript als String.
        """
        output_dir = "./src/transcripts"
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.basename(filePath)
        transcript_file = os.path.join(output_dir, f"{os.path.splitext(base_name)[0]}_transcript.txt")

        with open(transcript_file, "w", encoding="utf-8") as f:
            f.write(transcript) 

        print(f"Transkript gespeichert unter: {transcript_file}")
        

    def assign_speakers(self, transcription: str, context: str, speakers: dict) -> str:

        # Dynamisches System-Prompt basierend auf den Speaker-Keys
        speaker_labels = "\n".join([f"{key}: [Text des {key}]" for key in speakers.keys()])
        print(f"speaker_labels {speaker_labels}")
        
        system_prompt = (
            "Du bist ein Assistent, der Interviewtranskripte annotiert. "
            "Deine Aufgabe ist es, jedem Absatz im Transkript Sprecherlabels zuzuweisen. "
            "Der Interviewer stellt Fragen, die in der Regel kürzer sind, während der Experte längere und detailliertere Antworten gibt. "
            "Berücksichtige, dass der Sprachanteil des Experten in diesem Interview deutlich höher ist und daran erkennbar sein könnte, "
            "dass seine Aussagen ausführlicher und inhaltlich spezifischer sind. "
            f"Antwort im folgenden Format:\n\n{speaker_labels}"
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


if __name__ == "__main__":
    transcriber = Transcriber()
    
    transcription = transcriber.transcribe("./src/interview_trimmed.mp3")
    
    context = "Das Interview behandelt die historische Entwicklung der Anatomie und Zahnmedizin, einschließlich persönlicher Erfahrungen mit Präparierkursen und prägenden Persönlichkeiten."
    speakers = {
        "Interviewer": "Interviewer, der Fragen zur Geschichte der Anatomie und Zahnmedizin stellt.",
        "Experte": "Experte und Zeitzeuge, der über seine Erfahrungen in anatomischen Instituten und Präparierkursen berichtet."
    }
    
    # Annotiere die Transkription
    transcription = transcriber.assign_speakers(transcription, context, speakers)
    print("transcription", transcription)