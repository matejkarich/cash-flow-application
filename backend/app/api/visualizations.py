from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from ..core.database import get_db
from ..services.visualization_service import VisualizationService

router = APIRouter()


@router.get("/sankey-diagram")
async def get_sankey_diagram(
    user_id: str = Query(..., description="User ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Generate a Sankey diagram showing cash flow from income to expenses"""
    try:
        # Parse dates if provided
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Create visualization service
        viz_service = VisualizationService(db)
        
        # Generate Sankey diagram
        result = viz_service.create_sankey_diagram(user_id, start_dt, end_dt)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Sankey diagram: {e}")


@router.get("/spending-pie-chart")
async def get_spending_pie_chart(
    user_id: str = Query(..., description="User ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Generate a pie chart showing spending by category"""
    try:
        # Parse dates if provided
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Create visualization service
        viz_service = VisualizationService(db)
        
        # Generate pie chart
        result = viz_service.create_spending_pie_chart(user_id, start_dt, end_dt)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating pie chart: {e}")


@router.get("/monthly-trends")
async def get_monthly_trends(
    user_id: str = Query(..., description="User ID"),
    months: int = Query(12, description="Number of months to include", ge=1, le=24),
    db: Session = Depends(get_db)
):
    """Generate a line chart showing monthly spending trends"""
    try:
        # Create visualization service
        viz_service = VisualizationService(db)
        
        # Generate trend chart
        result = viz_service.create_monthly_trend_chart(user_id, months)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating trend chart: {e}")


@router.get("/credit-card-usage")
async def get_credit_card_usage(
    user_id: str = Query(..., description="User ID"),
    db: Session = Depends(get_db)
):
    """Generate a chart showing credit card usage distribution"""
    try:
        # Create visualization service
        viz_service = VisualizationService(db)
        
        # Generate card usage chart
        result = viz_service.create_credit_card_usage_chart(user_id)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating card usage chart: {e}")


@router.get("/dashboard")
async def get_dashboard_data(
    user_id: str = Query(..., description="User ID"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all dashboard visualizations in one request"""
    try:
        # Parse dates if provided
        start_dt = None
        end_dt = None
        
        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Create visualization service
        viz_service = VisualizationService(db)
        
        # Generate all charts
        dashboard_data = {
            "sankey_diagram": viz_service.create_sankey_diagram(user_id, start_dt, end_dt),
            "spending_pie_chart": viz_service.create_spending_pie_chart(user_id, start_dt, end_dt),
            "monthly_trends": viz_service.create_monthly_trend_chart(user_id, 12),
            "credit_card_usage": viz_service.create_credit_card_usage_chart(user_id)
        }
        
        return dashboard_data
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating dashboard: {e}")