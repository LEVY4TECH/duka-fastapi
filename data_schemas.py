from pydantic import BaseModel

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
    
