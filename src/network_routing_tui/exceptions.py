class EdgeDoesNotExistError(Exception):
    """Raised when attempting to remove an edge that does not exist in the graph."""

    pass


class EdgeOverwriteWarning(Warning):
    """Warning raised when an edge is being overwritten in the graph."""

    pass


class NodeDoesNotExistWarning(Warning):
    """Warning raised when a node does not exist in the graph."""

    pass


class NodeDoesNotExistError(Exception):
    """Exception raised when a node does not exist in the graph."""

    pass


class RemovingEdgeWarning(Warning):
    """Warning raised when removing an edge that does not have any remaining edges."""

    pass


class CommandDoesNotExistError(Exception):
    """Exception raised when a command does not exist."""

    pass