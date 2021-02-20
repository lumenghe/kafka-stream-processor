import logging

from ksql import KSQLAPI
from ksql.errors import KSQLError

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, url):
        self.client = KSQLAPI(url)

    def start(self):
        self.create_stream_from_topic()
        self.rename_rowkey()
        self.join()
        # self.query()

    def create_stream_from_topic(self):
        raise NotImplementedError(
            self.__class__.__name__ + " must implement processor"
        )

    def rename_rowkey(self):
        raise NotImplementedError(
            self.__class__.__name__ + " must implement processor"
        )

    def join(self):
        raise NotImplementedError(
            self.__class__.__name__ + " must implement processor"
        )

    def query(self):
        query = self.client.query(
            query_string="select * from user emit changes",
            stream_properties={"ksql.streams.auto.offset.reset": "earliest"},
        )
        for item in query:
            logger.info(item)

    def ksql(self, ksql_string, stream_properties=None):
        try:
            self.client.ksql(
                ksql_string=ksql_string, stream_properties=stream_properties
            )
        except KSQLError as e:
            logger.info(e)

    def create_stream(
        self, table_name, columns_type, topic, value_format="JSON"
    ):
        try:
            self.client.create_stream(
                table_name=table_name,
                columns_type=columns_type,
                topic=topic,
                value_format=value_format,
            )
        except KSQLError as e:
            logger.info(e)
