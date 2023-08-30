class Interactor:
    def __init__(self, text_list) -> None:
        self.text = text_list # list of strings (where each string has at most 28 characters)

class Pokeball(Interactor):
    def __init__(self, text_list) -> None:
        super().__init__(text_list)