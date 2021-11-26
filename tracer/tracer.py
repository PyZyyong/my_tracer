# coding=utf-8
from __future__ import absolute_import

from jaeger_client import Config

from .config import Config as TracerConf


def setup_tracer(service_name=None):
    """入口服务使用，初始化链路监控"""
    config = {
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
        'generate_128bit_trace_id': True,
        'propagation': 'b3',
        'max_traceback_length': TracerConf.MAX_TRACEBACK_LENGTH,
        'max_tag_value_length': TracerConf.MAX_TAG_VALUE_LENGTH,
    }

    if service_name is None:
        service_name = TracerConf.SERVICE_NAME

    # use env to disable some conf
    if not TracerConf.TRACE_128BIT_TRACE_ID:
        del config['generate_128bit_trace_id']
    if not TracerConf.TRACE_B3_FORMAT:
        del config['propagation']

    # disable tracer report when TRACING_ENABLE set to False
    if not TracerConf.TRACING_ENABLE:
        print('env TRACING_ENABLE set to False, disable tracer report')
        config['sampler'] = {'type': 'const', 'param': 0}
    elif 0 <= TracerConf.SAMPLE_RATE <= 1:
        print('env TRACE_SAMPLE_RATE set to {}'.format(TracerConf.SAMPLE_RATE))
        config['sampler'] = {'type': 'probabilistic', 'param': TracerConf.SAMPLE_RATE}

    conf = Config(
        service_name=service_name,
        config=config,
        validate=True,
    )
    conf.initialize_tracer()
