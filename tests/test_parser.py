import pytest

from parser import Parser, SemanticError, parse_token_line


def parse_lines(lines):
    tokens = [parse_token_line(line) for line in lines]
    return Parser(tokens).parse()


# Happy paths

def test_parse_object():
    tree = parse_lines([
        "<LBRACE>",
        "<STRING, name>",
        "<COLON>",
        "<STRING, Bob>",
        "<COMMA>",
        "<STRING, age>",
        "<COLON>",
        "<NUMBER, 25>",
        "<RBRACE>",
    ])
    assert tree.node_type == "Object"
    assert len(tree.children) == 2

    first = tree.children[0]
    assert first.node_type == "Pair"
    assert first.children[0].node_type == "Key"
    assert first.children[0].value == "name"
    assert first.children[1].node_type == "String"
    assert first.children[1].value == "Bob"

    second = tree.children[1]
    assert second.children[0].value == "age"
    assert second.children[1].node_type == "Number"
    assert second.children[1].value == "25"


def test_parse_array():
    tree = parse_lines([
        "<LBRACKET>",
        "<NUMBER, 1>",
        "<COMMA>",
        "<NUMBER, 2>",
        "<RBRACKET>",
    ])
    assert tree.node_type == "Array"
    assert [child.value for child in tree.children] == ["1", "2"]
    assert all(child.node_type == "Number" for child in tree.children)


def test_parse_nested():
    tree = parse_lines([
        "<LBRACE>",
        "<STRING, person>",
        "<COLON>",
        "<LBRACE>",
        "<STRING, name>",
        "<COLON>",
        "<STRING, Bob>",
        "<RBRACE>",
        "<COMMA>",
        "<STRING, nums>",
        "<COLON>",
        "<LBRACKET>",
        "<NUMBER, 1>",
        "<COMMA>",
        "<NUMBER, 2>",
        "<RBRACKET>",
        "<RBRACE>",
    ])
    assert tree.node_type == "Object"
    person = tree.children[0].children[1]
    assert person.node_type == "Object"
    assert person.children[0].children[0].value == "name"
    assert person.children[0].children[1].value == "Bob"
    nums = tree.children[1].children[1]
    assert nums.node_type == "Array"
    assert [child.value for child in nums.children] == ["1", "2"]


def test_empty_object():
    tree = parse_lines(["<LBRACE>", "<RBRACE>"])
    assert tree.node_type == "Object"
    assert tree.children == []


def test_empty_array():
    tree = parse_lines(["<LBRACKET>", "<RBRACKET>"])
    assert tree.node_type == "Array"
    assert tree.children == []


def test_empty_input():
    with pytest.raises(Exception):
        Parser([]).parse()


def test_render_tree():
    tree = parse_lines([
        "<LBRACE>",
        "<STRING, name>",
        "<COLON>",
        "<STRING, Bob>",
        "<RBRACE>",
    ])
    assert str(tree) == "Object:\n  Pair:\n    Key: name\n    Value: String: Bob"


def test_missing_colon_raises():
    with pytest.raises(Exception, match="Expected ':'"):
        parse_lines([
            "<LBRACE>",
            "<STRING, name>",
            "<STRING, Bob>",
            "<RBRACE>",
        ])


# SemanticError types 1-7

@pytest.mark.parametrize("lines, error_type", [
    (["<LBRACE>", "<STRING, a>", "<COLON>", "<NUMBER, 3.>", "<RBRACE>"], 1),
    (["<LBRACE>", "<STRING, >", "<COLON>", "<NUMBER, 1>", "<RBRACE>"], 2),
    (["<LBRACE>", "<STRING, a>", "<COLON>", "<NUMBER, 05>", "<RBRACE>"], 3),
    (["<LBRACE>", "<STRING, true>", "<COLON>", "<NUMBER, 1>", "<RBRACE>"], 4),
    (["<LBRACE>", "<STRING, a>", "<COLON>", "<NUMBER, 1>", "<COMMA>",
      "<STRING, a>", "<COLON>", "<NUMBER, 2>", "<RBRACE>"], 5),
    (["<LBRACKET>", "<NUMBER, 1>", "<COMMA>", "<STRING, two>", "<RBRACKET>"], 6),
    (["<LBRACE>", "<STRING, a>", "<COLON>", "<STRING, true>", "<RBRACE>"], 7),
])
def test_semantic_error(lines, error_type):
    with pytest.raises(SemanticError) as exc:
        parse_lines(lines)
    assert exc.value.error_type == error_type
