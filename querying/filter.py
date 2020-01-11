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
        User(name="Wendy", fullname="Wendy Jones", nickname="windy"),
        User(name='Mary', fullname="Mary Contrary", nickname="nmary"),
        User(name="Fred", fullname="Fred Flintstone", nickname="freddy"),
        User(name="Ed", fullname="Ed Doe", nickname="Eddie")
    ]
    )

    session.commit()

    # Filter by something
    for user in session.query(User).filter(User.name == "Ed"):
        print(user)

    # Chaining filters
    for user in session.query(User).filter(User.name == "Ed").filter(User.nickname == "Eddie"):
        print(user)

    session.close()
