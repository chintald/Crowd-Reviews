from urllib.parse import urljoin
import graphene
from django.conf import settings
from api.core.enums import AccountErrorCode
from api.core.enums import PermissionEnum
from api.core.enums import PermissionGroupErrorCode
from api.core.enums import UploadErrorCode
from api.core.enums import TopicErrorCode


class Permission(graphene.ObjectType):
    code = PermissionEnum(description="Internal code for permission.", required=True)
    name = graphene.String(description="Describe action(s) allowed to do by permission.",
                           required=True)

    class Meta:
        description = "Represents a permission object in a friendly form."


class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class AccountError(Error):
    code = AccountErrorCode(description="The error code.", required=True)


class StaffError(AccountError):
    permissions = graphene.List(
        graphene.NonNull(PermissionEnum),
        description="List of permissions which causes the error.",
        required=False,
    )
    groups = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of permission group IDs which cause the error.",
        required=False,
    )
    users = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of user IDs which causes the error.",
        required=False,
    )


class PermissionGroupError(Error):
    code = PermissionGroupErrorCode(description="The error code.", required=True)
    permissions = graphene.List(
        graphene.NonNull(PermissionEnum),
        description="List of permissions which causes the error.",
        required=False,
    )
    users = graphene.List(
        graphene.NonNull(graphene.ID),
        description="List of user IDs which causes the error.",
        required=False,
    )


class UploadError(Error):
    code = UploadErrorCode(description="The error code.", required=True)


class Image(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the image.")
    alt = graphene.String(description="Alt text for an image.")

    class Meta:
        description = "Represents an image."

    @staticmethod
    def get_adjusted(image, alt, size, rendition_key_set, info):
        """Return Image adjusted with given size."""
        url = image.url
        url = info.context.build_absolute_uri(url)
        return Image(url, alt)


class File(graphene.ObjectType):
    url = graphene.String(required=True, description="The URL of the file.")
    content_type = graphene.String(
        required=False, description="Content type of the file."
    )

    @staticmethod
    def resolve_url(root, info):
        return info.context.build_absolute_uri(urljoin(settings.MEDIA_URL, root.url))


class PriceRangeInput(graphene.InputObjectType):
    gte = graphene.Float(description="Price greater than or equal to.", required=False)
    lte = graphene.Float(description="Price less than or equal to.", required=False)


class DateRangeInput(graphene.InputObjectType):
    gte = graphene.Date(description="Start date.", required=False)
    lte = graphene.Date(description="End date.", required=False)


class DateTimeRangeInput(graphene.InputObjectType):
    gte = graphene.DateTime(description="Start date.", required=False)
    lte = graphene.DateTime(description="End date.", required=False)


class IntRangeInput(graphene.InputObjectType):
    gte = graphene.Int(description="Value greater than or equal to.", required=False)
    lte = graphene.Int(description="Value less than or equal to.", required=False)


class TopicError(Error):
    code = TopicErrorCode(description="The error code.", required=True)
