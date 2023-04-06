from tkinter import *
from tkinter import ttk
from googletrans import Translator


class Language_Translator:
    def __init__(self, input_language='en', output_language='fr'):
        self.translator = Translator()
        self.input_language = input_language
        self.output_language = output_language

    def set_input_language(self, language):
        self.input_language = language

    def set_output_language(self, language):
        self.output_language = language

    def translate(self, text):
        translation = self.translator.translate(text, src=self.input_language, dest=self.output_language)
        return translation.text

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

        self.Trans = Language_Translator()

        self.button = Button(window, text="Перевести", command= self.output_text.insert(0,self.Trans.translate(str(self.input_text.get))),
                             font=("Times New Roman", 14))
        self.button.place(x=300, y=350)