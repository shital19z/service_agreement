"""Reusable components for PDF pages"""

def get_logo_html(logo_path):
    """
    Generate logo HTML
    
    Args:
        logo_path: Path to logo image file
    
    Returns:
        HTML string for logo
    """
    if logo_path and logo_path.strip():
        return f'<img src="{logo_path}" class="logo-img" />'
    return '<div class="main-title">OPTIONS</div><div class="sub-title">FOR SENIOR AMERICA</div>'


def get_footer(footer_version):
    """
    Generate footer HTML
    
    Args:
        footer_version: Version code for footer
    
    Returns:
        HTML string for footer
    """
    return f'<div class="footer-code">{footer_version}</div>'