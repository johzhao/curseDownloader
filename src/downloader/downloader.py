import logging
import os
import requests

logger = logging.getLogger(__name__)


class Downloader:

    def __init__(self):
        self.session = None
        pass

    def __enter__(self):
        self.session = requests.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None

    def get_project_url(self, project_id) -> str:
        url = 'https://minecraft.curseforge.com/projects/{}'.format(project_id)
        logger.info('Request for name of the project {} by url {}'.format(project_id, url))
        response = self.session.get(url, allow_redirects=True)
        return response.url

    def download_mod(self, project_url: str, file_id) -> (str, bytes):
        url = '{}/download/{}/file'.format(project_url, file_id)
        response = requests.get(url)
        filename = os.path.basename(response.url)
        return filename, response.content
