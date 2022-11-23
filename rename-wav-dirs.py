import os
import glob

file_list = glob.glob('./multi-speaker-tacotron-tensorflow/datasets/taeyong/*/*.wav')

print(len(file_list))

for idx, file in enumerate(file_list):
    print(idx)
    os.rename(file, './multi-speaker-tacotron-tensorflow/datasets/taeyong/audio/{}.wav'.format(idx))