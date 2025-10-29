from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    """Represent a product."""
    product_id: str
    product_type: str
    product_name: str
    opened_date: str
    status: str

    def __init__(self):
        self.product_id = ""
        self.product_type = ""
        self.product_name = ""
        self.opened_date = ""
        self.status = ""

    def __str__(self):
        return f"Product name: {self.product_name}, type: {self.product_type} opened: {self.opened_date}, status: {self.status}"

@dataclass
class Transaction:
    """Represent a transaction."""
    transaction_id: str
    product_id: str
    date: str
    amount: str
    currency: str
    description: str
    transaction_type : str

    def __init__(self):
        self.transaction_id = ""
        self.product_id = ""
        self.date = ""
        self.amount = ""
        self.currency = ""
        self.description = ""
        self.transaction_type = ""


@dataclass
class Customer:
    """Represent a customer."""

    customer_id: str
    name: str
    birth_date: str
    address: str
    phone_number: str
    email: str
    segment_code: str
    # products: List[Product]

    def __init__(self):
        self.customer_id = ""
        self.name = ""
        self.birth_date = ""
        self.address = ""
        self.phone_number = ""
        self.segment_code = ""

    def __str__(self):
        return f"Customer ID: {self.customer_id}, Name: {self.name}"
