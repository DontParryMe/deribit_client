from sqlalchemy import BigInteger, Column, Integer, Numeric, String

from ..db.base import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ticker = Column(String(16), index=True, nullable=False)
    price = Column(Numeric(18, 2), nullable=False)
    ts = Column(BigInteger, index=True, nullable=False)
