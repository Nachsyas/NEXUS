class ProjectError(Exception):
    """Base exception for Project domain errors."""

    def __init__(self, code: str, message: str, status_code: int = 400) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ProjectNotFoundError(ProjectError):
    def __init__(self, message: str = "Project not found.") -> None:
        super().__init__(code="PROJECT_NOT_FOUND", message=message, status_code=404)


class ProjectSlugConflictError(ProjectError):
    def __init__(self, message: str = "A project with this slug already exists for user.") -> None:
        super().__init__(code="PROJECT_SLUG_CONFLICT", message=message, status_code=409)


class ProjectInvalidStateError(ProjectError):
    def __init__(self, message: str = "Project operation invalid in current state.") -> None:
        super().__init__(code="PROJECT_INVALID_STATE", message=message, status_code=400)
