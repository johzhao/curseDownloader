import os

import src.common.logger

src.common.logger.config_logger(os.environ.get('LOG_CONFIG', './conf/logger.json'))  # noqa: E402

import logging
import json

from src.downloader.downloader import Downloader

logger = logging.getLogger(__name__)


def download_mods(manifest_filepath: str, dest_path: str):
    os.makedirs(dest_path, exist_ok=True)

    with open(manifest_filepath, 'r') as manifest_file:
        data = json.load(manifest_file)

    downloader = Downloader()
    with downloader:
        for file in data['files']:
            project_id = str(file['projectID'])
            file_id = str(file['fileID'])

            filename, data = downloader.download_mod(project_id, file_id)
            with open(os.path.join(dest_path, filename), 'wb') as mod_file:
                mod_file.write(data)


def main():
    finished = False
    while not finished:
        try:
            download_mods('./examples/manifest.json', './mods')
            finished = True
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    main()
