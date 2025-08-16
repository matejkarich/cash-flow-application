import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from ..models import Transaction, Category, CreditCard
from ..schemas.transaction import TransactionResponse


class VisualizationService:
    """Service for creating financial visualizations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_sankey_diagram(self, user_id: str, start_date: Optional[datetime] = None, 
                            end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Create a Sankey diagram showing cash flow from income to expenses"""
        
        # Get transactions for the period
        query = self.db.query(Transaction).filter(Transaction.user_id == user_id)
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.all()
        
        if not transactions:
            return self._empty_sankey()
        
        # Separate income and expenses
        income_transactions = [t for t in transactions if t.amount > 0]
        expense_transactions = [t for t in transactions if t.amount < 0]
        
        # Build nodes and links
        nodes = []
        links = []
        node_map = {}
        
        # Add income sources
        income_sources = self._group_income_sources(income_transactions)
        for source, amount in income_sources.items():
            node_id = len(nodes)
            nodes.append({
                "label": source,
                "color": "#27ae60",  # Green for income
                "value": float(amount)
            })
            node_map[f"income_{source}"] = node_id
        
        # Add "Available Money" node
        total_income = sum(income_sources.values())
        available_money_id = len(nodes)
        nodes.append({
            "label": "Available Money",
            "color": "#3498db",  # Blue for available money
            "value": float(total_income)
        })
        node_map["available_money"] = available_money_id
        
        # Create links from income sources to available money
        for source, amount in income_sources.items():
            links.append({
                "source": node_map[f"income_{source}"],
                "target": available_money_id,
                "value": float(amount),
                "color": "rgba(39, 174, 96, 0.3)"
            })
        
        # Group expenses by category
        category_expenses = self._group_expenses_by_category(expense_transactions)
        
        # Add category nodes
        for category_name, category_data in category_expenses.items():
            category_id = len(nodes)
            nodes.append({
                "label": category_name,
                "color": category_data.get("color", "#e74c3c"),  # Default red
                "value": float(category_data["total"])
            })
            node_map[f"category_{category_name}"] = category_id
            
            # Link from available money to category
            links.append({
                "source": available_money_id,
                "target": category_id,
                "value": float(category_data["total"]),
                "color": "rgba(52, 152, 219, 0.3)"
            })
            
            # Add subcategory nodes if they exist
            for subcategory_name, subcategory_amount in category_data.get("subcategories", {}).items():
                subcategory_id = len(nodes)
                nodes.append({
                    "label": f"{category_name} > {subcategory_name}",
                    "color": category_data.get("color", "#e74c3c"),
                    "value": float(subcategory_amount)
                })
                
                # Link from category to subcategory
                links.append({
                    "source": category_id,
                    "target": subcategory_id,
                    "value": float(subcategory_amount),
                    "color": "rgba(231, 76, 60, 0.3)"
                })
        
        # Calculate remaining money
        total_expenses = sum(abs(t.amount) for t in expense_transactions)
        remaining_money = total_income - total_expenses
        
        if remaining_money > 0:
            remaining_id = len(nodes)
            nodes.append({
                "label": "Remaining/Savings",
                "color": "#f39c12",  # Orange for savings
                "value": float(remaining_money)
            })
            
            links.append({
                "source": available_money_id,
                "target": remaining_id,
                "value": float(remaining_money),
                "color": "rgba(243, 156, 18, 0.3)"
            })
        
        # Create Plotly Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=[node["label"] for node in nodes],
                color=[node["color"] for node in nodes]
            ),
            link=dict(
                source=[link["source"] for link in links],
                target=[link["target"] for link in links],
                value=[link["value"] for link in links],
                color=[link["color"] for link in links]
            )
        )])
        
        fig.update_layout(
            title_text="Cash Flow Diagram",
            font_size=12,
            height=600
        )
        
        return {
            "chart": fig.to_dict(),
            "summary": {
                "total_income": float(total_income),
                "total_expenses": float(total_expenses),
                "net_amount": float(remaining_money),
                "period": {
                    "start": start_date.isoformat() if start_date else None,
                    "end": end_date.isoformat() if end_date else None
                }
            }
        }
    
    def create_spending_pie_chart(self, user_id: str, start_date: Optional[datetime] = None,
                                end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Create a pie chart showing spending by category"""
        
        query = self.db.query(Transaction).filter(
            and_(Transaction.user_id == user_id, Transaction.amount < 0)
        )
        
        if start_date:
            query = query.filter(Transaction.date >= start_date)
        if end_date:
            query = query.filter(Transaction.date <= end_date)
        
        transactions = query.all()
        
        if not transactions:
            return self._empty_pie_chart()
        
        # Group by category
        category_totals = {}
        for transaction in transactions:
            category_name = "Uncategorized"
            if transaction.category:
                category_name = transaction.category.name
            
            if category_name not in category_totals:
                category_totals[category_name] = 0
            category_totals[category_name] += abs(float(transaction.amount))
        
        # Create pie chart
        fig = px.pie(
            values=list(category_totals.values()),
            names=list(category_totals.keys()),
            title="Spending by Category"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        
        return {
            "chart": fig.to_dict(),
            "data": category_totals
        }
    
    def create_monthly_trend_chart(self, user_id: str, months: int = 12) -> Dict[str, Any]:
        """Create a line chart showing monthly spending trends"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30 * months)
        
        transactions = self.db.query(Transaction).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= end_date
            )
        ).all()
        
        if not transactions:
            return self._empty_trend_chart()
        
        # Group by month
        monthly_data = {}
        for transaction in transactions:
            month_key = transaction.date.strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {"income": 0, "expenses": 0}
            
            if transaction.amount > 0:
                monthly_data[month_key]["income"] += float(transaction.amount)
            else:
                monthly_data[month_key]["expenses"] += abs(float(transaction.amount))
        
        # Prepare data for chart
        months_list = sorted(monthly_data.keys())
        income_values = [monthly_data[month]["income"] for month in months_list]
        expense_values = [monthly_data[month]["expenses"] for month in months_list]
        net_values = [income - expense for income, expense in zip(income_values, expense_values)]
        
        # Create line chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=months_list,
            y=income_values,
            mode='lines+markers',
            name='Income',
            line=dict(color='#27ae60')
        ))
        
        fig.add_trace(go.Scatter(
            x=months_list,
            y=expense_values,
            mode='lines+markers',
            name='Expenses',
            line=dict(color='#e74c3c')
        ))
        
        fig.add_trace(go.Scatter(
            x=months_list,
            y=net_values,
            mode='lines+markers',
            name='Net (Income - Expenses)',
            line=dict(color='#3498db')
        ))
        
        fig.update_layout(
            title="Monthly Financial Trends",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            height=500,
            hovermode='x unified'
        )
        
        return {
            "chart": fig.to_dict(),
            "data": monthly_data
        }
    
    def create_credit_card_usage_chart(self, user_id: str) -> Dict[str, Any]:
        """Create a chart showing credit card usage distribution"""
        
        # Get transactions with credit cards
        transactions = self.db.query(Transaction).filter(
            and_(
                Transaction.user_id == user_id,
                Transaction.credit_card_id.isnot(None),
                Transaction.amount < 0  # Only expenses
            )
        ).all()
        
        if not transactions:
            return self._empty_card_usage_chart()
        
        # Group by credit card
        card_usage = {}
        for transaction in transactions:
            card_name = transaction.credit_card.name if transaction.credit_card else "Unknown Card"
            if card_name not in card_usage:
                card_usage[card_name] = 0
            card_usage[card_name] += abs(float(transaction.amount))
        
        # Create bar chart
        fig = px.bar(
            x=list(card_usage.keys()),
            y=list(card_usage.values()),
            title="Credit Card Usage",
            labels={"x": "Credit Card", "y": "Total Spent ($)"}
        )
        
        fig.update_layout(height=400)
        
        return {
            "chart": fig.to_dict(),
            "data": card_usage
        }
    
    def _group_income_sources(self, income_transactions: List[Transaction]) -> Dict[str, Decimal]:
        """Group income transactions by source/description"""
        sources = {}
        for transaction in income_transactions:
            # Use category name if available, otherwise use description
            source_name = "Other Income"
            if transaction.category:
                source_name = transaction.category.name
            elif "salary" in transaction.description.lower() or "payroll" in transaction.description.lower():
                source_name = "Salary"
            elif "freelance" in transaction.description.lower():
                source_name = "Freelance"
            elif "interest" in transaction.description.lower():
                source_name = "Interest"
            elif "dividend" in transaction.description.lower():
                source_name = "Dividends"
            
            if source_name not in sources:
                sources[source_name] = Decimal('0')
            sources[source_name] += transaction.amount
        
        return sources
    
    def _group_expenses_by_category(self, expense_transactions: List[Transaction]) -> Dict[str, Dict[str, Any]]:
        """Group expense transactions by category and subcategory"""
        categories = {}
        
        for transaction in expense_transactions:
            category_name = "Uncategorized"
            category_color = "#95a5a6"  # Gray for uncategorized
            
            if transaction.category:
                category_name = transaction.category.name
                category_color = transaction.category.color
            
            if category_name not in categories:
                categories[category_name] = {
                    "total": Decimal('0'),
                    "color": category_color,
                    "subcategories": {}
                }
            
            amount = abs(transaction.amount)
            categories[category_name]["total"] += amount
            
            # Handle subcategories
            if transaction.subcategory:
                subcategory_name = transaction.subcategory.name
                if subcategory_name not in categories[category_name]["subcategories"]:
                    categories[category_name]["subcategories"][subcategory_name] = Decimal('0')
                categories[category_name]["subcategories"][subcategory_name] += amount
        
        return categories
    
    def _empty_sankey(self) -> Dict[str, Any]:
        """Return empty Sankey diagram"""
        fig = go.Figure(data=[go.Sankey(
            node=dict(label=["No Data"], color=["#95a5a6"]),
            link=dict(source=[], target=[], value=[])
        )])
        fig.update_layout(title_text="No transactions found for the selected period")
        
        return {
            "chart": fig.to_dict(),
            "summary": {"total_income": 0, "total_expenses": 0, "net_amount": 0}
        }
    
    def _empty_pie_chart(self) -> Dict[str, Any]:
        """Return empty pie chart"""
        fig = px.pie(values=[1], names=["No Data"], title="No spending data available")
        return {"chart": fig.to_dict(), "data": {}}
    
    def _empty_trend_chart(self) -> Dict[str, Any]:
        """Return empty trend chart"""
        fig = go.Figure()
        fig.update_layout(title="No transaction data available")
        return {"chart": fig.to_dict(), "data": {}}
    
    def _empty_card_usage_chart(self) -> Dict[str, Any]:
        """Return empty card usage chart"""
        fig = px.bar(x=[], y=[], title="No credit card usage data available")
        return {"chart": fig.to_dict(), "data": {}}