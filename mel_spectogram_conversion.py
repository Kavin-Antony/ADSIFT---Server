import os
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib
matplotlib.use('Agg')  

class MelSpectrogramConversion():
    def __init__(self, output_dir = '/Users/kavinantonyar/Projects/MINI_PROJECT/trial/mel', n_mels=128, resnet_input_size=(224, 224)):
        self.output_dir = output_dir
        self.n_mels = n_mels
        self.resnet_input_size = resnet_input_size
        os.makedirs(self.output_dir, exist_ok=True)

    def convert(self, file_path):
        
        filename = os.path.basename(file_path)
        y, sr = librosa.load(file_path, sr=None)
        mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=self.n_mels)
        mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

        plt.figure(figsize=(3, 3))
        librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel', cmap='viridis')
        plt.axis('off')
        plt.tight_layout(pad=0)

        output_path = os.path.join(self.output_dir, f"{os.path.splitext(filename)[0]}.png")
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close() 

        with Image.open(output_path) as img:
            img_resized = img.resize(self.resnet_input_size)
            img_resized.save(output_path)

        return output_path  
