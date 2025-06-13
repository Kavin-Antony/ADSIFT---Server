import os
import time
import threading
import subprocess

class Record():
    def __init__(self, url, seq):
        self.stream_url = url
        self.output_dir = "/Users/kavinantonyar/Projects/MINI_PROJECT/trial/recorded"
        self.segment_duration = 5
        self.i = 1
        self.seq = seq
    def record_stream(self):
        output_file = f"{self.output_dir}/{self.seq}_{self.i}.wav" 
        self.i += 1
        subprocess.run([
        'ffmpeg', '-y', '-i', self.stream_url, '-t', str(self.segment_duration),
        '-c:a', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_file
        ])
        return output_file
