from typing import List, Tuple

# List of variable name, is_used pairs in current context
ContextVarTracker = List[Tuple[str, bool]]

# Holds unused variable error
# line number, column offset, error code, var name
ErrorMessage = Tuple[int, int, int, str]
