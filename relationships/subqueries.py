from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, func, ForeignKey, exists
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(email_address='{self.email_address}')>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    addresses = relationship("Address", order_by=Address.id, back_populates="user")

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
    ])

    jack = User(name="Jack", fullname="Jack Bauer", nickname="Jax")
    jack.addresses = [
        Address(email_address="jack@hotmail.com"), Address(email_address="jack@gmail.com")
    ]

    session.add(jack)
    session.commit()

    subquery = session.query(
        Address.user_id, func.count("*").label("address_count")
    ).group_by(Address.user_id).subquery()

    print("All users and their email counts:")
    for user, count in (
            session.query(User, subquery.c.address_count)
            .outerjoin(subquery, User.id == subquery.c.user_id)
            .order_by(User.id)):
        print(user.fullname, count)

    exists_query = exists().where(Address.user_id == User.id)

    for user in session.query(User).filter(exists_query):
        print(user)
