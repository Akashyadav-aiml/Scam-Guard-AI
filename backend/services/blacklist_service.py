"""
Blacklist Service for Domain Reputation Checking
"""
import asyncio
import socket
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class BlacklistService:
    """Service for checking domain against blacklists"""
    
    # DNS-based blacklists (DBL)
    DOMAIN_BLACKLISTS = [
        'dbl.spamhaus.org',
        'multi.uribl.com',
        'rhsbl.sorbs.net',
        'nomail.rhsbl.sorbs.net',
    ]
    
    # IP-based blacklists (DNSBL)
    IP_BLACKLISTS = [
        'zen.spamhaus.org',
        'bl.spamcop.net',
        'dnsbl.sorbs.net',
        'cbl.abuseat.org',
    ]
    
    # Known scam patterns
    SCAM_KEYWORDS = [
        'verify-account',
        'confirm-identity',
        'suspended-account',
        'urgent-action',
        'claim-prize',
        'free-money',
        'crypto-giveaway',
        'bitcoin-generator'
    ]
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
    
    async def check_domain(self, domain: str, ip: str = None) -> Dict:
        """
        Check domain against various blacklists
        
        Args:
            domain: Domain to check
            ip: Optional IP address
            
        Returns:
            Dict with blacklist information
        """
        result = {
            'domain': domain,
            'blacklist_hits': 0,
            'blacklists': [],
            'scam_pattern_detected': False,
            'risk_indicators': []
        }
        
        try:
            # Check domain-based blacklists
            domain_hits = await self._check_domain_blacklists(domain)
            result['blacklists'].extend(domain_hits)
            
            # Check IP-based blacklists if IP provided
            if ip:
                ip_hits = await self._check_ip_blacklists(ip)
                result['blacklists'].extend(ip_hits)
            
            result['blacklist_hits'] = len(result['blacklists'])
            
            # Check for scam patterns in domain name
            if self._check_scam_patterns(domain):
                result['scam_pattern_detected'] = True
                result['risk_indicators'].append('Domain name contains scam-related keywords')
            
            # Check for suspicious TLDs
            suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.club']
            if any(domain.endswith(tld) for tld in suspicious_tlds):
                result['risk_indicators'].append('Domain uses commonly abused TLD')
            
            # Check for lookalike domains (homograph attack indicators)
            if self._has_unicode_chars(domain):
                result['risk_indicators'].append('Domain contains non-ASCII characters (possible homograph attack)')
            
            logger.info(f"Blacklist check for {domain}: {result['blacklist_hits']} hits")
            
        except Exception as e:
            logger.error(f"Blacklist check error for {domain}: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    async def _check_domain_blacklists(self, domain: str) -> List[Dict]:
        """Check domain against DNS-based blacklists"""
        hits = []
        
        for blacklist in self.DOMAIN_BLACKLISTS:
            try:
                is_listed = await self._query_dbl(domain, blacklist)
                if is_listed:
                    hits.append({
                        'blacklist': blacklist,
                        'type': 'domain',
                        'listed': True
                    })
            except Exception as e:
                logger.debug(f"Error checking {blacklist} for {domain}: {str(e)}")
        
        return hits
    
    async def _check_ip_blacklists(self, ip: str) -> List[Dict]:
        """Check IP against DNS-based blacklists"""
        hits = []
        
        # Reverse IP for DNSBL lookup
        reversed_ip = '.'.join(reversed(ip.split('.')))
        
        for blacklist in self.IP_BLACKLISTS:
            try:
                is_listed = await self._query_dnsbl(reversed_ip, blacklist)
                if is_listed:
                    hits.append({
                        'blacklist': blacklist,
                        'type': 'ip',
                        'listed': True,
                        'ip': ip
                    })
            except Exception as e:
                logger.debug(f"Error checking {blacklist} for {ip}: {str(e)}")
        
        return hits
    
    async def _query_dbl(self, domain: str, blacklist: str) -> bool:
        """Query domain blacklist"""
        query = f"{domain}.{blacklist}"
        return await self._dns_lookup(query)
    
    async def _query_dnsbl(self, reversed_ip: str, blacklist: str) -> bool:
        """Query IP blacklist"""
        query = f"{reversed_ip}.{blacklist}"
        return await self._dns_lookup(query)
    
    async def _dns_lookup(self, query: str) -> bool:
        """Perform DNS lookup to check blacklist"""
        try:
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(None, socket.gethostbyname, query),
                timeout=self.timeout
            )
            # If we get a result (typically 127.0.0.2 or similar), domain is listed
            return result is not None
        except socket.gaierror:
            # NXDOMAIN means not listed
            return False
        except asyncio.TimeoutError:
            logger.debug(f"Timeout querying {query}")
            return False
        except Exception as e:
            logger.debug(f"Error querying {query}: {str(e)}")
            return False
    
    def _check_scam_patterns(self, domain: str) -> bool:
        """Check if domain contains scam-related patterns"""
        domain_lower = domain.lower()
        
        # Check for known scam keywords
        for keyword in self.SCAM_KEYWORDS:
            if keyword in domain_lower:
                return True
        
        # Check for excessive numbers (common in scam domains)
        digit_count = sum(c.isdigit() for c in domain)
        if digit_count > 5:
            return True
        
        # Check for excessive hyphens
        hyphen_count = domain.count('-')
        if hyphen_count > 3:
            return True
        
        return False
    
    def _has_unicode_chars(self, domain: str) -> bool:
        """Check if domain contains non-ASCII characters"""
        try:
            domain.encode('ascii')
            return False
        except UnicodeEncodeError:
            return True
