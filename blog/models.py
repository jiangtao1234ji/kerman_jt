# @Author  :_kerman jt
# @Time    : 19-10-14 下午12:12
import hashlib
from datetime import datetime
from random import choice, sample, randint
from typing import Union, Optional, Type
import sqlalchemy as sc
import sqlalchemy.orm
from slugify import slugify
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from flask import Flask, current_app, json, url_for
from flask_sqlalchemy import SQLAlchemy, event
from flask_whooshee import Whooshee
from flask_login import UserMixin
from flask_migrate import Migrate

from .md import markdown

db: SQLAlchemy = SQLAlchemy()
whooshee: Whooshee = Whooshee()

tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('blog_id', db.Integer, db.ForeignKey('blog.id'))
)

DEFAULT_SETTINGS = {
    "locale": "en",
    "name": "Kerman",
    "cover_url": "/static/images/cover.jpg",
    "avatar": "/static/images/violet.jpeg",
    "description": "A simple blog powered by Flask",
}


def auto_delete_orphans(cls: db.Model, attr: str) -> None:
    @event.listens_for(sc.orm.Session, "after_flush")
    def delete_orphan_listener(session, ctx):
        session.query(cls).filter(~getattr(cls, attr).any()).delete(
            synchronize_session=False
        )


@whooshee.register_model('title', 'description', 'content')
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    last_update = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    image = db.Column(db.String(400))
    lang = db.Column(db.String(20))
    content = db.Column(db.Text())
    html = db.Column(db.Text())
    toc = db.Column(db.Text())
    url = db.Column(db.String(100))
    comment = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(400))
    author = db.Column(db.String(30))
    tags = db.relationship("Tag", secondary=tags, backref="blogs")
    slug = db.Column(db.String(100))
    is_draft = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    comments = db.relationship("Comment", backref="blog", lazy="dynamic")

    def __init__(self, **kwargs):
        if isinstance(kwargs.get("category"), str):
            kwargs["category"] = Category.get_one_or_new(kwargs["category"])
        tags = kwargs.get("tags")
        if tags and isinstance(tags[0], str):
            kwargs["tags"] = [Tag.get_one_or_new(tag) for tag in tags]
        kwargs.pop("date", None)
        kwargs.pop("last_update", None)
        super().__init__(**kwargs)

    def to_dict(self, ensure_text=False) -> dict:
        return dict(
            id=self.id,
            title=self.title,
            date=self.date,
            last_update=self.last_update,
            image=self.image,
            lang=self.lang,
            content=self.content,
            comment=self.comment,
            description=self.description,
            author=self.author,
            slug=self.slug,
            is_draft=self.is_draft,
            category=self.category if not ensure_text else str(self.category),
            tags=self.tags if not ensure_text else [str(tag) for tag in self.tags]
        )

    def __repr__(self) -> str:
        return f"<Blog: {self.title}>"

    @property
    def previous_one(self) -> "Blog":
        return Blog.query.order_by(Blog.id.desc()).filter(Blog.id < self.id).first()

    @property
    def next_one(self) -> "Blog":
        return Blog.query.order_by(Blog.id.asc()).filter(Blog.id > self.id).first()

    def related_blog(self) -> Union["Blog", None]:
        blogs = Blog.query.join(Blog.tags).filter(
            Tag.id.in_([tag.id for tag in self.tags]),
            Blog.id != self.id,
            ~Blog.is_draft,
        )
        if blogs.count() > 0:
            return choice(blogs.all())
        return None


