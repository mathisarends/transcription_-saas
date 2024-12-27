import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Lade eine Audiodatei
audio_file = './src/interview_trimmed.wav'
y, sr = librosa.load(audio_file)

# Berechne die Grundfrequenz
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Zeige ein Spektrogramm an
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max),
                         sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Spektrogramm')
plt.show()