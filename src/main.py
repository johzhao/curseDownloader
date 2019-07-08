import os

import src.common.logger

src.common.logger.config_logger(os.environ.get('LOG_CONFIG', './conf/logger.json'))  # noqa: E402

import logging

logger = logging.getLogger(__name__)


def main():
    pass


if __name__ == '__main__':
    main()
