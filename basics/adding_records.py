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

    ed_user = User(name="Ed", fullname="Ed Jones", nickname="Scissorhands")

    print("Ed before adding him to the database: ")
    print(ed_user.id, ed_user)

    session = Session()

    session.add(ed_user)

    our_user = session.query(User).first()

    print("User retrieved from db: ")
    print(our_user.id, our_user)

    print("Ed after adding him to the database: ")
    print(ed_user.id, ed_user)

    print(f"Is it the same user? {our_user is ed_user}")
