# coding=utf-8
from __future__ import absolute_import

import traceback

import opentracing
from opentracing import tags, logs


def get_current_scope():
    return opentracing.tracer.scope_manager.active


def close_current_scope():
    scope = get_current_scope()
    if scope:
        scope.close()


def get_current_span():
    scope = get_current_scope()
    return scope.span if scope else None


def active_span(span):
    return opentracing.tracer.scope_manager.activate(span, finish_on_close=True)


def log_kv(kv):
    """
    kv: dict
    """
    span = get_current_span()
    if span:
        return span.log_kv(kv)


def set_tag(k, v):
    span = get_current_span()
    if span:
        return span.set_tag(k, v)


def trace_exception(exc_str=None):
    span = get_current_span()
    if span:
        if exc_str is None:
            exc_str = traceback.format_exc()
        span.set_tag(tags.ERROR, True)
        span.set_tag(tags.SAMPLING_PRIORITY, 1)
        span.log_kv({logs.STACK: exc_str})
