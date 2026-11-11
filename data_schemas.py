from pydantic import BaseModel, Field
from datetime import datetime, timezone

class ProductRequest(BaseModel):
    product_name : str
    buying_price : float
    selling_price : float
    stock_quantity : int
    
class ProductResponse(BaseModel):
    id : int
    product_name : str
    buying_price : float
    selling_price : float
    stock_quantity : int
    
class SaleRequest(BaseModel):
    product_id : int
    amount : float
    
class SaleResponse(BaseModel):
    id : int
    product_id : int
    amount : float
    sale_date : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class SaleDetailsRequest(BaseModel):
    sale_id : int
    product_id : int
    quantity : int
    selling_price : float
    
class SaleDetailsResponse(BaseModel):
    id : int
    sale_id : int
    product_id : int
    quantity : int
    selling_price : float
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
class PaymentRequest(BaseModel):
    sales_id : int
    amount : float
    transaction_code : str
    mrid : int
    crid : int
    payment_status : str
    phone_number : str
    
class PaymentResponse(BaseModel):
    id : int
    sales_id : int
    amount : float
    transaction_code : str
    mrid : int
    crid : int
    payment_status : str
    payment_date : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    
    
    
    
    
