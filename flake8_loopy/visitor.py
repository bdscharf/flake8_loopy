import ast
from typing import List, Set

from flake8_loopy.defs import ContextVarTracker, ErrorMessage

ALLOWED_NAMES = ["_"]


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        # line number, column, code, unused name
        self.errors: List[ErrorMessage] = []
        self.enumerate_contexts: List[ContextVarTracker] = []
        self.context_vars: List[Set[str]] = []

    def _collect_enumerate_names(
        self, node: ast.AST, current_context: ContextVarTracker
    ) -> None:
        """Gathers all names in enumerate Tuple(s) and adds to current context

        Args:
            node (ast.AST): ast node
            current_context (ContextVarTracker): current context variables and uses
        """
        if isinstance(node, ast.Name) and node.id not in ALLOWED_NAMES:
            current_context.append((node.id, False))
        elif isinstance(node, ast.Tuple) or isinstance(node, ast.List):
            for var in node.elts:
                self._collect_enumerate_names(var, current_context)

    def _collect_loop_names(self, node: ast.AST, loop_context: Set[str]) -> None:
        if isinstance(node, ast.Name):
            loop_context.add(node.id)
        elif isinstance(node, ast.Tuple) or isinstance(node, ast.List):
            for var in node.elts:
                self._collect_loop_names(var, loop_context)

    def _find_shadowed_loop_vars(self, node: ast.For) -> None:
        if isinstance(node, ast.For) and node.target:
            loop_ctx: Set[str] = set()
            self._collect_loop_names(node.target, loop_ctx)
        else:
            return
        # Check if created variables have shadowed an outer context variable
        if loop_ctx and self.context_vars:
            shadowed_vars = self.context_vars[-1] & loop_ctx
            if shadowed_vars:
                for shadowed in shadowed_vars:
                    self.errors.append(
                        (node.lineno - 1, node.col_offset, 101, shadowed)
                    )

    def visit_For(self, node: ast.For) -> None:
        has_enumerate = (
            isinstance(node.target, ast.Tuple)
            and node.target.elts
            and isinstance(node.iter, ast.Call)
            and isinstance(node.iter.func, ast.Name)
            and node.iter.func.id == "enumerate"  # type: ignore
        )
        if has_enumerate:
            enumerate_variables: ContextVarTracker = []
            for enumerate_result in node.target.elts:  # type: ignore
                self._collect_enumerate_names(enumerate_result, enumerate_variables)
            self.enumerate_contexts.append(enumerate_variables)

        # Get variable names created by for loop
        self._find_shadowed_loop_vars(node)

        # Skip iteration of the target and iter fields
        for n in node.body:
            self.visit(n)

        if has_enumerate:
            ctx_vars = self.enumerate_contexts.pop()
            for ctx_var, ctx_var_used in ctx_vars:
                if not ctx_var_used:
                    self.errors.append((node.lineno - 1, node.col_offset, 100, ctx_var))

    def visit_Assign(self, node: ast.Assign) -> None:
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.context_vars[-1].add(target.id)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        for this_ctx in self.enumerate_contexts:
            for ctx_var_idx, (ctx_var, _) in enumerate(this_ctx):
                if node.id == ctx_var:
                    this_ctx[ctx_var_idx] = (ctx_var, True)
        self.generic_visit(node)

    def visit_Context(self, node: ast.AST) -> None:
        """Generic to create and pop context variables

        Args:
            node (ast.AST): context-creating node
        """
        self.context_vars.append(set())
        self.generic_visit(node)
        self.context_vars.pop()

    visit_AsyncFunctionDef = visit_Context
    visit_FunctionDef = visit_Context
    visit_Lambda = visit_Context
    visit_Global = visit_Context
    visit_Module = visit_Context
