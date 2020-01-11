from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, func, ForeignKey
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

    jack = User(name="Jack", fullname="Jack Bauer", nickname="Jax")

    print("Jack addresses after init:", jack.addresses)

    jack.addresses = [
        Address(email_address="jack@hotmail.com"), Address(email_address="jack@gmail.com")
    ]

    session.add(jack)
    session.commit()

    print("Using filter:")
    for user, address in session.query(User, Address).filter(User.id == Address.user_id):
        print(user, address)

    print("Using query.join:")
    for user in session.query(User).join(Address).all():
        print(user, user.addresses)