import ast
import io
import unittest
from contextlib import redirect_stdout

from ast_rewriter.transformer import transform_simple_assignments


def run_transformed_source(source_code):
    
    tree = ast.parse(source_code)
    transformed_tree = transform_simple_assignments(tree)
    transformed_source = ast.unparse(transformed_tree)

    output = io.StringIO()
    with redirect_stdout(output):
        exec(transformed_source, {})

    return output.getvalue()


class TestTransformer(unittest.TestCase):

    def test_simple_assignment_is_tracked_when_run(self):
        output = run_transformed_source("x = 10")
        self.assertIn("[TRACK] Line 1: x = 10", output)

    def test_multiple_target_assignment_is_tracked(self):
        output = run_transformed_source("a = b = 5")
        self.assertIn("a = 5", output)
        self.assertIn("b = 5", output)

    def test_mutation_is_tracked_with_new_value(self):
        output = run_transformed_source("x = 10\nx += 5")
        self.assertIn("x = 15", output)

    def test_loop_assignment_tracked_once_per_iteration(self):
        output = run_transformed_source("for i in range(3):\n    w = i")
        track_lines = [line for line in output.splitlines() if "w = " in line]
        self.assertEqual(len(track_lines), 3)

    def test_function_assignment_tracked_only_when_called(self):
        source = (
            "def greet():\n"
            "    message = 'hello'\n"
            "    return message\n"
        )
        
        output = run_transformed_source(source)
        self.assertEqual(output, "")

        output_when_called = run_transformed_source(source + "greet()\n")
        self.assertIn("message = hello", output_when_called)

    def test_original_source_text_is_not_modified(self):
        original_source = "x = 10"
        tree = ast.parse(original_source)
        transform_simple_assignments(tree)

        self.assertEqual(original_source, "x = 10")

    def test_attribute_assignment_tracks_real_value(self):
        source = (
            "class Counter:\n"
            "    def __init__(self):\n"
            "        self.count = 0\n"
            "counter = Counter()\n"
            "counter.count = 99\n"
        )
        output = run_transformed_source(source)
        self.assertIn("counter.count = 99", output)


if __name__ == "__main__":
    unittest.main()