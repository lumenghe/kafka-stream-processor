import logging

from kafka_stream_processor.processor import Processor
from ksql.errors import KSQLError

logger = logging.getLogger(__name__)


class User(Processor):
    def __init__(self, url):
        super().__init__(url)

    def join(self):
        self.ksql(
            ksql_string="create stream summary_index as \
            select user.after->user_id as user_id, \
            user.after->name as user_name, \
            video.after->video_name as video_name ,\
            photo.after->photo_name as photo_name \
            from user \
                left join video within 7 days on user.after->user_id = video.after->user_id \
                left join photo within 7 days on user.after->user_id = photo.after->user_id;",
            stream_properties={"ksql.streams.auto.offset.reset": "earliest"},
        )

    def rename_rowkey(self):
        pass

    def create_stream_from_topic(self):
        self.create_stream(
            table_name="user",
            columns_type=[
                "after STRUCT<user_id int, name string>"
            ],
            topic="legacy.lumenghe.user",
        )

        self.create_stream(
            table_name="video",
            columns_type=[
                "after STRUCT<video_id int, user_id int, video_name string>"
            ],
            topic="legacy.lumenghe.video",
        )

        self.create_stream(
            table_name="photo",
            columns_type=[
                "after STRUCT<photo_id int, user_id int, photo_name string>"
            ],
            topic="legacy.lumenghe.photo",
        )
