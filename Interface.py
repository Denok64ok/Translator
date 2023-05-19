from abc import ABC, abstractmethod

class Interface_Translator(ABC):
    @abstractmethod
    def set_input_language(self, language):
        pass

    @abstractmethod
    def set_output_language(self, language):
        pass

    @abstractmethod
    def translate(self, text):
        pass
