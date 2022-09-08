import opentracing
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject

from core.tracing import should_trace
from api.views import API_PATH, GraphQLView
from graphql import ResolveInfo


def get_user(request):
    if not hasattr(request, "_cached_user"):
        request._cached_user = authenticate(request=request)
    return request._cached_user


class JWTMiddleware:
    def resolve(self, next, root, info, **kwargs):
        request = info.context

        def user():
            return get_user(request) or AnonymousUser()

        request.user = SimpleLazyObject(lambda: user())
        return next(root, info, **kwargs)


class OpentracingGrapheneMiddleware:
    @staticmethod
    def resolve(next_, root, info: ResolveInfo, **kwargs):
        if not should_trace(info):
            return next_(root, info, **kwargs)
        operation = f"{info.parent_type.name}.{info.field_name}"
        with opentracing.global_tracer().start_active_span(operation) as scope:
            span = scope.span
            span.set_tag(opentracing.tags.COMPONENT, "graphql")
            span.set_tag("graphql.parent_type", info.parent_type.name)
            span.set_tag("graphql.field_name", info.field_name)
            return next_(root, info, **kwargs)


def process_view(self, request, view_func, *args):
    if hasattr(view_func, "view_class") and issubclass(
        view_func.view_class, GraphQLView
    ):
        request._graphql_view = True


if settings.ENABLE_DEBUG_TOOLBAR:
    import warnings

    try:
        from graphiql_debug_toolbar.middleware import DebugToolbarMiddleware
    except ImportError:
        warnings.warn("The graphiql debug toolbar was not installed.")
    else:
        DebugToolbarMiddleware.process_view = process_view