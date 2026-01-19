"""
Data Formatting Utilities
"""
from datetime import datetime
from typing import Optional


# PUBLIC_INTERFACE
def format_price(price: float) -> str:
    """
    Format price for display.
    
    Args:
        price: Price value
        
    Returns:
        str: Formatted price string
    """
    return f"${price:.2f}"


# PUBLIC_INTERFACE
def format_date(date_str: Optional[str]) -> Optional[str]:
    """
    Format ISO date string to readable format.
    
    Args:
        date_str: ISO format date string
        
    Returns:
        Optional[str]: Formatted date or None
    """
    if not date_str:
        return None
    
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return date_str
