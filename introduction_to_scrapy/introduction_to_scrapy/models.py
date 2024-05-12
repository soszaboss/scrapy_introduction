from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, Integer, Float, String

class Base(DeclarativeBase):
    pass

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(75), nullable=False)
    price: Mapped[float] = mapped_column()
    description = mapped_column(Text)
    upc: Mapped[str] = mapped_column(String(18), nullable=False, unique=True)
    avaibility: Mapped[int] = mapped_column()
