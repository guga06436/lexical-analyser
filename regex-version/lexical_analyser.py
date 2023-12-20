import re
from typing import List
from exception import LexicalException
import sys

class LexicalAnalyzer:
    
    def __init__(self, reserved_words_filename: str):
        self.patterns: List[tuple[str, str]] = [
            ('RESERVED_WORD', r'\b(?:' + '|'.join(map(re.escape, self.get_reserved_words(reserved_words_filename))) + r')\b'),
            ('IDENTIFICADOR', r'\b[a-zA-Z_]\w*\b'),
            ('REAL', r'\b\d+\.\d+\b'),
            ('INT', r'\b\d+\b'),
            ('ASSIGN', r':='),
            ('RELATIONAL_OPERATOR', r'(?:=|<>|<=|>=|<|>)'),
            ('ADDITIVE_OPERATOR', r'(?:\+|-|or)'),
            ('MULTIPLICATIVE_OPERATOR', r'(?:\*|/|and)'),
            ('DELIMITATORS', r'[;,.:()]'),
        ]

    def get_reserved_words(self, filename: str):
        word_list: List[str] = []

        with open(filename, 'r') as file:
            for line in file:
                word: str = line.strip()
                word_list.append(word)

        return word_list

    def process_input(self, input_string: str):
        
        # Remover comentários entre {}
        input_string, comment_count = re.subn(r'\{.*?\}', '', input_string, flags=re.DOTALL)
        
        # Check if there are unclosed comments
        if comment_count % 2 != 0:
            raise LexicalException("Unclosed comment in the input.")
        
        # Compilação dos padrões regex
        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.patterns)
        lexer = re.compile(token_regex, re.VERBOSE)

        # Tokenização (separação dos tokens) da string de entrada
        tokens = []
        lines = input_string.split('\n')

        for i, line in enumerate(lines, start=1):
            matches = list(lexer.finditer(line))
            for match in matches:
                for name, pattern in self.patterns:
                    token = match.group(name)
                    if token:
                        tokens.append((name, token, i))
                        break

    
        # Verificar se há partes não reconhecidas na string de entrada
        remaining_input = input_string
        for token in tokens:
            remaining_input = remaining_input.replace(token[1], '', 1)

        remaining_input = remaining_input.strip()
        if remaining_input:
            raise LexicalException(f"Unrecognized Symbols: '{remaining_input}'")

        # Retornar a lista de tokens com informações de linha
        return tokens
    
def read_program_as_string(filename):
    with open(filename, 'r') as file:
        program_string = file.read()
    return program_string

if __name__ == "__main__":
  
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py input_file.pas")
        sys.exit(1)

    program_filename = sys.argv[1]
    
    # Assuming you have a file named 'reserved_words.txt' containing reserved words
    reserved_words_filename: str = 'pascal_reserved_words.txt'

    # Create an instance of the LexicalAnalyzer
    lexical_analyzer: LexicalAnalyzer = LexicalAnalyzer(reserved_words_filename)

    # Example input string
    input_string = read_program_as_string(program_filename)
    
    # Process the input and get the lexical table
    try:
        lexical_table = lexical_analyzer.process_input(input_string)
    except LexicalException as lex_exception:
        print(f"Error detected: {lex_exception}")
        exit()
    
    # Print the lexical table with formatted columns
    print("-" * 55)
    print(f"{'Token':<20}{'Classification':<30}{'Line':<5}")  # Header
    print("-" * 55)

    for row in lexical_table:
        print(f"{row[0]:<20}{row[1]:<30}{row[2]:<5}")

    print("-" * 55)