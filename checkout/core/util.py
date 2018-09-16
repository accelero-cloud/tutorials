from appkernel import config
from appkernel.http_client import HttpClientServiceProxy


class LazyLoaderProxy(object):

    def __init__(self, service_name):
        self.service_name = service_name

    def __getattr__(self, item):
        if isinstance(item, str) and item in ['client_proxy', 'member_tag']:
            raise AttributeError(f'{item} is not on this object')
        if not hasattr(self, 'client_proxy') and hasattr(config, 'cfg_engine'):
            url = config.cfg_engine.get(f'appkernel.services.{self.service_name}')
            if not url:
                url = 'http://localhost:5000/'
            self.client_proxy = HttpClientServiceProxy(url)
        elif not hasattr(self, 'client_proxy') and not hasattr(config, 'cgf_engine'):
            raise AttributeError('Config object has no attribute cfg_engine')
        return getattr(self.client_proxy, item)


def get_client_proxy(service_name):
    return LazyLoaderProxy(service_name)
