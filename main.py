import prediction as pred
import mel_spectogram_conversion as mel
import record as rec
import os
import time
import threading
import queue
import json

mel_spec = mel.MelSpectrogramConversion()
predict = pred.Prediction_Model()

# List of radio streams with IDs
streams = {
    1: "https://listen.openstream.co/4428/audio",
    2: "https://radios.crabdance.com:8002/5",
    3: "https://radios.crabdance.com:8002/1",
    4: "https://radios.crabdance.com:8002/2",
    5: "https://radios.crabdance.com:8002/4"
}

recordings = {fm_id: rec.Record(url, fm_id) for fm_id, url in streams.items()}

audio_queue = queue.Queue()
fm_status = {"fm_id": []}  # Dictionary to track active FM stations

print("Started recording & classification...")

def record_audio(fm_id, recording):
    while True:
        start_record_time = time.time()
        audio_file = recording.record_stream()
        end_record_time = time.time()

        record_duration = end_record_time - start_record_time
        audio_queue.put((fm_id, audio_file))  # Store fm_id with file

        print(f"\nRecording from FM {fm_id} | Time: {record_duration:.2f} seconds\n")

        sleep_time = max(5 - record_duration, 0)
        #time.sleep(sleep_time)

def classify_audio():
    while True:
        fm_id, audio_file = audio_queue.get()
        start_classify_time = time.time()

        mel_spec_file = mel_spec.convert(audio_file)
        prediction_result = predict.Prediction(mel_spec_file)
        end_classify_time = time.time()

        classify_duration = end_classify_time - start_classify_time
        mel_file_name = os.path.basename(mel_spec_file)

        if "ads" in prediction_result.lower():
            if fm_id in fm_status["fm_id"]:
                fm_status["fm_id"].remove(fm_id)
        else:
            if fm_id not in fm_status["fm_id"]:
                fm_status["fm_id"].append(fm_id)

        print(f"\nFM {fm_id} | {mel_file_name} -> {prediction_result} | Classification Time: {classify_duration:.2f} seconds\n")
        print(f"Active FM IDs: {fm_status["fm_id"]}")

def write_status_to_file():
    while True:
        with open("output.txt", "w") as file:
            json.dump(fm_status, file)
        time.sleep(5)

record_threads = [threading.Thread(target=record_audio, args=(fm_id, rec), daemon=True) for fm_id, rec in recordings.items()]
classify_thread = threading.Thread(target=classify_audio, daemon=True)
write_thread = threading.Thread(target=write_status_to_file, daemon=True)

for thread in record_threads:
    thread.start()
classify_thread.start()
write_thread.start()

while True:
    time.sleep(1)
