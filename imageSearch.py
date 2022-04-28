import os
import ssl
import urllib3
from difPy import dif
from PIL import Image
import requests as r
import urllib.request as ur
from config import * 
def imageSearch(args):
    get_image(args) # google custom search
    rm_dup()    # 이미지 중복 제거
    changeName(IMAGE_PATH,'image') # 이미지 이름 변경
    cnt = len(os.listdir(IMAGE_PATH)) #이미지 개수

    for i in range(0, 5):
        resize_image(os.path.join(IMAGE_PATH, "image{}.jpg".format(i)))  # 이미지 크기 변경
    for i in range(0, 5):
        resize_image2(os.path.join(IMAGE_PATH, "image{}.jpg".format(i))) # 이미지 크기 변경

    for i in range(0, cnt): # 가로가 1080, 세로가 720보다 큰 이미지 제거
        f_name = os.path.join(IMAGE_PATH, "image{}.jpg".format(i))
        original_image = Image.open(f_name)
        width, height = original_image.size
        original_image.close()
        if(width > 1080 or height > 720):
            os.remove(f_name)

    changeName(IMAGE_PATH,'image-')    # 이미지 이름 변경
    cnt = len(os.listdir(IMAGE_PATH)) # 이미지 개수

    return cnt

def get_image(args):
    context = ssl._create_unverified_context()
    
    f = open(os.path.join(KEYWORD_PATH, 'keys.txt'),'r',encoding="utf-8")
    query = f.readline()
    f.close()

    api_key = args.search_api_key
    cs_key = args.search_cs_key

    print(query)
    url = "https://www.googleapis.com/customsearch/v1"
    for j in range(0, 11, 9):
        param = {
            "key" : api_key,
            "cx" : cs_key,
            "q" : query,
            "fileType" : "jpg",
            "searchType" : "image",
            "num" : 7,
            "start":j,
            "imgSize"
            "dateRestrict" : "m2",
            "imgSize" : "xlarge"
        }

        s = r.Session()
        urllib3.disable_warnings()
        test = s.get(url,params=param,verify=False).json()

        savePath = "./image"
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            for i in range(0, len(test.get("items"))):
                print(test.get('items')[i].get("title"))
                print(test.get('items')[i].get("link"))
                FileName = os.path.join(savePath, "google" + str(i) + str(j) + '.jpg')
                print('full name : {}'.format(FileName))
                ur.urlretrieve(test.get("items")[i].get("link"),FileName)
        except:
            continue
            
def rm_dup():
    search = dif("./image/",similarity="normal",sort_output=False, delete=False)
    dup = set(search.lower_quality)
    for i in dup:
        os.remove(i)
        

def changeName(path, cName):
    i = 0
    for filename in os.listdir(path):
        print(path+filename, '=>', path+str(cName)+str(i)+'.jpg')
        os.rename(path+filename, path+str(cName)+str(i)+'.jpg')
        i += 1
        
def resize_image(filename):
    original_image = Image.open(filename)
    width, height = original_image.size
    
    max_width = 1080
    max_height = 720
    
    new_width = width
    new_height = height
    
    if height > max_height:
        new_height = 720
        new_width = max_height * (float(width) / float(height))
    if width > max_width:
        new_width = 1080
        new_height = max_width * (float(height) / float(width))

    if(new_width % 2 != 0):
        new_width += 1;
    if(new_height % 2 != 0):
        new_height += 1;

    resize_image = original_image.resize((int(new_width), int(new_height)))
    resize_image.save(filename)
    
def resize_image2(filename):
    original_image = Image.open(filename)
    width, height = original_image.size
    

    if(width % 2 != 0):
        width += 1;
    if(height % 2 != 0):
        height += 1;

    resize_image = original_image.resize((int(width), int(height)))
    resize_image.save(filename) 
