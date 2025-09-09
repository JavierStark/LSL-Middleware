import pylsl
import struct
import random

def receive_eeg_stream():
    # Resolve an EEG stream on the network
    print("Looking for an EEG stream...")
    streams = pylsl.resolve_stream('type', 'EEG')
    if not streams:
        print("No EEG stream found.")
        return

    # Create an inlet to read from the stream
    inlet = pylsl.StreamInlet(streams[0])
    print("EEG stream found. Receiving data...")

    try:
        while True:
            sample, timestamp = inlet.pull_sample()
            print(f"Timestamp: {timestamp}, Sample: {sample}")
    except KeyboardInterrupt:
        print("Stopped receiving.")

def decode_and_print_eeg_data(receiveBufferFloat, numberOfAcquiredChannels=8, FrameLength=1):
    for frame_idx in range(FrameLength):
        frame_data = receiveBufferFloat[frame_idx * numberOfAcquiredChannels : (frame_idx + 1) * numberOfAcquiredChannels]
        print(f"Frame {frame_idx}: {frame_data}")


if __name__ == "__main__":
    print("Looking for an EEG stream...")
    streams = pylsl.resolve_stream('type', 'EEG')
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
        except KeyboardInterrupt:
            print("Stopped receiving.")