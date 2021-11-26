from opentracing import tags

from ..tracer import init_span
from ..tracer.context import close_current_scope, set_tag, trace_exception
from ..tracer.patches import install_default_patches
from ..tracer.tracer import setup_tracer

# for flask framework


def before_request_do():
    # @app.before_request
    setup_tracer(service_name='activity')
    install_default_patches()
    init_span(from_source='Flask')


def after_request_do(response):
    # @app.after_request
    set_tag(tags.HTTP_STATUS_CODE, response.status_code)
    close_current_scope()


def exception_do():
    # @app.errorhandler(Exception)
    # def exception_handler():
    #     exception_do()
    trace_exception()
