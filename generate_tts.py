import os
import shutil
import re
from unicodedata import normalize
import soundfile as sf

import g2pk
from TTS.utils.synthesizer import Synthesizer
from config import *

g2p = g2pk.G2p()

def normalize_text(text):                    #문장 정규화
    global symbols
    
    text = text.strip()

    for c in ",;:":
        text = text.replace(c, ".")                     
    text = remove_duplicated_punctuations(text)         

    text = jamo_text(text)

    text = g2p.idioms(text)
    text = g2pk.english.convert_eng(text, g2p.cmu)
    text = g2pk.utils.annotate(text, g2p.mecab)
    text = g2pk.numerals.convert_num(text)
    text = re.sub("/[PJEB]", "", text)

    text = alphabet_text(text)

    # remove unreadable characters
    text = normalize("NFD", text)
#     text = "".join(c for c in text if c in symbols)        # 원본코드
# 수정 김선무  22.2.17
    for i in range(len(text)):
        if text[i] not in symbols:
            text = re.sub(text[i], ' ', text)
# /수정
        
    text = normalize("NFC", text)

# 수정 김선무 22.2.17
    text = text.replace('  ', ' ')
# /수정

    text = text.strip()
    if len(text) == 0:
        return ""

    # only single punctuation              
    if text in '.!?':
        return punctuation_text(text)

    # append punctuation if there is no punctuation at the end of the text             #문장부호 없으면 . 추가
    if text[-1] not in '.!?':
        text += '.'

    return text


def remove_duplicated_punctuations(text):                  #문장 부호 중복 제거            ex) 안녕하세요.!     ->     안녕하세요!
    text = re.sub(r"[.?!]+\?", "?", text)         
    text = re.sub(r"[.?!]+!", "!", text)
    text = re.sub(r"[.?!]+\.", ".", text)
    return text


def split_text(text):                                      # 문장부호 기준으로 문장 분리         ex) 안녕하세요. 반갑습니다.    -> texts[0] = 안녕하세요.    ,  texts[1] = 반갑습니다.
    text = remove_duplicated_punctuations(text)

    texts = []
    for subtext in re.findall(r'[^.!?\n]*[.!?\n]', text):
        texts.append(subtext.strip())

    return texts


def alphabet_text(text):                                    # 알파벳을 한글 발음으로 변경
    text = re.sub(r"(a|A)", "에이", text)
    text = re.sub(r"(b|B)", "비", text)
    text = re.sub(r"(c|C)", "씨", text)
    text = re.sub(r"(d|D)", "디", text)
    text = re.sub(r"(e|E)", "이", text)
    text = re.sub(r"(f|F)", "에프", text)
    text = re.sub(r"(g|G)", "쥐", text)
    text = re.sub(r"(h|H)", "에이치", text)
    text = re.sub(r"(i|I)", "아이", text)
    text = re.sub(r"(j|J)", "제이", text)
    text = re.sub(r"(k|K)", "케이", text)
    text = re.sub(r"(l|L)", "엘", text)
    text = re.sub(r"(m|M)", "엠", text)
    text = re.sub(r"(n|N)", "엔", text)
    text = re.sub(r"(o|O)", "오", text)
    text = re.sub(r"(p|P)", "피", text)
    text = re.sub(r"(q|Q)", "큐", text)
    text = re.sub(r"(r|R)", "알", text)
    text = re.sub(r"(s|S)", "에스", text)
    text = re.sub(r"(t|T)", "티", text)
    text = re.sub(r"(u|U)", "유", text)
    text = re.sub(r"(v|V)", "브이", text)
    text = re.sub(r"(w|W)", "더블유", text)
    text = re.sub(r"(x|X)", "엑스", text)
    text = re.sub(r"(y|Y)", "와이", text)
    text = re.sub(r"(z|Z)", "지", text)

    return text


def punctuation_text(text):                                    # 문장 부호를 한글 발음으로 변경
    # 문장부호
    text = re.sub(r"!", "느낌표", text)
    text = re.sub(r"\?", "물음표", text)
    text = re.sub(r"\.", "마침표", text)

    return text


