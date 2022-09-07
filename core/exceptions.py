class OtpExpiredError(Exception):
    def __init__(self, message=None):
        default_message = "The One time password you have entered is expired. please create new one"
        if message is None:
            message = default_message
        super().__init__(message)


class PermissionDenied(Exception):
    def __init__(self, message=None):
        default_message = "You do not have permission to perform this action"
        if message is None:
            message = default_message
        super().__init__(message)


class ReadOnlyException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = "API runs in read-only mode"
        super().__init__(msg)
