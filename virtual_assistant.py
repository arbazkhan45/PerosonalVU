from tkinter import *
import tkinter.messagebox as tm
import pyttsx3
from threading import Thread
import time
import webbrowser
import datetime
from wikipedia import summary
import os
from tkinter import filedialog
import random
import speech_recognition
from plyer import notification
from bs4 import BeautifulSoup
import requests
from functools import partial

engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices', )
engine.setProperty('voice', voices[0].id)
engine2 = pyttsx3.init("sapi5")
voices2 = engine2.getProperty('voices', )
engine2.setProperty('voice', voices2[0].id)
root = Tk()
root.title("PersonalVU")
root.geometry("550x650")
root.iconbitmap("p.ico")
username = StringVar()
temp_var = StringVar()


def speak(text):
    """
    Speaks the given the text
    """
    root.config()
    showing_commands.insert(END, f"VU: {text}\n")
    engine.say(text=text)
    engine.runAndWait()


def listening():
    """
    listen and then convert into text
    """
    q = ""
    r = speech_recognition.Recognizer()
    try:

        with speech_recognition.Microphone() as source:

            showing_commands.insert(END, "Listening...\n")
            st_bar_change("Listening...", "green")
            r.pause_threshold = 1
            audio = r.listen(source, phrase_time_limit=5)

            showing_commands.insert(END, f"VU: Recognizing...\n")
            st_bar_change("Recognizing...", "green")
    except Exception as e:
        exit()
    try:
        q = r.recognize_google(audio, language="en-us")

        showing_commands.insert(END, f"User: {q}\n")
        return q
    except Exception:

        st_bar_change("Error due to nework connection! Please say again", "red")
        # speak("Error due to nework connection! Please say again")

        return "error"


# def audio_text(audiof):
#     # Initialize recognizer class
#     r = speech_recognition.Recognizer()
#     # audio object
#     audio = speech_recognition.AudioFile(rf"C:\Users\Arbaz Khan\PycharmProjects\PythonTuts\PythonPrograms\{audiof}")
#     # read audio object and transcribe
#     with audio as source:
#         audio = r.record(source)
#         result = r.recognize_google(audio)
#     print(result)
#     return str(result)


def start_vu():
    """
    handling queries and tasks
    """
    showing_commands.delete('1.0', END)
    st_bar_change("Welcome to your PersonalVU!", "white")
    engine.runAndWait()
    speak(f"Hello {username.get()}! I am VU")

    engine.runAndWait()
    speak("How may I assist you?")

    while True:
        # query = input("Enter your query\n").lower()
        query = listening().lower()
        # query = audio_text(query).lower()

        if "reminder" in query or "notification" in query:
            try:
                engine.runAndWait()
                speak("Which remainder do you want to set (Title)?")
                # query = input("")
                query = listening().lower()
                # query = audio_text(query)
                title = query
                engine.runAndWait()
                speak("Which message do you want to set as remainder?")
                # query = input("")
                query = listening().lower()
                # query = audio_text(query)
                mesg = query
                engine.runAndWait()
                speak("What duration do you want to set?")
                # query = input("")
                query = listening().lower()
                # query = audio_text(query)
                duration = query
                t = Thread(target=set_notifier, args=[title, mesg, duration])
                t.start()

            except EXCEPTION as e:
                pass

        elif "weather" in query:
            engine.runAndWait()
            weather_forcasting(query)
        elif "who are you" in query or "introduce yourself" in query or "tell me about yourself" in query or "hello" in query:
            speak("Hi, I am not a human.I can not have emotions. I am an AI which is build to make your life easy!")
        elif "wikipedia" in query or "Tell me about" in query:
            speak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            try:

                results = summary(query, sentences=2)
                engine.runAndWait()
                speak(f"According to wikipedia! {results}")
            except Exception as e:
                speak(f"Sorry nothing found or may be network error")

        elif "open google" in query:
            engine.runAndWait()
            speak("Opening Google")
            webbrowser.open("google.com")
        elif "open youtube" in query:
            engine.runAndWait()
            speak("Opening Youtube")
            webbrowser.open("youtube.com")
        elif "time" in query:
            engine.runAndWait()
            speak(f"The current time is: {time.asctime()}")
        elif "play music" in query:
            speak("Please select music files and I will play a random song for you...")
            files = filedialog.askopenfilenames()
            try:
                os.startfile(rf"{random.choice(files)}")
            except Exception as e:
                speak("Might be some error, Try again!")
                st_bar_change("Might be some error, Try again!", "red")

        elif "wish me" in query:
            engine.runAndWait()
            wishme()

        elif query == "error" or query == "":
            pass

        elif "quit" in query:
            break


        else:
            engine.runAndWait()
            speak("Please give me specified commands")
    root.destroy()


