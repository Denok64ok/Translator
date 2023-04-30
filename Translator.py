from tkinter import *
from tkinter import ttk
import pyautogui
import keyboard
from googletrans import Translator
import pytesseract
import cv2
import speech_recognition as sr
import pyttsx3


class Interface_Translator:
    def __init__(self, input_language='en', output_language='fr'):
        self.input_language = input_language
        self.output_language = output_language

    def set_input_language(self, language):
        raise NotImplementedError()

    def set_output_language(self, language):
        raise NotImplementedError()

    def translate(self, text):
        raise NotImplementedError()


class Translator_Googletrans(Interface_Translator):
    def __init__(self, input_language='en', output_language='fr'):
        super().__init__(input_language, output_language)
        self.translator = Translator()

    def set_input_language(self, language):
        self.input_language = language

    def set_output_language(self, language):
        self.output_language = language

    def translate(self, text):
        translation = self.translator.translate(text, src=self.input_language, dest=self.output_language)
        return translation.text


class Screenshot:
    def __init__(self, x1=0, y1=0, x2=pyautogui.size()[0], y2=pyautogui.size()[1]):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def cut_area(self, name):
        keyboard.wait("enter")
        self.x1, self.y1 = pyautogui.position()
        keyboard.wait("enter")
        self.x2, self.y2 = pyautogui.position()
        screenshot = pyautogui.screenshot(region=(self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))
        screenshot.save(name)


class Technic_OCR:
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def __init__(self, photo, language='eng'):
        self.photo = photo
        self.language = language

    def set_photo(self, photo):
        self.photo = photo

    def set_language(self, language):
        self.language = language

    def text_search(self):
        image = cv2.imread(self.photo)
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        custom_config = r'--oem 3 --psm 6'
        return pytesseract.image_to_string(image, config=custom_config, lang=self.language)


class Voice_Recognition:
    def __init__(self, language='ru-RU'):
        self.r = sr.Recognizer()
        self.language = language

    def set_language(self, language):
        self.language = language

    def voice_text(self):
        with sr.Microphone() as source:
            print("Говорите...")
            audio = self.r.listen(source)

        try:
            text = self.r.recognize_google(audio, language=self.language)
            print("Вы сказали: " + text)
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
        except sr.RequestError as e:
            print("Ошибка сервиса распознавания речи; {0}".format(e))


class Text_Voiceover:
    def __init__(self, language='ru',
                 id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"):
        self.engine = pyttsx3.init()
        self.language = language
        self.id = id

    def set_language(self, language):
        self.language = language

    def set_id(self, id):
        self.id = id

    def voice_text(self, text, settings=None):
        if settings is None:
            settings = [150, 0.7]
        self.engine.setProperty('rate', settings[0])
        self.engine.setProperty('volume', settings[1])
        self.engine.setProperty('voice', self.id)
        self.engine.say(text)
        self.engine.runAndWait()


class File_Reading:
    def __init__(self, text):
        self.text = text

    def set_text(self, text):
        self.text = text

    def Reading(self):
        with open(self.text, "r") as file:
            data = file.read()
        return data


class File_writing:
    def __init__(self, text, content):
        self.text = text
        self.content = content

    def set_text(self, text):
        self.text = text

    def set_content(self, content):
        self.content = content

    def writing(self):
        with open(self.text, "r") as file:
            file.write(self.content)


class GUI_application:
    def __init__(self, window):
        self.window = window
        window.title("Переводчик")
        window.geometry('700x450')
        window.grid_columnconfigure(0, weight=1)

        self.languages = ["Англиский", "Русский", "Немецкий", "Французкий"]

        self.choice_input_language = ttk.Combobox(values=self.languages)
        self.choice_input_language.place(x=40, y=50)

        self.input_text = Text(window, width=35, height=15, wrap="word")
        self.input_text.place(x=40, y=100)
        self.input_text.focus()

        self.input_scrollbar = Scrollbar(window, orient="vertical", command=self.input_text.yview)
        self.input_scrollbar.place(x=310, y=100, height=245)

        self.input_text["yscrollcommand"] = self.input_scrollbar.set

        self.choice_output_language = ttk.Combobox(values=self.languages)
        self.choice_output_language.place(x=350, y=50)

        self.output_text = Text(window, width=35, height=15, wrap="word")
        self.output_text.place(x=350, y=100)

        self.output_scrollbar = Scrollbar(window, orient="vertical", command=self.output_text.yview)
        self.output_scrollbar.place(x=620, y=100, height=245)

        self.output_text["yscrollcommand"] = self.output_scrollbar.set

        self.Trans = Translator_Googletrans()

        self.button = Button(window, text="Перевести",
                             command=self.output_text.insert(0, self.Trans.translate(str(self.input_text.get))),
                             font=("Times New Roman", 14))
        self.button.place(x=300, y=350)
