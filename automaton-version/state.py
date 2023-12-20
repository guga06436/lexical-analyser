from lexical_analyser import LexicalAnalyzer
from exception import LexicalException

class State:
    def __init__(self, analyzer: LexicalAnalyzer):
        self.analyzer = analyzer

    def handle_input(self, char: str):
        raise NotImplementedError("Subclasses must implement the handle_input method")

class InitialState(State):
    def handle_input(self, char: str):
        if char in self.analyzer.useless_symbols:
            if char == '\n':
                self.analyzer.line_count += 1
        elif char == '{':
            self.analyzer.current_state = CommentaryState(self.analyzer)
        else:
            self.analyzer.current_word.append(char)
            if char.isalpha():
                self.analyzer.current_state = StringState(self.analyzer)
            elif char.isnumeric():
                self.analyzer.current_state = IntegerState(self.analyzer)
            elif char == '.':
                self.analyzer.current_state = DotState(self.analyzer)
            elif char == ':':
                self.analyzer.current_state = ColonState(self.analyzer)
            elif char == "=" or char == "<" or char == ">":
                self.analyzer.current_state = RelationalOperatorState(self.analyzer)
            elif char == "+" or char == "-":
                self.analyzer.current_state = AdditiveOperatorState(self.analyzer)
            elif char == "*" or char == "/":
                self.analyzer.current_state = MultiplicativeOperator(self.analyzer)
            elif char in self.analyzer.delimitators:
                self.analyzer.current_state = DelimitatorState(self.analyzer)
                self.analyzer.current_word.pop(-1)
                self.analyzer.current_state.handle_input(char)
            else:
                raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")

                    

class CommentaryState(State):
    def handle_input(self, char: str):
        if char == '\n':
            self.analyzer.line_count += 1
        if char == '}':
            self.analyzer.current_state = InitialState(self.analyzer)

class StringState(State):
    def handle_input(self, char: str):
        if char in self.analyzer.useless_symbols:
            self.analyzer.classify_word()
            if char == '\n':
                self.analyzer.line_count += 1
        elif char == ':':
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = ColonState(self.analyzer)
        elif char in self.analyzer.delimitators:
            self.analyzer.classify_word()
            self.analyzer.current_state = DelimitatorState(self.analyzer)
            self.analyzer.current_state.handle_input(char)
        elif char == "=" or char == "<" or char == ">":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = RelationalOperatorState(self.analyzer)
        elif char == "+" or char == "-":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = AdditiveOperatorState(self.analyzer)
        elif char == "*" or char == "/":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = MultiplicativeOperator(self.analyzer)
        elif char.isalnum() or char == '_':
            self.analyzer.current_word.append(char)
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")


class IntegerState(State):
    def handle_input(self, char: str):
        if char == '.':
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = RealState(self.analyzer)
        elif char == ':':
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = ColonState(self.analyzer)
        elif char in self.analyzer.delimitators:
            self.analyzer.classify_word()
            self.analyzer.current_state = DelimitatorState(self.analyzer)
            self.analyzer.current_state.handle_input(char)
        elif char == "=" or char == "<" or char == ">":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = RelationalOperatorState(self.analyzer)
        elif char == "+" or char == "-":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = AdditiveOperatorState(self.analyzer)
        elif char == "*" or char == "/":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = MultiplicativeOperator(self.analyzer)
        elif char in self.analyzer.useless_symbols:
            self.analyzer.classify_word()
            if char == '\n':
                self.analyzer.line_count += 1
        elif char.isnumeric():
            self.analyzer.current_state = IntegerState(self.analyzer)
        elif char.lower() == 'e':
            self.analyzer.current_state = Base10State(self.analyzer)
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")


class DotState(State):
    def handle_input(self, char: str):
        if char.isnumeric():
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = RealState(self.analyzer)
        elif char in self.analyzer.useless_symbols:
            self.analyzer.classify_word()
            if char == '\n':
                self.analyzer.line_count += 1
            self.analyzer.current_state = DelimitatorState(self.analyzer)
            self.analyzer.current_state.handle_input(char)
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")


class Base10State(State):
    def handle_input(self, char: str):
        if char.isnumeric():
            self.analyzer.current_word.append(char) 
            self.analyzer.current_state = RealState(self.analyzer)
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")


class RealState(State):
    def handle_input(self, char: str):
        if char.isnumeric():
            self.analyzer.current_word.append(char)
        elif char in self.analyzer.delimitators:
            self.analyzer.classify_word()
            self.analyzer.current_state = DelimitatorState(self.analyzer)
            self.analyzer.current_state.handle_input(char)
        elif char == "=" or char == "<" or char == ">":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = RelationalOperatorState(self.analyzer)
        elif char == "+" or char == "-":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = AdditiveOperatorState(self.analyzer)
        elif char == "*" or char == "/":
            self.analyzer.classify_word()
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = MultiplicativeOperator(self.analyzer)
        elif char.isnumeric():
            self.analyzer.current_state = RealState(self.analyzer)
        elif char in self.analyzer.useless_symbols:
            self.analyzer.classify_word()
            if char == '\n':
                self.analyzer.line_count += 1
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")

            
class DelimitatorState(State):
    def handle_input(self, char: str):
        self.analyzer.current_word.append(char)
        self.analyzer.classify_word()
        
class ColonState(State):
    def handle_input(self, char: str):
        if char == '=':
            self.analyzer.current_state = AssignState(self.analyzer)
            self.analyzer.current_state.handle_input(char)
        else:
            self.analyzer.current_state = DelimitatorState(self.analyzer)
            self.analyzer.classify_word()
            if char.isalnum():
                self.analyzer.current_word.append(char)
                self.analyzer.current_state = StringState(self.analyzer)
            elif char in self.analyzer.useless_symbols:
                if char == '\n':
                    self.analyzer.line_count += 1
            else:
                raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")

        
class AssignState(State):
    def handle_input(self, char: str):
        self.analyzer.current_word.append(char)
        self.analyzer.classify_word()
        
class RelationalOperatorState(State):
    def handle_input(self, char: str):
        if char == "=" or char == "<" or char == ">":
            self.analyzer.current_word.append(char)
        else:
            self.analyzer.classify_word()
            if char.isnumeric():
                self.analyzer.current_state = IntegerState(self.analyzer)
            elif char.isalpha():
                self.analyzer.current_state = StringState(self.analyzer)
            elif char in self.analyzer.useless_symbols:
                self.analyzer.current_state = InitialState(self.analyzer)
            else:
                raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")

class AdditiveOperatorState(State):
    def handle_input(self, char: str):
        self.analyzer.classify_word()
        if char.isnumeric():
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = IntegerState(self.analyzer)
        elif char.isalpha():
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = StringState(self.analyzer)
        elif char in self.analyzer.useless_symbols:
            self.analyzer.current_state = InitialState(self.analyzer)
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")
            
class MultiplicativeOperator(State):
    def handle_input(self, char: str):
        self.analyzer.classify_word()
        if char.isnumeric():
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = IntegerState(self.analyzer)
        elif char.isalpha():
            self.analyzer.current_word.append(char)
            self.analyzer.current_state = StringState(self.analyzer)
        elif char in self.analyzer.useless_symbols:
            self.analyzer.current_state = InitialState(self.analyzer)
        else:
            raise LexicalException(f"Char {char} not recognized on line {self.analyzer.line_count}")