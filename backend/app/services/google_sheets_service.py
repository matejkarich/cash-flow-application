import os
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from decimal import Decimal
import hashlib
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import io
import csv

from ..schemas.transaction import TransactionCreate, TransactionSource


class GoogleSheetsService:
    """Service for importing data from Google Sheets"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    def __init__(self):
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        creds = None
        token_path = 'token.json'
        credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', './credentials/google_credentials.json')
        
        # Load existing token
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(credentials_path):
                    flow = InstalledAppFlow.from_client_secrets_file(credentials_path, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    raise Exception(f"Google credentials file not found at {credentials_path}")
            
            # Save credentials for next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('sheets', 'v4', credentials=creds)
    
    def read_sheet_data(self, spreadsheet_id: str, range_name: str = 'Sheet1') -> List[List[str]]:
        """Read data from a Google Sheet"""
        if not self.service:
            raise Exception("Google Sheets service not authenticated")
        
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        
        return values
    
    def parse_financial_data(self, sheet_data: List[List[str]], user_id: str) -> List[TransactionCreate]:
        """Parse Google Sheets data into transaction objects"""
        if not sheet_data:
            return []
        
        # Assume first row is headers
        headers = [h.lower().strip() for h in sheet_data[0]]
        transactions = []
        
        # Find column indices
        date_col = self._find_column_index(headers, ['date', 'transaction date', 'day'])
        description_col = self._find_column_index(headers, ['description', 'memo', 'transaction', 'details'])
        amount_col = self._find_column_index(headers, ['amount', 'value', 'cost', 'price'])
        category_col = self._find_column_index(headers, ['category', 'cat'])
        subcategory_col = self._find_column_index(headers, ['subcategory', 'subcat', 'sub category'])
        payment_method_col = self._find_column_index(headers, ['payment method', 'card', 'method', 'payment'])
        
        for row_idx, row in enumerate(sheet_data[1:], start=2):  # Skip header row
            try:
                # Skip empty rows
                if not row or all(not cell.strip() for cell in row):
                    continue
                
                # Parse date
                date_str = self._get_cell_value(row, date_col)
                if not date_str:
                    continue
                
                transaction_date = self._parse_date(date_str)
                if not transaction_date:
                    print(f"Warning: Could not parse date '{date_str}' in row {row_idx}")
                    continue
                
                # Parse amount
                amount_str = self._get_cell_value(row, amount_col)
                if not amount_str:
                    continue
                
                amount = self._parse_amount(amount_str)
                if amount == 0:
                    continue
                
                # Parse description
                description = self._get_cell_value(row, description_col) or f"Transaction {row_idx}"
                
                # Parse optional fields
                category = self._get_cell_value(row, category_col)
                subcategory = self._get_cell_value(row, subcategory_col)
                payment_method = self._get_cell_value(row, payment_method_col)
                
                # Generate import hash for duplicate detection
                import_hash = self._generate_import_hash(transaction_date, amount, description)
                
                transaction = TransactionCreate(
                    date=transaction_date,
                    amount=amount,
                    description=description,
                    category_id=None,  # Will be resolved later
                    subcategory_id=None,  # Will be resolved later
                    payment_method=payment_method,
                    source=TransactionSource.GOOGLE_SHEETS,
                    user_id=user_id,
                    original_description=description,
                    import_hash=import_hash,
                    verified=False
                )
                
                transactions.append(transaction)
                
            except Exception as e:
                print(f"Error parsing row {row_idx}: {e}")
                continue
        
        return transactions
    
    def import_from_csv_file(self, file_content: bytes, user_id: str) -> List[TransactionCreate]:
        """Import transactions from uploaded CSV file"""
        try:
            # Detect encoding
            import chardet
            encoding = chardet.detect(file_content)['encoding'] or 'utf-8'
            
            # Read CSV content
            csv_content = file_content.decode(encoding)
            csv_reader = csv.reader(io.StringIO(csv_content))
            
            # Convert to list format similar to Google Sheets
            sheet_data = list(csv_reader)
            
            return self.parse_financial_data(sheet_data, user_id)
            
        except Exception as e:
            raise Exception(f"Error importing CSV file: {e}")
    
    def _find_column_index(self, headers: List[str], possible_names: List[str]) -> Optional[int]:
        """Find column index by matching possible names"""
        for name in possible_names:
            for idx, header in enumerate(headers):
                if name in header.lower():
                    return idx
        return None
    
    def _get_cell_value(self, row: List[str], col_index: Optional[int]) -> Optional[str]:
        """Safely get cell value from row"""
        if col_index is None or col_index >= len(row):
            return None
        return row[col_index].strip() if row[col_index] else None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string into datetime object"""
        date_formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d/%m/%Y',
            '%m-%d-%Y',
            '%d-%m-%Y',
            '%Y/%m/%d',
            '%B %d, %Y',
            '%b %d, %Y',
            '%m/%d/%y',
            '%d/%m/%y'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _parse_amount(self, amount_str: str) -> Decimal:
        """Parse amount string into Decimal"""
        try:
            # Remove currency symbols and commas
            cleaned = amount_str.replace('$', '').replace(',', '').replace(' ', '')
            
            # Handle parentheses for negative amounts
            if cleaned.startswith('(') and cleaned.endswith(')'):
                cleaned = '-' + cleaned[1:-1]
            
            return Decimal(cleaned)
        except:
            return Decimal('0')
    
    def _generate_import_hash(self, date: datetime, amount: Decimal, description: str) -> str:
        """Generate hash for duplicate detection"""
        hash_string = f"{date.strftime('%Y-%m-%d')}_{amount}_{description}"
        return hashlib.md5(hash_string.encode()).hexdigest()
    
    def validate_sheet_format(self, sheet_data: List[List[str]]) -> Dict[str, Any]:
        """Validate that the sheet has the required format"""
        if not sheet_data:
            return {"valid": False, "error": "Sheet is empty"}
        
        headers = [h.lower().strip() for h in sheet_data[0]]
        
        # Check for required columns
        required_columns = ['date', 'amount', 'description']
        missing_columns = []
        
        for required in required_columns:
            if not any(required in header for header in headers):
                missing_columns.append(required)
        
        if missing_columns:
            return {
                "valid": False, 
                "error": f"Missing required columns: {', '.join(missing_columns)}",
                "headers": headers
            }
        
        return {
            "valid": True,
            "headers": headers,
            "row_count": len(sheet_data) - 1  # Exclude header
        }