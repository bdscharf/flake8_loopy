from typing import List, Tuple

# List of variable name, is_used pairs in current context
ContextVars = List[Tuple[str, bool]]

# Holds unused variable error
# line number, column offset, error code, var name
UnusedVarError = Tuple[int, int, int, str]
