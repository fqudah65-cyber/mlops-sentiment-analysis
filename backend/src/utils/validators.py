"""
Input Validators
Utility functions for validating API inputs
"""

import re
from typing import Any, Tuple

def validate_input(data: Any, required_fields: list) -> Tuple[bool, str]:
    """
    Validate input data has required fields
    
    Args:
        data: Input data to validate
        required_fields: List of required field names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not data:
        return False, "Input data is empty"
    
    if not isinstance(data, dict):
        return False, "Input must be a dictionary"
    
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        
        if data[field] is None or (isinstance(data[field], str) and len(data[field].strip()) == 0):
            return False, f"Field '{field}' cannot be empty"
    
    return True, ""

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_text_length(text: str, min_length: int = 1, max_length: int = 5000) -> Tuple[bool, str]:
    """
    Validate text length
    
    Args:
        text: Text to validate
        min_length: Minimum length
        max_length: Maximum length
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(text, str):
        return False, "Text must be a string"
    
    text_length = len(text.strip())
    
    if text_length < min_length:
        return False, f"Text must be at least {min_length} characters"
    
    if text_length > max_length:
        return False, f"Text exceeds maximum length of {max_length} characters"
    
    return True, ""

def sanitize_text(text: str) -> str:
    """
    Sanitize input text
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove multiple consecutive spaces
    text = re.sub(r'\s+', ' ', text)
    
    return text
