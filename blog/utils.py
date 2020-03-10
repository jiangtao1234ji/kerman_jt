# @Author  :_kerman jt
# @Time    : 19-10-14 下午12:06

from sqlalchemy import func
from typing import Iterable
from .models import Tag, Blog


def get_tag_cloud() -> Iterable[Tag]:
    """Get tags order by its heat to generate a tag cloud"""
    tags = Tag.query.join(Tag.blogs).with_entities(Tag, func.count(Blog.id)) \
                                    .group_by(Tag.id) \
                                    .order_by(func.count(Blog.id).desc())
    return tags.all()
