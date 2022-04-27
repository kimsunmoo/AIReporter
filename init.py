import os
import shutil
import sys

from config import *

def init():
    if os.path.exists(ARTICLE_PATH) == False:
        os.mkdir(ARTICLE_PATH) 
    if os.path.exists(IMAGE_PATH) == False:
        os.mkdir(IMAGE_PATH) 
    if os.path.exists(KEYWORD_PATH) == False:
        os.mkdir(KEYWORD_PATH) 
    if os.path.exists(FONT_PATH) == False:
        os.mkdir(FONT_PATH) 
    if os.path.exists(AUDIO_PATH) == False:
        shutil.rmtree(AUDIO_PATH)
    os.mkdir(AUDIO_PATH)
    
    rmCheck_point(os.path.join(AUDIO_PATH, ".ipynb_checkpoints")) #audio checkpoint 지우기
    rmCheck_point(os.path.join(AUDIO_PATH, ".ipynb_checkpoints")) #audio checkpoint 지우기
    rmImg(IMAGE_PATH) # 폴더안 모든 파일 삭제

    if(os.path.isfile(os.path.join(AUDIO_PATH, 'sounds.wav'))):
        os.remove(os.path.join(AUDIO_PATH, 'sounds.wav'))

    print("기사 제목 입력")
    article_name=  input()
    
    return article_name


def rmImg(filePath):
    for file in os.scandir(filePath):
        os.remove(file.path)

def rmCheck_point(path):
    if(os.path.isdir(path)):
        shutil.rmtree(path)