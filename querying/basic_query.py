from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

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

    # Query all users
    print("Basic query:")
    for user in session.query(User):
        print(user)

    # Query only specific fields
    for row in session.query(User.fullname, User.nickname):
        print(row.fullname, row.nickname)

    # Query only specific fields - alternative version
    for fullname, nickname in session.query(User.fullname, User.nickname):
        print(fullname, nickname)

    session.close()
