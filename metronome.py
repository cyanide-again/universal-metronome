import math
import wave
import numpy as np

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
    if metronome1 != None:
        with wave.open(metronome1, "rb") as f:
            mWav1 = np.frombuffer(f.readframes(f.getnframes()), np.int16)
    else:
        mWav1 = (np.sin(2 * np.pi * 880 * np.linspace(0, 0.1, int(44100*0.1), endpoint=False)) * 32767).astype(np.int16)
    if metronome2 != None:
        with wave.open(metronome2, "rb") as f:
            mWav2 = np.frombuffer(f.readframes(f.getnframes()), np.int16)
    else:
        mWav2 = (np.sin(2 * np.pi * 440 * np.linspace(0, 0.1, int(44100*0.1), endpoint=False)) * 32767).astype(np.int16)
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

# Example
# 
# Generate a metronome at 150 bpm with a time signature of 7/8 and output it to .\output.wav
# generateMetronome("output.wav", 150, 7, 8)