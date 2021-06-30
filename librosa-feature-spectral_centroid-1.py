# From time-series input:
import librosa
import numpy as np
import librosa.display
y, sr = librosa.load('songs\heart.mp3') #example_audio_file() is an example audio in librosa
cent = librosa.feature.spectral_centroid(y=y, sr=sr)
print(sr)
# array([[ 4382.894,   626.588, ...,  5037.07 ,  5413.398]])

# From spectrogram input:

S, phase = librosa.magphase(librosa.stft(y=y))
librosa.feature.spectral_centroid(S=S)
# array([[ 4382.894,   626.588, ...,  5037.07 ,  5413.398]])

# Using variable bin center frequencies:

y, sr = librosa.load(librosa.util.example_audio_file())
if_gram, D = librosa.ifgram(y)
librosa.feature.spectral_centroid(S=np.abs(D), freq=if_gram)
# array([[ 4420.719,   625.769, ...,  5011.86 ,  5221.492]])

# Plot the result

import matplotlib.pyplot as plt
plt.figure()
#plt.subplot(2, 1, 1)
plt.semilogy(cent.T, label='Spectral centroid')
#plt.ylabel('Hz')
#plt.xticks([])
plt.xlim([0, cent.shape[-1]])
plt.legend()
##plt.subplot(2, 1, 2)
#librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time')
#plt.title('log Power spectrogram')
plt.tight_layout()
plt.show()
