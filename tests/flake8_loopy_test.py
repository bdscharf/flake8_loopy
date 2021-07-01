import ast
from typing import Set

from flake8_loopy import LoopyPlugin


def _results(s: str) -> Set[str]:
    tree = ast.parse(s)
    plugin = LoopyPlugin(tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results("") == set()


def test_wasted_count():
    ret = _results(
        """
table = ["Row 1", "Row 2"]
for i, row in enumerate(table):
    print(row)
print("Loop ended.")
"""
    )
    assert ret == {"2:0 LPY100 variable 'i' created by enumerate() is not used"}


def test_used_count():
    assert (
        _results(
            """
table = ["Row 1", "Row 2"]
for i, row in enumerate(table):
    print(i)
    print(row)
print("Loop ended.")
"""
        )
        == set()
    )


def test_one_wasted():
    ret = _results(
        """
table = ["Row 1", "Row 2"]
for i, row in enumerate(table):
    for c_idx, c in enumerate(row):
        print(row)
        print(c_idx)
        print(c)
"""
    )
    assert ret == {"2:0 LPY100 variable 'i' created by enumerate() is not used"}


def test_nested_waste():
    ret = _results(
        """
table = ["Row 1", "Row 2"]
for i, row in enumerate(table):
    for c_idx, c in enumerate(row):
        print(row)
        print(i)
        print(c)
"""
    )
    assert ret == {"3:4 LPY100 variable 'c_idx' created by enumerate() is not used"}


def test_underscore_allowed():
    assert (
        _results(
            """
table = ["Row 1", "Row 2"]
for i, _ in enumerate(table):
    print(i)
print("Loop ended.")
"""
        )
        == set()
    )


def test_var_is_shadowed():
    ret = _results(
        """
i = "Hello there"
table = ["Row 1", "Row 2"]
for i in table:
    print(i)
print(i)
"""
    )
    assert ret == {
        "3:0 LPY101 variable 'i' created by for loop shadows another value in its context"
    }


def test_var_not_shadowed():
    assert (
        _results(
            """
j = "my message"
table = ["Row 1", "Row 2"]
for i in table:
    i = "message"
print(j)
"""
        )
        == set()
    )


def test_nested_shadowing():
    ret = _results(
        """
j = "my message"
table = ["Row 1", "Row 2"]
for i in table:
    i = "message"
    for j in table:
        print(j)
print(j)
"""
    )
    assert ret == {
        "5:4 LPY101 variable 'j' created by for loop shadows another value in its context"
    }
