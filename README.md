# Lexical Analyzer for Pascal-like Language

This project comprises two versions of a simple lexical analyzer for a Pascal-like programming language. It was developed as part of the Compiler Construction course at the Federal University of Paraíba (UFPB).

## Versions

### Automaton Version

The automaton version of the lexical analyzer utilizes finite automata to tokenize input programs. This version is designed to provide a deep understanding of the lexical analysis process using automata.

### Regex Version

The regex version employs regular expressions (using the Python `re` module) to tokenize input programs. It provides a more concise implementation using regular expression patterns to recognize different lexical elements.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/guga06436/lexical-analyzer.git
    cd lexical-analyzer
    ```

## Usage

To use the lexical analyzer, follow these steps:

1. Choose the directory of the version you want.
1. Ensure you have the file containing reserved words named `pascal_reserved_words.txt`.
3. Ensure you have a pascal program on the directory.
2. Run the `main.py` script:

    ```bash
    python lexical_analyser.py program_name.pas
    ```

3. View the generated lexical table in the console output.

## File Structure

- `lexical_analyzer.py`: Implementation of the LexicalAnalyzer class.
- `state.py`: Implementation of Automata States.
- `pascal_reserved_words.txt`: File containing Pascal-like language reserved words.