def jamo_text(text):                                           #기본 자모음을 한글 발음으로 변경 
    # 기본 자모음
    text = re.sub(r"ㄱ", "기역", text)
    text = re.sub(r"ㄴ", "니은", text)
    text = re.sub(r"ㄷ", "디귿", text)
    text = re.sub(r"ㄹ", "리을", text)
    text = re.sub(r"ㅁ", "미음", text)
    text = re.sub(r"ㅂ", "비읍", text)
    text = re.sub(r"ㅅ", "시옷", text)
    text = re.sub(r"ㅇ", "이응", text)
    text = re.sub(r"ㅈ", "지읒", text)
    text = re.sub(r"ㅊ", "치읓", text)
    text = re.sub(r"ㅋ", "키읔", text)
    text = re.sub(r"ㅌ", "티읕", text)
    text = re.sub(r"ㅍ", "피읖", text)
    text = re.sub(r"ㅎ", "히읗", text)
    text = re.sub(r"ㄲ", "쌍기역", text)
    text = re.sub(r"ㄸ", "쌍디귿", text)
    text = re.sub(r"ㅃ", "쌍비읍", text)
    text = re.sub(r"ㅆ", "쌍시옷", text)
    text = re.sub(r"ㅉ", "쌍지읒", text)
    text = re.sub(r"ㄳ", "기역시옷", text)
    text = re.sub(r"ㄵ", "니은지읒", text)
    text = re.sub(r"ㄶ", "니은히읗", text)
    text = re.sub(r"ㄺ", "리을기역", text)
    text = re.sub(r"ㄻ", "리을미음", text)
    text = re.sub(r"ㄼ", "리을비읍", text)
    text = re.sub(r"ㄽ", "리을시옷", text)
    text = re.sub(r"ㄾ", "리을티읕", text)
    text = re.sub(r"ㄿ", "리을피읍", text)
    text = re.sub(r"ㅀ", "리을히읗", text)
    text = re.sub(r"ㅄ", "비읍시옷", text)
    text = re.sub(r"ㅏ", "아", text)
    text = re.sub(r"ㅑ", "야", text)
    text = re.sub(r"ㅓ", "어", text)
    text = re.sub(r"ㅕ", "여", text)
    text = re.sub(r"ㅗ", "오", text)
    text = re.sub(r"ㅛ", "요", text)
    text = re.sub(r"ㅜ", "우", text)
    text = re.sub(r"ㅠ", "유", text)
    text = re.sub(r"ㅡ", "으", text)
    text = re.sub(r"ㅣ", "이", text)
    text = re.sub(r"ㅐ", "애", text)
    text = re.sub(r"ㅒ", "얘", text)
    text = re.sub(r"ㅔ", "에", text)
    text = re.sub(r"ㅖ", "예", text)
    text = re.sub(r"ㅘ", "와", text)
    text = re.sub(r"ㅙ", "왜", text)
    text = re.sub(r"ㅚ", "외", text)
    text = re.sub(r"ㅝ", "워", text)
    text = re.sub(r"ㅞ", "웨", text)
    text = re.sub(r"ㅟ", "위", text)
    text = re.sub(r"ㅢ", "의", text)

    return text


def normalize_multiline_text(long_text):                       # 멀티 라인 문장 정규화
    texts = split_text(long_text)
    normalized_texts = [normalize_text(text).strip() for text in texts]
    return [text for text in normalized_texts if len(text) > 0]

def synthesize(text):                                        # 해당 text 내용으로 음성 합성    -> 음성 파일 리턴
    global synthesizer
    wavs = synthesizer.tts(text, None, None)
    return wavs


def generate_tts():
    global synthesizer, symbols
    synthesizer = Synthesizer(
        GLOW_CHECKPOINT,
        GLOW_CONFIG,
        None,
        HIFI_CHECKPOINT,
        HIFI_CONFIG,
        None,
        None,
        False,
    )
    symbols = synthesizer.tts_config.characters.characters
    f = open(os.path.join(ARTICLE_PATH, "article.txt"), 'r')
    texts = f.read()
    f.close() 

    f = open('audiometa', 'w')
    i=1
    for text in normalize_multiline_text(texts):
        wav = synthesizer.tts(text, None, None)
        sf.write(os.path.join(AUDIO_PATH, 'audio{}.wav'.format(i)), wav, 22050, 'PCM_24')
        
        with sf.SoundFile(os.path.join(AUDIO_PATH, 'audio{}.wav'.format(i))) as wavfile:
            f.write(wavfile.frames/wavfile.samplerate, '\n')
        i+=1
    f.close() 
if __name__ == "__main__":
    generate_tts()