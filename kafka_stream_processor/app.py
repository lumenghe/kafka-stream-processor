import asyncio
import logging
import logging.config
import os
import traceback

from kafka_stream_processor.user import User as UserProcessor

logger = logging.getLogger(__name__)



def main():
    # create config builder for getting sub keys config
    try:
        processor = UserProcessor("http://ksqldb-server:8088")

        processor.start()

    # pylint: disable=broad-except
    # reason: we want to catch all exceptions
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}: {}".format(e.__class__.__name__, stacktrace))
