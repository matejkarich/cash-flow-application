from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import json

from ..core.database import get_db
# from ..services.google_sheets_service import GoogleSheetsService  # Temporarily disabled
from ..schemas.transaction import TransactionCreate, BulkTransactionImport

router = APIRouter()


@router.post("/google-sheets")
async def import_from_google_sheets(
    spreadsheet_id: str = Form(..., description="Google Sheets spreadsheet ID"),
    range_name: str = Form("Sheet1", description="Range to import (e.g., 'Sheet1' or 'A1:F100')"),
    user_id: str = Form(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Import transactions from a Google Sheets document"""
    try:
        # Google Sheets service temporarily disabled
        raise HTTPException(status_code=501, detail="Google Sheets import temporarily disabled. Please use CSV upload instead.")
        
        # Initialize Google Sheets service
        # sheets_service = GoogleSheetsService()
        
        # Read data from the sheet
        # sheet_data = sheets_service.read_sheet_data(spreadsheet_id, range_name)
        
        if not sheet_data:
            raise HTTPException(status_code=400, detail="No data found in the specified range")
        
        # Validate sheet format
        validation_result = sheets_service.validate_sheet_format(sheet_data)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["error"])
        
        # Parse data into transactions
        transactions = sheets_service.parse_financial_data(sheet_data, user_id)
        
        if not transactions:
            raise HTTPException(status_code=400, detail="No valid transactions found in the sheet")
        
        return {
            "message": f"Successfully parsed {len(transactions)} transactions",
            "transaction_count": len(transactions),
            "preview": [
                {
                    "date": t.date.strftime("%Y-%m-%d"),
                    "amount": float(t.amount),
                    "description": t.description,
                    "payment_method": t.payment_method
                }
                for t in transactions[:5]  # Show first 5 transactions as preview
            ],
            "validation": validation_result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing from Google Sheets: {e}")


@router.post("/csv-upload")
async def import_from_csv(
    file: UploadFile = File(..., description="CSV file to upload"),
    user_id: str = Form(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Import transactions from an uploaded CSV file"""
    try:
        # Check file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        # Read file content
        file_content = await file.read()
        
        # Temporarily use simple CSV parsing
        import csv
        import io
        import chardet
        from datetime import datetime
        from decimal import Decimal
        
        # Detect encoding and parse CSV
        encoding = chardet.detect(file_content)['encoding'] or 'utf-8'
        csv_content = file_content.decode(encoding)
        csv_reader = csv.DictReader(io.StringIO(csv_content))
        
        transactions = []
        for i, row in enumerate(csv_reader):
            try:
                # Parse date
                date_str = row.get('Date', row.get('date', ''))
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Parse amount
                amount_str = row.get('Amount', row.get('amount', '0'))
                amount = Decimal(amount_str.replace('$', '').replace(',', ''))
                
                # Get description
                description = row.get('Description', row.get('description', f'Transaction {i+1}'))
                
                # Simple transaction object (mock)
                transactions.append({
                    'date': date_obj.strftime('%Y-%m-%d'),
                    'amount': float(amount),
                    'description': description,
                    'payment_method': row.get('Payment Method', row.get('payment_method', ''))
                })
            except Exception as e:
                print(f"Error parsing row {i}: {e}")
                continue
        
        if not transactions:
            raise HTTPException(status_code=400, detail="No valid transactions found in the CSV file")
        
        return {
            "message": f"Successfully parsed {len(transactions)} transactions from CSV",
            "transaction_count": len(transactions),
            "filename": file.filename,
            "preview": transactions[:5]  # Show first 5 transactions as preview
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing CSV file: {e}")


@router.post("/validate-format")
async def validate_import_format(
    file: UploadFile = File(..., description="File to validate"),
    db: Session = Depends(get_db)
):
    """Validate the format of an uploaded file before importing"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Initialize Google Sheets service
        sheets_service = GoogleSheetsService()
        
        # Parse file to get sheet data format
        if file.filename.endswith('.csv'):
            sheet_data = []
            import csv
            import io
            import chardet
            
            encoding = chardet.detect(file_content)['encoding'] or 'utf-8'
            csv_content = file_content.decode(encoding)
            csv_reader = csv.reader(io.StringIO(csv_content))
            sheet_data = list(csv_reader)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload a CSV file.")
        
        # Validate format
        validation_result = sheets_service.validate_sheet_format(sheet_data)
        
        return {
            "valid": validation_result["valid"],
            "filename": file.filename,
            "headers": validation_result.get("headers", []),
            "row_count": validation_result.get("row_count", 0),
            "error": validation_result.get("error", None),
            "suggestions": {
                "required_columns": ["date", "amount", "description"],
                "optional_columns": ["category", "subcategory", "payment method", "card"],
                "supported_date_formats": [
                    "YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY", 
                    "MM-DD-YYYY", "DD-MM-YYYY", "YYYY/MM/DD"
                ],
                "amount_format_notes": [
                    "Negative amounts for expenses, positive for income",
                    "Use parentheses for negative amounts: (100.00)",
                    "Currency symbols will be automatically removed"
                ]
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating file format: {e}")


@router.get("/templates/csv")
async def download_csv_template():
    """Download a CSV template for importing transactions"""
    template_content = """Date,Description,Amount,Category,Subcategory,Payment Method
2024-01-15,Grocery Store,-85.32,Food,Groceries,Chase Sapphire
2024-01-16,Salary,3500.00,Income,Job,Direct Deposit
2024-01-17,Netflix,-15.99,Entertainment,Streaming,Amex Gold
2024-01-18,Gas Station,-45.67,Transportation,Gas,Debit Card
2024-01-19,Restaurant,-67.89,Food,Dining Out,Chase Sapphire"""
    
    return {
        "content": template_content,
        "filename": "finance_import_template.csv",
        "headers": ["Date", "Description", "Amount", "Category", "Subcategory", "Payment Method"],
        "sample_data": [
            {
                "Date": "2024-01-15",
                "Description": "Grocery Store",
                "Amount": "-85.32",
                "Category": "Food",
                "Subcategory": "Groceries", 
                "Payment Method": "Chase Sapphire"
            },
            {
                "Date": "2024-01-16",
                "Description": "Salary", 
                "Amount": "3500.00",
                "Category": "Income",
                "Subcategory": "Job",
                "Payment Method": "Direct Deposit"
            }
        ],
        "instructions": [
            "Use negative amounts for expenses and positive for income",
            "Date format should be YYYY-MM-DD, MM/DD/YYYY, or similar standard formats",
            "Category and Subcategory are optional but recommended for better categorization",
            "Payment Method helps track which cards/accounts you use most"
        ]
    }