import argparse
import requests
import base64
import os
from io import BytesIO
import sys
from PIL import Image


def changeByte(size:int)-> str:
    byte = float(size)
    kb = float(1024)
    mb = float(1024**2)
    gb = float(1024**3)
    tb = float(1024**4)

    if byte<kb:
        return f"{size} Bytes"
    elif kb<= size < mb:
        return f"{size/kb} Kib"
    elif mb<= size < gb:
        return f"{size/mb} Mib"
    elif gb<= size < tb:
        return f"{size/gb} Gib"
    elif tb<=size:
        return f"{size/tb} Tib"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url",help = "Enter the url of image", type = str)
    args = parser.parse_args()
    flag = False
    while flag == False:
        try:
            result = {}
            # To use an actual request 
            response = requests.get(args.url)
            img_details = BytesIO(response.content)
            # The response is in bytes so we need to utf encode 
            im = Image.open(img_details)
            im.save(img_details, format="PNG")
            result['original_size']=changeByte(img_details.tell())
            w,h = im.size
            result['original_resolution']=f"{w} x {h}" 
        
            im.thumbnail((250,250))
            # im.show()
            buffered = BytesIO()
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im.save(buffered, format='JPEG')
            im.save("image/thumbnail.jpg", format='JPEG')
            result['tumbnail_path'] = os.getcwd()+"image\thumbnail.jpg"
            size = buffered.tell()
            w,h = im.size
            result['thumbnail_resolution'] = f"{w} x {h}" 
            result['thumbnail_size'] = changeByte(size) 
            img_str = base64.b64encode(buffered.getvalue())
            # result['thumbnail_base64'] = img_str
            
            flag = True
            print(result)
            
            
        except Exception as e:
            print(e)
            print("Incorrect Url")
            args.url = input("Please enter a valid url:")