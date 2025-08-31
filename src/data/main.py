from database import engine, SessionLocal
import models 
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
# Dependency to get DB Session


@app.get("/")
def index(request: Request):
    db = SessionLocal()
    try: 
        all_rows = db.query(models.Stock).all()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
    all_rows = db.query(models.Stock).order_by(models.Stock.symbol).all()

    return templates.TemplateResponse("index.html", {"request": request, "stocks":all_rows})


@app.get("/stock/{symbol}")
def stock_detail(request: Request, symbol):
    db = SessionLocal()
    try: 
        all_rows = db.query(models.Stock).all()
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()
    all_rows = db.query(models.Stock).filter_by(models.Stock.symbol).all()

    return templates.TemplateResponse("stock.html", {"request": request, "stocks":all_rows})

    return symbol