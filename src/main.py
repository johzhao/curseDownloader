import os

import src.common.logger

src.common.logger.config_logger(os.environ.get('LOG_CONFIG', './conf/logger.json'))  # noqa: E402

import logging
import json
import time

from src.database.database import Database
from src.downloader.downloader import Downloader
from src.exceptions import *

logger = logging.getLogger(__name__)


def download_mod(database: Database, downloader: Downloader, project_id: str, file_id: str, dest_path: str):
    try:
        project_url = database.get_project_url(project_id)
        filename, data = downloader.download_mod(project_url, file_id)
        database.set_data(project_id, file_id, filename, data)
        with open(os.path.join(dest_path, filename), 'wb') as mod_file:
            mod_file.write(data)
    except ProjectNotFoundException:
        project_url = downloader.get_project_url(project_id)
        database.set_project_url(project_id, project_url)
        download_mod(database, downloader, project_id, file_id, dest_path)


def download_mods(manifest_filepath: str, dest_path: str):
    os.makedirs(dest_path, exist_ok=True)

    with open(manifest_filepath, 'r') as manifest_file:
        data = json.load(manifest_file)

    database = Database()
    downloader = Downloader()
    with downloader:
        for file in data['files']:
            project_id = str(file['projectID'])
            file_id = str(file['fileID'])
            try:
                filename, data = database.get_data(project_id, file_id)
                with open(os.path.join(dest_path, filename), 'wb') as mod_file:
                    mod_file.write(data)
            except ModNotFoundException:
                download_mod(database, downloader, project_id, file_id, dest_path)

            time.sleep(1)


def main():
    finished = False
    while not finished:
        try:
            download_mods('./examples/manifest.json', './examples/mods')
        except Exception as e:
            logger.error(e)
            finished = True
        else:
            finished = True


if __name__ == '__main__':
    main()
