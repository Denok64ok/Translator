from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PIL import ImageGrab
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog
from googletrans import Translator
import pytesseract
import cv2
import speech_recognition as sr
import pyttsx3
import pyperclip as clipboard


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
        r = QtCore.QRect(self.start_point, self.end_point).normalized()
        self.hide()
        img = ImageGrab.grab(bbox=r.getCoords())
        img.save("Images/snapshot.png")
        QtWidgets.QApplication.restoreOverrideCursor()
        self.closed.emit()
        self.start_point = QtCore.QPoint()
        self.end_point = QtCore.QPoint()

    def paintEvent(self, event):
        trans = QtGui.QColor(22, 100, 233)
        r = QtCore.QRectF(self.start_point, self.end_point).normalized()
        qp = QtGui.QPainter(self)
        trans.setAlphaF(0.2)
        qp.setBrush(trans)
        outer = QtGui.QPainterPath()
        outer.addRect(QtCore.QRectF(self.rect()))
        inner = QtGui.QPainterPath()
        inner.addRect(r)
        qp.drawPath(outer - inner)
        qp.setPen(
            QtGui.QPen(QtGui.QColor("red"), 2)
        )
        trans.setAlphaF(0)
        qp.setBrush(trans)
        qp.drawRect(r)


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
        try:
            with sr.Microphone() as source:
                audio = self.recogn.listen(source)
            text = self.recogn.recognize_google(audio, language=self.language)
            return text
        except:
            pass


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

    def set_text(self, file):
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(593, 403)
        MainWindow.setMinimumSize(QtCore.QSize(593, 403))
        MainWindow.setMaximumSize(QtCore.QSize(593, 403))
        MainWindow.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0.172249, y1:0.205, x2:0.80226, y2:0.79, stop:0.0677966 rgba(4, 87, 120, 255), stop:0.926136 rgba(6, 145, 201, 255));")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 261, 361))
        self.frame.setStyleSheet("background-color: rgba(53,203,204,0.6);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.textedit_input = QtWidgets.QTextEdit(self.frame)
        self.textedit_input.setGeometry(QtCore.QRect(63, 60, 191, 241))
        self.textedit_input.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                          "border: 4px solid #35cbcc;\n"
                                          "border-radius: 10px;\n"
                                          "color: rgb(0, 0, 0);")
        self.textedit_input.setObjectName("textedit_input")

        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(150, 20, 69, 22))
        self.comboBox.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                    "color: rgb(255, 153, 0);")
        self.comboBox.setObjectName("comboBox")

        self.insert_button = QtWidgets.QPushButton(self.frame)
        self.insert_button.setGeometry(QtCore.QRect(10, 240, 41, 41))
        self.insert_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                         "color: rgb(255, 153, 0);")
        self.insert_button.setObjectName("insert_button")
        self.insert_button.clicked.connect(self.pasting_text)

        self.read_file_button = QtWidgets.QPushButton(self.frame)
        self.read_file_button.setGeometry(QtCore.QRect(10, 180, 41, 41))
        self.read_file_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                            "color: rgb(255, 153, 0);")
        self.read_file_button.setObjectName("read_file_button")
        self.read_file_button.clicked.connect(self.reading_file)

        self.voice_recording_button = QtWidgets.QPushButton(self.frame)
        self.voice_recording_button.setGeometry(QtCore.QRect(10, 120, 41, 41))
        self.voice_recording_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                                  "color: rgb(255, 153, 0);")
        self.voice_recording_button.setObjectName("voice_recording_button")
        self.voice_recording_button.clicked.connect(self.voicing_recogn)

        self.scissors_button = QtWidgets.QPushButton(self.frame)
        self.scissors_button.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.scissors_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                           "color: rgb(255, 153, 0);")
        self.scissors_button.setObjectName("scissors_button")
        self.scissors_button.clicked.connect(self.scissors)

        self.define_language_button = QtWidgets.QPushButton(self.frame)
        self.define_language_button.setGeometry(QtCore.QRect(70, 20, 61, 21))
        self.define_language_button.setAutoFillBackground(False)
        self.define_language_button.setStyleSheet("background-color: rgb(53, 203, 225);")
        self.define_language_button.setObjectName("define_language_button")
        self.define_language_button.clicked.connect(self.defining_language)

        self.voice_input_button = QtWidgets.QPushButton(self.frame)
        self.voice_input_button.setGeometry(QtCore.QRect(80, 310, 41, 41))
        self.voice_input_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                              "color: rgb(255, 153, 0);")
        self.voice_input_button.setObjectName("voice_input_button")
        self.voice_input_button.clicked.connect(lambda: self.voicing_text("input"))

        self.write_file_input_button = QtWidgets.QPushButton(self.frame)
        self.write_file_input_button.setGeometry(QtCore.QRect(140, 310, 41, 41))
        self.write_file_input_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                                   "color: rgb(255, 153, 0);")
        self.write_file_input_button.setObjectName("write_file_input_button")
        self.write_file_input_button.clicked.connect(lambda: self.writing_file("input"))

        self.copy_input_button = QtWidgets.QPushButton(self.frame)
        self.copy_input_button.setGeometry(QtCore.QRect(200, 310, 41, 41))
        self.copy_input_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                             "color: rgb(255, 153, 0);")
        self.copy_input_button.setObjectName("copy_input_button")
        self.copy_input_button.clicked.connect(lambda: self.coping_text("input"))

        self.change_languages_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_languages_button.setGeometry(QtCore.QRect(300, 30, 41, 41))
        self.change_languages_button.setStyleSheet("background-color: rgb(53, 203, 225);")
        self.change_languages_button.setObjectName("change_languages_button")

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(360, 20, 211, 361))
        self.frame_2.setStyleSheet("background-color: rgba(53,203,204,0.6);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.textedit_output = QtWidgets.QTextEdit(self.frame_2)
        self.textedit_output.setGeometry(QtCore.QRect(10, 60, 191, 241))
        self.textedit_output.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                           "border: 4px solid #35cbcc;\n"
                                           "border-radius: 10px;\n"
                                           "color: rgb(0, 0, 0);")
        self.textedit_output.setObjectName("textedit_output")
        self.textedit_output.setReadOnly(True)

        self.comboBox_3 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_3.setGeometry(QtCore.QRect(70, 20, 69, 22))
        self.comboBox_3.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                      "color: rgb(255, 153, 0);")
        self.comboBox_3.setObjectName("comboBox_3")

        self.voice_output_button = QtWidgets.QPushButton(self.frame_2)
        self.voice_output_button.setGeometry(QtCore.QRect(30, 310, 41, 41))
        self.voice_output_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                               "color: rgb(255, 153, 0);")
        self.voice_output_button.setObjectName("voice_output_button")
        self.voice_output_button.clicked.connect(lambda: self.voicing_text("output"))

        self.write_file_output_button = QtWidgets.QPushButton(self.frame_2)
        self.write_file_output_button.setGeometry(QtCore.QRect(90, 310, 41, 41))
        self.write_file_output_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                                    "color: rgb(255, 153, 0);")
        self.write_file_output_button.setObjectName("write_file_output_button")
        self.write_file_output_button.clicked.connect(lambda: self.writing_file("output"))

        self.copy_output_button = QtWidgets.QPushButton(self.frame_2)
        self.copy_output_button.setGeometry(QtCore.QRect(150, 310, 41, 41))
        self.copy_output_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                              "color: rgb(255, 153, 0);")
        self.copy_output_button.setObjectName("copy_output_button")
        self.copy_output_button.clicked.connect(lambda: self.coping_text("output"))

        self.change_texts_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_texts_button.setGeometry(QtCore.QRect(300, 120, 41, 41))
        self.change_texts_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                               "color: rgb(255, 153, 0);")
        self.change_texts_button.setObjectName("change_texts_button")
        self.change_texts_button.clicked.connect(self.changing_text)

        self.translate_button = QtWidgets.QPushButton(self.centralwidget)
        self.translate_button.setGeometry(QtCore.QRect(300, 240, 41, 41))
        self.translate_button.setStyleSheet("background-color: rgb(53, 203, 225);\n"
                                            "color: rgb(255, 153, 0);")
        self.translate_button.setObjectName("translate_button")
        self.translate_button.clicked.connect(self.translating)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.snipper = Screenshot()
        self.snipper.closed.connect(self.on_closed)

    def changing_text(self):
        input_text = self.textedit_input.toPlainText()
        self.textedit_input.setText(self.textedit_output.toPlainText())
        self.textedit_output.setText(input_text)

    def translating(self):
        translate_text = Translator_Googletrans(self.id_input_language(1), self.id_output_language(1))
        try:
            self.textedit_output.setText(translate_text.translate(self.textedit_input.toPlainText()))
        except:
            pass

    def reading(self, name):
        languages = []
        with open(name, 'r', encoding="utf8") as file:
            for line in file:
                line = line.split()
                if line:
                    languages.append(line)
        return languages

    def adding_language(self):
        _translate = QtCore.QCoreApplication.translate
        lang = self.reading("bd.txt")
        n = 0
        for i in lang:
            self.comboBox.addItem("")
            self.comboBox.setItemText(n, _translate("MainWindow", i[0]))
            self.comboBox_3.addItem("")
            self.comboBox_3.setItemText(n, _translate("MainWindow", i[0]))
            n += 1

    def id_input_language(self, j):
        lang = self.reading("bd.txt")
        for i in lang:
            if i[0] == self.comboBox.currentText():
                return i[j]

    def id_output_language(self, j):
        lang = self.reading("bd.txt")
        for i in lang:
            if i[0] == self.comboBox_3.currentText():
                return i[j]

    def defining_language(self):
        translate_text = Translator_Googletrans()
        detect_lang = translate_text.define_language(self.textedit_input.toPlainText())
        lang = self.reading("bd.txt")
        for i in lang:
            if i[1] == detect_lang.lang:
                self.comboBox.setCurrentText(i[0])
                return 0

    def coping_text(self, put):
        if put == "input":
            clipboard = Loading_Clipboard(self.textedit_input.toPlainText())
        elif put == "output":
            clipboard = Loading_Clipboard(self.textedit_output.toPlainText())
        clipboard.copy_text()

    def pasting_text(self):
        clipboard = Upload_Clipboard()
        self.textedit_input.setText(clipboard.paste_text())

    def voicing_text(self, put):
        if put == "input":
            voice = Text_Voiceover(
                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\\" + self.id_input_language(2))
            voice.voice_text(self.textedit_input.toPlainText())
        elif put == "output":
            voice = Text_Voiceover(
                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\\" + self.id_output_language(2))
            voice.voice_text(self.textedit_output.toPlainText())

    def voicing_recogn(self):
        voice = Voice_Recognition(self.id_input_language(3))
        self.textedit_input.setText(voice.voice_text())

    def selecting_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            return dialog.selectedFiles()

    def reading_file(self):
        graphic_formats = ["svg", "pdf", "eps", "ai", "cdr", "png", "jpeg", "gif", "raw", "tiff", "bmp", "psd"]
        file = self.selecting_file()[0]
        try:
            if file.split(".")[-1] in graphic_formats:
                image = Technic_OCR(file, self.id_input_language(4))
                self.textedit_input.setText(image.text_search())
            else:
                text = File_Reading(file)
                self.textedit_input.setText(text.reading())
        except:
            pass

    def writing_file(self, put):
        if put == "input":
            file = File_Writing(self.selecting_file()[0], self.textedit_input.toPlainText())
        elif put == "output":
            file = File_Writing(self.selecting_file()[0], self.textedit_output.toPlainText())
        file.writing()

    def scissors(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        MainWindow.hide()

    def on_closed(self):
        MainWindow.show()
        image = Technic_OCR("Images/snapshot.png", self.id_input_language(4))
        self.textedit_input.setText(image.text_search())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.adding_language()
        self.insert_button.setText(_translate("MainWindow", "Вставить"))
        self.read_file_button.setText(_translate("MainWindow", "Прочитать из файла"))
        self.voice_recording_button.setText(_translate("MainWindow", "голосовая запись"))
        self.scissors_button.setText(_translate("MainWindow", "ножницы"))
        self.define_language_button.setText(_translate("MainWindow", "Определить язык"))
        self.voice_input_button.setText(_translate("MainWindow", "Озвучить"))
        self.write_file_input_button.setText(_translate("MainWindow", "Записать в файл"))
        self.copy_input_button.setText(_translate("MainWindow", "Копировать"))

        self.voice_output_button.setText(_translate("MainWindow", "Озвучить"))
        self.write_file_output_button.setText(_translate("MainWindow", "Записать в файл"))
        self.copy_output_button.setText(_translate("MainWindow", "Копировать"))

        self.change_languages_button.setText(_translate("MainWindow", "Поменять языки"))
        self.change_texts_button.setText(_translate("MainWindow", "Поменять текст"))
        self.translate_button.setText(_translate("MainWindow", "Перевести"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
