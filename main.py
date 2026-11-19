from fastapi import FastAPI, HTTPException, status, Depends
from data_schemas import ProductRequest, ProductResponse, SaleRequest, SaleResponse, SaleDetailsRequest, SaleDetailsResponse, PaymentRequest, PaymentResponse, LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from models import Base, Product, User, Sale, SaleDetail, Payment
from myjwt import verify_password, create_access_token, get_password_hash, get_current_user

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


# authentication Routes
@app.post("/login",response_model=LoginResponse)
def login(user : LoginRequest):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
     
    query = select(User).where(User.email == user.email)
    db_user = session.scalars(query).first()
    
    if not db_user:
        raise credentials_exception 
           
    if not verify_password(user.password, db_user.password):
        raise credentials_exception
    
    db_user.token = create_access_token({"sub" : db_user.email})
    
    return db_user

@app.post("/register", response_model=RegisterResponse)
def register(user : RegisterRequest):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    query = select(User).where(User.email == user.email)
    db_user = session.scalars(query).first()
    
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
        
    db_user = User(full_name = user.full_name,
                email = user.email,
                password = get_password_hash(user.password)
            )
    
    session.add(db_user)
    session.commit()
    
    db_user.token = create_access_token({"sub" : db_user.email})
    
    return db_user
        
    

# Products Route

@app.post("/products", response_model = ProductResponse)
def create_product(prod : ProductRequest, current_user : str = Depends(get_current_user)):
    print("USER IS--------------------", current_user)
    
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
def get_products(current_user : str = Depends(get_current_user)):
    print("USER IS--------------------", current_user)
    query = select(Product)
    products = session.scalars(query)
    
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_single_product(product_id):
    query = select(Product).where(Product.id == product_id)
    product = session.scalars(query).first()
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
        
    return product
    

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id : int, prod : ProductRequest):
    query = select(Product).where(Product.id == product_id)
    product = session.scalars(query).first()
    
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
        
    product.product_name = prod.product_name
    product.buying_price = prod.buying_price
    product.selling_price = prod.selling_price
    product.stock_quantity = prod.stock_quantity
    
    
    
    session.commit()
    
    
    return product

# End product routes

# sales route

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

@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_single_sale(sale_id):
    query = select(Sale).where(Sale.id == sale_id)
    sale = session.scalars(query).first()
    
    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )
        
        
    return sale

@app.put("/sales/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id : int, sale : SaleRequest):
    query = select(Sale).where(Sale.id == sale_id)
    sale = session.scalars(query).first()
    
    if sale is None:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )
        
    sale.product_id = sale.product_id
    sale.amount = sale.amount
    
    session.commit()
    return sale
    
    

# End of sales route

# Sale Details route

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

@app.get("/sale_details/{saleDetail_id}", response_model=SaleDetailsResponse)
def get_single_sale_detail(saleDetail_id):
    query = select(SaleDetail).where(SaleDetail.id == saleDetail_id)
    sale_detail = session.scalars(query).first()
    
    if sale_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Sale detail not found"
        )
        
    return sale_detail

@app.put("/sale_details/{saleDetail_id}", response_model=SaleDetailsResponse)
def update_sale_detail(saleDetail_id : int, detail : SaleDetailsRequest):
    query = select(SaleDetail).where(SaleDetail.id == saleDetail_id)
    sale_detail = session.scalars(query).first()
    
    if sale_detail is None:
        raise HTTPException(
            status_code=404,
            detail="Sale detail not found"
        )
        
    detail.sale_id = sale_detail.sale_id
    detail.product_id = sale_detail.product_id
    detail.quantity = sale_detail.quantity
    detail.selling_price = sale_detail.selling_price
    
    session.commit()
    return sale_detail
    
    

# End of sale details route

# Payments Route

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

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_single_payment(payment_id):
    query = select(Payment).where(Payment.id == payment_id)
    payment = session.scalars(query).first()
    
    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="payment not found"
        )
        
    return payment

@app.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id : int, pay : PaymentRequest):
    query = select(Payment).where(Payment.id == payment_id)
    payment = session.scalars(query).first()
    
    if payment is None:
        raise HTTPException(
            status_code=404,
            detail="payment not found"
        )
        
    pay.sales_id = pay.sales_id
    pay.amount = pay.amount
    pay.transaction_code = pay.transaction_code
    pay.mrid = pay.mrid
    pay.crid = pay.crid
    pay.payment_status = pay.payment_status
    pay.phone_number = pay.phone_number
    
    session.commit()
    return payment
    
    

# End of payments route
    
    