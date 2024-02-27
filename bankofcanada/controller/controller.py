import configparser

from bankofcanada.utils import get_model

class Controller:
    EXTRACT_MODE = 'extract'
    LOAD_MODE = 'load'
    config_path = 'etc/config/config.ini'
    config_extract = []
    config_load = []

    def __init__(self):
        pass

    def start(self):
        self.get_config_data()

        # Extract
        self.extract_data()

        # Transform

        # Load
        # load_type = self.config_load['type']
        # load_model = get_model(self.LOAD_MODE, load_type)


    def get_config_data(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.config_path)
            config_dict = dict()
            config_dict = {section: dict(config.items(section)) for section in config.sections()}
            for key, conf in config_dict.items():
                config_data = conf
                config_data['name'] = key
                if conf['type'] == 'extract':
                    self.config_extract.append(config_data)
                elif conf['type'] == 'load':
                    self.config_load.append(config_data)
        except Exception as e:
            print('could not read configuration file:' + str(e))

    def extract_data(self):
        if not self.config_extract:
            print("Not data to extract")
        for extract_node in self.config_extract:
            extract_type = extract_node['connect_type']
            extract_model = get_model(self.EXTRACT_MODE, extract_type)
            data = getattr(extract_model, 'request_data', self)(extract_node)