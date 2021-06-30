import os
from pydub import AudioSegment
import numpy as np
#from scipy import signal
import matplotlib.pyplot as plt
#from cv2 import cv2
from pathlib import Path
from PIL import Image
import imagehash

def save(name):
    #cv2.imwrite('songs_spectro_png\{}.png'.format(name), Sxx)
    plt.savefig('songs_spectro_png\{}.png'.format(name))
   
paths = Path('songs').glob('**/*.mp3')
for path in paths:
    # because path is object not string
    path_in_str = str(path)
    #print(path_in_str)
    mp3_audio = AudioSegment.from_file(path, format="mp3")[:60000]  #read first 1 minute
    samples = mp3_audio.get_array_of_samples()
    samples = np.array(samples)
    #f, t, Sxx = signal.spectrogram(samples, mp3_audio.frame_rate)
    plt.clf()
    plt.specgram(samples, NFFT=128, Fs=740, noverlap=128/2)
    #print(mp3_audio.frame_rate)
    save(os.path.basename(path_in_str))
    
###########################################_get phash for songs_##############################
paths = Path('songs_spectro_png').glob('**/*.png')
paths2=Path('songs').glob('**/*.mp3')
spectrogram2=imagehash.phash(Image.open('mix.png'))
for path ,path2 in zip(paths , paths2):
    # because path is object not string
    path_in_str = str(path2)
    #print(path_in_str)              
    spectrogram=imagehash.phash(Image.open(path))
    #print(str(spectrogram))
    print(os.path.basename(path_in_str),'difference :'+ str(spectrogram2-spectrogram))

    