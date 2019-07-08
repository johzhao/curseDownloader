import logging
import os

import urllib3

from src.database.database import Database
from src.exceptions import *

logger = logging.getLogger(__name__)


class Downloader:

    def __init__(self):
        self.http = None
        self.database = Database()
        pass

    def __enter__(self):
        self.http = urllib3.PoolManager()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.http.clear()
        self.http = None

    def download_mod(self, project_id: str, file_id: str) -> (str, bytes):
        try:
            return self.database.get_data(project_id, file_id)
        except ModNotFoundException:
            return self._download_mod_impl(project_id, file_id)

    def get_project_url(self, project_id: str) -> str:
        url = 'https://minecraft.curseforge.com/projects/{}'.format(project_id)
        logger.info('Request for name of the project {} by url {}'.format(project_id, url))
        response = self.http.request('GET', url, redirect=False)
        return response.headers['location']

    def download_mod_file(self, project_id: str, project_url: str, file_id: str) -> (str, bytes):
        url = '{}/download/{}/file'.format(project_url, file_id)
        response = self.http.request('GET', url)
        filename = os.path.basename(response.geturl())
        self.database.set_data(project_id, file_id, filename, response.data)
        return filename, response.data

    def _download_mod_impl(self, project_id: str, file_id: str) -> (str, bytes):
        try:
            project_url = self.database.get_project_url(project_id)
        except ProjectNotFoundException:
            project_url = self.get_project_url(project_id)
            self.database.set_project_url(project_id, project_url)

        return self.download_mod_file(project_id, project_url, file_id)
