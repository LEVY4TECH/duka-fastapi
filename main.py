from fastapi import FastAPI
from data_schemas import ProductRequest, ProductResponse, SaleRequest, SaleResponse, SaleDetailsRequest, SaleDetailsResponse, PaymentRequest, PaymentResponse
from models import Base, Product, User, Sale, SaleDetail, Payment

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

@app.post("/sales", response_model=SaleResponse)
def create_sale(sale : SaleRequest):
    dbprod = Sale(
        product_id = sale.product_id,
        amount = sale.amount
    )
    session.add(dbprod)
    session.commit()
    session.refresh(dbprod)
    return dbprod

@app.get("/sales", response_model=list[SaleResponse])
def get_sales():
    query = select(Sale)
    sales = session.scalars(query)
    
    return sales

@app.post("/sale_details", response_model=SaleDetailsResponse)
def create_sale_detail(sale_detail : SaleDetailsRequest):
    dbprod = SaleDetail(
        sale_id = sale_detail.sale_id,
        product_id = sale_detail.product_id,
        quantity = sale_detail.quantity,
        selling_price = sale_detail.selling_price
    )
    session.add(dbprod)
    session.commit()
    session.refresh(dbprod)
    
    return dbprod

@app.get("/sale_details", response_model=list[SaleDetailsResponse])
def get_sale_details():
    query = select(SaleDetail)
    sale_details = session.scalars(query)
    
    return sale_details

@app.post("/payments", response_model=PaymentResponse)
def create_payment(pay : PaymentRequest):
    dbprod = Payment(
        sales_id = pay.sales_id,
        amount = pay.amount,
        transaction_code = pay.transaction_code,
        mrid = pay.mrid,
        crid = pay.crid,
        payment_status = pay.payment_status,
        phone_number = pay.phone_number
    )
    session.add(dbprod)
    session.commit()
    session.refresh(dbprod)
    
    return dbprod

@app.get("/payments", response_model=list[PaymentResponse])
def get_payments():
    query = select(Payment)
    payments = session.scalars(query)
    
    return payments
    
    