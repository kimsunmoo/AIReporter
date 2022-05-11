import sys
import os
import cv2
import numpy as np
import natsort
import wave
from PIL import ImageFont, ImageDraw, Image
from config import *

def videoGen(cnt, length, article_name):
    #이미지 크기 1080:720 으로 만들기, 검정색으로 패딩 넣기
    os.chdir(IMAGE_PATH)
    os.system('ffmpeg -i "image-%d.jpg" -vf "scale=-1:-1, pad=1080:720:(1080-iw)/2:(720-ih)/2:color=black" "output%d.jpg"')

    #원본 이미지 삭제
    for i in range(cnt):
        os.remove('image-{}.jpg'.format(i))

    # 이미지로 영상 제작 ffmpeg 사용
    for i in range(1, cnt+1):
        print(length, cnt)
        os.system('ffmpeg -framerate 1/{} -i "output{}.jpg" -c:v libx264 -preset:v veryfast -crf 22 -r 24 -y -pix_fmt yuv420p "test{}.mp4"'.format(length/cnt,i,i))

    dissolve(IMAGE_PATH, cnt) #디졸브 효과
    video_cv2(article_name) # 자막, 마크 등등..

    os.chdir(IMAGE_PATH)
    os.system('ffmpeg -i result2.mp4 -i ../audio/sounds.wav -c:v copy -c:a aac -strict experimental output.mp4')

    print("영상 생성 완료.")

