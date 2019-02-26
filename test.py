from alchemy import db_session
import alchemy as db
from sqlalchemy import and_
import datetime

# news = db.db_session.query(db.News).filter(db.News.id == 28).first()
# field = db.db_session.query(db.Field).filter(db.Field.id == 1).first()
# news.fields.append(field)
# print(news.fields)
# db.db_session.commit()

start_time = datetime.datetime.today() - datetime.timedelta(days=3)
field = db.db_session.query(db.Field).filter(db.Field.id == 1).first()
print(field)
news_set = db.db_session.query(db.News).filter(and_(db.News.site_id == 10, db.News.datetime >= start_time, db.News.fields.contains(field))).first()

print(news_set.id)
