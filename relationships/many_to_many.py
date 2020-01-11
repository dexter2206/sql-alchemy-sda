from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, func, ForeignKey, Text, Table
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


post_keywords = Table(
    "post_keywords",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("keyword_id", ForeignKey("keywords.id"), primary_key=True),
)


class BlogPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    body = Column(Text)
    keywords = relationship("Keyword", secondary=post_keywords, back_populates="posts")

    author = relationship("User", back_populates="posts")


class Keyword(Base):
    __tablename__ = "keywords"

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False)
    unique = True
    posts = relationship(BlogPost, secondary=post_keywords, back_populates="keywords")


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses", cascade="all")

    def __repr__(self):
        return f"<Address(email_address='{self.email_address}')>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    addresses = relationship("Address", order_by=Address.id, back_populates="user")
    posts = relationship(BlogPost, order_by=BlogPost.author_id, back_populates="author")

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')"


if __name__ == "__main__":
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()
    session.add_all([
        User(name="Ed", fullname="Ed Jones", nickname="Scissorhands"),
        User(name="Wendy", fullname="Wendy Williams", nickname="windy"),
        User(name='Mary', fullname="Mary Contrary", nickname="nmary"),
        User(name="fred", fullname="Fred Flintstone", nickname="freddy")
    ]
    )

    session.commit()

    print("Are there any new records?")
    print(session.new)

    session.close()

    wendy = session.query(User).filter_by(name="Wendy").one()

    post = BlogPost(body="Some content", author=wendy)
    session.add(post)

    post.keywords.append(Keyword(keyword="wendy"))
    post.keywords.append(Keyword(keyword="firstpost"))

    mary = session.query(User).filter_by(name="Mary").one()

    post = BlogPost(body="Hello World!", author=mary)
    post.keywords.append(Keyword(keyword="firstpost"))
    session.add(post)

    post = BlogPost(body="Second post!", author=mary)
    session.add(post)

    session.commit()

    print("All posts with keyword 'firstpost':")
    for post, user in session.query(BlogPost, User).join(User).filter(
            BlogPost.keywords.any(Keyword.keyword == "firstpost")
    ):
        print(post, user)

    session.close()