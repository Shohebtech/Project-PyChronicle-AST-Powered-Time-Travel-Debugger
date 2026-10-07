import ast
import unittest

from ast_rewriter.assignment_detector import find_assignments


class TestAssignmentDetector(unittest.TestCase):

    def test_simple_assignment(self):
        tree = ast.parse("x = 10")
        assignments = find_assignments(tree)

        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0]["variable"], "x")
        self.assertEqual(assignments[0]["value"], "10")
        self.assertEqual(assignments[0]["context"], "module")
        self.assertEqual(assignments[0]["kind"], "assign")

    def test_multiple_target_assignment(self):
        tree = ast.parse("a = b = 5")
        assignments = find_assignments(tree)

        self.assertEqual(len(assignments), 2)
        variables = [a["variable"] for a in assignments]
        self.assertIn("a", variables)
        self.assertIn("b", variables)

    def test_tuple_unpacking_matches_values(self):
        tree = ast.parse("x, y = 1, 2")
        assignments = find_assignments(tree)

        self.assertEqual(len(assignments), 2)
        values_by_variable = {a["variable"]: a["value"] for a in assignments}
        self.assertEqual(values_by_variable["x"], "1")
        self.assertEqual(values_by_variable["y"], "2")

    def test_attribute_assignment_label(self):
        tree = ast.parse("obj.x = 5")
        assignments = find_assignments(tree)

        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0]["variable"], "obj.x")

    def test_subscript_assignment_label(self):
        tree = ast.parse("arr[0] = 42")
        assignments = find_assignments(tree)

        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0]["variable"], "arr[0]")

    def test_mutation_is_tagged_correctly(self):
        tree = ast.parse("x += 5")
        assignments = find_assignments(tree)

        self.assertEqual(len(assignments), 1)
        self.assertEqual(assignments[0]["kind"], "mutation")
        self.assertEqual(assignments[0]["value"], "x += 5")

    def test_if_context(self):
        tree = ast.parse("if x > 5:\n    y = 20")
        assignments = find_assignments(tree)

        self.assertEqual(assignments[0]["context"], "if")

    def test_elif_context(self):
        source = (
            "if x > 10:\n"
            "    y = 1\n"
            "elif x > 5:\n"
            "    y = 2\n"
            "else:\n"
            "    y = 3\n"
        )
        tree = ast.parse(source)
        assignments = find_assignments(tree)

        contexts = [a["context"] for a in assignments]
        self.assertEqual(contexts, ["if", "elif", "else"])

    def test_for_loop_context(self):
        tree = ast.parse("for i in range(3):\n    w = i")
        assignments = find_assignments(tree)

        self.assertEqual(assignments[0]["context"], "for")

    def test_function_context_includes_name(self):
        tree = ast.parse("def greet():\n    message = 'hi'")
        assignments = find_assignments(tree)

        self.assertEqual(assignments[0]["context"], "function: greet")

    def test_try_except_contexts(self):
        source = (
            "try:\n"
            "    a = 1\n"
            "except Exception:\n"
            "    a = 2\n"
            "finally:\n"
            "    done = True\n"
        )
        tree = ast.parse(source)
        assignments = find_assignments(tree)

        contexts = [a["context"] for a in assignments]
        self.assertEqual(contexts, ["try", "except", "finally"])

    def test_no_assignments_returns_empty_list(self):
        tree = ast.parse("print('hello')")
        assignments = find_assignments(tree)

        self.assertEqual(assignments, [])


if __name__ == "__main__":
    unittest.main()