import transliterate


class StringTransformer:
    def __init__(self) -> None:
        self.eng_string = '''`qwertyuiop[]asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'''
        self.rus_string = '''ёйцукенгшщзхъфывапролджэячсмитьбю.Ё!"№;%:?*()_+ЙЦУКЕНГШЩЗХЪ/ФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,'''
        self.ru2en = {}
        self.en2ru = {}

        for i in range(len(self.eng_string)):
            self.en2ru[self.eng_string[i]] = self.rus_string[i]
            self.ru2en[self.rus_string[i]] = self.eng_string[i]

    def transform_by_layout(self, input_str, to) -> str:
        """
        Transform string by keyboard layout to specific language:

        params:
        to: ['ru', 'en']
        """
        res_str = ''

        if to == 'en':
            for c in input_str:
                if c in self.ru2en:
                    res_str += self.ru2en[c]
                else:
                    res_str += c
        elif to == 'ru':
            for c in input_str:
                if c in self.en2ru:
                    res_str += self.en2ru[c]
                else:
                    res_str += c
        
        return res_str
    
    def transform_by_translit(self, input_str, to) -> str:
        """
        Transform string by keyboard layout to specific language:

        params:
        to: ['ru', 'en']
        """
        if to == 'en':
            return transliterate.translit(input_str, 'ru', reversed=True)
        if to == 'ru':
            return transliterate.translit(input_str, 'ru')
