import pylsl
import requests
import json

def send_eeg_data_to_firebase(data, timestamp, api_key):
    url = "https://neurostream-skani-default-rtdb.asia-southeast1.firebasedatabase.app/eeg_data.json?auth=" + api_key
    # If data is already a dict (JSON), just add timestamp
    payload = dict(data)  # Make a copy to avoid mutating original
    payload["timestamp"] = timestamp
    response = requests.post(url, data=json.dumps(payload))
    print("Response:", response.status_code, response.text)

def decode_and_print_eeg_data(receiveBufferFloat, numberOfAcquiredChannels=8, FrameLength=1):
    for frame_idx in range(FrameLength):
        frame_data = receiveBufferFloat[frame_idx * numberOfAcquiredChannels : (frame_idx + 1) * numberOfAcquiredChannels]
        print(f"Frame {frame_idx}: {frame_data}")


if __name__ == "__main__":
    print("Looking for an EEG stream...")
    streams = pylsl.resolve_byprop('name', 'UN-2023.07.21', timeout=5)
    if not streams:
        print("No EEG stream found.")
    else:
        inlet = pylsl.StreamInlet(streams[0])
        print("EEG stream found. Receiving and decoding data...")
        numberOfAcquiredChannels = inlet.info().channel_count()
        FrameLength = 1  # One frame per sample
        try:
            while True:
                sample, timestamp = inlet.pull_sample()
                print(f"Timestamp: {timestamp}")
                decode_and_print_eeg_data(sample, numberOfAcquiredChannels, FrameLength)
                send_eeg_data_to_firebase(sample, timestamp, "AIzaSyAMHsvcktvyXhnGHHmwNedmobqhLsFV7q0")
        except KeyboardInterrupt:
            print("Stopped receiving.")