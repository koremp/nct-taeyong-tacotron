import glob
import os

from pydub import AudioSegment
from pydub.silence import split_on_silence

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def getWavFilesFromPath(path):
    return glob.glob(path)

def split_silence_from_Wav(idx, wavPath):
    # Load your audio.
    song = AudioSegment.from_wav(wavPath)

    # Split track where the silence is 2 seconds or more and get chunks using
    # the imported function.
    chunks = split_on_silence (
        # Use the loaded audio.
        song,
        # Specify that a silent chunk must be at least 2 seconds or 2000 ms long.
        min_silence_len = 400,
        # Consider a chunk silent if it's quieter than -16 dBFS.
        # (You may want to adjust this parameter.)
        silence_thresh = -40
    )

    os.mkdir('./output/{0}/'.format(idx))

    # Process each chunk with your parameters
    for i, chunk in enumerate(chunks):
        # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
        silence_chunk = AudioSegment.silent(duration=100)
        # Add the padding chunk to beginning and end of the entire chunk.
        audio_chunk = silence_chunk + chunk + silence_chunk
        # Normalize the entire chunk.
        normalized_chunk = match_target_amplitude(audio_chunk, -20.0)
        # make file


        # Export the audio chunk with new bitrate.no
        chunk.export("./output/{0}/{1}.wav".format(idx, i), format="wav")


path = './taeyong-wav/*/*.wav'
files = getWavFilesFromPath(path)


for idx, file in enumerate(files):
    print(idx, file)
    split_silence_from_Wav(idx, file)

