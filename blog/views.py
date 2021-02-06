# @Author  :_kerman jt
# @Time    : 19-10-14 下午12:05

import io

from urllib.parse import urljoin
from typing import Tuple
from flask import g, current_app, render_template, request, abort, send_file, Flask
from werkzeug.wrappers import Response
from werkzeug.contrib.atom import AtomFeed

from .models import User, Blog, Category, Tag, Page, Comment
from .utils import get_tag_cloud
from .md import markdown


def load_site_config() -> None:
    if "site" not in g:
        user = User.get_one()
        g.site = user.read_setting()


def home() -> str:
    paginate = (
        Blog.query.join(Blog.category)
            .filter(Category.text != "About")
            .union(Blog.query.filter(Blog.category_id.is_(None)))
            .filter(~Blog.is_draft)
            .order_by(Blog.date.desc())
            .paginate(per_page=current_app.config["BLOG_PER_PAGE"])
    )
    tag_cloud = get_tag_cloud()
    return render_template("index.html", blogs=paginate.items,
                           tag_cloud=tag_cloud, paginate=paginate)


def blog(year: str, date: str, title: str) -> str:
    blog = None
    for item in Blog.query.all():
        if item.url == request.path:
            blog = item
            break
    if not blog:
        abort(404)
    comments = (
        blog.comments.filter_by(parent=None).order_by(Comment.time.asc()).all()
        if blog.comment
        else []
    )
    comments_count = blog.comments.count()
    return render_template("blog.html", blog=blog, comments=comments, comments_count=comments_count)


def tag(text: str) -> str:
    tag = Tag.query.filter_by(url=request.path).first_or_404()
    blogs = (
        Blog.query.join(Blog.tags)
            .filter(Tag.text == tag.text)
            .filter(~Blog.is_draft)
            .order_by(Blog.date.desc())
    )
    tag_cloud = get_tag_cloud()
    return render_template("index.html", blogs=blogs, tag_cloud=tag_cloud, tag=tag)


def category(cat_id: int) -> str:
    cat = Category.query.get(cat_id)
    blogs = cat.blogs.filter(~Blog.is_draft)
    tag_cloud = get_tag_cloud()

    return render_template("index.html", blogs=blogs, tag_cloud=tag_cloud, cat=cat)


def favicon() -> Response:
    return current_app.send_static_file("images/favicon.ico")


def atom_feed() -> Response:
    feed = AtomFeed(g.site["name"], feed_url=request.url, url=request.url_root)
    blogs = Blog.query.filter_by(is_draft=False).order_by(Blog.date.desc()).limit(15)
    for blog in blogs:
        feed.add(blog.title,
                 str(markdown(blog.content)),
                 content_type='html',
                 author=blog.author or "Unnamed",
                 url=urljoin(request.url_root, blog.url),
                 updated=blog.last_update,
                 published=blog.date)
    return feed.get_response()


def sitemap() -> Response:
    blogs = Blog.query.filter_by(is_draft=False).order_by(Blog.date.desc())
    fp = io.BytesIO(render_template("sitemap.xml", blogs=blogs).encode("utf-8"))
    return send_file(fp, attachment_filename="sitemap.xml")


def page_not_found(error: Exception) -> Tuple[str, int]:
    return render_template("404.html"), 404


def search() -> str:
    search_str = request.args.get("search")
    paginate = (
        Blog.query.filter(~Blog.is_draft)
            .whooshee_search(search_str)
            .order_by(Blog.date.desc())
            .paginate(per_page=10)
    )
    return render_template("search.html", paginate=paginate, highlight=search_str)


def page(slug: str) -> str:
    item = Page.query.filter_by(slug=slug).first_or_404()
    return render_template("page.html", page=item)


def articles() -> str:
    from itertools import groupby

    def grouper(item):
        return item.date.year, item.date.month

    result = groupby(Blog.query.filter_by(is_draft=False).order_by(Blog.date.desc()), grouper)
    return render_template("articles.html", items=result, tag_cloud=get_tag_cloud())


def init_app(app: Flask) -> None:
    app.add_url_rule("/", "home", home)
    app.add_url_rule("/<int:year>/<date>/<title>", "blog", blog)
    app.add_url_rule("/tag/<text>", "tag", tag)
    app.add_url_rule("/cat/<int:cat_id>", "category", category)
    app.add_url_rule("/feed.xml", "feed", atom_feed)
    app.add_url_rule("/sitemap.xml", "sitemap", sitemap)
    app.add_url_rule("/favicon.ico", "favicon", favicon)
    app.add_url_rule("/search", "search", search)
    app.add_url_rule("/articles", "articles", articles)
    app.add_url_rule("/<path:slug>", "page", page)

    app.register_error_handler(404, page_not_found)
    app.before_request(load_site_config)
