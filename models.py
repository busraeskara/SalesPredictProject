from pydantic import BaseModel

#Pydantic olarak veri doğrulama ve serileştirme işlemleri yapılacak.

class OrderPydantic(BaseModel):
    order_id: int
    customer_id: str
    employee_id: int
    order_date: str
    required_date: str
    shipped_date: str
    ship_via: int
    freight: float
    ship_name: str
    ship_address: str
    ship_city: str
    ship_region: str
    ship_postal_code: str
    ship_country: str

class OrderDetailPydantic(BaseModel):
    order_id: int
    product_id: int
    unit_price: float
    quantity: int
    discount: float

class ProductPydantic(BaseModel):
    product_id: int
    product_name: str
    supplier_id: int
    category_id: int
    quantity_per_unit: str
    unit_price: float
    units_in_stock: int
    units_on_order: int
    reorder_level: int
    discontinued: bool

class CustomerPydantic(BaseModel):
    customer_id: str
    company_name: str
    contact_name: str
    contact_title: str
    address: str
    city: str
    region: str
    postal_code: str
    country: str
    phone: str
    fax: str

class CategoryPydantic(BaseModel):
    category_id: int
    category_name: str
    description: str


class PredictSalesRequestPydantic(BaseModel):
    order_date: str  # ISO formatta string (örn: "2025-04-06")
    product_id: int
    order_month: int
    order_dayofweek: int
    order_is_weekend: int  # 0 ya da 1

class PredictSalesResponsePydantic(BaseModel):
    predicted_sales: float

class TrainModelResponsePydantic(BaseModel):
    message: str

class MonthlySalesItemPydantic(BaseModel):
    month: str
    total_sales: int
    total_revenue: float

class ProductSalesItemPydantic(BaseModel):
    product_id: int
    product_name: str
    total_sales: int
    total_revenue: float

class PredictionInputPydantic(BaseModel):
    product_id: int
    order_date: str