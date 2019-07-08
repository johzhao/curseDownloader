import os

import src.common.logger

src.common.logger.config_logger(os.environ.get('LOG_CONFIG', './conf/logger.json'))  # noqa: E402

from src.database.database import Database
import logging
from src.exceptions import *

logger = logging.getLogger(__name__)


def test_database_01():
    project_id = '224472'
    db = Database()
    try:
        url = db.get_project_url(project_id)
        logger.info('The url for project {} was {}'.format(project_id, url))
    except ProjectNotFoundException:
        logger.error('The project {} was not in database.'.format(project_id))
    pass
