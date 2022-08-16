
from algocean.utils import get_object
from algocean.config.loader import ConfigLoader

class BaseModule:
    client = None
    default_cfg_path = None

    def __init__(self, config=None):
        self.config_loader = ConfigLoader()
        self.config = self.get_config(config=config)

        self.client = self.get_clients(self.config.get('client'))

    def get_clients(self, config=None):
        if config != None:
            return self.get_object('client.module.ClientModule')(config={})
            
    def get_config(self, config=None):
        if config == None:

            assert self.default_cfg_path != None
            config = self.config_loader.load(path=self.default_cfg_path)
        return config
    
    @staticmethod
    def get_object(key, prefix = 'algocean', handle_failure= False):
        return get_object(path=key, prefix=prefix, handle_failure=handle_failure)

