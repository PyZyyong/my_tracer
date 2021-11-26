import traceback

from opentracing import tags

from tracer import set_tag, init_span
from tracer.context import close_current_scope, trace_exception
from tracer.patches import install_default_patches
from tracer.tracer import setup_tracer

try:
    # django>=1.10
    from django.utils.deprecation import MiddlewareMixin
    MiddlewareClass = MiddlewareMixin
except ImportError:
    # django<1.10
    MiddlewareClass = object


# for django framework
class TracerMiddleware(MiddlewareClass):
    def __init__(self, get_response=None):
        self.get_response = get_response
        install_default_patches()
        setup_tracer()

    def process_request(self, request):
        self._init_span(request)

    def process_exception(self, request, e):
        format_exc = traceback.format_exc()
        trace_exception(format_exc)

    def process_response(self, request, response):
        set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        close_current_scope()

        return response

    def _init_span(self, request):
        init_span(request)
