"""
FraudLens: Transaction Management Router
"""

import io
import csv
from typing import Optional
from fastapi import APIRouter, Query, HTTPException, Response
from app.backend.repositories import get_repo, is_live_mode
from app.backend.schemas.common import ApiResponse, PaginatedData
from app.backend.schemas.transaction import TransactionCreate, TransactionResponse

router = APIRouter(tags=["Transactions"])

@router.get("/transactions", response_model=ApiResponse[PaginatedData[TransactionResponse]])
def list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    account_id: Optional[int] = Query(None),
    channel: Optional[str] = Query(None),
    transaction_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    search: Optional[str] = Query(None)
):
    """Returns paginated, searchable, filterable transaction stream."""
    repo = get_repo()
    items, total = repo.get_transactions(
        page=page,
        page_size=page_size,
        account_id=account_id,
        channel=channel,
        transaction_type=transaction_type,
        status=status,
        min_amount=min_amount,
        max_amount=max_amount,
        search=search
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    
    return ApiResponse(
        success=True,
        data=PaginatedData(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        ),
        is_live_oracle=is_live_mode()
    )

@router.get("/transactions/export/csv")
def export_transactions_csv(
    account_id: Optional[int] = Query(None),
    channel: Optional[str] = Query(None),
    transaction_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None)
):
    """Exports safe CSV stream of transactions."""
    repo = get_repo()
    items, _ = repo.get_transactions(
        page=1,
        page_size=1000,
        account_id=account_id,
        channel=channel,
        transaction_type=transaction_type,
        status=status,
        search=search
    )
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Transaction ID", "Account ID", "Account Number", "Customer Name",
        "Type", "Amount (INR)", "Date", "Channel", "Status",
        "Counterparty", "Description", "Alert Triggered"
    ])
    for item in items:
        writer.writerow([
            item["transaction_id"],
            item["account_id"],
            item.get("account_number", ""),
            item.get("customer_name", ""),
            item["transaction_type"],
            f"{item['amount']:.2f}",
            item["transaction_date"],
            item["channel"],
            item["status"],
            item.get("counterparty_account", ""),
            item.get("description", ""),
            item.get("rule_triggered", "None")
        ])
        
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=fraudlens_transactions.csv"}
    )

@router.get("/transactions/{transaction_id}", response_model=ApiResponse[TransactionResponse])
def get_transaction(transaction_id: int):
    """Fetches details for a specific transaction."""
    repo = get_repo()
    tx = repo.get_transaction_by_id(transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail=f"Transaction ID {transaction_id} not found.")
    return ApiResponse(
        success=True,
        data=tx,
        is_live_oracle=is_live_mode()
    )

@router.post("/transactions", response_model=ApiResponse[TransactionResponse], status_code=201)
def create_transaction(payload: TransactionCreate):
    """
    Submits a validated financial transaction.
    If amount > threshold (₹50,000), evaluates procedural surveillance rule,
    sets status to FLAGGED, and creates an alert record.
    """
    repo = get_repo()
    try:
        new_tx = repo.create_transaction(
            account_id=payload.account_id,
            transaction_type=payload.transaction_type,
            amount=payload.amount,
            channel=payload.channel,
            counterparty_account=payload.counterparty_account,
            description=payload.description
        )
        return ApiResponse(
            success=True,
            data=new_tx,
            message=f"Transaction {new_tx['transaction_id']} successfully recorded." + 
                    (f" Breached >50k threshold: Alert {new_tx['alert_id']} generated!" if new_tx.get('alert_generated') else ""),
            is_live_oracle=is_live_mode()
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/accounts")
def list_active_accounts():
    """Returns active accounts for transaction creation dropdown."""
    repo = get_repo()
    accounts = repo.get_active_accounts()
    return ApiResponse(
        success=True,
        data=accounts,
        is_live_oracle=is_live_mode()
    )
