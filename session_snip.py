import soundfile
import numpy as np
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

outpath="/Users/christof/Documents/CleanedSessions/"


# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)


for dirpath, dirnames, filenames in os.walk("/Users/christof/Dropbox/JamSessions"):
    print(f"Entering {dirpath}")
    for file in filenames:
        file_to_read = os.path.join(dirpath, file)
        base, ext = os.path.splitext(file)
        if ext == ".flac":
            data, samplerate = soundfile.read(file_to_read)
            # export the full file
            file_to_read = os.path.join(outpath, base + ".wav")
            soundfile.write(file_to_read, data=data, samplerate=samplerate, format="WAV")
        elif ext != ".wav":
            print(f"Skipping file {file}")
            continue

        segment = AudioSegment.from_wav(file_to_read)

        chunks = split_on_silence(
            segment,
            min_silence_len=2000,
            silence_thresh=-30,
            seek_step=100
        )

        for i, chunk in enumerate(chunks):
            if chunk.duration_seconds < 10:
                continue

            # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
            silence_chunk = AudioSegment.silent(duration=500)

            # Add the padding chunk to beginning and end of the entire chunk.
            audio_chunk = silence_chunk + chunk + silence_chunk

            # Normalize the entire chunk.
            # normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

            # Export the audio chunk with new bitrate.
            export_file = os.path.join(outpath, f".//{file}_chunk{i}.mp3")
            print(f"Exporting {export_file}")
            audio_chunk.export(
                export_file,
                bitrate="192k",
                format="mp3")

