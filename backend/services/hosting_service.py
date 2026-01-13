"""
Hosting Service for Provider and ASN Lookup
"""
import asyncio
import socket
from typing import Dict, Optional
import logging
import ipaddress

logger = logging.getLogger(__name__)


class HostingService:
    """Service for hosting provider and ASN information"""
    
    # Known cloud/hosting providers and their reputation scores
    HOSTING_REPUTATION = {
        'amazon': {'score': 70, 'name': 'Amazon Web Services'},
        'google': {'score': 75, 'name': 'Google Cloud'},
        'microsoft': {'score': 75, 'name': 'Microsoft Azure'},
        'cloudflare': {'score': 80, 'name': 'Cloudflare'},
        'digitalocean': {'score': 65, 'name': 'DigitalOcean'},
        'ovh': {'score': 60, 'name': 'OVH'},
        'hetzner': {'score': 65, 'name': 'Hetzner'},
        'linode': {'score': 70, 'name': 'Linode'},
        'vultr': {'score': 65, 'name': 'Vultr'},
        'namecheap': {'score': 55, 'name': 'Namecheap'},
        'godaddy': {'score': 55, 'name': 'GoDaddy'},
    }
    
    # Known bulletproof hosting (low reputation)
    BULLETPROOF_INDICATORS = [
        'offshore',
        'privacy',
        'anonymous',
        'bulletproof',
    ]
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
    
    async def get_hosting_info(self, domain: str, ip: Optional[str] = None) -> Dict:
        """
        Get hosting provider information
        
        Args:
            domain: Domain name
            ip: IP address (optional)
            
        Returns:
            Dict with hosting information
        """
        result = {
            'domain': domain,
            'ip': ip,
            'hosting_provider': 'Unknown',
            'reputation_score': 50,  # Neutral
            'asn': None,
            'country': None,
            'is_cloud': False,
            'risk_factors': []
        }
        
        try:
            if ip:
                # Try to determine hosting provider from reverse DNS
                hostname = await self._get_reverse_dns(ip)
                if hostname:
                    result['hosting_provider'] = self._identify_provider(hostname)
                    
                    # Calculate reputation score
                    provider_info = self._get_provider_reputation(result['hosting_provider'])
                    if provider_info:
                        result['reputation_score'] = provider_info['score']
                        result['is_cloud'] = True
                
                # Check if IP is in suspicious ranges
                if self._is_suspicious_ip(ip):
                    result['risk_factors'].append('IP in suspicious range')
                    result['reputation_score'] -= 15
                
                # Simulate ASN lookup (in production, use actual ASN database)
                result['asn'] = self._simulate_asn_lookup(ip)
                result['country'] = self._simulate_geo_lookup(ip)
            
            # Check for bulletproof hosting indicators
            if any(indicator in result['hosting_provider'].lower() for indicator in self.BULLETPROOF_INDICATORS):
                result['risk_factors'].append('Possible bulletproof hosting')
                result['reputation_score'] -= 25
            
            # Adjust score boundaries
            result['reputation_score'] = max(0, min(100, result['reputation_score']))
            
            logger.info(f"Hosting info for {domain}: {result['hosting_provider']} (score: {result['reputation_score']})")
            
        except Exception as e:
            logger.error(f"Error getting hosting info for {domain}: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    async def _get_reverse_dns(self, ip: str) -> Optional[str]:
        """Get reverse DNS for IP"""
        try:
            loop = asyncio.get_event_loop()
            hostname = await asyncio.wait_for(
                loop.run_in_executor(None, socket.gethostbyaddr, ip),
                timeout=self.timeout
            )
            return hostname[0] if hostname else None
        except Exception as e:
            logger.debug(f"Reverse DNS lookup failed for {ip}: {str(e)}")
            return None
    
    def _identify_provider(self, hostname: str) -> str:
        """Identify hosting provider from hostname"""
        hostname_lower = hostname.lower()
        
        for provider_key, provider_info in self.HOSTING_REPUTATION.items():
            if provider_key in hostname_lower:
                return provider_info['name']
        
        # Extract domain from hostname
        parts = hostname.split('.')
        if len(parts) >= 2:
            return f"{parts[-2]}.{parts[-1]}"
        
        return hostname
    
    def _get_provider_reputation(self, provider: str) -> Optional[Dict]:
        """Get reputation information for provider"""
        provider_lower = provider.lower()
        
        for provider_key, provider_info in self.HOSTING_REPUTATION.items():
            if provider_key in provider_lower:
                return provider_info
        
        return None
    
    def _is_suspicious_ip(self, ip: str) -> bool:
        """Check if IP is in suspicious ranges"""
        try:
            ip_obj = ipaddress.ip_address(ip)
            
            # Check for private IPs
            if ip_obj.is_private:
                return True
            
            # Check for loopback
            if ip_obj.is_loopback:
                return True
            
            # Check for reserved
            if ip_obj.is_reserved:
                return True
            
            return False
        except Exception:
            return False
    
    def _simulate_asn_lookup(self, ip: str) -> Optional[str]:
        """Simulate ASN lookup (in production, use real ASN database)"""
        try:
            first_octet = int(ip.split('.')[0])
            
            # Simulate based on IP ranges
            if first_octet in range(3, 8):
                return "AS7018 (AT&T)"
            elif first_octet in range(8, 16):
                return "AS15169 (Google)"
            elif first_octet in range(16, 32):
                return "AS16509 (Amazon)"
            elif first_octet in range(52, 54):
                return "AS8075 (Microsoft)"
            else:
                return f"AS{first_octet * 1000} (Unknown)"
        except Exception:
            return None
    
    def _simulate_geo_lookup(self, ip: str) -> Optional[str]:
        """Simulate geographical lookup"""
        try:
            # Simulate based on IP ranges (very simplified)
            first_octet = int(ip.split('.')[0])
            
            if first_octet < 50:
                return "United States"
            elif first_octet < 100:
                return "Europe"
            elif first_octet < 150:
                return "Asia"
            else:
                return "Other"
        except Exception:
            return "Unknown"
