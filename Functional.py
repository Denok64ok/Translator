from Interface import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import ImageGrab
from googletrans import Translator
import pytesseract
import cv2
import speech_recognition as sr
import pyttsx3
import pyperclip as clipboard


class Translator_Googletrans(Interface_Translator):
    def __init__(self, input_language='en', output_language='fr'):
        self.input_language = input_language
        self.output_language = output_language
        self.translator = Translator()

    def set_input_language(self, language):
        self.input_language = language

    def set_output_language(self, language):
        self.output_language = language

    def define_language(self, text):
        return self.translator.detect(text)

    def translate(self, text):
        translation = self.translator.translate(text, src=self.input_language, dest=self.output_language)
        return translation.text


class Screenshot(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Screenshot, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground, True)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background:transparent;")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def mousePressEvent(self, event):
        self.start_point = event.pos()
        self.end_point = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end_point = event.pos()
        self.update()

    def mouseReleaseEvent(self, QMouseEvent):
        snapshot_area = QtCore.QRect(self.start_point, self.end_point).normalized()
        self.hide()
        img = ImageGrab.grab(bbox=snapshot_area.getCoords())
        try:
            img.save("Images/snapshot.png")
        except:
            pass
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def paintEvent(self, event):
        color_backdrop = [22, 100, 233]
        backdrop = QtGui.QColor(color_backdrop[0], color_backdrop[1], color_backdrop[2])
        snapshot_area = QtCore.QRectF(self.start_point, self.end_point).normalized()
        area_draughtsman = QtGui.QPainter(self)
        backdrop.setAlphaF(0.2)
        area_draughtsman.setBrush(backdrop)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(snapshot_area)
        area_draughtsman.drawPath(outer - inner)
        color_box = QtGui.QColor("red")
        width_box = 2
        area_draughtsman.setPen(
            QtGui.QPen(color_box, width_box)
        )
        backdrop.setAlphaF(0)
        area_draughtsman.setBrush(backdrop)
        area_draughtsman.drawRect(snapshot_area)


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
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(image, config=custom_config, lang=self.language)
        return text.replace("\n", " ")


class Voice_Recognition:
    def __init__(self, language='ru-RU'):
        self.recogn = sr.Recognizer()
        self.language = language

    def set_language(self, language):
        self.language = language

    def voice_text(self):
        with sr.Microphone() as source:
            audio = self.recogn.listen(source)
        text = self.recogn.recognize_google(audio, language=self.language)
        return text


class Text_Voiceover:
    def __init__(self, id_voice="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"):
        self.engine = pyttsx3.init()
        self.id_voice = id_voice

    def set_id(self, id_voice):
        self.id_voice = id_voice

    def voice_text(self, text, settings=None):
        if settings is None:
            settings = [150, 0.7]
        self.engine.setProperty('rate', settings[0])
        self.engine.setProperty('volume', settings[1])
        self.engine.setProperty('voice', self.id_voice)
        self.engine.say(text)
        self.engine.runAndWait()


class File_Reading:
    def __init__(self, file):
        self.file = file

    def set_file(self, file):
        self.file = file

    def reading(self):
        with open(self.file, "r", encoding="utf8") as file:
            data = file.read()
        return data


class File_Writing:
    def __init__(self, file, data):
        self.file = file
        self.data = data

    def set_file(self, file):
        self.file = file

    def set_content(self, data):
        self.data = data

    def writing(self):
        with open(self.file, "w", encoding="utf8") as file:
            file.write(self.data)


class Loading_Clipboard:
    def __init__(self, text):
        self.text = text

    def set_text(self, text):
        self.text = text

    def copy_text(self):
        clipboard.copy(self.text)


class Upload_Clipboard:
    def paste_text(self):
        return clipboard.paste()
