from PyQt5 import QtWidgets, QtCore
from pydub import AudioSegment
import numpy as np
from scipy import signal
import imagehash
from PIL import Image
from pathlib import Path
import librosa
import matplotlib.pyplot as plt
#import cv2
from fingerprint import Ui_MainWindow
import os
import sys
import logging

logging.basicConfig(filename="Fingerprint.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w')
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.setCheckable(True) 
        self.ui.pushButton_2.setCheckable(True)
        self.my_button_group = QtWidgets.QButtonGroup()
        self.my_button_group.addButton(self.ui.pushButton)
        self.my_button_group.addButton(self.ui.pushButton_2)
        self.ui.horizontalSlider.valueChanged['int'].connect(self.mixer)
        self.ui.tableWidget.setItem(0,0,QtWidgets.QTableWidgetItem("song"))
        self.ui.tableWidget.setItem(0,1,QtWidgets.QTableWidgetItem("percentage"))
        header = self.ui.tableWidget.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
       
    def load(self):
        if self.ui.pushButton.isChecked():
            self.song1 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file','',' *.mp3')[0]
            self.ui.lineEdit.setText(self.song1)
            print('yes')
            
        if self.ui.pushButton_2.isChecked():
            self.song2 = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file','',' *.mp3')[0]
            self.ui.lineEdit_2.setText(self.song2)
            print('okk')
            
    def read(self,path):
        mp3_audio = AudioSegment.from_file(path, format="mp3")[:60000]  #read first 1 minute
        samples = mp3_audio.get_array_of_samples()
        samples = np.array(samples)
        return samples

            
    def mixer(self,value):
        print(value)
        self.samples_1=self.read(self.song1)
        self.samples_2=self.read(self.song2)
        self.fourier_1=np.fft.fft(self.samples_1)
        self.fourier_2=np.fft.fft(self.samples_2)
        self.mix=np.multiply((value/100)*np.abs(self.fourier_1),(1-(value/100))*np.exp(1j*np.angle(self.fourier_2)))
        self.mix=np.real(np.fft.ifft(self.mix))
        self.mix=np.abs(self.mix)
        self.frequency, self.time, self.spectro= signal.spectrogram(self.mix, 44100)
        self.ui.tableWidget.sortItems(1, QtCore.Qt.DescendingOrder)
        
    def comparison(self):
        paths2=Path('songs').glob('**/*.mp3')
        if self.ui.hash_radiobtn.isChecked():
            paths = Path('songs_spectro_png').glob('**/*.png')
            #cv2.imwrite('mix.png', self.spectro)
            plt.specgram(self.mix, NFFT=128, Fs=740, noverlap=128/2)
            plt.savefig('mix.png')
            spectrogram2=imagehash.phash(Image.open('mix.png'))
            songs=[]
            results=[] 
            for path ,path2 in zip(paths , paths2):
                path_in_str = str(path2)
                spectrogram=imagehash.phash(Image.open(path))
                difference=spectrogram2-spectrogram
                songs.append(os.path.basename(path_in_str))
                results.append(difference)
            for m,i in zip( range(1,len(songs)+1),range(0,len(songs))):
                self.ui.tableWidget.setItem(m,0,QtWidgets.QTableWidgetItem(songs[i]))
                self.ui.tableWidget.setItem(m,1,QtWidgets.QTableWidgetItem(str((100-results[i])/100)))
        if self.ui.feature_radiobtn.isChecked():
             cent = librosa.feature.spectral_centroid(y=self.mix, sr=22050)
             S, phase = librosa.magphase(librosa.stft(y=self.mix))
             librosa.feature.spectral_centroid(S=S)
             plt.clf()
             plt.semilogy(cent.T, label='Spectral centroid')
             plt.legend()
             plt.savefig('mix_feature.png')
             feature2=imagehash.phash(Image.open('mix_feature.png'))
             songs=[]
             results=[]
             paths3=Path('songs_features').glob('**/*.png')
             for path3 ,path2 in zip(paths3 , paths2):
                path_in_str = str(path2)
                feature=imagehash.phash(Image.open(path3))
                difference=feature2-feature
                songs.append(os.path.basename(path_in_str))
                results.append(difference)
             for m,i in zip( range(1,len(songs)+1),range(0,len(songs))):
                self.ui.tableWidget.setItem(m,0,QtWidgets.QTableWidgetItem(songs[i]))
                self.ui.tableWidget.setItem(m,1,QtWidgets.QTableWidgetItem(str((100-results[i])/100)))
                
        
            
def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()