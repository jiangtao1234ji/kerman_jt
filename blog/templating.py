# @Author  :_kerman jt
# @Time    : 19-10-29 下午5:20


from datetime import datetime
from urllib.parse import urljoin
from flask import Flask, request, json
from jinja2 import Markup
from slugify import slugify

from .md import markdown
from .models import Category, Integration, Page


def date(s: datetime, format: str = '%Y-%m-%d') -> str:
    return s.strftime(format)


def get_current_time() -> dict:
    return {'current_time': datetime.now()}


def text_part(text: str, find_str: str, extra: int = 100) -> str:
    pos = text.lower().find(find_str.lower())
    res = text[max(0, pos - extra):max(extra, pos + extra)]
    if pos - extra > 0:
        res = '...' + res
    if pos + extra < len(text):
        res += '...'
    return res


def blog_objects() -> dict:
    url = request.url
    title = request.url_rule.endpoint if request.url_rule else ''
    categories = Category.query.filter(Category.text != 'About').all()
    pages = Page.query.order_by(Page.id.asc()).all()
    rv = {'url': url, 'title': title.title()}
    return {'page': rv, 'urljoin': urljoin, 'categories': categories, 'pages': pages}


def make_slugify(s) -> str:
    return slugify(s)


def render_markdown(s) -> str:
    return Markup(markdown(s))


def get_integrations() -> dict:
    return {
        'integration': {
            item.name: {**{'enabled': item.enabled}, **json.loads(item.settings)}
            for item in Integration.query}
    }


def init_app(app: Flask) -> None:
   app.add_template_filter(date)
   app.add_template_filter(make_slugify, 'slugify')
   app.add_template_filter(render_markdown, 'render')
   app.add_template_filter(text_part, 'textpart')
   app.context_processor(get_current_time)
   app.context_processor(blog_objects)
   app.context_processor(get_integrations)