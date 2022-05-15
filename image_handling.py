# For cli arguments
import argparse
# creating web requests
import requests
# For base64 encoding
import base64
# For file path
import os
# For creating buffer of memory for image
from io import BytesIO
# For returning JSON values
import json
# Pillow library for opening and manipulating images
from PIL import Image


# Creating human readble size of files
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

# Returning size, width, height and base64 encoded string(if exists)
def saveAndReturnSize(img_object, getBase64=False)-> dict:
    # Arguments 
    # img_object : image object
    # getBase64 : default false 

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
    res['height'] = h
    return res


if __name__ == "__main__":
    # python image_handling.py https://www.google.com/logos/doodles/2021/uefa-euro-2020-6753651837109267-l.png
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
            result['original_resolution']=f"{original_image['width']} x {original_image['height']} pixels" 
        
            ''' Resizing to window 250X250
            # Takes the largest one from breath and height and finds the corresponding from the aspect ratio of actual image 
            # and takes that and finds the alternative if height taken then width is found and vise versa 

            -->Nearest Neighbour shrinking
            # With help of shrinking factor we take the array value of bits that the images is represented by 
            # and for each row element taken the factor is added onto the index so the whole image shrinks
            # does the same for the coloumn
            # For example if it is a 8x8 and needs to shrink to 4x4 we just take (0,0) (0,2) (0,4) (0,6) (2,0) (2,2) (2,4)
            # and so on
            '''
            im.thumbnail((250,250), Image.NEAREST)
            resized_image = saveAndReturnSize(im, True)
            result['thumbnail_resolution'] = f"{resized_image['width']} x {resized_image['height']} pixels"
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
            print("The image is not valid!!!!")
        
    except Exception:
        print("Incorrect Url!!!")