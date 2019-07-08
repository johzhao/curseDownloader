import os
import src.common.logger

src.common.logger.config_logger(os.environ.get('LOG_CONFIG', './conf/logger.json'))  # noqa: E402

import logging
import json
import requests

logger = logging.getLogger(__name__)


def test_prototype():
    with open('./examples/manifest.json', 'r') as manifest_file:
        data = json.load(manifest_file)
    data = data['files'][0]
    logger.debug(data)
    url = 'https://minecraft.curseforge.com/projects/{}'.format(data['projectID'])
    logger.info('URL: {}'.format(url))
    res = requests.get(url, allow_redirects=True)
    url = res.url
    url = os.path.join(url, 'download', str(data['fileID']), 'file')
    logger.info('URL: {}'.format(url))
    res = requests.get(url)
    url = res.url
    name = os.path.basename(url)
    with open('./{}'.format(name), 'wb') as res_file:
        res = requests.get(url, stream=True)
        for data in res.iter_content():
            res_file.write(data)
        # res = requests.get(url)
        # res_file.write(res.content)
