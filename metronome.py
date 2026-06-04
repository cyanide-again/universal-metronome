import argparse
import sys
import math
import wave
import numpy as np

def help():
    print(f"""
Generates a metronome as a .wav file with a customizable BPM and time signature.

Usage: python {sys.argv[0]} <outputfp> [OPTIONS]

Options:
    -h, --help
        Displays this help message
    -bpm [BPM]
        The beats per minute (AKA tempo) of the metronome
        Default value: 120
    -t, --timesig [NUMERATOR/DENOMINATOR]
        The time signature of the metronome
        Default value: 4/4
    -m, --measures [MEASURES]
        How many bars to generate
        Default value: 8
    -m1, --metronome1 [METRONOME1]
        The file path to the sound to play for the first beat of a bar
        Default value: None
    -m2, --metronome2 [METRONOME2]
        The file path to the sound to play for the other beats in a bar
        Default value: None

Example usages:
    python {sys.argv[0]} output.wav -t 7/8 -m1 path_to_file.wav -m2 path_to_other_file.wav
    python {sys.argv[0]} output.wav -bpm 210 -m 16
""")

def generateMetronome(outputfp: str, bpm: float = 120, numerator: float = 4, denominator: float = 4, measures: int = 8, metronome1: str | None = None, metronome2: str | None = None) -> None:
    """
    Generate a metronome as a .wav file and write it to `outputfp`.

    :param bpm: The beats per minute of the metronome.
    :param numerator: The number at the top of the time signature (e.g. 3/4 numerator is 3).
    :param denominator: The number at the bottom of the time signature (e.g. 3/4 numerator is 4).
    :param measures: How many bars of the metronome to generate.
    :param metronome1: The file path to the first metronome sample.
    :param metronome2: The file path to the second metronome sample."""
    # Load metronome samples
    t = np.linspace(0, 0.1, int(44100 * 0.1), endpoint=False)
    if metronome1 != None:
        with wave.open(metronome1, "rb") as f:
            mWav1 = np.frombuffer(f.readframes(f.getnframes()), np.int16)
    else:
        mWav1 = (((2 / np.pi) * np.arcsin(np.sin(2 * np.pi * 880 * t))) * 32767).astype(np.int16)
    if metronome2 != None:
        with wave.open(metronome2, "rb") as f:
            mWav2 = np.frombuffer(f.readframes(f.getnframes()), np.int16)
    else:
        mWav2 = (((2 / np.pi) * np.arcsin(np.sin(2 * np.pi * 440 * t))) * 32767).astype(np.int16)
    sampleRate = 44100
    beatRate = int(np.ceil(sampleRate*((60/bpm) * (4/denominator))))
    measureBuffer: np.ndarray = np.zeros((beatRate*math.ceil(numerator)), np.int16)
    with wave.open(outputfp, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sampleRate)
        for beat in range(0,math.ceil(numerator)):
            beatBuffer = np.zeros(int(beatRate), np.int16)
            metronome = mWav1 if beat == 0 else mWav2
            l = min(len(metronome), beatRate)  # Make sure the metronome sample doesn't go past the length of each beat
            beatBuffer[:l] = metronome[:l]
            measureBuffer[beat*beatRate:(beat*beatRate)+len(beatBuffer)] = beatBuffer
        measureBuffer = measureBuffer[:round(beatRate*numerator)]
        measureBuffer = np.tile(measureBuffer, measures)
        f.writeframes(measureBuffer)

args = sys.argv[1:]
if args == [] or "-h" in args or "--help" in args:
    help()
else:
    outputfp = args[0]
    bpm = 120
    numerator = 4
    denominator = 4
    measures = 8
    metronome1 = None
    metronome2 = None
    if "-bpm" in args:
        bpm = float(args[args.index("-bpm") + 1])
    if "-t" in args or "--timesig" in args:
        numerator, denominator = map(float, args[args.index("-t" if "-t" in args else "--timesig") + 1].split("/"))
    if "-m" in args or "--measures" in args:
        measures = int(args[args.index("-m" if "-m" in args else "--measures") + 1])
    if "-m1" in args or "--metronome1" in args:
        metronome1 = args[args.index("-m1" if "-m1" in args else "--metronome1") + 1]
    if "-m2" in args or "--metronome2" in args:
        metronome2 = args[args.index("-m2" if "-m2" in args else "--metronome2") + 1]
    generateMetronome(outputfp, bpm, numerator, denominator, measures, metronome1, metronome2)