def set_notifier(title, msg, duration):
    """
    Set remainders
    Requires Title, message and duration
    """
    global init_sec
    try:

        digits_diff = int(re.findall(r'\d+', duration)[0])
        init_sec = round(time.time())
    except Exception as e:
        speak("Please say in proper format (value minutes)")
        st_bar_change("Please say in proper format (value minutes)", "red")
        return None

    if (("hour" in duration or "hours" in duration or "hr" in duration) and (
            "minute" in duration or "minutes" in duration or "min" in duration)):
        speak("Please say in proper format (value minutes)")
        st_bar_change("Please say in proper format (value minutes)", "red")
        return None
    elif "hour" in duration or "hours" in duration:
        notification.notify(
            title=title,
            message=f"You remainder has set. You will receive notification after every {duration}",
            app_name="PersonalVU",
            app_icon="p.ico"
        )
        speak(f"You remainder has been set.You will receive notification after every {duration}")
        while True:
            # print("checking", round(time.time()), init_sec + (digits_diff * 60 * 60))
            if round(time.time()) == init_sec + (digits_diff * 60 * 60):
                init_sec = round(time.time())
                try:
                    speak(f"Your Remainder {title}: It's times to {msg}")
                    notification.notify(
                        title=title,
                        message=msg,
                        app_name="PersonalVU",
                        app_icon="p.ico"
                    )
                except Exception as e:
                    showing_commands.insert(END, f"VU: It's time {msg}")


    elif "minute" in duration or "minutes" in duration:
        notification.notify(
            title=title,
            message=f"You remainder has set. You will receive notification after every {duration}",
            app_name="PersonalVU",
            app_icon="p.ico"
        )
        speak(f"You remainder has been set.You will receive notification after every {duration}")

        while True:
            # print("checking", round(time.time()) - (init_sec + digits_diff * 60))
            if round(time.time()) == (init_sec * 60):
                init_sec = round(time.time())
                try:
                    speak(f"Your Remainder {title}: It's times to {msg}")
                    notification.notify(
                        title=title,
                        message=msg,
                        app_name="PersonalVU",
                        app_icon="p.ico"
                    )

                except Exception as e:
                    showing_commands.insert(END, f"VU: It's time {msg}")


    else:
        speak("Please say in proper format (value minutes or hours)")
        st_bar_change("Please say in proper format (value minutes or hours)", "red")
        return None


def welcome_window(event):
    """
    display AI window along with commands
    """
    if username.get() == "":
        root.update()
        speak("Please provide your username!")
        st_bar_change("Please provide your username!", "red")
        return None
    frame.forget()
    VU_frame.pack(fill=X, pady=10)
    Buttonframe.pack(fill=X)

    root.config(bg="#346878")
    Thread(target=start_vu).start()


def wishme():
    """
    Wish user according to time
    """
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good morning, Sir")
        return "Good morning, Sir"
    elif 12 <= hour < 18:
        speak(f"Good evening, Sir")
        return "Good evening, Sir"
    elif 18 <= hour < 24:
        speak(f"Good night, Sir")
        return "Good night, Sir"


