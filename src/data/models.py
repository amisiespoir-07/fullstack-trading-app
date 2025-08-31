from sqlalchemy import Column, String, ForeignKey, Float, Date, Integer
from sqlalchemy.orm import relationship
from database import Base

class Stock(Base):
    __tablename__ = "stock"

    id = Column(String, primary_key=True, index=True)
    symbol = Column(String, index=True)
    name = Column(String, index=True)

    #relationship
    prices = relationship("StockPrice", back_populates="stock")

class StockPrice(Base):
    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True)
    stock_id = Column(String, ForeignKey('stock.id'))
    date  = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)

    stock = relationship("Stock", back_populates="prices")