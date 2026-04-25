# Max Janisse - 2026
import scipy.io.wavfile as wav
import numpy as np
import argparse

VERBOSE = False

def tone_power(samples, f, fs):
    I = 0
    Q = 0
    length = len(samples) - 1
    for n in range(length):
        angle = 2. * np.pi * f * (n / fs)
        I += (samples[n] * np.cos(angle))
        Q += (samples[n] * np.sin(angle))
    return I**2 + Q**2

def read_wav_file(filename):
    try:
        rate, data = wav.read(filename)
        if type(data[0]) is np.ndarray:
            raise ValueError(f"Multiple ({len(data[0])}) audio tracks detected. Only mono tracks are supported.")
        return rate, data
    except ValueError as e:
            print(f"*** failed to read file: {e}")
            exit(1)

def convert_wav_to_bin(rate, data, chunk_size):
    binary_data = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        mark = tone_power(chunk, 2225, rate)
        space = tone_power(chunk, 2025, rate)
        bit = 0 if space > mark else 1
        binary_data.append(bit)
        if VERBOSE:
            print(f"Space: {space}, Mark: {mark} = {bit}")
    return binary_data

def main(args):
    rate, data = read_wav_file(args.filename)

    binary_data = convert_wav_to_bin(rate, data, args.block_size)

    message = ""
    for j in range(0, len(binary_data), 10):
        bits = binary_data[j+1:j+9]
        bits.reverse()
        binary_str = ''.join(list(map(str, bits)))
        message += chr(int(binary_str, 2))
    print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("filename", help="Name of WAV file to read")
    parser.add_argument("-b", "--block-size", default=160, help="Set the size of ")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    VERBOSE = args.verbose
    main(args)