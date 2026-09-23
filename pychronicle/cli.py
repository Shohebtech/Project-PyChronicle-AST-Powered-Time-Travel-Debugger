import argparse
import os
import sys

from ast_rewriter.parser import parse_file
from ast_rewriter.transformer import transform_simple_assignments, write_transformed_file


def validate_file(filepath):
    
    if not os.path.exists(filepath):
        print(f"Error: File not found -> {filepath}")
        sys.exit(1)

    if not filepath.endswith(".py"):
        print(f"Error: Expected a .py file, got -> {filepath}")
        sys.exit(1)


def run_command(filepath):
    
    validate_file(filepath)

    print(f"Reading: {filepath}")

    try:
        tree = parse_file(filepath)
    except SyntaxError as e:
        print(f"Error: Invalid Python syntax in {filepath}")
        print(e)
        sys.exit(1)

    print("Parsing and transforming...")
    transformed_tree = transform_simple_assignments(tree)

    base_name = os.path.basename(filepath)         
    name_without_ext = os.path.splitext(base_name)[0] 
    output_path = os.path.join("output", f"{name_without_ext}_transformed.py")

    write_transformed_file(transformed_tree, output_path)

    print(f"Transformed file written to: {output_path}")


def main():
   
    parser = argparse.ArgumentParser(
        prog="pychronicle",
        description="PyChronicle - AST-Powered Time-Travel Debugger"
    )

    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run PyChronicle on a Python script")
    run_parser.add_argument("filepath", help="Path to the target .py file")

    args = parser.parse_args()

    if args.command == "run":
        run_command(args.filepath)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()