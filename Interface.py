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
