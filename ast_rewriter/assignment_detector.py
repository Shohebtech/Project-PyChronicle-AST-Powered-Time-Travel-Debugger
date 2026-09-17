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
                        "context": context,
                        "kind": "assign"
                    })

        elif isinstance(node, ast.AugAssign):
            
            if isinstance(node.target, ast.Name):
                line_number = node.lineno

                full_expression = ast.unparse(node)

                assignments.append({
                    "variable": node.target.id,
                    "line": line_number,
                    "value": full_expression,
                    "context": context,
                    "kind": "mutation"
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
        if assignment["kind"] == "mutation":
            display_text = assignment["value"]  
        else:
            display_text = f"{assignment['variable']} = {assignment['value']}"

        print(f"Line {assignment['line']}: {display_text} (context: {assignment['context']}, kind: {assignment['kind']})")