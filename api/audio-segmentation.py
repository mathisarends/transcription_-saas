import os
from pydub import AudioSegment

def parse_diarization_file(file_path):
    """
    Liest eine Datei mit Diarisation-Daten ein und erstellt eine strukturierte Datenstruktur.

    :param file_path: Pfad zur Datei mit den Diarisation-Daten.
    :return: Liste von Sprecher-Einträgen und ein Dictionary mit Gesamtsprechzeiten pro Sprecher.
    """
    speaker_entries = []
    total_speaking_times = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        
        for line in file:
            print(f"line: {line}")
            line = line.strip()
            if not line:
                continue

            try:
                parts = line.split()
                print(parts[0])
                print(parts[1])
                print(parts[2])
                
                start = float(parts[0].split('=')[1][:-1])
                stop = float(parts[1].split('=')[1][:-1])
                speaker = parts[2]                

                duration = stop - start

                speaker_entries.append({
                    "start": start,
                    "stop": stop,
                    "speaker": speaker,
                    "duration": duration
                })

                # Gesamtsprechzeit berechnen
                if speaker not in total_speaking_times:
                    total_speaking_times[speaker] = 0
                total_speaking_times[speaker] += duration

            except (ValueError, IndexError) as e:
                print(f"Warnung: Fehler beim Verarbeiten der Zeile: {line}\nFehler: {e}")
                break

    return speaker_entries, total_speaking_times

def merge_short_pauses(speaker_entries, pause_threshold=1):
    """
    Kombiniert aufeinanderfolgende Sprecher-Einträge, wenn die Pause dazwischen kürzer als ein bestimmter Schwellenwert ist.

    :param speaker_entries: Liste von Sprecher-Einträgen (start, stop, speaker, duration).
    :param pause_threshold: Schwellenwert für die Pause in Sekunden.
    :return: Liste von kombinierten Sprecher-Einträgen.
    """
    if not speaker_entries:
        return []

    merged_entries = []
    current_entry = speaker_entries[0]

    for next_entry in speaker_entries[1:]:
        # Überprüfen, ob der Sprecher gleich ist und die Pause kürzer als der Schwellenwert ist
        if (
            current_entry['speaker'] == next_entry['speaker']
            and next_entry['start'] - current_entry['stop'] <= pause_threshold
        ):
            # Einträge zusammenführen
            current_entry['stop'] = next_entry['stop']
            current_entry['duration'] += next_entry['duration']
        else:
            # Aktuellen Eintrag zur Liste hinzufügen und neuen Eintrag starten
            merged_entries.append(current_entry)
            current_entry = next_entry

    # Letzten Eintrag hinzufügen
    merged_entries.append(current_entry)

    return merged_entries

def split_audio(file_path, output_dir, segments):
    """
    Schneidet die Audiodatei basierend auf den Segmenten.
    
    :param file_path: Pfad zur Eingabe-Audiodatei.
    :param output_dir: Zielordner für die geschnittenen Audiodateien.
    :param segments: Liste von Segmenten mit Start, Stop und Sprecher.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Lade die Audiodatei
    audio = AudioSegment.from_wav(file_path)
    
    for idx, segment in enumerate(segments):
        start_ms = int(segment["start"] * 1000)  # Umwandlung in Millisekunden
        stop_ms = int(segment["stop"] * 1000)   # Umwandlung in Millisekunden
        speaker = segment["speaker"]
        
        # Schneide das Segment
        segment_audio = audio[start_ms:stop_ms]
        
        # Dateiname erstellen
        output_file = os.path.join(output_dir, f"segment_{idx+1}_{speaker}.wav")
        
        # Segment speichern
        segment_audio.export(output_file, format="wav")
        print(f"Gespeichert: {output_file}")


if __name__ == "__main__":
    file_path = "./src/audio-segmentation.txt"

    # Daten verarbeiten
    speaker_entries, total_speaking_times = parse_diarization_file(file_path)
    
    merged_speaker_entries = merge_short_pauses(speaker_entries)

    # Ergebnisse anzeigen
    print("Einträge der Sprecher:")
    for entry in merged_speaker_entries:
        print(entry)

    print("\nGesamtsprechzeiten:")
    for speaker, total_time in total_speaking_times.items():
        print(f"{speaker}: {total_time:.2f} Sekunden")
        
    
    output_directory = "./src/audio_segments"
    audio_file_path = "./src/interview_trimmed.wav"
    
    split_audio(audio_file_path, output_directory, merged_speaker_entries)