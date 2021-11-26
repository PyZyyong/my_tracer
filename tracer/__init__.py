import opentracing
from flask import Request, request as f_request
from opentracing import Format, tags

from ..tracer.context import set_tag


def wsgi_header_convert(wsgi_header):
    """
        HTTP_X_* -> x-*
    """
    return wsgi_header.lstrip('HTTP_').replace('_', '-').lower()


def init_span(from_source, request: Request = f_request):
    """
    :return:
    """
    from .. import get_tracer
    if from_source == 'Flask':
        headers = {wsgi_header_convert(_k): _v for _k, _v in request.environ.items()}
    else:
        headers = {wsgi_header_convert(_k): _v for _k, _v in request.META.items()}

    try:
        span_ctx = get_tracer().extract(
            format=Format.HTTP_HEADERS,
            carrier=headers
        )
    except:
        span_ctx = None

    span = get_tracer().start_span(
        operation_name=request.path,
        child_of=span_ctx,
        tags={
            tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER
        },
    )
    opentracing.tracer.scope_manager.activate(span, True)
    set_tag("pattern", request.path)
