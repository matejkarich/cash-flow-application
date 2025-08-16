# Personal Finance Cash Flow Analyzer

A comprehensive personal finance application that creates interactive cash flow diagrams similar to Monarch Money, with advanced credit card rewards optimization and transaction analysis.

## 🎯 Project Overview

This application transforms your financial data into beautiful, interactive visualizations that help you understand your spending patterns, optimize credit card usage, and track cash flow from income to specific expense categories.

## ✨ Key Features

### Core Functionality
- **Cash Flow Diagrams**: Interactive Sankey charts showing money flow from income through categories to subcategories
- **Google Sheets Import**: Direct integration with your existing financial tracking spreadsheets
- **Multi-Level Categorization**: Hierarchical expense categorization (General → Specific subcategories)
- **Interactive Dashboards**: Multiple chart types for spending analysis

### Advanced Features
- **Credit Card Analytics**: Track which cards you use most and optimize usage
- **Rewards Calculator**: Calculate points/cashback based on your card's reward rules
- **Card Comparison Tool**: Compare rewards potential across different credit cards
- **Bank Transaction Import**: Parse and categorize bank/credit card transaction files
- **Manual Adjustments**: Easy categorization override and correction system

## 🏗️ Architecture Design

### Technology Stack
- **Backend**: Python with FastAPI
- **Frontend**: React with TypeScript
- **Visualization**: Plotly.js for interactive charts
- **Data Processing**: Pandas for financial data manipulation
- **Database**: SQLite for local storage, PostgreSQL for production
- **File Processing**: openpyxl for Excel/Google Sheets, pandas for CSV

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Input    │────│  Core Engine    │────│  Visualization  │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ Google Sheets   │    │ Transaction     │    │ Sankey Diagrams │
│ Bank Files      │    │ Processor       │    │ Pie Charts      │
│ Manual Entry    │    │ Categorization  │    │ Bar Charts      │
│ Credit Cards    │    │ Rewards Engine  │    │ Line Charts     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Data Flow Architecture

```
Input Sources → Data Processor → Category Engine → Rewards Calculator → Visualization Engine
     ↓               ↓               ↓                   ↓                   ↓
Google Sheets → Parse & Clean → Auto-Categorize → Calculate Points → Generate Charts
Bank Files   → Standardize   → Manual Review   → Apply Rules     → Export Reports
Manual Entry → Validate      → Store Categories→ Compare Cards   → Interactive UI
```

## 📊 Core Models

### Transaction Model
```python
class Transaction:
    id: str
    date: datetime
    amount: Decimal
    description: str
    category: str
    subcategory: str
    payment_method: str  # credit card, cash, etc.
    source: str  # google_sheets, bank_import, manual
    verified: bool
```

### Category Hierarchy
```python
class Category:
    id: str
    name: str
    parent_id: Optional[str]
    color: str
    icon: str
    budget_limit: Optional[Decimal]
```

### Credit Card Model
```python
class CreditCard:
    id: str
    name: str
    bank: str
    reward_rules: List[RewardRule]
    annual_fee: Decimal
    active: bool

class RewardRule:
    category: str
    rate: Decimal  # points per dollar
    cap: Optional[Decimal]  # spending cap for this rate
    quarterly_bonus: bool
```

## 🚀 Implementation Plan

### Phase 1: Foundation (MVP)
1. **Project Setup**
   - Initialize Python project with FastAPI
   - Set up React frontend
   - Configure development environment

2. **Core Data Models**
   - Implement transaction, category, and card models
   - Set up SQLite database with SQLAlchemy
   - Create basic CRUD operations

3. **Google Sheets Integration**
   - Google Sheets API integration
   - CSV upload functionality
   - Data validation and cleaning

4. **Basic Visualization**
   - Simple Sankey diagram for cash flow
   - Basic spending breakdown charts

### Phase 2: Advanced Analytics
1. **Enhanced Categorization**
   - Machine learning-based auto-categorization
   - Manual categorization interface
   - Category management system

2. **Credit Card Analytics**
   - Card usage tracking
   - Basic rewards calculation
   - Spending by payment method

### Phase 3: Rewards Optimization
1. **Rewards Engine**
   - Complex reward rule implementation
   - Points calculation across multiple cards
   - Quarterly bonus tracking

2. **Card Comparison Tool**
   - Side-by-side card comparison
   - Optimization recommendations
   - "What-if" scenarios

### Phase 4: Bank Integration
1. **Transaction Import**
   - CSV/OFX file parsing
   - Multiple bank format support
   - Duplicate detection

2. **Advanced Features**
   - Automatic transaction categorization
   - Budget tracking and alerts
   - Monthly/yearly reports

## 📁 Project Structure

```
finance-analyzer/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── services/
│   │   ├── api/
│   │   └── core/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   ├── public/
│   └── package.json
├── data/
│   ├── sample_data/
│   └── schemas/
├── docs/
└── README.md
```

## 🛠️ Development Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Installation Steps

1. **Clone and Setup Backend**
```bash
git clone <repository>
cd finance-analyzer
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r backend/requirements.txt
```

2. **Setup Frontend**
```bash
cd frontend
npm install
```

3. **Initialize Database**
```bash
cd backend
python -m alembic upgrade head
```

4. **Run Development Servers**
```bash
# Backend (from backend/)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (from frontend/)
npm start
```

## 📋 Sample Data Format

### Google Sheets Expected Format
```csv
Date,Description,Amount,Category,Subcategory,Payment Method
2024-01-15,Grocery Store,-85.32,Food,Groceries,Chase Sapphire
2024-01-16,Salary,3500.00,Income,Job,Direct Deposit
2024-01-17,Netflix,-15.99,Entertainment,Streaming,Amex Gold
```

### Bank Transaction File Format
```csv
Date,Description,Amount,Type
01/15/2024,GROCERY STORE #123,-85.32,Purchase
01/16/2024,PAYROLL DEPOSIT,3500.00,Credit
01/17/2024,NETFLIX.COM,-15.99,Purchase
```

## 🎨 Visualization Examples

### Cash Flow Sankey Diagram
- Income sources → General categories → Specific subcategories
- Color-coded by category
- Interactive hover details
- Monthly/yearly views

### Spending Analysis Charts
- Pie chart: Spending by category percentage
- Bar chart: Monthly spending trends
- Line chart: Account balance over time
- Heat map: Spending patterns by day/category

### Credit Card Analytics
- Card usage distribution
- Rewards earned by card
- Optimization suggestions

## 🔧 Configuration

### Environment Variables
```env
DATABASE_URL=sqlite:///./finance.db
GOOGLE_SHEETS_API_KEY=your_api_key
SECRET_KEY=your_secret_key
DEBUG=true
```

### Rewards Rules Configuration
```json
{
  "chase_sapphire": {
    "dining": 2.0,
    "travel": 2.0,
    "general": 1.0,
    "annual_fee": 95
  },
  "amex_gold": {
    "dining": 4.0,
    "groceries": 4.0,
    "general": 1.0,
    "annual_fee": 250
  }
}
```

## 🚦 Getting Started

1. Follow the installation steps above
2. Upload your Google Sheets file or CSV
3. Review and adjust auto-categorization
4. Add your credit cards and reward rules
5. Generate your first cash flow diagram!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📈 Future Enhancements

- Mobile app with React Native
- Integration with bank APIs (Plaid)
- Investment tracking
- Tax optimization suggestions
- Bill prediction and budgeting
- Multi-user support for families
- Export to financial planning software

## 📄 License

MIT License - See LICENSE file for details
