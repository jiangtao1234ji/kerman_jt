# @Author  :_kerman jt
# @Time    : 20-2-26 下午3:33

from datetime import datetime, timezone
import os
import sqlite3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

path = os.path.dirname(__file__)

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
update_sql = 'update blog set date = ?  where id = 1'
c.execute(update_sql, datetime.utcfromtimestamp(1580906944))
conn.commit()
utc_time = datetime.utcnow()
print(datetime.utcfromtimestamp(1580906944))
print(datetime.now(timezone.utc))
print(datetime.utcnow().timestamp())
