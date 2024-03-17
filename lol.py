txt = "\nimport unittest\nclass TestSeparateParenGroups(unittest.TestCase):\n\n    def test_separate_paren_groups_1(self):\n        self.assertEqual(\n            separate_paren_groups('(()()) ((())) () ((())()())'),\n            ['(()())', '((()))', '()', '((())()())']\n        )\n\n    def test_separate_paren_groups_2(self):\n        self.assertEqual(\n            separate_paren_groups('() (()) ((())) (((())))'),\n            ['()', '(())', '((()))', '(((())))']\n        )\n\n    def test_separate_paren_groups_3(self):\n        self.assertEqual(\n            separate_paren_groups('(()(())((())))'),\n            ['(()(())((())))']\n        )\n\n    def test_separate_paren_groups_4(self):\n        self.assertEqual(\n            separate_paren_groups('( ) (( )) (( )( ))'),\n            ['()', '(())', '(()())']\n        )\n\n    def test_separate_paren_groups_5(self):\n        self.assertEqual(\n            separate_paren_groups('(())'),\n            ['(())']\n        )\n\n    def test_separate_paren_groups_6(self):\n        self.assertEqual(\n            separate_paren_groups('(())(())'),\n            ['(())', '(())']\n        )\n\n    def test_separate_paren_groups_7(self):\n        self.assertEqual(\n            separate_paren_groups('((()))()'),\n            ['((()))', '()']\n        )\n\n\nif __name__ == '__main__':\n    unittest.main(argv=['first-arg-is-ignored'])()\n"
import re

total_num = len(re.findall(r"self\.assert", txt, flags=re.MULTILINE))

print(total_num)