def weather_forcasting(city):
    """
    Takes city as input and display weather information from google page
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    city_name = city
    city = city.replace(" ", "+")

    try:

        res = requests.get(
            f'https://www.google.com/search?client=opera-gx&q={city}+weather&sourceid=opera&ie=UTF-8&oe=UTF-8',
            headers=headers)
        speak("Searching Weather...")
        soup = BeautifulSoup(res.text, 'html.parser')
        location = soup.select('span', {"class":"BBwThe"})[0].getText()
        print(location)
        time = soup.select('#wob_dts')[0].getText().strip()
        info = soup.select('#wob_dc')[0].getText().strip()
        weather = soup.select('#wob_tm')[0].getText().strip()
        perspiration = soup.select("#wob_pp")[0].getText().strip()
        humidity = soup.select("#wob_hm")[0].getText().strip()
        wind = soup.select("#wob_ws")[0].getText().strip()
        speak(f"Location: {city_name}\ttime: {time}")
        speak(f"Info: {info}\tweather: {weather}°C")
        speak(f"Perspiration: {perspiration}\tHumidity: {humidity}")
        speak(f"Wind: {wind}\tHave a nice day:)")
    except Exception as e:
        speak("Please provide correct city name or may be network error")
        st_bar_change("Please provide correct city name or may be network error", "red")
        return None


def st_bar_change(text, color):
    """
    Change status in status bar
    """
    try:
        status_var.set(text)
        status_bar.config(fg=color)
    except Exception as e:
        exit()


def bk():
    root.destroy()


# Creating a main menu
main_menu = Menu(root, bd=0, relief=GROOVE, )
# Adding commands to menu
main_menu.add_command(label="Help", command=lambda: tm.showinfo("Commands!", " Weather Forcastring (city weather)\n "
                                                                             "Setting Remainders (Title, Message, Duration) \n Search Wikipedia (Topic) \n Play Music \n Time\n Open (google, "
                                                                             "youtube) "))
main_menu.add_command(label="About", command=lambda: tm.showinfo("Info!", "PersonalVU by Arbaaz Khan\n Version: 1.O"))
root.config(menu=main_menu)

# main label
lable_frame = Frame(root, bg="#346878")
Label(lable_frame, text="Welcome To Your PersonalVu", font="lucinda 17 bold", bg="#346878", fg="white",
      pady=10).pack(
    fill=X, padx=1,
    pady=1)
lable_frame.pack(side=TOP, fill=X)

# initial window frame
frame = Frame(root, bg="#346878", bd=1, relief=GROOVE)
Label(frame, text="Please tell me your name!", font="lucinda 17 bold", bg="#346878", fg="white", width=90).pack(
    fill=X,
    padx=1, pady=1)
user = Entry(frame, borderwidth=0, textvariable=username)
user.pack(ipady=2, padx=5, pady=10)
user.bind('<Return>', welcome_window)
strt = Button(frame, width=7, text="Start", overrelief=SUNKEN, font='lucinda 8 italic', bg='black', fg='white',
              activebackground='white', activeforeground='black', command=partial(welcome_window, "event"))

user.focus_set()

strt.pack(
    anchor='n', padx=10, pady=10)
frame.pack(side=TOP, fill=X, pady=20)

# Text area for showing commands
VU_frame = LabelFrame(root, text=f"Hello {username.get()}! I am Jarvis, How may I help you?", height=180,
                      font="lucida 10 bold")
showing_commands = Text(VU_frame, bd=0)
showing_commands.pack(expand=True, padx=2, pady=2, fill=BOTH)

# Frame for button
Buttonframe = Frame(root, bg="#346878")
Button(Buttonframe, text="Clear", width=7, overrelief=SUNKEN, font='lucinda 8 italic', bg='black', fg='white',
       activebackground='white', activeforeground='black', command=lambda: showing_commands.delete('1.0', END)).pack(
    side=LEFT, anchor='n', padx=10)
Button(Buttonframe, width=7, text="Quit", overrelief=SUNKEN, font='lucinda 8 italic', bg='black', fg='white',
       activebackground='white', activeforeground='black', command=bk).pack(side=RIGHT,
                                                                            anchor='n',

                                                                            padx=10)

# Status bar
status_frame = Frame(root, relief=SUNKEN, borderwidth=3, bg="#23292E")
status_var = StringVar()
status_bar = Label(status_frame, textvariable=status_var, pady=8, bg="#23292E", fg="white",
                   font="timesnewroman 8 italic")
status_bar.pack(anchor="w")

st_bar_change("Please Tell me you name", "white")
status_frame.pack(side=BOTTOM, fill=X)

if __name__ == '__main__':

    root.mainloop()
