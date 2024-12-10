import atexit
import os
import datetime


from sqlalchemy import create_engine, DateTime, Integer, String, func, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped, relationship

POSTGRES_DB = os.getenv("POSTGRES_DB", "netology_flask_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "qwerty12")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
          f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(PG_DSN)

atexit.register(engine.dispose)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):

    @property
    def id_dict(self):
        return {'id': self.id}


class User(Base):
    __tablename__ = "app_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(72), nullable=False)
    email: Mapped[str] = mapped_column(String(72), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email,
            'registration_time': self.registration_time.isoformat()
        }


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    heading: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    date_creation: Mapped[datetime.date] = mapped_column(Date, server_default=func.current_date())
    creator: Mapped[int] = mapped_column(Integer, ForeignKey('app_user.id'), nullable=False)

    user = relationship(User, backref='advertisement')

    @property
    def dict(self):
        return {
            'id': self.id,
            'heading': self.heading,
            'description': self.description,
            'date_creation': self.date_creation.isoformat(),
            'creator': self.creator
        }



Base.metadata.create_all(bind=engine)