def dissolve(image_path, cnt):
    for i in range(1,cnt):
        v1=os.path.join(image_path, 'test1.mp4')
        v2=os.path.join(image_path, 'test{}.mp4'.format(i+1))
        path = os.path.join(image_path, 'result.mp4')
        cap1 = cv2.VideoCapture(v1)
        cap2 = cv2.VideoCapture(v2)

        if not cap1.isOpened():
            print('video1 open failed!')
            sys.exit

        if not cap2.isOpened():
            print('video2 open failed!')
            sys.exit

        # 두 동영상의 크기, FPS는 같다고 가정하겠습니다.
        # 크기 : 1280 X 720, FPS : 24
        frame_cnt1 = round(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_cnt2 = round(cap2.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap1.get(cv2.CAP_PROP_FPS)

        # 48프레임. 첫 번째 영상의 2초, 두 번째 영상의 2초를 겹쳐서 효과 줌
        effect_frame = int(fps * 0.5)

        print('frame_cnt1 :', frame_cnt1)
        print('frame_cnt2 :', frame_cnt2)
        print('FPS :', fps)

        # 프레임 간 시간 간격
        delay = int(1000 / fps)

        # 저장을 위해 w,h,fourcc 속성 값 추출
        w = round(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = round(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # 출력 동영상 객체 생성
        out = cv2.VideoWriter(path, fourcc, fps, (w, h))


        # 1번 동영상 복사
        for i in range(frame_cnt1 - effect_frame): # 뒤에 2초 남겨두고 앞부분만 저장
            ret1, frame1 = cap1.read()

            if not ret1:
                print('frame read error!')
                sys.exit()

            out.write(frame1)

    #         cv2.imshow('output', frame1) # 프레임1 출력
    #         cv2.waitKey(delay)


        # 1번 동영상 뒷부분과 2번 동영상 앞부분을 합성
        for i in range(effect_frame): # 48번
            ret1, frame1 = cap1.read()
            ret2, frame2 = cap2.read()

            if not ret1 or not ret2:
                print('frame read error!')
                sys.exit()

            # 합성, 짤라내기 위한 변수, w 넓이를 48로 나눔
            dx = int((w / effect_frame) * i)

            # 프레임을 하나 생성
            alpha = i / effect_frame
            frame = cv2.addWeighted(frame1, 1 - alpha, frame2, alpha, 0)

            # 프레임 저장
            out.write(frame)

    #         cv2.imshow('output', frame) # 영상 출력
    #         cv2.waitKey(delay)


        # 2번 동영상 저장
        for i in range(effect_frame, frame_cnt2):
            ret2, frame2 = cap2.read()

            if not ret2:
                print('video read error!')
                sys.exit()

            out.write(frame2)

    #         cv2.imshow('output', frame2)
    #         cv2.waitKey(delay)


        # 프레임을 받아온 후 꼭 release를 써야 한다. 사용한 자원 해제 
        cap1.release()
        cap2.release()
        out.release()
        cv2.destroyAllWindows()
        os.remove(v1)
        os.remove(v2)
        os.rename(path,v1)
    os.rename(v1, 'result.mp4')

def video_cv2(article_name):
    video_file = os.path.join(IMAGE_PATH, "result.mp4") # 동영상 파일 경로
    src2 = cv2.imread(os.path.join(LOGO_IMAGE_PATH, 'logo.png')) #로고파일 읽기
    src3 = cv2.imread(os.path.join(LOGO_IMAGE_PATH, 'logo2.png'))
    cap = cv2.VideoCapture(video_file) # 동영상 캡쳐 객체 생성  ---①
    w = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # 또는 cap.get(3)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # 또는 cap.get(4)
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(os.path.join(IMAGE_PATH, 'result2.mp4'), fourcc, fps, (int(width), int(height)))
    
    caption_frames = []
    captions = []
    with open(os.path.join(PROJECT_HOME, 'audiometa'), 'r') as f:
        caption_frames.append(f.readline()*fps)
        captions.append(f.readline())
    print(caption_frames)
    print(captions)
    caption_index = 0

    if cap.isOpened():                 # 캡쳐 객체 초기화 확인
        cur_frame = 0
        while True:
            ret, img = cap.read()      # 다음 프레임 읽기      --- ②
            if ret:                     # 프레임 읽기 정상
                cur_frame += 1
                if cur_frame > caption_frames[caption_index]:
                    caption_index += 1
                    cur_frame = 1

                rows, cols, channels = src2.shape #로고파일 픽셀값 저장
                roi = img[70:rows+70,900:cols+900] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
                
                gray = cv2.cvtColor(src2, cv2.COLOR_BGR2GRAY) #로고파일의 색상을 그레이로 변경
                ret, mask = cv2.threshold(gray, 160, 255, cv2.THRESH_BINARY) #배경은 흰색으로, 그림을 검정색으로 변경
                mask_inv = cv2.bitwise_not(mask)
                
                src1_bg = cv2.bitwise_and(roi,roi,mask=mask) #배경에서만 연산 = src1 배경 복사
                src2_fg = cv2.bitwise_and(src2,src2, mask = mask_inv) #로고에서만 연산

                dst = cv2.bitwise_or(src1_bg, src2_fg) #src1_bg와 src2_fg를 합성
                img[70:rows+70,900:cols+900] = dst #src1에 dst값 합성               
                
                
                rows2, cols2, channels2 = src3.shape #로고파일 픽셀값 저장
                roi2 = img[550:rows2+550,40:cols2+40] #로고파일 필셀값을 관심영역(ROI)으로 저장함.

                img[550:rows2+550,40:cols2+40] = src3 #src1에 dst값 합성         
                
                
#                 rows2, cols2, channels2 = src3.shape #로고파일 픽셀값 저장
#                 roi2 = img[550:rows2+550,40:cols2+40] #로고파일 필셀값을 관심영역(ROI)으로 저장함.
#                 img[550:rows2+550,40:cols2+40] = src3 #src1에 dst값 합성   
                np_array = np.array(img)
                
#                 cv2.rectangle(np_array, (40, 550), (190, 661), (53, 136, 5), 3 )
                cv2.rectangle(np_array, (190, 550), (1040, 660), (255, 255, 255), -1 )
                output = PutText(FONT_PATH, np_array, captions[caption_index], font_size = 50, xy = (210, 585), bgr = (0, 0, 0))
                out.write(output)
            else:                       # 다음 프레임 읽을 수 없슴,
                break                   # 재생 완료
    else:
        print("can't open video.")      # 캡쳐 객체 초기화 실패

    out.release()
    cap.release()                       # 캡쳐 자원 반납l
    cv2.destroyAllWindows()

def PutText(font_path, src, text, font_size, xy, bgr):

#     font = ImageFont.load_default()
    fontpath = os.path.join(font_path, "HMFMMUEX.TTC")
    font = ImageFont.truetype(fontpath, font_size)
    src_pil = Image.fromarray(src)
    draw = ImageDraw.Draw(src_pil)
    draw.text(xy, text, font=font, fill=bgr,style="bold")
    target = np.array(src_pil)
    return target

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