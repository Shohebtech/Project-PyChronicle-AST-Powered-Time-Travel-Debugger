import ast

from ast_rewriter.parser import parse_file


def find_assignments(tree):
    
    assignments = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                variable_name = node.targets[0].id
                line_number = node.lineno

                value_text = ast.unparse(node.value)

                assignments.append({
                    "variable": variable_name,
                    "line": line_number,
                    "value": value_text
                })

    return assignments


if __name__ == "__main__":

    test_file = "tests/sample_scripts/sample1.py"

    tree = parse_file(test_file)
    assignments = find_assignments(tree)

    print(f"Found {len(assignments)} assignment(s) in {test_file}:")
    for assignment in assignments:
        print(f"Line {assignment['line']}: {assignment['variable']} = {assignment['value']}")