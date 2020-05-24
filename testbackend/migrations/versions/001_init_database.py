from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
import migrate
from sqlalchemy.dialects.postgresql import JSON, UUID
from datetime import datetime
# import uuid

metadata = MetaData()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", UUID, index=True, nullable=False, unique=True),
    Column("username", String(16), nullable=False),
    Column("password_hash", String(128), nullable=False),
    Column("created_on", DateTime(), default=datetime.now()),
    Column("updated_on", DateTime(), default=datetime.now(), onupdate=datetime.now())
)

posts = Table(
    "posts", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(16)),
    Column("post_id", UUID, index=True, unique=True),
    Column("preview", String(256), nullable=False),
    Column("content", Text, nullable=False),
    Column("created_on", DateTime(), default=datetime.now()),
    Column("updated_on", DateTime(), default=datetime.now(), onupdate=datetime.now()),
    Column("public", Boolean, default=True),
    Column("author", String(16), nullable=False),
    Column("user_id", UUID, nullable=False)
)

tag = Table(
    'tag', metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("name", String(8), unique=True),
    Column("tag_id", UUID, nullable=False),
    Column("user_id", UUID, index=True),
    Column("posts",Text)
)

posts_comments = Table(
    "posts_comments", metadata,
    Column("id",Integer, primary_key=True, autoincrement=True),
    Column("post_comment_id",UUID, nullable=False),
    Column("post_id",UUID, index=True),
    Column("username",String(8), nullable=False),
    Column("email",String(32), nullable=False),
    Column("comments",JSON, nullable=False),
    Column("created_on",DateTime(), default=datetime.now())
)

def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    metadata.bind = migrate_engine
    users.create()
    posts.create()
    tag.create()
    posts_comments.create()
    pass


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    metadata.bind = migrate_engine
    users.drop()
    posts.drop()
    tag.drop()
    posts_comments.drop()
    pass
