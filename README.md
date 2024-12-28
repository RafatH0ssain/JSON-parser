# JSON Parser and Interpreter Project

## Overview

This project is a JSON parser and interpreter that processes tokenized JSON-like input, constructs a parse tree, and handles semantic errors. The parser is designed to process a predefined set of tokens, construct a hierarchical representation of the data, and detect any errors such as duplicate keys in objects or inconsistent types in arrays. The project consists of three parts:

1. **Scanner (Lexer)**: Tokenizes the input string into different token types.
2. **Parser**: Parses the tokenized input into a JSON-like structure and generates a parse tree.
3. **Interpreter**: Outputs the parsed data in a human-readable format and detects errors.

The project is structured into multiple Python files and includes a well-defined directory setup for input and output files.

---

## Table of Contents

1. [Features](#features)
2. [Setup](#setup)
3. [Running the Parser](#running-the-parser)
4. [File Structure](#file-structure)
5. [Detailed Code Explanation](#detailed-code-explanation)
6. [Assumptions](#assumptions)
7. [Example](#example)

---

## Features

- **Tokenizer (Scanner)**: Converts a JSON string into a series of tokens, including objects, arrays, strings, numbers, booleans, nulls, and structural symbols like braces, brackets, commas, and colons.
- **Parser**: Constructs a parse tree from the tokenized input, handling different JSON structures like objects, arrays, key-value pairs, and elements.
- **Error Handling**: Detects semantic errors such as duplicate keys and inconsistent element types within arrays.
- **Interpreter Output**: Converts the parse tree into a readable format, showing a hierarchical representation of the parsed JSON.

---

## Setup

### Prerequisites

- Python 3.x or later

### Directory Structure

Ensure the following directories exist in your project:

- `input_files`: Place the tokenized input files here.
- `output_files`: Parsed output will be written to this directory (it will be created automatically if not already present).

### Install Requirements

There are no external dependencies beyond Python's built-in libraries.

---

## Running the Parser

1. **Prepare Input Files**:
   - Place your input token files in the `input_files` directory. Each line in the file should be in the format `<TokenType, TokenValue>`, as defined by the lexer.
   
2. **Run the Parser**:
   - The script `parser.py` reads the token files from the `input_files` directory, parses them, and writes the output to corresponding files in the `output_files` directory.

3. **Sample Command to Run**:
   ```bash
   python parser.py

## File Structure

The project consists of the following files:

- **`lexer.py`**: Contains the `TokenType` and `Token` classes for tokenizing input strings.
- **`parser.py`**: Contains the main parsing logic and the `ParseNode` and `Parser` classes to build the parse tree and handle errors.
- **`input_files/`**: Directory containing input token files.
- **`output_files/`**: Directory where parsed output files are written.

---

## Detailed Code Explanation


- **`TokenTypes Class`**: Defines different token types (e.g., `LBRACE`, `STRING`, `NUMBER`).
- **`Token Class`**: Represents a single token, including its type and value.
- **`Lexer Class`**: Handles the process of tokenizing the input string. It includes methods like:
  - `advance()`: Moves to the next character.
  - `skip_whitespace()`: Ignores whitespace characters.
  - `recognize_string()`, `recognize_number()`, `recognize_keyword()`: Methods to identify and capture string, number, and keyword tokens respectively.
  - `get_next_token()`: Returns the next token based on the input string.
  - `tokenize()`: Generates a list of tokens by repeatedly calling `get_next_token()`.

**Key Functionality**: This part processes a hardcoded JSON string and converts it into tokens, printing the token list to the console.


- **`ParseNode Class`**: Represents nodes in the parse tree.
- **`Parser Class`**: Main class responsible for parsing the tokens. Key methods include:
  - `parse()`: Initiates the parsing process and builds the parse tree.
  - `parse_object()`, `parse_array()`, `parse_value()`: Methods to handle specific JSON structures (objects, arrays, key-value pairs).
  - `report_error()`: Reports any semantic errors such as duplicate keys in objects or inconsistent types in arrays.
  - `output_tree()`: Outputs the parsed structure as a tree.

**Key Functionality**: This part takes the tokenized input, constructs a parse tree, and outputs it to a file in a readable format.


## Assumptions

- The input files contain well-formed tokens as produced by the lexer.
- Each token in the input is in the format `<TokenType, TokenValue>`.
- The input tokens correspond to the JSON grammar defined in the lexer.
- The parser expects a well-formed input and reports semantic errors for common issues such as:
  - Duplicate keys in objects.
  - Inconsistent types in arrays.
- Whitespace characters are ignored in the lexer.
