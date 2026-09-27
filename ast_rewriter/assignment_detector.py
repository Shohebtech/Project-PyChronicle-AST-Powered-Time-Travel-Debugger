import ast

from ast_rewriter.parser import parse_file


def extract_labels(target):
    
    labels = []

    if isinstance(target, ast.Name):
        labels.append(target.id)
    elif isinstance(target, (ast.Tuple, ast.List)):
        for element in target.elts:
            labels.extend(extract_labels(element))
    elif isinstance(target, (ast.Attribute, ast.Subscript)):
        labels.append(ast.unparse(target))

    return labels


def find_assignments(tree):
    
    assignments = []

    def visit(node, context):
        
        if isinstance(node, ast.Assign):
            line_number = node.lineno

            for target in node.targets:
                labels = extract_labels(target)

                if isinstance(target, (ast.Name, ast.Attribute, ast.Subscript)):
                    value_texts = [ast.unparse(node.value)]

                elif (
                    isinstance(target, (ast.Tuple, ast.List))
                    and isinstance(node.value, (ast.Tuple, ast.List))
                    and len(node.value.elts) == len(labels)
                ):
                    value_texts = [ast.unparse(element) for element in node.value.elts]

                else:
                    shared_value = ast.unparse(node.value)
                    value_texts = [shared_value] * len(labels)

                for label, value_text in zip(labels, value_texts):
                    assignments.append({
                        "variable": label,
                        "line": line_number,
                        "value": value_text,
                        "context": context,
                        "kind": "assign"
                    })

            return 

        elif isinstance(node, ast.AugAssign):
            
            labels = extract_labels(node.target)

            if labels:
                line_number = node.lineno
                full_expression = ast.unparse(node)

                assignments.append({
                    "variable": labels[0],
                    "line": line_number,
                    "value": full_expression,
                    "context": context,
                    "kind": "mutation"
                })

            return  

        elif isinstance(node, ast.If):

            for child in node.body:
                visit(child, "if")

            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                
                visit_elif_chain(node.orelse[0])
            else:
                for child in node.orelse:
                    visit(child, "else")

            return  

        if isinstance(node, ast.For):
            child_context = "for"
        elif isinstance(node, ast.While):
            child_context = "while"
        elif isinstance(node, ast.FunctionDef):
            
            child_context = f"function: {node.name}"
        else:
            
            child_context = context

        for child in ast.iter_child_nodes(node):
            visit(child, child_context)

    def visit_elif_chain(node):
        
        for child in node.body:
            visit(child, "elif")

        if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            visit_elif_chain(node.orelse[0])
        else:
            for child in node.orelse:
                visit(child, "else")

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