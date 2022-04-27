from mutagen.wave import WAVE
import wave
import os
import natsort
from config import *

def audio():
    #오디오 정렬 & 파일 합치기
    audio_merge(AUDIO_PATH)
    audio = WAVE(os.path.join(AUDIO_PATH, "sounds.wav"))

    audio_info = audio.info
    length = int(audio_info.length)

    return length

def audio_merge(path):
    os.chdir(path)
    infiles = os.listdir(path)
    infiles_order = natsort.natsorted(infiles)
    outfile = "sounds.wav"

    data= []
    for infile in infiles_order:
        w = wave.open(infile, 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()
    
    output = wave.open(outfile, 'wb')
    output.setparams(data[0][0])
    for i in range(len(data)):
        output.writeframes(data[i][1])
    output.close()