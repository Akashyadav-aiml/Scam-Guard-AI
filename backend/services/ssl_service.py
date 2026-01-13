"""
SSL/HTTPS Service for Certificate Validation
"""
import ssl
import socket
import asyncio
from datetime import datetime
from typing import Dict
import logging

logger = logging.getLogger(__name__)


class SSLService:
    """Service for SSL/HTTPS certificate checking"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    async def check_ssl(self, domain: str) -> Dict:
        """
        Check SSL certificate for domain
        
        Args:
            domain: Domain name to check
            
        Returns:
            Dict with SSL information
        """
        try:
            loop = asyncio.get_event_loop()
            ssl_info = await asyncio.wait_for(
                loop.run_in_executor(None, self._sync_check_ssl, domain),
                timeout=self.timeout
            )
            return ssl_info
        except asyncio.TimeoutError:
            logger.warning(f"SSL check timeout for {domain}")
            return self._get_no_ssl_response(domain, "timeout")
        except Exception as e:
            logger.error(f"SSL check error for {domain}: {str(e)}")
            return self._get_no_ssl_response(domain, str(e))
    
    def _sync_check_ssl(self, domain: str) -> Dict:
        """Synchronous SSL check"""
        result = {
            'domain': domain,
            'has_ssl': False,
            'ssl_valid': False,
            'issuer': None,
            'valid_from': None,
            'valid_until': None,
            'days_until_expiry': None,
            'version': None,
            'cipher': None
        }
        
        try:
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect to domain
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    version = ssock.version()
                    
                    result['has_ssl'] = True
                    result['ssl_valid'] = True
                    result['version'] = version
                    result['cipher'] = cipher[0] if cipher else None
                    
                    # Parse certificate details
                    if cert:
                        # Issuer
                        issuer = dict(x[0] for x in cert.get('issuer', []))
                        result['issuer'] = issuer.get('organizationName', 'Unknown')
                        
                        # Valid from
                        not_before = cert.get('notBefore')
                        if not_before:
                            result['valid_from'] = self._parse_cert_date(not_before)
                        
                        # Valid until
                        not_after = cert.get('notAfter')
                        if not_after:
                            valid_until = self._parse_cert_date(not_after)
                            result['valid_until'] = valid_until
                            
                            # Calculate days until expiry
                            if valid_until:
                                expiry_date = datetime.fromisoformat(valid_until)
                                days_left = (expiry_date - datetime.now()).days
                                result['days_until_expiry'] = days_left
                    
                    logger.info(f"SSL check successful for {domain}")
                    
        except ssl.SSLError as e:
            logger.warning(f"SSL error for {domain}: {str(e)}")
            result['has_ssl'] = True  # Has SSL but invalid
            result['ssl_valid'] = False
            result['error'] = str(e)
            
        except socket.gaierror:
            logger.warning(f"DNS resolution failed for {domain}")
            result['error'] = "DNS resolution failed"
            
        except ConnectionRefusedError:
            logger.warning(f"Connection refused for {domain}:443")
            result['error'] = "HTTPS port not accessible"
            
        except socket.timeout:
            logger.warning(f"Connection timeout for {domain}")
            result['error'] = "Connection timeout"
            
        except Exception as e:
            logger.error(f"Unexpected error checking SSL for {domain}: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    def _parse_cert_date(self, date_str: str) -> str:
        """Parse certificate date format"""
        try:
            # Certificate dates are in format: 'Jan 1 00:00:00 2024 GMT'
            dt = datetime.strptime(date_str, '%b %d %H:%M:%S %Y %Z')
            return dt.isoformat()
        except Exception as e:
            logger.error(f"Error parsing certificate date '{date_str}': {str(e)}")
            return date_str
    
    def _get_no_ssl_response(self, domain: str, error: str) -> Dict:
        """Return response for domains without SSL"""
        return {
            'domain': domain,
            'has_ssl': False,
            'ssl_valid': False,
            'issuer': None,
            'valid_from': None,
            'valid_until': None,
            'days_until_expiry': None,
            'version': None,
            'cipher': None,
            'error': error
        }
