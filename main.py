from fastapi import FastAPI
from data_schemas import ProductRequest, ProductResponse
from models import Base, Product, User

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from datetime import datetime

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

def add_user():
    user = User(
        full_name = "Levy Leshan",
        email = "leshan@gmail.com",
        password = "hgyt123",
        created_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()

add_user()

@app.post("/products", response_model = ProductResponse)
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
    
@app.get("/products", response_model=list[ProductResponse])
def get_products():
    query = select(Product)
    products = session.scalars(query)
    
    return products
    
    