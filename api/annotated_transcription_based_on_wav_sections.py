import os
from pydub import AudioSegment
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai = OpenAI()

def transcribe_segment(file_path, speaker, segment_index):
    """
    Erstellt einen Transkriptions-Prompt und sendet ihn an das LLM.

    :param file_path: Pfad zur Audiodatei.
    :param speaker: Sprecherinformation aus dem Dateinamen.
    :param segment_index: Segmentnummer.
    :return: Transkribierter Text.
    """
    # Lade die Audiodatei
    with open(file_path, "rb") as audio_file:
        # Transkribieren mit OpenAI (Whisper oder GPT)
        transcription = openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            prompt=f"Segment {segment_index}, Sprecher: {speaker}. Transkribiere den Text."
        )

        return transcription.text

def process_audio_segments(directory):
    """
    Iteriert über alle Audiodateien im Verzeichnis und transkribiert sie.

    :param directory: Verzeichnis mit den Audiodateien.
    """
    all_transcriptions = []

    # Dateien numerisch sortieren
    files = sorted(
        os.listdir(directory),
        key=lambda x: int(x.split("_")[1]) if x.endswith(".wav") else float("inf")
    )

    for file_name in files:
        if file_name.endswith(".wav"):
            # Dateipfad
            file_path = os.path.join(directory, file_name)

            # Sprecher und Segmentnummer aus dem Dateinamen extrahieren
            parts = file_name.split("_")
            segment_index = parts[1]
            speaker = parts[-1].replace(".wav", "")
            
            print(f"segment_index: {segment_index} speaker: {speaker}")

            # Transkribieren
            """ transcription = transcribe_segment(file_path, speaker, segment_index) """

            # Format speichern
            """ all_transcriptions.append(f"{speaker} ({segment_index}): {transcription}")
            print(f"Segment {segment_index} transkribiert.") """
    return all_transcriptions

def save_transcriptions_to_file(transcriptions, output_file):
    """
    Speichert die Transkriptionen in eine Datei.

    :param transcriptions: Liste der Transkriptionen.
    :param output_file: Ausgabedatei.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        for transcription in transcriptions:
            f.write(transcription + "\n")
    print(f"Transkriptionen gespeichert in {output_file}")

if __name__ == "__main__":
    # Ordner mit den Segmenten
    directory = "./src/audio_segments"

    # Transkriptionen verarbeiten
    transcriptions = process_audio_segments(directory)

    # Ergebnisse speichern
    output_file = "transcriptions.txt"
    """ save_transcriptions_to_file(transcriptions, output_file) """

# TODO: hier kriege ich einen audio file is to short fehler leider

