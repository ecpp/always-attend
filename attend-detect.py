import datetime
from time import sleep
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pygetwindow
import pyautogui
from timeit import default_timer as timer
import telegram
import requests
import json
import keyboard

# CONFIGURATION

TELEGRAM_BOT_TOKEN = 'xxx'
TELEGRAM_CHAT_ID = 'xxx'
writeToChat = "name surnmame"  # to write for attendance. in my case NAME SURNAME
path1 = '/Users/xxxx/Desktop/temp1.png'
path2 = '/Users/xxxx/Desktop/temp2.jpg'
timezone = 3  # in my case its +3 so its 3. it is needed for telegram api to check whether last message is sent on time!
zoom_window_name = 'Sohbet'  # name of the zoom application window

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
last_input = "no"


def get_user_input():
    global last_input
    link = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/getUpdates"
    try:
        print("Telegram connection success!")
        data = requests.get(link).text
    except Exception as e:
        print("Error while connecting to telegram servers! ", e)
        return last_input
    data = json.loads(data)
    data_to_dict = data['result']
    for obj in data_to_dict:
        time_of_message = obj['message']['date']  # UNIX time
        time_of_message = datetime.datetime.utcfromtimestamp(time_of_message)
        now = datetime.datetime.now()
        if (((time_of_message.minute == now.minute) or (time_of_message.minute == now.minute - 1)) and (
                time_of_message.hour + timezone == now.hour)):
            last_input = obj['message']['text']
            return last_input


def ocr_process():  # take SS of window and process it with ocr
    window = pygetwindow.getWindowsWithTitle(zoom_window_name)[0]
    print("Found window.")
    x1 = window.left
    y1 = window.top
    height = window.height
    width = window.width

    x2 = x1 + width
    y2 = y1 + height
    print("Taking screenshot.")
    pyautogui.screenshot(path1)
    start = timer()
    print("Image processing in progress...")

    # IMAGE CORRECTION AND PROCESSING
    im = Image.open(path1)
    im = im.crop((x1 + 20, y1 + 70, x2, y2 - 150))
    im.save(path1)
    im = Image.open(path1)
    im = im.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(2)
    im = im.convert('1')

    im.save(path2)
    text = pytesseract.image_to_string(Image.open(path2))
    end = timer()
    print("Image processing completed. It took:", (end - start))
    print(text)
    return text


def attendance_detect():  # Attendance detection algorithm. Needs to be improved.
    global last_input
    len1 = len(ocr_process())
    sleep(3)
    len2 = len(ocr_process())
    sleep(3)
    len3 = len(ocr_process())

    if len2 - len1 > 10 or len3 - len2 > 10:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Attendance detected...")
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(path1, 'rb'))
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Do you want to attend? You have 30 seconds!")
        sleep(30)
        last_input = get_user_input()
        sleep(3)
        if last_input == "yes" or last_input == "Yes":
            print("Attended!")
            keyboard.write(writeToChat)
            keyboard.press_and_release('enter')
        else:
            print("not attend.!")
        last_input = "no"

    sleep(15)


if __name__ == '__main__':
    while True:
        attendance_detect()
