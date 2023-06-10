import os

count = 0

dir = "/Users/claire/repos/github/koremp/nct-taeyong-taco-tts/taeyong/audio"

for file in os.listdir(dir):
    count += 1
    file_oldname = os.path.join(dir, file)
    file_newname_newfile = os.path.join(dir, str(count)+".wav")
    os.rename(file_oldname, file_newname_newfile)
