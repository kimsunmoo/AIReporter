import os

PROJECT_HOME = os.getcwd()
UTAGGER_HOME = os.path.join(PROJECT_HOME, 'utagger/bin')

IMAGE_PATH = os.path.join(PROJECT_HOME, 'image/')
ARTICLE_PATH = os.path.join(PROJECT_HOME, 'article/')
KEYWORD_PATH = os.path.join(PROJECT_HOME, 'key/')
AUDIO_PATH = os.path.join(PROJECT_HOME, 'audio/')
FONT_PATH = os.path.join(PROJECT_HOME, 'font/')
LOGO_IMAGE_PATH = os.path.join(PROJECT_HOME, 'logo_imgae/')

GLOW_CHECKPOINT = "/home/jovyan/glow_cp/glowtts-KSS/glowtts-v2-March-29-2022_04+50AM-3aa165a/best_model.pth.tar"
HIFI_CHECKPOINT = "/home/jovyan/hifi_cp/hifigan-KSS/hifigan-v2-March-29-2022_07+27AM-3aa165a/best_model.pth.tar"
GLOW_CONFIG = "/home/jovyan/glow_cp/glowtts-KSS/glowtts-v2-March-29-2022_04+50AM-3aa165a/config.json"
HIFI_CONFIG = "/home/jovyan/hifi_cp/hifigan-KSS/hifigan-v2-March-29-2022_07+27AM-3aa165a/config.json"