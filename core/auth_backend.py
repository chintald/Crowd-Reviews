from django.core.exceptions import ValidationError
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from api.jwt import get_token_from_request, get_user_from_access_token

USER = get_user_model()


class JSONWebTokenBackend(ModelBackend):
    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        token = get_token_from_request(request)
        if not token:
            return None
        return get_user_from_access_token(token)

    def get_user(self, user_id):
        try:
            return USER.objects.get(email=user_id, is_active=True)
        except USER.DoesNotExist:
            return None

    def _get_user_permissions(self, user_obj):
        # overwrites base method to force using our permission field
        return user_obj.effective_permissions

    def _get_group_permissions(self, user_obj):
        # overwrites base method to force using our permission field
        return user_obj.effective_permissions

    def _get_permissions(self, user_obj, obj, from_name):
        """Return the permissions of `user_obj` from `from_name`.
        `from_name` can be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = "_effective_permissions_cache"
        if not getattr(user_obj, perm_cache_name, None):
            perms = getattr(self, "_get_%s_permissions" % from_name)(user_obj)
            perms = perms.values_list("content_type__app_label", "codename").order_by()
            setattr(
                user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms}
            )
        return getattr(user_obj, perm_cache_name)


class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        user = self.get_user(username)

        if user:
            if user.is_blocked:
                raise ValidationError("Your account has been inactivated, kindly contact your administrator.")
            if user.check_password(password):
                return user

            else:
                return None
        else:
            return None

    def get_user(self, username):
        try:
            return USER.objects.get(
                (Q(email=username) | Q(username=username))
            )
        except Exception:
            return None
