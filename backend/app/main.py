from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from .core.database import create_tables
from .api import transactions, categories, credit_cards, visualizations, imports

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Personal Finance Cash Flow Analyzer",
    description="A comprehensive personal finance application for analyzing cash flow and optimizing credit card rewards",
    version="1.0.0"
)

# Configure CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Include API routers
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["transactions"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(credit_cards.router, prefix="/api/v1/credit-cards", tags=["credit-cards"])
app.include_router(visualizations.router, prefix="/api/v1/visualizations", tags=["visualizations"])
app.include_router(imports.router, prefix="/api/v1/imports", tags=["imports"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Personal Finance API is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Personal Finance Cash Flow Analyzer API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "health_url": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)