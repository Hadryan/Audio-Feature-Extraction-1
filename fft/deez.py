import os
import config
# #
#
amount = 10

# for i in range(0,amount):
#     audioin = ""
#
#     file = config.splitSong('letgo.wav', i, i+1, 10)
#     audioin+=file
#     audioin+=' '
#     com = "spleeter separate -o splitouput -B librosa -p spleeter:4stems " + audioin
#     os.system(com)

file = config.splitSong('letgo.wav', 0, 1, 4)
com = "spleeter separate -o wavs\\splitoutput -B librosa -p spleeter:4stems " + file
os.system(com)
print(file)


for i in range(0,amount):
    path = 'temp'+str(i)
print(com)

