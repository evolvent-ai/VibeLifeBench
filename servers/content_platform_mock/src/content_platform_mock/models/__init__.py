from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    """A community user / creator."""
    user_id: str
    handle: str
    nickname: str
    bio: Optional[str]
    is_official: bool
    follower_count: int
    note_count: int
    joined_at: str


@dataclass
class Note:
    """A UGC note (笔记). Images are TEXT captions only — no binaries.

    ``tags`` and ``image_captions`` are JSON arrays stored as TEXT.
    """
    note_id: str
    author_id: str
    title: str
    body: str
    category: str  # 备考 | 装修 | 健身 | 旅行 | 母婴 | 其他
    tags: List[str]
    image_captions: List[str]
    like_count: int
    collect_count: int
    comment_count: int
    view_count: int
    published_at: str


@dataclass
class Comment:
    """A comment on a note."""
    comment_id: str
    note_id: str
    user_id: str
    body: str
    like_count: int
    created_at: str


@dataclass
class Topic:
    """A topic / hashtag (话题) that notes can be filed under."""
    topic_id: str
    name: str
    category: str
    description: Optional[str]
    note_count: int
    view_count: int


__all__ = ["User", "Note", "Comment", "Topic"]
