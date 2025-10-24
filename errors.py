"""Custom exceptions for the Sequential Thinking MCP server."""


class SequentialThinkingError(Exception):
    """Base exception for all Sequential Thinking MCP errors."""
    pass


class SessionError(SequentialThinkingError):
    """Raised when session operations fail."""
    pass


class NoActiveSessionError(SessionError):
    """Raised when no active session is available."""
    pass


class SessionNotFoundError(SessionError):
    """Raised when a specific session cannot be found."""
    pass


class ValidationError(SequentialThinkingError):
    """Raised when input validation fails."""
    pass


class StorageError(SequentialThinkingError):
    """Raised when file/disk operations fail."""
    pass


class MemoryError(SequentialThinkingError):
    """Raised when memory operations fail."""
    pass


class BranchError(SequentialThinkingError):
    """Raised when branch operations fail."""
    pass


class PackageExplorationError(SequentialThinkingError):
    """Raised when package exploration fails."""
    pass


class ExportError(SequentialThinkingError):
    """Raised when export operations fail."""
    pass