# coding = utf-8
from __future__ import unicode_literals, print_function, absolute_import

import os

from ..utils import get_boolean


class Config(object):
    # 启用 Trace 上报，默认为True，设为False则不上报请求trace信息，不patch libs
    # TRACING_ENABLE = get_boolean(os.environ.get('TRACING_ENABLE', 'true'), default=True)
    TRACING_ENABLE = True

    # from 0 ~ 1, 当 TRACING_ENABLE 为true, 且 TRACE_SAMPLE_RATE设值 >= 0时生效
    SAMPLE_RATE = float(os.environ.get('TRACE_SAMPLE_RATE', -1))

    SERVICE_NAME = os.environ.get('TRACE_SERVICE_NAME', 'UNKNOWN')

    # 是否启用128bit trace id, 默认启用，兼容 envoy 上报的数据
    TRACE_128BIT_TRACE_ID = get_boolean(os.environ.get('TRACE_128BIT_TRACE_ID', 'true'), default=True)
    # 是否启用 b3 format 的 header, 默认启用，兼容 envoy 上报的数据
    TRACE_B3_FORMAT = get_boolean(os.environ.get('TRACE_B3_FORMAT', 'true'), default=True)

    # patch 所有lib, 默认 false
    # PATCH_ALL = get_boolean(os.environ.get('TRACE_PATCH_ALL', 'false'), default=False)
    PATCH_ALL = True
    # patch(trace) 的 lib
    PATCH_LIBS = list(filter(lambda lib: lib != '', os.environ.get('TRACE_PATCH_LIBS', '').split(',')))

    # 是否记录请求参数，默认为 True，记录
    TRACE_REQ_PARAM = get_boolean(os.environ.get('TRACE_REQ_PARAM', 'true'), default=True)
    # 是否记录请求响应，默认为 True，记录
    TRACE_RESP_BODY = get_boolean(os.environ.get('TRACE_RESP_BODY', 'true'), default=True)

    MAX_TRACEBACK_LENGTH = int(os.environ.get('TRACE_MAX_TRACEBACK_LENGTH', '40960'))
    MAX_TAG_VALUE_LENGTH = int(os.environ.get('TRACE_MAX_TAG_VALUE_LENGTH', '4096'))
