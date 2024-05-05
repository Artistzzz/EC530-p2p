from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from cryptography.fernet import Fernet

Base = declarative_base()
key = Fernet.generate_key()
cipher_suite = Fernet(key)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    IP_address = Column(String(100))

    @staticmethod
    def add_user(username, IP_address, engine):
        encrypted_username = cipher_suite.encrypt(username.encode()).decode()
        encrypted_ip = cipher_suite.encrypt(IP_address.encode()).decode()
        new_user = User(username=encrypted_username, IP_address=encrypted_ip)
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
        return [{"username": cipher_suite.decrypt(user.username.encode()).decode(), 
                 "IP_address": cipher_suite.decrypt(user.IP_address.encode()).decode()} for user in users]

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

def init_db(uri='sqlite:///chat.db'):
    engine = create_engine(uri, echo=False)
    Base.metadata.create_all(engine)
    return engine