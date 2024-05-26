from sqlalchemy import Text, Integer, Float, String, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(75), nullable=False)
    price = Column(Float)
    description = Column(Text)
    upc = Column(String(18), nullable=False, unique=True)
    availability = Column(Integer)
