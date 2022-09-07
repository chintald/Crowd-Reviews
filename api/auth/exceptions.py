# class CredentialsNotValid(Exception):
#     def __init__(self, message=None):
#         default_message = "Please check the credentials."
#         sucess = False
#         if message is None:
#             message = default_message
#         super().__init__(message)

class UserCredentials():
    def credentials_not_valid(self, message=None):
        if not message:
            message = "Please check the credentials"
        return message

    def user_already_exist(self, message=None):
        if not message:
            message = "Account already exist"
        return message

