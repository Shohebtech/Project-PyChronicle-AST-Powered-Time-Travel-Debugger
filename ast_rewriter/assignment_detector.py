import ast

from ast_rewriter.parser import parse_file


def find_assignments(tree):
    
    assignments = []

    def visit(node, context):

        if isinstance(node, ast.Assign):

            line_number = node.lineno
 
            value_text = ast.unparse(node.value)
 
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assignments.append({
                        "variable": target.id,
                        "line": line_number,
                        "value": value_text,
                        "context": context
                    })

        if isinstance(node, ast.If):
            child_context = "if"
        elif isinstance(node, ast.For):
            child_context = "for"
        elif isinstance(node, ast.While):
            child_context = "while"
        elif isinstance(node, ast.FunctionDef):
            child_context = f"function: {node.name}"
        else:
            
            child_context = context
 
        for child in ast.iter_child_nodes(node):
            visit(child, child_context)
 
    visit(tree, "module")

    return assignments


if __name__ == "__main__":

    test_file = "tests/sample_scripts/sample1.py"

    tree = parse_file(test_file)
    assignments = find_assignments(tree)

    print(f"Found {len(assignments)} assignment(s) in {test_file}:")

    for assignment in assignments:
        print(f"Line {assignment['line']}: {assignment['variable']} = {assignment['value']} (context: {assignment['context']})")