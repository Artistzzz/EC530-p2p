from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    IP_address = Column(String(100))

    @staticmethod
    def add_user(username, IP_address, engine):
        new_user = User(username=username, IP_address=IP_address)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.add(new_user)
        session.commit()
        session.close()

    @staticmethod
    def get_users(engine):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        users = session.query(User).all()
        session.close()
        return users

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, Sequence('message_id_seq'), primary_key=True)
    sender = Column(String(50))
    recipient = Column(String(50))
    message = Column(String(500))
    time = Column(DateTime, default=func.now())

    @staticmethod
    def add_message(sender, recipient, message, engine):
        new_message = Message(sender=sender, recipient=recipient, message=message)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        session.add(new_message)
        session.commit()
        session.close()

    @staticmethod
    def get_messages(engine, recipient):
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        messages = session.query(Message).filter_by(recipient=recipient).all()
        session.close()
        return messages

def init_db(uri='sqlite:///chat.db'):
    engine = create_engine(uri, echo=False)
    Base.metadata.create_all(engine)
    return engine