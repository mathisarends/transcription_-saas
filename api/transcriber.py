import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class Transcriber:
    def __init__(self):
        self.openai = OpenAI()

    def transcribe(self, filePath: str) -> str:
        """
        Transcribes the given audio file using OpenAI Whisper.
        """
        audio_file = open(filePath, "rb")
        transcription = self.openai.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
        return transcription.text

    def assign_speakers(self, transcription: str, context: str, speakers: dict) -> str:
        """
        Assigns speakers to the transcribed text using OpenAI GPT.

        :param transcription: The raw transcription text.
        :param context: Context for the conversation (e.g., interview topic).
        :param speakers: Dictionary mapping speaker roles (e.g., "A", "B") to descriptions.
        :return: Text with speakers assigned to each paragraph.
        """
        # Create the system and user prompts
        system_prompt = (
            "You are an assistant helping to annotate interview transcripts. "
            "Your task is to assign speaker labels (e.g., A, B) to each paragraph of the transcription. "
            "Provide the annotated text in the following format: "
            "A: [Interviewer text]\nB: [Expert response text]."
        )
        
        # Speaker descriptions as part of the user prompt
        speaker_info = "\n".join([f"{key}: {value}" for key, value in speakers.items()])
        
        user_prompt = (
            f"The interview topic is: {context}\n"
            f"The following speakers are involved:\n{speaker_info}\n\n"
            f"Here is the raw transcription:\n\n{transcription}\n\n"
            f"Please assign the speaker labels to each paragraph accordingly."
        )

        # Generate the output using GPT
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content


if __name__ == "__main__":
    transcriber = Transcriber()
    
    transcription = transcriber.transcribe("./src/interview_trimmed.mp3")
    
    context = "This interview discusses dentistry."
    speakers = {
        "A": "Interviewer asking questions about dentistry.",
        "B": "Expert in dentistry."
    }
    annotated_transcription = transcriber.assign_speakers(transcription, context, speakers)
    # Print the annotated transcription
    
    print(annotated_transcription)