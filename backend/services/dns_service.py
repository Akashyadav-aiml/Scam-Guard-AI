"""
DNS Service for Domain Resolution
"""
import socket
import asyncio
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class DNSService:
    """Service for DNS resolution and IP lookup"""
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
    
    async def resolve_domain(self, domain: str) -> Dict:
        """
        Resolve domain to IP address
        
        Args:
            domain: Domain name to resolve
            
        Returns:
            Dict with DNS resolution information
        """
        try:
            loop = asyncio.get_event_loop()
            dns_info = await asyncio.wait_for(
                loop.run_in_executor(None, self._sync_resolve, domain),
                timeout=self.timeout
            )
            return dns_info
        except asyncio.TimeoutError:
            logger.warning(f"DNS resolution timeout for {domain}")
            return self._get_failed_resolution(domain, "timeout")
        except Exception as e:
            logger.error(f"DNS resolution error for {domain}: {str(e)}")
            return self._get_failed_resolution(domain, str(e))
    
    def _sync_resolve(self, domain: str) -> Dict:
        """Synchronous DNS resolution"""
        result = {
            'domain': domain,
            'resolved': False,
            'ip': None,
            'ip_addresses': [],
            'hostname': None,
            'ip_version': None
        }
        
        try:
            # Get primary IP address
            ip = socket.gethostbyname(domain)
            result['resolved'] = True
            result['ip'] = ip
            result['ip_addresses'].append(ip)
            
            # Determine IP version
            if ':' in ip:
                result['ip_version'] = 'IPv6'
            else:
                result['ip_version'] = 'IPv4'
            
            # Try to get all addresses
            try:
                addr_info = socket.getaddrinfo(domain, None)
                for addr in addr_info:
                    ip_addr = addr[4][0]
                    if ip_addr not in result['ip_addresses']:
                        result['ip_addresses'].append(ip_addr)
            except Exception as e:
                logger.debug(f"Error getting all addresses for {domain}: {str(e)}")
            
            # Try reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)
                result['hostname'] = hostname[0] if hostname else None
            except Exception as e:
                logger.debug(f"Reverse DNS lookup failed for {ip}: {str(e)}")
            
            logger.info(f"DNS resolution successful for {domain} -> {ip}")
            
        except socket.gaierror as e:
            logger.warning(f"DNS lookup failed for {domain}: {str(e)}")
            result['error'] = "Domain not found"
            
        except socket.timeout:
            logger.warning(f"DNS timeout for {domain}")
            result['error'] = "DNS timeout"
            
        except Exception as e:
            logger.error(f"Unexpected DNS error for {domain}: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    def _get_failed_resolution(self, domain: str, error: str) -> Dict:
        """Return response for failed DNS resolution"""
        return {
            'domain': domain,
            'resolved': False,
            'ip': None,
            'ip_addresses': [],
            'hostname': None,
            'ip_version': None,
            'error': error
        }
    
    def is_private_ip(self, ip: str) -> bool:
        """Check if IP is in private range"""
        try:
            parts = ip.split('.')
            if len(parts) != 4:
                return False
            
            first_octet = int(parts[0])
            second_octet = int(parts[1])
            
            # Private IP ranges
            if first_octet == 10:
                return True
            if first_octet == 172 and 16 <= second_octet <= 31:
                return True
            if first_octet == 192 and second_octet == 168:
                return True
            if first_octet == 127:  # Loopback
                return True
            
            return False
        except Exception:
            return False
