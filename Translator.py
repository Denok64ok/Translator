from PIL import ImageGrab
from PyQt5 import QtCore, QtGui, QtWidgets
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

        self.outsideSquareColor = "red"
        self.squareThickness = 2

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
        r_path = outer - inner
        qp.drawPath(r_path)
        qp.setPen(
            QtGui.QPen(QtGui.QColor(self.outsideSquareColor), self.squareThickness)
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


class Loading_clipboard:
    def __init__(self, text):
        self.text = text

    def set_text(self, text):
        self.text = text

    def copy_text(self):
        clipboard.copy(self.text)


class Upload_clipboard:
    def paste_text(self):
        return clipboard.paste()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(593, 403)
        MainWindow.setMinimumSize(QtCore.QSize(593, 403))
        MainWindow.setMaximumSize(QtCore.QSize(593, 403))
        MainWindow.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.172249, y1:0.205, x2:0.80226, y2:0.79, stop:0.0677966 rgba(4, 87, 120, 255), stop:0.926136 rgba(6, 145, 201, 255));")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 20, 261, 361))
        self.frame.setStyleSheet("background-color: rgba(53,203,204,0.6);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(63, 60, 191, 241))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 4px solid #35cbcc;\n"
"border-radius: 10px;\n"
"color: rgb(0, 0, 0);")
        self.textEdit.setObjectName("textEdit")
        self.comboBox = QtWidgets.QComboBox(self.frame)
        self.comboBox.setGeometry(QtCore.QRect(150, 20, 69, 22))
        self.comboBox.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 240, 41, 41))
        self.pushButton_3.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 180, 41, 41))
        self.pushButton_4.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 120, 41, 41))
        self.pushButton_5.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.frame)
        self.pushButton_6.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.pushButton_6.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_10 = QtWidgets.QPushButton(self.frame)
        self.pushButton_10.setGeometry(QtCore.QRect(70, 20, 61, 21))
        self.pushButton_10.setAutoFillBackground(False)
        self.pushButton_10.setStyleSheet("background-color: rgb(53, 203, 225);")
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_18 = QtWidgets.QPushButton(self.frame)
        self.pushButton_18.setGeometry(QtCore.QRect(80, 310, 41, 41))
        self.pushButton_18.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_18.setObjectName("pushButton_18")
        self.pushButton_19 = QtWidgets.QPushButton(self.frame)
        self.pushButton_19.setGeometry(QtCore.QRect(140, 310, 41, 41))
        self.pushButton_19.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_19.setObjectName("pushButton_19")
        self.pushButton_20 = QtWidgets.QPushButton(self.frame)
        self.pushButton_20.setGeometry(QtCore.QRect(200, 310, 41, 41))
        self.pushButton_20.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_20.setObjectName("pushButton_20")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(300, 30, 41, 41))
        self.pushButton_8.setStyleSheet("background-color: rgb(53, 203, 225);")
        self.pushButton_8.setObjectName("pushButton_8")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(360, 20, 211, 361))
        self.frame_2.setStyleSheet("background-color: rgba(53,203,204,0.6);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.textEdit_3 = QtWidgets.QTextEdit(self.frame_2)
        self.textEdit_3.setGeometry(QtCore.QRect(10, 60, 191, 241))
        self.textEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 4px solid #35cbcc;\n"
"border-radius: 10px;\n"
"color: rgb(0, 0, 0);")
        self.textEdit_3.setObjectName("textEdit_3")
        self.comboBox_3 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_3.setGeometry(QtCore.QRect(70, 20, 69, 22))
        self.comboBox_3.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.comboBox_3.setObjectName("comboBox_3")
        self.pushButton_21 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_21.setGeometry(QtCore.QRect(30, 310, 41, 41))
        self.pushButton_21.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_21.setObjectName("pushButton_21")
        self.pushButton_22 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_22.setGeometry(QtCore.QRect(90, 310, 41, 41))
        self.pushButton_22.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_22.setObjectName("pushButton_22")
        self.pushButton_23 = QtWidgets.QPushButton(self.frame_2)
        self.pushButton_23.setGeometry(QtCore.QRect(150, 310, 41, 41))
        self.pushButton_23.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_23.setObjectName("pushButton_23")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(300, 170, 41, 41))
        self.pushButton_9.setStyleSheet("background-color: rgb(53, 203, 225);\n"
"color: rgb(255, 153, 0);")
        self.pushButton_9.setObjectName("pushButton_9")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Аглийский"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Китайский"))
        self.pushButton_3.setText(_translate("MainWindow", "Вставить"))
        self.pushButton_4.setText(_translate("MainWindow", "Прочитать из файла"))
        self.pushButton_5.setText(_translate("MainWindow", "голосовая запись"))
        self.pushButton_6.setText(_translate("MainWindow", "ножницы"))
        self.pushButton_10.setText(_translate("MainWindow", "Определить язык"))
        self.pushButton_18.setText(_translate("MainWindow", "Озвучить"))
        self.pushButton_19.setText(_translate("MainWindow", "Записать в файл"))
        self.pushButton_20.setText(_translate("MainWindow", "Копировать"))
        self.pushButton_8.setText(_translate("MainWindow", "Поменять языки"))
        self.pushButton_21.setText(_translate("MainWindow", "Озвучить"))
        self.pushButton_22.setText(_translate("MainWindow", "Записать в файл"))
        self.pushButton_23.setText(_translate("MainWindow", "Копировать"))
        self.pushButton_9.setText(_translate("MainWindow", "Перевести"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
