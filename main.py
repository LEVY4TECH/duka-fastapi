from fastapi import FastAPI
from data_schemas import ProductRequest, ProductResponse
from models import Base, Product

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = FastAPI()

# Create a connection to the database using SQLAlchemy engine
engine = create_engine("sqlite:///./duka_fastapi.db", echo=True)

# Create the Tables into the database using SQLAlchemy
Base.metadata.create_all(engine)

# Create a session to do sql transactions
session = Session(engine)

@app.get("/")
def home():
    return {"Duka FastAPI version" : "1.0"}

@app.post("/products")
def create_product(prod : ProductRequest):
    # store in the database
    dbprod = Product(
        product_name = prod.product_name,
        buying_price = prod.buying_price,
        selling_price = prod.selling_price,
        stock_quantity = prod.stock_quantity
    )
    session.add(dbprod)
    session.commit()
    session.refresh(dbprod)
    return dbprod
    
    