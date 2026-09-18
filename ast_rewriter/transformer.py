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


def transform_simple_assignments(tree):
    
    new_body = []

    for node in tree.body:
        new_body.append(node)

        if isinstance(node, ast.Assign):
            if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                variable_name = node.targets[0].id
                line_number = node.lineno

                track_call = build_track_call(variable_name, line_number)
                new_body.append(track_call)

    tree.body = new_body

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