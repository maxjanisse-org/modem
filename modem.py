# Max Janisse - 2026
import scipy.io.wavfile as wav
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
        bit = 1 if mark >= space else 0
        if VERBOSE:
            print(f"[{i}] M:{mark}, S:{space}, B:{bit}\n{chunk}")
        binary_data.append(bit)
    return binary_data

def convert(rate, data, bit_size):
    d = []
    i = 0
    while i < len(data)-1:
        if data[i] >= rate/bit_size:
            chunk = data[i:i+bit_size]
            mark = tone_power(chunk, 2225, rate)
            space = tone_power(chunk, 2025, rate)
            bit = 1 if mark >= space else 0
            d.append(bit)
            i += bit_size
            continue
        i += 1
    return d

def convert_bin_to_ascii(data, byte_size):
    message = ""
    i = 0
    while i < len(data)-1:
        if data[i] == 0:
            bits = data[i+1:i+(byte_size-1)]
            bits.reverse()
            bin_string = ''.join(list(map(str, bits)))
            message += chr(int(bin_string, 2))
            i += byte_size
            continue
        i += 1
    return message

def main(args):
    rate, data = read_wav_file(args.filename)

    assert rate == 48000

    # Normalize the Gain to -3db

    #if sample_count_check > 0:
    #    pad_size = (args.block_size - sample_count_check) + args.block_size
    #    if VERBOSE:
    #        print(f"# of Samples: {len(data)}, Padding Size: {pad_size} zeros")
    #    data = np.concatenate((np.zeros(pad_size, dtype=np.float16), data))

    binary_data = convert_wav_to_bin(rate, data, args.block_size)
    #binary_data = convert(rate, data, args.block_size)
  
    message = convert_bin_to_ascii(binary_data, 10)
    #for j in range(0, len(binary_data), 10):
    #    bits = binary_data[j+1:j+9]
    #    bits.reverse()
    #    binary_str = ''.join(list(map(str, bits)))
    #    message += chr(int(binary_str, 2))
    print(message)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("filename", help="Name of WAV file to read")
    parser.add_argument("-b", "--block-size", default=160, help="the number of samples per block")
    parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
    args = parser.parse_args()
    VERBOSE = args.verbose
    main(args)