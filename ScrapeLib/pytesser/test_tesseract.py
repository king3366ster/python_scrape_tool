from PIL import Image, ImageEnhance, ImageFilter
import pdb
import numpy as np
# import matplotlib.pyplot as plt
import pytesseract
from PIL import ImageEnhance

def inverse_image (img):
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            temp = 255 if pixels[x, y] < 128 else 0
            img.putpixel((x,y), (temp,))
    return img

def black_image (img):
    pixels = img.load()
    for x in range(img.width):
        for y in range(img.height):
            temp = 255 if pixels[x, y] > 224 else 0
            img.putpixel((x,y), (temp,))
    return img

def format_image(img):
    img_n = img.convert('L')
    img_n = img_n.resize((img.size[0] * 4, img.size[1] * 4), Image.NEAREST)
    return img_n

def enhance_image(img):
    img_n = ImageEnhance.Brightness(img).enhance(1.6)
    img_n = ImageEnhance.Contrast(img_n).enhance(2)
    return img_n

def smooth_image(img):
    img_s = img.filter(ImageFilter.GaussianBlur(radius = 2))
    img_s = black_image(img_s)
    # img_s = img_s.filter(ImageFilter.EDGE_ENHANCE)
    return img_s

def recognize_numbers(img):
    # img.show()
    img_n = format_image(img)
    img_n = enhance_image(img_n)
    img_n = black_image(img_n)
    img_n = smooth_image(img_n)
    img_n.show()
    result = pytesseract.image_to_string(img_n, lang='eng', config='-oem 3 -psm 7 digits')
    # result = pytesseract.image_to_string(img_n, lang='eng', config='-oem 3 -psm 7')
    # result = pytesseract.image_to_string(img_n, lang='chi_sim', config='-oem 3 -psm 7')
    return result

if __name__ == '__main__':
    # im = Image.open('checkcode0.png')
    # im = Image.open('testphone2.png')
    im = Image.open('testphone2.png')
    print recognize_numbers(im)
