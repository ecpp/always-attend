#!/usr/bin/env python3

from time import sleep
import numpy as np
from PIL import ImageGrab
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from textblob import TextBlob
import pygetwindow
import pyautogui
from timeit import default_timer as timer
import telegram
import requests
import json
import keyboard


TELEGRAM_BOT_TOKEN = 'xxxx'
TELEGRAM_CHAT_ID = 'xxxxx'
lastinput = "no"

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)




path = '/Users/Eren/Desktop/result.png' #path where SS of the window will be saved.

len1 = 0
len2 = 0
len3 = 0

def getUserinput():
    link = "https://api.telegram.org/botYOURTELEGRAMTOKEN" #bot will stay (botXXXXXXXXXXXX)
    data = requests.get(link).text
    data = json.loads(data)
    Dict = data['result']
    for obj in Dict:
        lastinput = obj['message']['text']
    return lastinput

def ocrProcess(): #take SS of window and process it with ocr
    window = pygetwindow.getWindowsWithTitle('Zoom Chat')[0] #window name of zoom chat
    print("Found window.")
    x1 = window.left
    y1 = window.top
    height = window.height
    width = window.width

    x2 = x1 + width
    y2 = y1 + height
    print("Taking screenshot.")
    pyautogui.screenshot(path)
    start = timer()
    print("Image processing in progress...")
    im = Image.open(path)
    im = im.crop((x1+20, y1+70, x2, y2-150))
    im.save(path)
    im = Image.open(path) # the second one 
    im = im.filter(ImageFilter.MedianFilter()) #some corrections for ocr
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')
    im.save('/Users/Eren/Desktop/temp2.jpg')
    text = pytesseract.image_to_string(Image.open('/Users/Eren/Desktop/temp2.jpg'))
    end = timer()
    print("Image processing completed. It took:", (end - start))
    return text

while True:
    len1 = len(ocrProcess())
    print(len(ocrProcess()))
    sleep(2)
    len2 = len(ocrProcess())
    print(len(ocrProcess()))
    sleep(2)
    len3 = len(ocrProcess())
    print(len(ocrProcess()))
    
    if(len2-len1 > 10 or len3-len2 > 10):
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Attendance detected...")
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(path, 'rb'))
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Do you want to attend? You have 30 seconds!")
        sleep(30)
        if(getUserinput()=="yes"):
            print("Attended!")
            keyboard.write('What should it write down???')
            keyboard.press_and_release('enter')
        else:
            print("not attend.!")
        
    print(len(ocrProcess()))
    sleep(15)
