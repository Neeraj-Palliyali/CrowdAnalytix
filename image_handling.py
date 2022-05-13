import argparse
import requests
import base64
import os
from io import BytesIO
import json
from PIL import Image


def changeByte(size:int)-> str:
    byte = float(size)
    kb = float(1024)
    mb = float(1024**2)
    gb = float(1024**3)
    tb = float(1024**4)

    if byte<kb:
        return f"{size:.2f} Bytes"
    elif kb<= size < mb:
        return f"{size/kb:.2f} Kib"
    elif mb<= size < gb:
        return f"{size/mb:.2f} Mib"
    elif gb<= size < tb:
        return f"{size/gb:.2f} Gib"
    elif tb<=size:
        return f"{size/tb:.2f} Tib"

def saveAndReturnSize(img_object, getBase64=False)-> dict:
    res = {}
    buffer = BytesIO()
    img_object.save(buffer, format="PNG")
    
    if getBase64:
        # The image is in the buffer
        # This get's encoded ie ascii to bytes 
        img_str = base64.b64encode(buffer.getvalue())
        res['base'] = img_str
    size = changeByte(buffer.tell())
    w,h = img_object.size
    res['size'] = size
    res['width'] = w
    res['hieght'] = h
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url",help = "Enter the url of image", type = str)
    args = parser.parse_args()
    flag = False
    
    try:
        result = {}
        # To use an actual request 
        response = requests.get(args.url)
        try:
            # The response is in bytes so we need to utf encode 
            im = Image.open(BytesIO(response.content))
            # getting details of original image
            original_image = saveAndReturnSize(im)
            result['original_size']=original_image['size']
            result['original_resolution']=f"{original_image['width']} x {original_image['hieght']} pixels" 
        
            # resizing to window 250X250
            im.thumbnail((250,250))
            resized_image = saveAndReturnSize(im, True)
            result['thumbnail_resolution'] = f"{resized_image['width']} x {resized_image['hieght']} pixels"
            result['thumbnail_size'] = resized_image['size']

            # saving the resized image 
            im.save("image/thumbnail.jpg", format='PNG')
            result['thumbnail_path'] = os.getcwd()+"image\thumbnail.jpg"

            # base64 encrypted image in string 
            if 'base' in resized_image:
                result['thumbnail_base64'] = resized_image['base'].decode('utf-8')
            
            # json Output
            print(json.dumps(result))
        
        except Exception as e:
            print("The image is not valid")
        
    except Exception:
        print("Incorrect Url")