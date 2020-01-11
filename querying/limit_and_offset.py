from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, aliased

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
        User(name="Fred", fullname="Fred Flintstone", nickname="freddy")
    ]
    )

    session.commit()

    # Using limit
    for user in session.query(User).order_by(User.name).limit(2):
        print(user)

    # Using offset
    for user in session.query(User).order_by(User.name).offset(2).limit(2):
        print(user)

    # Using offset with slices
    for user in session.query(User).order_by(User.name)[2:4]:
        print(user)

    session.close()
