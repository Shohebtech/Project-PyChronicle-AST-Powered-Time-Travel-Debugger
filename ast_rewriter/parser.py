import ast


def parse_file(filepath):
    
    with open(filepath, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code, filename=filepath)

    return tree


if __name__ == "__main__":
    
    test_file = "tests/sample_scripts/sample1.py"

    try:
        tree = parse_file(test_file)
        print(f"Successfully parsed: {test_file}")
        print(f"Top-level AST node type: {type(tree).__name__}")
        print(f"Number of top-level statements: {len(tree.body)}")
    except FileNotFoundError:
        print(f"Error: File not found -> {test_file}")
    except SyntaxError as e:
        print(f"Error: Invalid Python syntax in {test_file}")
        print(e)