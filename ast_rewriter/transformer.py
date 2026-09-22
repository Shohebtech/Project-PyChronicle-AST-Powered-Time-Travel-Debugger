import ast
import os

from ast_rewriter.parser import parse_file

TRACK_STUB_CODE = (
    "def track(name, value, line):\n"
    "    print(f\"[TRACK] Line {line}: {name} = {value}\")\n"
)


def build_track_call(variable_name, line_number):
    
    call_node = ast.Expr(
        value=ast.Call(
            func=ast.Name(id="track", ctx=ast.Load()),
            args=[
                ast.Constant(value=variable_name),  
                ast.Name(id=variable_name, ctx=ast.Load()),  
            ],
            keywords=[
                ast.keyword(arg="line", value=ast.Constant(value=line_number)),
            ],
        )
    )
    return call_node


def transform_block(statements):
    
    new_statements = []

    for node in statements:
        new_statements.append(node)

        if isinstance(node, ast.Assign):
            line_number = node.lineno

            for target in node.targets:
                if isinstance(target, ast.Name):
                    track_call = build_track_call(target.id, line_number)
                    new_statements.append(track_call)

        elif isinstance(node, (ast.If, ast.For, ast.While)):
           
            node.body = transform_block(node.body)

            if node.orelse:
                node.orelse = transform_block(node.orelse)

        elif isinstance(node, ast.FunctionDef):
            node.body = transform_block(node.body)

        elif isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Name):
                line_number = node.lineno
                track_call = build_track_call(node.target.id, line_number)
                new_statements.append(track_call)

    return new_statements


def transform_simple_assignments(tree):
   
    tree.body = transform_block(tree.body)

    stub_tree = ast.parse(TRACK_STUB_CODE)
    tree.body.insert(0, stub_tree.body[0])

    ast.fix_missing_locations(tree)

    return tree


def write_transformed_file(tree, output_path):
   
    source_code = ast.unparse(tree)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(source_code)


if __name__ == "__main__":

    input_file = "tests/sample_scripts/sample1.py"
    output_file = "output/sample1_transformed.py"

    tree = parse_file(input_file)
    transformed_tree = transform_simple_assignments(tree)
    write_transformed_file(transformed_tree, output_file)

    print(f"Transformed version written to: {output_file}")
    print("Run it with: python output/sample1_transformed.py")