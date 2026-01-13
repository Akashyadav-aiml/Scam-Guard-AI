"""
Rule-Based Risk Engine for Domain Safety Assessment
"""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class RiskEngine:
    """
    Rule-based risk assessment engine
    Combines multiple signals to calculate risk score and generate explanations
    """
    
    def __init__(self):
        self.max_score = 100
        
        # Risk point allocation
        self.risk_rules = {
            'domain_age': {
                'critical': (0, 7, 25),      # 0-7 days: 25 points
                'high': (8, 30, 20),          # 8-30 days: 20 points
                'medium': (31, 90, 10),       # 31-90 days: 10 points
                'low': (91, 180, 5),          # 91-180 days: 5 points
            },
            'ssl': {
                'no_ssl': 15,
                'invalid_ssl': 10,
                'expiring_soon': 5,
            },
            'blacklist': {
                'per_hit': 30,  # 30 points per blacklist
            },
            'hosting': {
                'bulletproof': 20,
                'low_reputation': 10,
            },
            'content': {
                'high_risk_keywords': 15,
                'medium_risk_keywords': 5,
                'phishing_forms': 10,
            },
            'dns': {
                'no_resolution': 20,
            },
            'patterns': {
                'suspicious_tld': 10,
                'long_domain': 5,
                'many_numbers': 5,
                'homograph': 15,
            }
        }
    
    def calculate_risk_score(self, signals: Dict) -> float:
        """
        Calculate rule-based risk score (0-100)
        
        Args:
            signals: Dict containing all analysis signals
            
        Returns:
            Risk score (0-100)
        """
        total_score = 0
        
        try:
            # Domain age analysis
            whois = signals.get('whois', {})
            domain_age_days = whois.get('domain_age_days', 0)
            age_score = self._calculate_age_score(domain_age_days)
            total_score += age_score
            
            # SSL analysis
            ssl = signals.get('ssl', {})
            ssl_score = self._calculate_ssl_score(ssl)
            total_score += ssl_score
            
            # Blacklist analysis
            blacklist = signals.get('blacklist', {})
            blacklist_score = self._calculate_blacklist_score(blacklist)
            total_score += blacklist_score
            
            # Hosting analysis
            hosting = signals.get('hosting', {})
            hosting_score = self._calculate_hosting_score(hosting)
            total_score += hosting_score
            
            # Content analysis
            content = signals.get('content', {})
            content_score = self._calculate_content_score(content)
            total_score += content_score
            
            # DNS analysis
            dns = signals.get('dns', {})
            dns_score = self._calculate_dns_score(dns)
            total_score += dns_score
            
            # Pattern analysis
            pattern_score = self._calculate_pattern_score(signals)
            total_score += pattern_score
            
            # Cap at maximum
            final_score = min(total_score, self.max_score)
            
            logger.info(f"Rule-based risk score: {final_score}")
            return final_score
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            return 50.0  # Return neutral score on error
    
    def generate_explanations(self, signals: Dict, risk_score: float) -> List[str]:
        """
        Generate human-readable explanations for the risk score
        
        Args:
            signals: Dict containing all analysis signals
            risk_score: Calculated risk score
            
        Returns:
            List of explanation strings
        """
        explanations = []
        
        try:
            # Domain age
            whois = signals.get('whois', {})
            domain_age_days = whois.get('domain_age_days', 0)
            if domain_age_days < 7:
                explanations.append("🚨 CRITICAL: Domain is extremely new (less than 1 week old)")
            elif domain_age_days < 30:
                explanations.append("⚠️ HIGH RISK: Domain is very new (less than 1 month old)")
            elif domain_age_days < 90:
                explanations.append("⚠️ MEDIUM: Domain is relatively new (less than 3 months old)")
            elif domain_age_days > 365:
                explanations.append("✅ POSITIVE: Domain is well-established (over 1 year old)")
            
            # SSL
            ssl = signals.get('ssl', {})
            if not ssl.get('has_ssl', False):
                explanations.append("🚨 CRITICAL: No HTTPS/SSL certificate detected")
            elif not ssl.get('ssl_valid', False):
                explanations.append("⚠️ HIGH RISK: SSL certificate is invalid or expired")
            else:
                days_until_expiry = ssl.get('days_until_expiry')
                if days_until_expiry and days_until_expiry < 30:
                    explanations.append("⚠️ WARNING: SSL certificate expiring soon")
                else:
                    explanations.append("✅ POSITIVE: Valid SSL certificate detected")
            
            # Blacklist
            blacklist = signals.get('blacklist', {})
            blacklist_hits = blacklist.get('blacklist_hits', 0)
            if blacklist_hits > 0:
                explanations.append(f"🚨 CRITICAL: Found on {blacklist_hits} security blacklist(s)")
                if blacklist.get('blacklists'):
                    bl_names = [bl['blacklist'] for bl in blacklist.get('blacklists', [])]
                    explanations.append(f"   Blacklists: {', '.join(bl_names[:3])}")
            
            # Scam patterns
            if blacklist.get('scam_pattern_detected', False):
                explanations.append("⚠️ HIGH RISK: Domain name contains scam-related keywords")
            
            # Risk indicators
            risk_indicators = blacklist.get('risk_indicators', [])
            for indicator in risk_indicators:
                explanations.append(f"⚠️ WARNING: {indicator}")
            
            # Hosting
            hosting = signals.get('hosting', {})
            rep_score = hosting.get('reputation_score', 50)
            if rep_score < 40:
                explanations.append("⚠️ MEDIUM: Hosted on service with low reputation score")
            elif rep_score > 70:
                explanations.append(f"✅ POSITIVE: Hosted by reputable provider ({hosting.get('hosting_provider', 'Unknown')})")
            
            # Content
            content = signals.get('content', {})
            if content.get('content_available', False):
                high_risk = content.get('high_risk_keywords', [])
                if high_risk:
                    explanations.append(f"🚨 HIGH RISK: Found {len(high_risk)} high-risk scam keywords in content")
                    if high_risk[:2]:
                        explanations.append(f"   Examples: '{high_risk[0]}', '{high_risk[1] if len(high_risk) > 1 else ''}'")
                
                medium_risk = content.get('medium_risk_keywords', [])
                if medium_risk:
                    explanations.append(f"⚠️ MEDIUM: Found {len(medium_risk)} marketing-related keywords")
                
                if content.get('has_forms', False) and (high_risk or medium_risk):
                    explanations.append("⚠️ WARNING: Site contains forms and suspicious keywords (possible phishing)")
            
            # DNS
            dns = signals.get('dns', {})
            if not dns.get('resolved', False):
                explanations.append("🚨 CRITICAL: Domain does not resolve to an IP address")
            
            # Overall verdict explanation
            if risk_score >= 70:
                explanations.insert(0, "🚨 VERDICT: This domain shows multiple indicators of being a SCAM")
            elif risk_score >= 40:
                explanations.insert(0, "⚠️ VERDICT: This domain is SUSPICIOUS - exercise caution")
            else:
                explanations.insert(0, "✅ VERDICT: This domain appears relatively SAFE based on available data")
            
            # Add disclaimer
            explanations.append("")
            explanations.append("ℹ️ Note: This analysis is based on automated checks. Always exercise caution online.")
            
        except Exception as e:
            logger.error(f"Error generating explanations: {str(e)}")
            explanations.append("Error generating detailed explanations")
        
        return explanations
    
    def _calculate_age_score(self, domain_age_days: int) -> float:
        """Calculate risk score based on domain age"""
        for level, (min_days, max_days, points) in self.risk_rules['domain_age'].items():
            if min_days <= domain_age_days <= max_days:
                return points
        return 0  # Very old domains (>180 days)
    
    def _calculate_ssl_score(self, ssl: Dict) -> float:
        """Calculate risk score based on SSL status"""
        score = 0
        
        if not ssl.get('has_ssl', False):
            score += self.risk_rules['ssl']['no_ssl']
        elif not ssl.get('ssl_valid', False):
            score += self.risk_rules['ssl']['invalid_ssl']
        else:
            days_until_expiry = ssl.get('days_until_expiry')
            if days_until_expiry and days_until_expiry < 30:
                score += self.risk_rules['ssl']['expiring_soon']
        
        return score
    
    def _calculate_blacklist_score(self, blacklist: Dict) -> float:
        """Calculate risk score based on blacklist hits"""
        hits = blacklist.get('blacklist_hits', 0)
        return min(hits * self.risk_rules['blacklist']['per_hit'], 50)  # Cap at 50
    
    def _calculate_hosting_score(self, hosting: Dict) -> float:
        """Calculate risk score based on hosting provider"""
        score = 0
        
        rep_score = hosting.get('reputation_score', 50)
        if rep_score < 30:
            score += self.risk_rules['hosting']['bulletproof']
        elif rep_score < 50:
            score += self.risk_rules['hosting']['low_reputation']
        
        return score
    
    def _calculate_content_score(self, content: Dict) -> float:
        """Calculate risk score based on content analysis"""
        score = 0
        
        high_risk = len(content.get('high_risk_keywords', []))
        if high_risk > 0:
            score += self.risk_rules['content']['high_risk_keywords']
        
        medium_risk = len(content.get('medium_risk_keywords', []))
        if medium_risk > 2:
            score += self.risk_rules['content']['medium_risk_keywords']
        
        if content.get('has_forms', False) and (high_risk > 0 or medium_risk > 0):
            score += self.risk_rules['content']['phishing_forms']
        
        return score
    
    def _calculate_dns_score(self, dns: Dict) -> float:
        """Calculate risk score based on DNS resolution"""
        if not dns.get('resolved', False):
            return self.risk_rules['dns']['no_resolution']
        return 0
    
    def _calculate_pattern_score(self, signals: Dict) -> float:
        """Calculate risk score based on various patterns"""
        score = 0
        
        blacklist = signals.get('blacklist', {})
        risk_indicators = blacklist.get('risk_indicators', [])
        
        for indicator in risk_indicators:
            if 'TLD' in indicator:
                score += self.risk_rules['patterns']['suspicious_tld']
            elif 'homograph' in indicator:
                score += self.risk_rules['patterns']['homograph']
        
        # Check domain characteristics
        whois = signals.get('whois', {})
        domain = whois.get('domain', '')
        
        if len(domain) > 30:
            score += self.risk_rules['patterns']['long_domain']
        
        digit_count = sum(c.isdigit() for c in domain)
        if digit_count > 5:
            score += self.risk_rules['patterns']['many_numbers']
        
        return score
