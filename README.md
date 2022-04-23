# What is this?
This python program alerts when there is a attendance for your zoom class (by processing zoom chat) and asks you if you want to attend via Telegram. The operations goes like this;
- Get screenshot of Zoom Chat 
- OCR screenshot
- If algorithm detects a attendance it will alert you via Telegram and asks you if you want to attend.
- If you answer "yes". It will write down to chat your name-surname-id

# Why I created this?
I have a class where my professor takes attendance with zoom chat, but the problem is you have 1 minutes to write down your name and surname when he says its "attendance time!"
there were times, which I was attending to the class but I could not write down my name because I was taking notes, could not hear etc.

# Is it working?
Yes and no, it is working for my class but you may need to change it according to your desires. Algorithm is not perfect, even is not good but it works for now...

# Some Notes
- I used OCR because there is no exact zoom api that you can use for getting the zoom chat.
- As I said above, detection algorithm probably sucks, i will modify it but dont know when. (I am saying algorithm but I know it is just a basic if check :( )
- Currently telegram bot is not working async. I know it should be, i will modify it when i have time.
- I even don't know why I have published this on github, i know nobody is going to use it but why not?

# Usage
- Change telegram bot api to yours.
- Change your name-surname-id
- Change detection algorithm. IT SUCKS!!!!!!!!!!!
- Install used packages.
- python3 attend-detect.py 
