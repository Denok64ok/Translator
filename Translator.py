from Functional import *
from speech_recognition import UnknownValueError
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QApplication
import icon_rc
import sys


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

        self.frame_input = QtWidgets.QFrame(self.centralwidget)
        self.frame_input.setGeometry(QtCore.QRect(20, 20, 261, 361))
        self.frame_input.setStyleSheet("background-color: rgba(53,203,204,0.6);")
        self.frame_input.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_input.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_input.setObjectName("frame_input")

        self.textedit_input = QtWidgets.QTextEdit(self.frame_input)
        self.textedit_input.setGeometry(QtCore.QRect(63, 60, 191, 241))
        self.textedit_input.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"
            "border: 4px solid #35cbcc;\n"
            "border-radius: 10px;\n"
            "color: rgb(0, 0, 0);")
        self.textedit_input.setObjectName("textedit_input")

        self.languages_input = QtWidgets.QComboBox(self.frame_input)
        self.languages_input.setGeometry(QtCore.QRect(140, 20, 91, 22))
        self.languages_input.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "color: rgb(255, 153, 0);")
        self.languages_input.setObjectName("languages_input")

        self.insert_button = QtWidgets.QPushButton(self.frame_input)
        self.insert_button.setGeometry(QtCore.QRect(10, 240, 41, 41))
        self.insert_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Past.png);")
        self.insert_button.setObjectName("insert_button")
        self.insert_button.setText("")
        self.insert_button.clicked.connect(self.pasting_text)

        self.read_file_button = QtWidgets.QPushButton(self.frame_input)
        self.read_file_button.setGeometry(QtCore.QRect(10, 180, 41, 41))
        self.read_file_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-image: url(:/images/Read.png);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;")
        self.read_file_button.setObjectName("read_file_button")
        self.read_file_button.setText("")
        self.read_file_button.clicked.connect(self.reading_file)

        self.voice_recording_button = QtWidgets.QPushButton(self.frame_input)
        self.voice_recording_button.setGeometry(QtCore.QRect(10, 120, 41, 41))
        self.voice_recording_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Micr.png);")
        self.voice_recording_button.setObjectName("voice_recording_button")
        self.voice_recording_button.setText("")
        self.voice_recording_button.clicked.connect(self.voicing_recogn)

        self.scissors_button = QtWidgets.QPushButton(self.frame_input)
        self.scissors_button.setGeometry(QtCore.QRect(10, 60, 41, 41))
        self.scissors_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Cuts.png);")
        self.scissors_button.setObjectName("scissors_button")
        self.scissors_button.setText("")
        self.scissors_button.clicked.connect(self.scissors)

        self.define_language_button = QtWidgets.QPushButton(self.frame_input)
        self.define_language_button.setGeometry(QtCore.QRect(80, 10, 41, 41))
        self.define_language_button.setAutoFillBackground(False)
        self.define_language_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Targ.png);")
        self.define_language_button.setObjectName("define_language_button")
        self.define_language_button.setText("")
        self.define_language_button.clicked.connect(self.defining_language)

        self.voice_input_button = QtWidgets.QPushButton(self.frame_input)
        self.voice_input_button.setGeometry(QtCore.QRect(80, 310, 41, 41))
        self.voice_input_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-image: url(:/images/Spea.png);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;")
        self.voice_input_button.setObjectName("voice_input_button")
        self.voice_input_button.setText("")
        self.voice_input_button.clicked.connect(lambda: self.voicing_text("input"))

        self.write_file_input_button = QtWidgets.QPushButton(self.frame_input)
        self.write_file_input_button.setGeometry(QtCore.QRect(140, 310, 41, 41))
        self.write_file_input_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Reco.png);")
        self.write_file_input_button.setObjectName("write_file_input_button")
        self.write_file_input_button.setText("")
        self.write_file_input_button.clicked.connect(lambda: self.writing_file("input"))

        self.copy_input_button = QtWidgets.QPushButton(self.frame_input)
        self.copy_input_button.setGeometry(QtCore.QRect(200, 310, 41, 41))
        self.copy_input_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-image: url(:/images/Copy.png);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;")
        self.copy_input_button.setObjectName("copy_input_button")
        self.copy_input_button.setText("")
        self.copy_input_button.clicked.connect(lambda: self.coping_text("input"))

        self.change_languages_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_languages_button.setGeometry(QtCore.QRect(300, 30, 41, 41))
        self.change_languages_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Reve.png);")
        self.change_languages_button.setObjectName("change_languages_button")
        self.change_languages_button.setText("")
        self.change_languages_button.clicked.connect(self.changing_language)

        self.frame_output = QtWidgets.QFrame(self.centralwidget)
        self.frame_output.setGeometry(QtCore.QRect(360, 20, 211, 361))
        self.frame_output.setStyleSheet("background-color: rgba(53,203,204,0.6);")
        self.frame_output.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_output.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_output.setObjectName("frame_output")

        self.textedit_output = QtWidgets.QTextEdit(self.frame_output)
        self.textedit_output.setGeometry(QtCore.QRect(10, 60, 191, 241))
        self.textedit_output.setStyleSheet(
            "background-color: rgb(255, 255, 255);\n"
            "border: 4px solid #35cbcc;\n"
            "border-radius: 10px;\n"
            "color: rgb(0, 0, 0);")
        self.textedit_output.setObjectName("textedit_output")
        self.textedit_output.setText("")
        self.textedit_output.setReadOnly(True)

        self.languages_output = QtWidgets.QComboBox(self.frame_output)
        self.languages_output.setGeometry(QtCore.QRect(60, 20, 91, 22))
        self.languages_output.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "color: rgb(255, 153, 0);")
        self.languages_output.setObjectName("languages_output")

        self.voice_output_button = QtWidgets.QPushButton(self.frame_output)
        self.voice_output_button.setGeometry(QtCore.QRect(30, 310, 41, 41))
        self.voice_output_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-image: url(:/images/Spea.png);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;")
        self.voice_output_button.setObjectName("voice_output_button")
        self.voice_output_button.setText("")
        self.voice_output_button.clicked.connect(lambda: self.voicing_text("output"))

        self.write_file_output_button = QtWidgets.QPushButton(self.frame_output)
        self.write_file_output_button.setGeometry(QtCore.QRect(90, 310, 41, 41))
        self.write_file_output_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-image: url(:/images/Reco.png);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;")
        self.write_file_output_button.setObjectName("write_file_output_button")
        self.write_file_output_button.setText("")
        self.write_file_output_button.clicked.connect(lambda: self.writing_file("output"))

        self.copy_output_button = QtWidgets.QPushButton(self.frame_output)
        self.copy_output_button.setGeometry(QtCore.QRect(150, 310, 41, 41))
        self.copy_output_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Copy.png);")
        self.copy_output_button.setObjectName("copy_output_button")
        self.copy_output_button.setText("")
        self.copy_output_button.clicked.connect(lambda: self.coping_text("output"))

        self.change_texts_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_texts_button.setGeometry(QtCore.QRect(300, 120, 41, 41))
        self.change_texts_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Chan.png);")
        self.change_texts_button.setObjectName("change_texts_button")
        self.change_texts_button.setText("")
        self.change_texts_button.clicked.connect(self.changing_text)

        self.translate_button = QtWidgets.QPushButton(self.centralwidget)
        self.translate_button.setGeometry(QtCore.QRect(300, 240, 41, 41))
        self.translate_button.setStyleSheet(
            "background-color: rgb(53, 203, 225);\n"
            "background-repeat: no-repeat;\n"
            "background-position: center;\n"
            "background-image: url(:/images/Trans.png);")
        self.translate_button.setText("")
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

    def changing_language(self):
        input_language = self.languages_input.currentIndex()
        self.languages_input.setCurrentIndex(self.languages_output.currentIndex())
        self.languages_output.setCurrentIndex(input_language)

    def translating(self):
        translate_text = Translator_Googletrans(
            self.id_language(self.languages_input, 1),
            self.id_language(self.languages_output, 1))
        self.textedit_output.setText(translate_text.translate(self.textedit_input.toPlainText()))

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
            self.languages_input.addItem("")
            self.languages_input.setItemText(n, _translate("MainWindow", i[0]))
            self.languages_output.addItem("")
            self.languages_output.setItemText(n, _translate("MainWindow", i[0]))
            n += 1

    def id_language(self, put, column_number):
        lang = self.reading("bd.txt")
        for i in lang:
            if i[0] == put.currentText():
                return i[column_number]

    def defining_language(self):
        translate_text = Translator_Googletrans()
        detect_lang = translate_text.define_language(self.textedit_input.toPlainText())
        lang = self.reading("bd.txt")
        for i in lang:
            if i[1] == detect_lang.lang:
                self.languages_input.setCurrentText(i[0])
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
                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\\" +
                self.id_language(self.languages_input, 2))
            voice.voice_text(self.textedit_input.toPlainText())
        elif put == "output":
            voice = Text_Voiceover(
                "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\\" +
                self.id_language(self.languages_output, 2))
            voice.voice_text(self.textedit_output.toPlainText())

    def voicing_recogn(self):
        voice = Voice_Recognition(self.id_language(self.languages_input, 3))
        try:
            error = QMessageBox()
            error.setWindowTitle("Внимание")
            error.setIcon(QMessageBox.Warning)
            error.setText("Производится запись голоса.\nПожалуйста говорите.")
            error.show()
            QApplication.processEvents()
            self.textedit_input.setText(voice.voice_text())
            error.close()
        except UnknownValueError:
            pass

    def selecting_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QDir.Files)
        if dialog.exec_():
            return dialog.selectedFiles()

    def reading_file(self):
        graphic_formats = ["svg", "pdf", "eps", "ai", "cdr", "png", "jpeg", "gif", "raw", "tiff", "bmp", "psd"]
        file = self.selecting_file()
        if file:
            file = file[0]
            if file.split(".")[-1] in graphic_formats:
                try:
                    image = Technic_OCR(file, self.id_language(self.languages_input, 4))
                    self.textedit_input.setText(image.text_search())
                except:
                    error = QMessageBox()
                    error.setWindowTitle("Произошла ощибка")
                    error.setIcon(QMessageBox.Warning)
                    error.setText("Путь до файла графического формата, содержит кириллицу")
                    error.exec_()
            else:
                text = File_Reading(file)
                self.textedit_input.setText(text.reading())

    def writing_file(self, put):
        file = self.selecting_file()
        if file:
            file = file[0]
            if put == "input":
                file = File_Writing(file, self.textedit_input.toPlainText())
            elif put == "output":
                file = File_Writing(file, self.textedit_output.toPlainText())
            file.writing()

    def scissors(self):
        self.snipper.showFullScreen()
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CrossCursor)
        MainWindow.hide()

    def on_closed(self):
        MainWindow.show()
        try:
            image = Technic_OCR("Images/snapshot.png", self.id_language(self.languages_input, 4))
            self.textedit_input.setText(image.text_search())
        except:
            pass

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Переводчик"))
        self.adding_language()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
