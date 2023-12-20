class LexicalException(Exception):
    def __init__(self, mensagem: str="Lexical Error Detected"):
        self.mensagem = mensagem
        super().__init__(self.mensagem)