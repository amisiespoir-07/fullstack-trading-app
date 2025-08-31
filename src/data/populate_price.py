import config
import alpaca_trade_api as tradeapi
from database import engine, SessionLocal
import models 

# CAll the database 
db = SessionLocal()
try: 
    ids = []
    symbols = []
    names = []
     # Initialize lists for different asset types
    stock_symbols = []
    crypto_symbols = []
    all_rows = db.query(models.Stock).all()
    for row in all_rows:
        #print(row.symbol)
        ids.append(row.id)
        if '/' in row.symbol or ' ' in row.symbol:
            crypto_symbols.append(row.symbol)
        else:
            stock_symbols.append(row.symbol)
        names.append(row.name)
        
    print(symbols)
    print("Database extracted successfully with stock data.")
    print(names)

except Exception as e:
    db.rollback()
    print(f"An error occurred: {e}")
finally:
    db.close()

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)
try: 
    
    chunk_size = 200
    for i in range(0, len(symbols), chunk_size):
        symbol_chunk = stock_symbols[i:i+chunk_size]

        barsets = api.get_bars(symbol_chunk, start="2022-07-01T16:15:00Z", timeframe="1D", limit=2)

        #for symbol, bars in barsets.items():
           # print(f"processing symbol: {symbol}")
         # loop through each current symbol in dictionar
        for bar in barsets:
            stock = db.query(models.Stock).filter_by(symbol=bar.S).first()
            if stock: 
                new_price = models.StockPrice(stock_id=stock.id,
                                           date=bar.t.date(), open=bar.o,
                                           high=bar.h, low=bar.l, 
                                           close=bar.c, volume=bar.v)
                db.add(new_price)
        
        db.commit() 
    print("Database populated successfully with stock data.")

except Exception as e:
    db.rollback()
    print(f"An error occurred: {e}")
finally:
    db.close()

    

"""
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)

barsets = api.get_bars(["AAPL","MSFT"], start="2022-07-01T16:15:00Z", timeframe="1D", limit=50)
for symbol in barsets:
    print(f"processing symbol: {symbol}")

    # loop through each current symbol in dictionar
    for bar in barsets:
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)
#print(barsets)


#barsets = api.get_bars(["AAPL","MSFT"], start="2022-07-01T16:15:00Z", timeframe="1D", limit=50)
for symbol in barsets:
    print(f"processing symbol: {symbol}")

    # loop through each current symbol in dictionar
    for bar in barsets:
        print(bar.t, bar.o, bar.h, bar.l, bar.c, bar.v)
#print(barsets)

models.Base.metadata.create_all(bind=engine)

# Populate the database table
db = SessionLocal()

try:
    for asset in assets:
        # Check if asset is tradable to avoid inserting non-tradable assets
        if asset.status =='active' and asset.tradable:
            # Create a new Stock object and add it to the session
            new_price = models.Stock(id=asset.id, symbol=asset.symbol, company=asset.name)
            db.add(new_price)
    db.commit()
    print("Database populated successfully with stock data.")

except Exception as e:
    db.rollback()
    print(f"An error occurred: {e}")
finally:
    db.close()
"""