@event.listens_for(Blog, 'before_insert')
@event.listens_for(Blog, 'before_update')
def render_markdown(
        mapper: Type[sc.orm.Mapper], connection: sc.engine.Connection, target: sc.orm.Mapper
) -> None:
    if not target.slug:
        target.slug = slugify(target.title)
    if not target.date:
        target.date = datetime.utcnow()
    target.html = markdown(target.content)
    target.toc = markdown.renderer.render_toc()
    target.url = "/{}/{}".format(target.date.strftime("%Y/%m-%d"), target.slug)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(100))
    password = db.Column(db.String(200))
    settings = db.Column(db.Text())
    name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean(), default=False)
    picture = db.Column(db.String(512))
    type = db.Column(db.String(16))
    comments = db.relationship("Comment", backref="author", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("username", "email", name="_username_email"),)

    def __init__(self, **kwargs) -> None:
        password = kwargs.pop("password")
        if password:
            password = generate_password_hash(password)
            kwargs["password"] = password
        if not kwargs.get('username') and kwargs.get('name'):
            kwargs['username'] = slugify(kwargs['name'])
        super(User, self).__init__(**kwargs)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    @property
    def display_name(self):
        return self.name or self.username

    @classmethod
    def get_one(cls) -> "User":
        """Get the admin user. The only one will be returned."""
        rv: Union[None, User] = cls.query.filter_by(is_admin=True).first()
        if not rv:
            rv = cls(
                username="admin",
                password=current_app.config["DEFAULT_ADMIN_PASSWORD"],
                email=current_app.config['ADMIN_EMAIL'],
                is_admin=True
            )
            db.session.add(rv)
            db.session.commit()
        return rv

    @property
    def avatar(self) -> str:
        """Get the gravatar image"""
        if self.picture:
            return self.picture
        email_hash = hashlib.md5((self.email or self.username).strip().lower().encode()).hexdigest()
        return f'https://www.gravatar.com/avatar/{email_hash}?d=identicon'

    def generate_token(self, expiration=24 * 60 * 60):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in=expiration)
        return s.dumps({"id": self.id})

    @classmethod
    def verify_auth_token(cls, token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except (BadSignature, SignatureExpired):
            return None
        user = cls.query.get(data["id"])
        return user

    def read_setting(self) -> dict:
        return json.loads(self.settings or json.dumps(DEFAULT_SETTINGS))

    def write_setting(self, data: dict) -> None:
        self.settings = json.dumps(data)
        db.session.commit()

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'avatar': self.avatar,
            'display_name': self.display_name
        }


class GetOrNewMixin:
    @classmethod
    def get_one_or_new(cls, text):
        record = cls.query.filter_by(text=text).first()
        if not record:
            record = cls(text=text)
        return record


class Tag(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(200))

    def __init__(self, **kwargs) -> None:
        with current_app.test_request_context():
            kwargs["url"] = url_for("tag", text=slugify(kwargs["text"]))
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"<Tag: {self.text}>"

    @property
    def number(self) -> int:
        return self.blogs.count()

    def __str__(self) -> str:
        return self.text


class Category(db.Model, GetOrNewMixin):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True)
    blogs = db.relationship("Blog", backref="category", lazy='dynamic')

    def __repr__(self) -> str:
        return f"<Category: {self.text}>"

    def __str__(self) -> str:
        return self.text


class Integration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    settings = db.Column(db.Text())
    enabled = db.Column(db.Boolean())


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    display = db.Column(db.Boolean(), default=False)
    ptype = db.Column(db.String(20), default="markdown")
    content = db.Column(db.Text())
    html = db.Column(db.Text())

    def to_dict(self):
        return {
            k: getattr(self, k)
            for k in ('id', 'slug', 'title', 'display', 'ptype', 'content')
        }


@event.listens_for(Page, 'before_insert')
@event.listens_for(Page, 'before_update')
def get_html(
        mapper: Type[sc.orm.Mapper], connection: sc.engine.Connection, target: sc.orm.Mapper
) -> None:
    if target.ptype == "html":
        target.html = target.content
    else:
        target.html = markdown(target.content)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey("blog.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    floor = db.Column(db.Integer)
    content = db.Column(db.Text())
    html = db.Column(db.Text())
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey("comment.id"))
    replies = db.relationship(
        "Comment", backref=db.backref("parent", remote_side=[id]), lazy="dynamic"
    )

    __table_args__ = (db.UniqueConstraint("blog_id", "floor", name="_blog_floor"),)

    @property
    def children(self):
        queue = self.replies.all()
        rv = []
        while queue:
            node = queue.pop(0)
            rv.append(node)
            queue.extend(node.replies or [])
        return sorted(rv, key=lambda x: x.time)

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author.to_dict(),
            'blog': {'title': self.blog.title, 'url': self.blog.url},
            'floor': self.floor,
            'content': self.content,
            'html': self.html,
            'time': self.time,
        }


@event.listens_for(Comment, "before_insert")
@event.listens_for(Comment, "before_update")
def comment_html(
        mapper: Type[sc.orm.Mapper], connection: sc.engine.Connection, target: sc.orm.Mapper
) -> None:
    target.html = markdown(target.content)


def init_app(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)
    whooshee.init_app(app)
    auto_delete_orphans(Tag, "blogs")
    auto_delete_orphans(Category, "blogs")
