import os

import src.common.logger

src.common.logger.config_logger(os.environ.get('LOG_CONFIG', './conf/logger.json'))  # noqa: E402

from src.downloader.downloader import Downloader
import logging
import json
import time

logger = logging.getLogger(__name__)


def test_downloader_01():
    with open('./examples/manifest.json', 'r') as manifest_file:
        data = json.load(manifest_file)

    project_ids = [file['projectID'] for file in data['files']]
    downloader = Downloader()
    with downloader:
        for index, project_id in enumerate(project_ids):
            if index >= 10:
                break
            project_url = downloader.get_project_url(project_id)
            name = os.path.basename(project_url)
            logger.debug('The name of project {} was {}'.format(project_id, name))
            time.sleep(0.5)


def test_downloader_02():
    with open('./examples/manifest.json', 'r') as manifest_file:
        data = json.load(manifest_file)

    project_ids = [file['projectID'] for file in data['files']]
    file_ids = [file['fileID'] for file in data['files']]

    downloader = Downloader()
    with downloader:
        for index, project_id in enumerate(project_ids):
            if index >= 3:
                break
            project_url = downloader.get_project_url(project_id)
            name = os.path.basename(project_url)
            logger.debug('The name of project {} was {}'.format(project_id, name))

            filename, data = downloader.download_mod_file(project_id, project_url, file_ids[index])
            with open('{}'.format(filename), 'wb') as mod_file:
                mod_file.write(data)

            time.sleep(0.5)
