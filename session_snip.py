import soundfile
import numpy as np
import os

outpath="/Users/christof/Documents/CleanedSessions/"

for dirpath, dirnames, filenames in os.walk("/Users/christof/Dropbox/JamSessions"):
    print(f"Entering {dirpath}")
    for file in filenames:
        base, ext = os.path.splitext(file)
        if ext == ".flac":
            data, samplerate = soundfile.read(os.path.join(dirpath, file))
        else:
            print(f"Skipping file {file}")
            continue
        soundfile.write(os.path.join(outpath, base + ".wav"), data=data, samplerate=samplerate, format="WAV")
