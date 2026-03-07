def check_text_length(text: str, max_len: int = 50000) -> bool:
    """
    Validates that the resume text is not excessively long.
    
    Args:
        text (str): The extracted text.
        max_len (int): Maximum allowed characters. Default 50,000 (~10-15 pages).
        
    Returns:
        bool: True if text length is within limits, False otherwise.
    """
    if text is None:
        return False
    return len(text) <= max_len
