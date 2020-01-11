from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, and_, or_
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
    engine = create_engine("sqlite:///:memory:", echo=False)
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

    print("Using like: ")
    for user in session.query(User).filter(User.fullname.like("Ed%")):
        print(user)

    print("Using ilike: ")
    for user in session.query(User).filter(User.fullname.like("%ed")):
        print(user)

    print("Using and_")
    for user in session.query(User).filter(and_(User.name == "Ed", User.nickname == "Eddie")):
        print(user)

    print("Using or_")
    for user in session.query(User).filter(or_(User.name == "Mary", User.name == "Wendy")):
        print(user)

    # Using in
    print("Using in_")
    for user in session.query(User).filter(User.name.in_(["Mary", "Wendy"])):
        print(user)

    session.close()
