"""
FraudLens: Transaction Schemas & Input Validation
"""

from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator

class TransactionBase(BaseModel):
    account_id: int = Field(..., description="Target Account ID (e.g. 2001)")
    transaction_type: str = Field("TRANSFER", description="DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT, UPI, NEFT, RTGS")
    amount: float = Field(..., gt=0, description="Amount in INR (> 0)")
    channel: str = Field("MOBILE_APP", description="MOBILE_APP, NET_BANKING, ATM, POS, UPI, BRANCH")
    counterparty_account: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Transaction amount must be strictly greater than 0.00 INR")
        return round(v, 2)

    @model_validator(mode="before")
    @classmethod
    def handle_aliases(cls, data: dict):
        if isinstance(data, dict):
            if "tx_type" in data and "transaction_type" not in data:
                data["transaction_type"] = data["tx_type"]
        return data

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(BaseModel):
    transaction_id: int
    account_id: int
    account_number: Optional[str] = None
    customer_id: Optional[int] = None
    customer_name: Optional[str] = None
    transaction_type: str
    amount: float
    transaction_date: str
    channel: str
    status: str
    counterparty_account: Optional[str] = None
    description: Optional[str] = None
    alert_generated: Optional[bool] = False
    alert_id: Optional[int] = None
    rule_triggered: Optional[str] = None

class TransactionFilter(BaseModel):
    account_id: Optional[int] = None
    channel: Optional[str] = None
    transaction_type: Optional[str] = None
    status: Optional[str] = None
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 10
