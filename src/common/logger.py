import json
import logging.config
import os


def config_logger(conf_file_path: str):
    if os.path.exists(conf_file_path) and os.path.isfile(conf_file_path):
        with open(conf_file_path, 'r') as conf_file:
            data = json.load(conf_file)
        logging.config.dictConfig(data)
    else:
        raise ValueError('The configuration file {} was not exist or not a file.'.format(conf_file_path))
