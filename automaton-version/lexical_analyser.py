from typing import List, Dict
from state import *
import sys

class LexicalAnalyzer:
    
    def __init__(self, reserved_words_filename: str):
        self.current_state: State = InitialState(self)
        self.line_count: int = 1
        self.current_word: List[str] = []
        self.lexical_table: List[Dict[str, str]] = []
        self.useless_symbols: List[str] = ['\n', '\t', ' ']
        self.delimitators: List[str] = [';', ',', '.', ':', '(', ')']
        self.reserved_words: List[str] = self.get_reserved_words(reserved_words_filename)

    def transition(self, char: str):
        self.current_state.handle_input(char)

    def classify_word(self):
        
        word: str = ''.join(self.current_word)
        
        if self.current_word == 'or':
            self.current_state = AdditiveOperatorState(self)
        if self.current_word == 'and':
            self.current_state = MultiplicativeOperator(self)        
        
        classification_table: Dict[State, str] = {
            StringState: 'Identificator' if word not in self.reserved_words else 'Reserved Word',
            IntegerState: 'Integer',
            RealState: 'Real',
            DelimitatorState: 'Delimitator',
            AssignState: 'Assign',
            RelationalOperatorState: 'Relational Operator',
            AdditiveOperatorState: 'Additive Operator',
            MultiplicativeOperator: 'Multiplicative Operator'
            
        }   
        self.lexical_table.append({'Token': word, 'Classification': classification_table[self.current_state.__class__], 'Line': self.line_count})
        self.current_word.clear()
        self.current_state = InitialState(self)

    def get_reserved_words(self, filename: str):
        word_list: List[str] = []

        with open(filename, 'r') as file:
            for line in file:
                word: str = line.strip()
                word_list.append(word)

        return word_list
    
    def process_input(self, input_string):
        for char in input_string:
            self.transition(char)
        if isinstance(self.current_state, CommentaryState):
            raise LexicalException("Commentary not closed")
        
        return self.lexical_table
    
    
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
        print(f"{row['Token']:<20}{row['Classification']:<30}{row['Line']:<5}")

    print("-" * 55)