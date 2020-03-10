# @Author  :_kerman jt
# @Time    : 19-10-29 下午8:25
import click
from flask.cli import with_appcontext
import faker
from .models import Blog, db
import random

fake = faker.Faker()


def generate_on_fake_blog():
    return {
        'title': fake.sentence(nb_words=6, variable_nb_words=True),
        'description': fake.sentence(nb_words=6, variable_nb_words=True),
        'image': fake.image_url(width=800, height=400),
        'slug': fake.slug(),
        'content': '## Hello World\n我是测试数据我是测试数据\n\n![](https://wpimg.wallstcn.com/4c69009c-0fd4-4153-b112-6cb53d1cf943)\n',
        'author': fake.name(),
        'date': fake.date_time(),
        'is_draft': random.choice([False, True]),
        'lang': random.choice(['en', 'zh_Hans_CN']),
        'category': random.choice(['programming', 'essay']),
        'tags': random.sample(['test', 'python', 'algorithm', 'reading'], random.randint(1, 3))
    }


@click.command()
@with_appcontext
def reindex():
    """Reindex the searchable models."""
    from .models import whooshee

    whooshee.reindex()
    click.echo("Index created for models.")


@click.command()
@with_appcontext
def fake_db():
    """Insert fake data into database."""
    for _ in range(100):
        blog = Blog(**generate_on_fake_blog())
        db.session.add(blog)
    db.session.commit()
    click.echo("Add 100 blogs")


def init_app(app):
    app.cli.add_command(reindex)
    app.cli.add_command(fake_db)
