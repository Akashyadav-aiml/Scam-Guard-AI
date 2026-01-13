"""
Utility Functions for Domain Validation
"""
import re
from typing import Optional
from urllib.parse import urlparse


def validate_domain(domain: str) -> bool:
    """
    Validate domain name format
    
    Args:
        domain: Domain name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not domain or not isinstance(domain, str):
        return False
    
    # Remove protocol if present
    domain = domain.lower().strip()
    domain = remove_protocol(domain)
    
    # Remove path if present
    domain = domain.split('/')[0]
    
    # Remove port if present
    domain = domain.split(':')[0]
    
    # Basic length check
    if len(domain) < 4 or len(domain) > 253:
        return False
    
    # Domain regex pattern
    # Allows: letters, numbers, hyphens, dots
    # Must have at least one dot
    # TLD must be at least 2 characters
    pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$'
    
    if not re.match(pattern, domain):
        return False
    
    # Additional validation
    labels = domain.split('.')
    
    # Check each label
    for label in labels:
        if not label or len(label) > 63:
            return False
        if label.startswith('-') or label.endswith('-'):
            return False
    
    # Must have at least 2 labels (domain.tld)
    if len(labels) < 2:
        return False
    
    return True


def remove_protocol(url: str) -> str:
    """
    Remove protocol from URL
    
    Args:
        url: URL string
        
    Returns:
        URL without protocol
    """
    if '://' in url:
        return url.split('://', 1)[1]
    return url


def extract_domain(url: str) -> Optional[str]:
    """
    Extract domain from URL
    
    Args:
        url: Full URL
        
    Returns:
        Domain name or None
    """
    try:
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'
        
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        
        # Remove port
        domain = domain.split(':')[0]
        
        return domain if domain else None
    except Exception:
        return None


def is_ip_address(text: str) -> bool:
    """
    Check if text is an IP address
    
    Args:
        text: Text to check
        
    Returns:
        True if IP address, False otherwise
    """
    # IPv4 pattern
    ipv4_pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    
    if re.match(ipv4_pattern, text):
        return True
    
    # IPv6 pattern (simplified)
    if ':' in text and len(text.split(':')) >= 3:
        return True
    
    return False


def sanitize_domain(domain: str) -> str:
    """
    Sanitize domain input
    
    Args:
        domain: Raw domain input
        
    Returns:
        Sanitized domain
    """
    # Remove whitespace
    domain = domain.strip()
    
    # Convert to lowercase
    domain = domain.lower()
    
    # Remove protocol
    domain = remove_protocol(domain)
    
    # Remove path
    domain = domain.split('/')[0]
    
    # Remove port
    domain = domain.split(':')[0]
    
    # Remove www prefix (optional)
    if domain.startswith('www.'):
        domain = domain[4:]
    
    return domain
