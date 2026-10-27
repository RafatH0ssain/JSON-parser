# JSON Parser

A recursive descent parser for a subset of JSON, written in Python. It tokenizes input, builds a parse tree, and enforces seven semantic rules that go beyond JSON syntax, such as no duplicate keys in objects and no mixed types in arrays.

Two entry points:

- `python parser.py` reads token-per-line files from `input_files/` and writes each parse tree to `output_files/`.
- `python ParserApp.py` opens a PyQt5 desktop app. Paste JSON, click Parse, and the tree appears in the output pane.

## What It Parses

Objects, arrays, strings (with escape sequences), numbers (optional sign, decimals, scientific notation), booleans, and null. The lexer rejects unclosed strings, invalid characters, malformed numbers, and integer literals with leading zeros.

## Semantic Rules

The batch parser reports a numbered `SemanticError` with the offending token when a rule is broken:

1. Decimal numbers need digits on both sides of the point.
2. Object keys cannot be empty.
3. Integer literals cannot have leading zeros.
4. Reserved words (true, false) cannot be object keys.
5. Object keys cannot repeat within an object.
6. Array elements must all have the same type.
7. Reserved keywords (true, false) cannot be used as string values.

## Running the Batch Parser

Requires Python 3, no external packages. Each line of an input file is one token in the form `<TYPE, value>`. A token file for `{"person": {"firstName": "Bob"}}` looks like:

```text
<LBRACE>
<STRING, person>
<COLON>
<LBRACE>
<STRING, firstName>
<COLON>
<STRING, Bob>
<RBRACE>
<RBRACE>
```

Run the parser:

```bash
python parser.py
```

It processes every file in `input_files/` and writes `output_files/parsed_<name>.txt`. Parsed trees print as an indented Object, Pair, Key, Value hierarchy. Semantic errors are written to the output file instead of the tree.

Sample files `input3.txt` through `input10.txt` use the token format. `input1.txt` and `input2.txt` hold raw JSON and will report a parse error; raw JSON is what the GUI accepts.

## Running the GUI

```bash
pip install PyQt5
python ParserApp.py
```

The GUI has its own lexer, so it takes raw JSON typed into the input box. It handles objects, including nested ones, and shows syntax errors in the output pane. It does not enforce the seven semantic rules; use the batch parser for those.

## Project Layout

- `lexer.py`: TokenType, Token, Lexer, and LexerError
- `parser.py`: ParseNode, Parser, SemanticError, and the batch entry point
- `ParserApp.py`: the PyQt5 GUI
- `input_files/`: sample token files
- `output_files/`: generated parse trees

## Tests

None yet.
