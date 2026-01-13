"""
WHOIS Service for Domain Age Detection
"""
import asyncio
import socket
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging
import re

logger = logging.getLogger(__name__)


class WhoisService:
    """Service for WHOIS domain information retrieval"""
    
    WHOIS_SERVERS = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.verisign-grs.com',
        'org': 'whois.pir.org',
        'io': 'whois.nic.io',
        'co': 'whois.nic.co',
        'uk': 'whois.nic.uk',
        'de': 'whois.denic.de',
        'default': 'whois.iana.org'
    }
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    async def get_domain_info(self, domain: str) -> Dict:
        """
        Get WHOIS information for domain
        
        Args:
            domain: Domain name to lookup
            
        Returns:
            Dict with domain age and registration info
        """
        try:
            tld = domain.split('.')[-1]
            whois_server = self.WHOIS_SERVERS.get(tld, self.WHOIS_SERVERS['default'])
            
            # Perform WHOIS lookup
            whois_data = await self._query_whois(domain, whois_server)
            
            if whois_data:
                parsed_data = self._parse_whois_data(whois_data, domain)
                return parsed_data
            else:
                # Fallback to simulated data for testing
                return self._generate_fallback_data(domain)
                
        except Exception as e:
            logger.warning(f"WHOIS lookup failed for {domain}: {str(e)}")
            return self._generate_fallback_data(domain)
    
    async def _query_whois(self, domain: str, server: str) -> Optional[str]:
        """Query WHOIS server"""
        try:
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, self._sync_whois_query, domain, server),
                timeout=self.timeout
            )
            return result
        except asyncio.TimeoutError:
            logger.warning(f"WHOIS query timeout for {domain}")
            return None
        except Exception as e:
            logger.error(f"WHOIS query error: {str(e)}")
            return None
    
    def _sync_whois_query(self, domain: str, server: str) -> str:
        """Synchronous WHOIS query"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect((server, 43))
                s.send(f"{domain}\r\n".encode())
                
                response = b""
                while True:
                    data = s.recv(4096)
                    if not data:
                        break
                    response += data
                
                return response.decode('utf-8', errors='ignore')
        except Exception as e:
            logger.error(f"Socket error in WHOIS query: {str(e)}")
            return ""
    
    def _parse_whois_data(self, whois_data: str, domain: str) -> Dict:
        """Parse WHOIS response data"""
        result = {
            'domain': domain,
            'domain_age_days': 0,
            'creation_date': None,
            'expiration_date': None,
            'registrar': None,
            'privacy_protected': False,
            'status': 'unknown'
        }
        
        # Extract creation date
        creation_patterns = [
            r'Creation Date:\s*(.+)',
            r'Created:\s*(.+)',
            r'Registered on:\s*(.+)',
            r'Registration Time:\s*(.+)'
        ]
        
        for pattern in creation_patterns:
            match = re.search(pattern, whois_data, re.IGNORECASE)
            if match:
                date_str = match.group(1).strip()
                creation_date = self._parse_date(date_str)
                if creation_date:
                    result['creation_date'] = creation_date.isoformat()
                    result['domain_age_days'] = (datetime.now() - creation_date).days
                    break
        
        # Extract expiration date
        expiration_patterns = [
            r'Registry Expiry Date:\s*(.+)',
            r'Expiration Date:\s*(.+)',
            r'Expiry Date:\s*(.+)'
        ]
        
        for pattern in expiration_patterns:
            match = re.search(pattern, whois_data, re.IGNORECASE)
            if match:
                date_str = match.group(1).strip()
                expiration_date = self._parse_date(date_str)
                if expiration_date:
                    result['expiration_date'] = expiration_date.isoformat()
                    break
        
        # Extract registrar
        registrar_match = re.search(r'Registrar:\s*(.+)', whois_data, re.IGNORECASE)
        if registrar_match:
            result['registrar'] = registrar_match.group(1).strip()
        
        # Check for privacy protection
        privacy_keywords = ['privacy', 'proxy', 'protected', 'redacted']
        result['privacy_protected'] = any(keyword in whois_data.lower() for keyword in privacy_keywords)
        
        # Domain status
        if 'clientTransferProhibited' in whois_data:
            result['status'] = 'active'
        
        return result
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        date_formats = [
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%d-%b-%Y',
            '%d/%m/%Y',
            '%Y.%m.%d',
        ]
        
        # Clean the date string
        date_str = date_str.split('(')[0].strip()
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    def _generate_fallback_data(self, domain: str) -> Dict:
        """Generate simulated WHOIS data for testing purposes"""
        # Simulate different domain ages based on domain characteristics
        # This is a fallback when real WHOIS is unavailable
        
        # Newer-looking domains (short, unusual TLDs) get younger ages
        tld = domain.split('.')[-1]
        suspicious_tlds = ['xyz', 'top', 'club', 'online', 'site', 'tech']
        
        if tld in suspicious_tlds or len(domain.split('.')[0]) > 20:
            # Simulate young domain (high risk)
            age_days = 15
        elif any(char.isdigit() for char in domain) and len(domain.split('.')[0]) > 12:
            # Domains with numbers and long names (medium risk)
            age_days = 45
        else:
            # Simulate older domain (lower risk)
            age_days = 800
        
        creation_date = datetime.now() - timedelta(days=age_days)
        expiration_date = datetime.now() + timedelta(days=365)
        
        return {
            'domain': domain,
            'domain_age_days': age_days,
            'creation_date': creation_date.isoformat(),
            'expiration_date': expiration_date.isoformat(),
            'registrar': 'Unknown (Simulated)',
            'privacy_protected': False,
            'status': 'simulated',
            'note': 'This is simulated data for demonstration purposes'
        }
