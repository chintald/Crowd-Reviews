# class CredentialsNotValid(Exception):
#     def __init__(self, message=None):
#         default_message = "Please check the credentials."
#         sucess = False
#         if message is None:
#             message = default_message
#         super().__init__(message)

class UserAccount():
    class CredentialsNotValid(Exception):
        def __init__(self, message=None):
            default_message = ['Please check the credentials.']
            if message is None:
                message = default_message
            super().__init__(message)

    class UserAlreadyExist(Exception):
        def __init__(self, message=None):
            default_message = ['Account already exist.']
            if message is None:
                message = default_message
            super().__init__(message)

    class UsernameExist(Exception):
        def __init__(self, message=None):
            default_message = ['Username already taken, please choose a different one.']
            if message is None:
                message = default_message
            super().__init__(message)
