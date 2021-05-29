import ast
from typing import List

from flake8_loopy.defs import ContextVars, UnusedVarError


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        # line number, column, code, unused name
        self.unused_errors: List[UnusedVarError] = []
        self.enumerate_context: List[ContextVars] = []

    def collect_names(self, node: ast.AST, current_context: ContextVars) -> None:
        if isinstance(node, ast.Name) and node.id != "_":
            current_context.append((node.id, False))
        elif isinstance(node, ast.Tuple):
            for var in node.elts:
                self.collect_names(var, current_context)

    def visit_For(self, node: ast.For) -> None:
        has_enumerate = (
            isinstance(node.target, ast.Tuple)
            and node.target.elts
            and isinstance(node.iter, ast.Call)
            and node.iter.func.id == "enumerate"  # type: ignore
        )
        if has_enumerate:
            enumerate_variables: ContextVars = []
            for enumerate_result in node.target.elts:  # type: ignore
                self.collect_names(enumerate_result, enumerate_variables)
            self.enumerate_context.append(enumerate_variables)

        # Skip iteration of the target and iter fields
        for n in node.body:
            self.visit(n)

        if has_enumerate:
            ctx_vars = self.enumerate_context.pop()
            for ctx_var, ctx_var_used in ctx_vars:
                if not ctx_var_used:
                    self.unused_errors.append(
                        (node.lineno - 1, node.col_offset, 100, ctx_var)
                    )

    def visit_Name(self, node: ast.Name) -> None:
        for this_ctx in self.enumerate_context:
            for ctx_var_idx, (ctx_var, _) in enumerate(this_ctx):
                if node.id == ctx_var:
                    this_ctx[ctx_var_idx] = (ctx_var, True)
        self.generic_visit(node)
