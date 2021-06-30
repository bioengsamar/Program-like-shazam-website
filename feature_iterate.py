import matplotlib.pyplot as plt
from pathlib import Path
import librosa
#import librosa.display
import os

def save(name):
    #cv2.imwrite('songs_spectro_png\{}.png'.format(name), Sxx)
    plt.savefig('songs_features\{}.png'.format(name))
   
paths = Path('songs').glob('**/*.mp3')
for path in paths:
    # because path is object not string
    path_in_str = str(path)
    #print(path_in_str)
    y, sr = librosa.load(path) #example_audio_file() is an example audio in librosa
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    S, phase = librosa.magphase(librosa.stft(y=y))
    librosa.feature.spectral_centroid(S=S)
    plt.clf()
    plt.semilogy(cent.T, label='Spectral centroid')
    plt.legend()
    save(os.path.basename(path_in_str))
    