from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy import Column, Integer, String, create_engine


class OrdersModel(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    employee_id = Column(Integer, index=True)
    order_date = Column(String, index=True)
    required_date = Column(String, index=True)
    shipped_date = Column(String, index=True)
    ship_via = Column(Integer, index=True)
    freight = Column(Integer, index=True)
    ship_name = Column(String, index=True)
    ship_address = Column(String, index=True)
    ship_city = Column(String, index=True)
    ship_region = Column(String, index=True)
    ship_postal_code = Column(String, index=True)
    ship_country = Column(String, index=True)

class OrderDetailsModel(Base):
    __tablename__ = "order_details"
    order_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, index=True)
    unit_price = Column(Integer, index=True)
    quantity = Column(Integer, index=True)
    discount = Column(Integer, index=True)

class ProductsModel(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    supplier_id = Column(Integer, index=True)
    category_id = Column(Integer, index=True)
    quantity_per_unit = Column(Integer, index=True)
    unit_price = Column(Integer, index=True)
    units_in_stock = Column(Integer, index=True)
    units_on_order = Column(Integer, index=True)
    reorder_level = Column(Integer, index=True)
    discontinued = Column(Integer, index=True)

class CustomersModel(Base):
    __tablename__ = "customers"
    customer_id = Column(String, primary_key=True, index=True)
    company_name = Column(String, index=True)
    contact_name = Column(String, index=True)
    contact_title = Column(String, index=True)
    address = Column(String, index=True)
    city = Column(String, index=True)
    region = Column(String, index=True)
    postal_code = Column(String, index=True)
    country = Column(String, index=True)
    phone = Column(String, index=True)
    fax = Column(String, index=True)

class CategoriesModel(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True)
    description = Column(String, index=True)


