# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

from opentracing_instrumentation.client_hooks import install_patches

from .config import Config


def _install_patches(patchers="all"):
    """ Patch 基础库. """

    opentracing_instrumentation_alls = {
        'boto3': 'opentracing_instrumentation.client_hooks.boto3.install_patches',
        'celery': 'opentracing_instrumentation.client_hooks.celery.install_patches',
        'mysqldb': 'opentracing_instrumentation.client_hooks.mysqldb.install_patches',
        'psycopg2': 'opentracing_instrumentation.client_hooks.psycopg2.install_patches',
        'strict_redis': 'opentracing_instrumentation.client_hooks.strict_redis.install_patches',
        'sqlalchemy': 'opentracing_instrumentation.client_hooks.sqlalchemy.install_patches',
        'tornado_http': 'opentracing_instrumentation.client_hooks.tornado_http.install_patches',
        'urllib': 'opentracing_instrumentation.client_hooks.urllib.install_patches',
        'urllib2': 'opentracing_instrumentation.client_hooks.urllib2.install_patches',
        'requests': 'opentracing_instrumentation.client_hooks.requests.install_patches',
    }

    opentracing_patchers = []

    if patchers == "all":
        opentracing_patchers = list(opentracing_instrumentation_alls.values())
    else:
        for lib in patchers:
            lib = lib.strip()
            if lib in opentracing_instrumentation_alls:
                opentracing_patchers.append(opentracing_instrumentation_alls[lib])
            else:
                print('WARN: lib {} not in current patch lib list {}'.format(
                    lib,
                    opentracing_instrumentation_alls.keys()
                ))

    if opentracing_patchers:
        install_patches(patchers=opentracing_patchers)
        print('patched libs from gm-tracer(opentracing_instrumentation): {}'.format(opentracing_patchers))


def install_default_patches():
    # 当环境变量 TRACING_ENABLE=False 或者 TRACE_DISABLE_PATCH=True 时不patch libs
    if not Config.TRACING_ENABLE:
        print('disable trace patch')
        return False

    if Config.PATCH_ALL:
        _install_patches(patchers="all")
        return True

    _install_patches(Config.PATCH_LIBS)
    return True
