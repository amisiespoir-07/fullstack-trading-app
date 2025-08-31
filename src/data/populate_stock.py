import alpaca_trade_api as tradeapi
from database import engine, SessionLocal
#from pydantic import BaseModel
import config
import models
# aplaca api client rest(api_ket, api_secrete)

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)
assets = api.list_assets()

# Create the table in the database
models.Base.metadata.create_all(bind=engine)

# Populate the database table
db = SessionLocal()

try:
    for asset in assets:
        # Check if asset is tradable to avoid inserting non-tradable assets
        if asset.status =='active' and asset.tradable:
            # Create a new Stock object and add it to the session
            new_stock = models.Stock(id=asset.id, symbol=asset.symbol, name=asset.name)
            db.add(new_stock)
    db.commit()
    print("Database populated successfully with stock data.")

except Exception as e:
    db.rollback()
    print(f"An error occurred: {e}")
finally:
    db.close()
