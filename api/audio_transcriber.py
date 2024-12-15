import speech_recognition as sr


class AudioTranscriber:
    """
    A class for transcribing audio files into text format.
    """

    def __init__(self, language: str = "de-DE"):
        """
        Initializes the AudioTranscriber with a Recognizer object and language setting.

        :param language: The language for transcription (default: German 'de-DE')
        """
        self.recognizer = sr.Recognizer()
        self.language = language

    def transcribe(self, file_path: str) -> str:
        """
        Transcribes a WAV audio file to text.

        :param file_path: Path to the audio file
        :return: Transcribed text as a string
        """
        try:
            # Load the audio file
            with sr.AudioFile(file_path) as source:
                print("Loading audio...")
                audio_data = self.recognizer.record(source)

            # Perform transcription
            print("Transcribing audio...")
            text = self.recognizer.recognize_google(audio_data, language=self.language)
            return text

        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio."
        except sr.RequestError as e:
            return f"An error occurred during the request: {e}"
