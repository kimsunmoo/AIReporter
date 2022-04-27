import argparse
import os
import sys

from audio import audio
from getKeyword import keyFile
from imageSearch import imageSearch
from init import init
from generate_tts import generate_tts
from videoGenerate import videoGen

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search_api_key', required=True)
    parser.add_argument('--search_cs_key', required=True)

    args = parser.parse_args()
    
    generate_tts() # 음성 생성
    article_name = init() # 프로젝트 초기화 및 제목 입력
    keyFile() # 키워드 추출 
    cnt = imageSearch(args) # 키워드로 사진 검색 및 저장
    length = audio() # 음성 합치기
    videoGen(cnt, length, article_name) # 비디오 생성