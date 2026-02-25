"""Utility functions for PDF generation"""

def safe_get(data_dict, key, default=""):
    """
    Safely get a value from dictionary
    
    Args:
        data_dict: Dictionary to get value from
        key: Key to look up
        default: Default value if key not found or value is None/empty
    
    Returns:
        String value
    """
    val = data_dict.get(key)
    if val is None or str(val).strip().lower() in ['none', 'null', '']:
        return default
    return str(val).strip()


def format_holidays_list(holidays):
    """
    Format holidays list into a readable string
    
    Args:
        holidays: List of holiday names
    
    Returns:
        Formatted string like "A, B, and C"
    """
    if not holidays:
        return ""
    if len(holidays) == 1:
        return holidays[0] + "."
    return ", ".join(holidays[:-1]) + ", and " + holidays[-1] + "."


def extract_state_from_display_name(display_name):
    """
    Extract state code from display name like 'Atlanta Home Care (GA)'
    
    Args:
        display_name: Branch display name
    
    Returns:
        Two-letter state code or 'MD' as default
    """
    import re
    state_match = re.search(r'\(([A-Z]{2})\)', display_name)
    return state_match.group(1) if state_match else 'MD'