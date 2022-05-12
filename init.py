import os
import shutil
import sys

from config import *

def init():
    if os.path.exists(ARTICLE_PATH) == False:
        os.mkdir(ARTICLE_PATH) 
    if os.path.exists(IMAGE_PATH):
        shutil.rmtree(IMAGE_PATH)
    os.mkdir(IMAGE_PATH) 
    if os.path.exists(KEYWORD_PATH) == False:
        os.mkdir(KEYWORD_PATH) 
    if os.path.exists(FONT_PATH) == False:
        os.mkdir(FONT_PATH) 
    if os.path.exists(AUDIO_PATH):
        shutil.rmtree(AUDIO_PATH)
    os.mkdir(AUDIO_PATH)