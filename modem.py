# Max Janisse - 2026
import scipy.io.wavfile as wav
from scipy.signal import butter, sosfiltfilt
import numpy as np
import argparse

VERBOSE = False

def tone_power(samples, f, fs):
    I = 0
    Q = 0
    length = len(samples)
    for n in range(length):
        angle = 2. * np.pi * f * (n / fs)
        I += (samples[n] * np.cos(angle))
        Q += (samples[n] * np.sin(angle))
    return I**2 + Q**2

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    
    sos = butter(order, [low, high], btype='bandpass', output="sos")
    
    y = sosfiltfilt(sos, data)
    return y

def detector_mode(rate, data, chunk_size):
    bits = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        mark = tone_power(chunk, 2225, rate)
        space = tone_power(chunk, 2025, rate)
        bit = 1 if mark >= space else 0
        bits.append(bit)
        ratio = round(mark/space if bit else space/mark)
        if ratio > 10:
            print(f"Odd ratio warning {ratio}")
        if VERBOSE:
            print("MARK " if bit else "SPACE", ratio, (round(mark,1), round(space,1)))
    if all([b == 1 for b in bits]):
        print("MARK tone detected 100%")
    elif all([b == 0 for b in bits]):
        print("SPACE tone detected 100%")
    else:
        print("Mixed tones detected")

def read_wav_file(filename):
    try:
        rate, data = wav.read(filename)
        if type(data[0]) is np.ndarray:
            raise ValueError(f"Multiple ({len(data[0])}) audio tracks detected. Only mono tracks are supported.")
        return rate, data.astype(np.float32)
    except ValueError as e:
            print(f"*** failed to read file: {e}")
            exit(1)

def convert_wav_to_bin(rate, data, bit_size):
    bits = []
    i = 0
    while i < len(data)-1:
        chunk = data[i:i+bit_size]
        mark = tone_power(chunk, 2225, rate)
        space = tone_power(chunk, 2025, rate)
        bit = 1 if mark >= space else 0
        bits.append(bit)
        i += bit_size
    return bits

def convert_bin_to_ascii(data, byte_size):
    message = ""
    i = 0
    while i < len(data)-1:
        close_bit = i + (byte_size-1)
        if data[i] == 0 and (close_bit < len(data) and data[close_bit] == 1):
            bits = data[i+1:close_bit]
            bits.reverse()
            bin_string = ''.join(list(map(str, bits)))
            num = int(bin_string, 2)
            if num <= 176:
                message += chr(num)
            i += byte_size
            continue
        i += 1
    return message

def main(args):
    BLOCK_SIZE = 160
    rate, data = read_wav_file(args.filename)

    assert rate == 48000

    if args.detector_mode:
        detector_mode(rate, data, BLOCK_SIZE)
        exit(0)

    if args.bandpass:
        data = butter_bandpass_filter(data, 1999, 2285, rate, 4)

    binary_data = convert_wav_to_bin(rate, data, BLOCK_SIZE)
  
    message = convert_bin_to_ascii(binary_data, 10)

    print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simulates a 300 baud modem receiver")
    parser.add_argument("filename", help="name of WAV file to read")
    parser.add_argument("-b", "--bandpass", action="store_true", help="enable the use of a bandpass filter")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    parser.add_argument("-d", "--detector-mode", action="store_true", help="enable tone detection mode (useful for debugging)")
    args = parser.parse_args()
    VERBOSE = args.verbose
    main(args)