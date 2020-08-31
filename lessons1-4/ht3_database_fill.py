from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ht3_models import Base, Post, Writer, Tag, Hub
from ht3_parser import HabrParser

if __name__ == '__main__':

    engine = create_engine('sqlite:///hubr_blog.db')
    Base.metadata.create_all(engine)

    session_db = sessionmaker(bind=engine)
    session = session_db()

    parser = HabrParser()
    parser.parse()

    for data in parser.posts_data:
        post = Post(title=data['title'], url=data['url'])
        for tag_set in data['tags']:
            tag = Tag(name=tag_set[0], url=tag_set[1])
            post.tag.append(tag)
        for hub_set in data['hubs']:
            hub = Hub(name=hub_set[0], url=hub_set[1])
            post.hub.append(hub)
        post.writer = Writer(name=data['author'], url=data['author_url'])


        session.query(Writer).filter_by(url = post.writer.url).delete()
        for tag in post.tag:
            session.query(Tag).filter_by(url = tag.url).delete()
        for hub in post.hub:
            session.query(Hub).filter_by(url = hub.url).delete()
        session.query(Post).filter_by(url = post.url).delete()
        session.add(post)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
    session.close()



