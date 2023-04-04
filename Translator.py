from googletrans import Translator


class Language_Translator:
    def __init__(self, input_language='en', output_language='fr'):
        self.translator = Translator()
        self.input_language = input_language
        self.output_language = output_language

    def translate(self, text):
        translation = self.translator.translate(text, src=self.input_language, dest=self.output_language)
        return translation.text
