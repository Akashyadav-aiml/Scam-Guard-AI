"""
Content Analyzer Service for NLP-based Scam Detection
"""
import asyncio
import re
from typing import Dict, List
from urllib.parse import urlparse
import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ContentAnalyzer:
    """Service for analyzing website content for scam indicators"""
    
    # Scam-related keywords categorized by severity
    HIGH_RISK_KEYWORDS = [
        'congratulations you won',
        'claim your prize',
        'act now',
        'limited time offer',
        'verify your account',
        'suspended account',
        'urgent action required',
        'confirm your identity',
        'update payment info',
        'winner',
        'free money',
        'click here immediately',
        'account will be closed',
        'unusual activity',
        'verify identity',
        'tax refund',
        'inheritance',
        'nigerian prince',
        'bitcoin giveaway',
        'double your crypto',
        'guaranteed returns',
        'risk-free investment'
    ]
    
    MEDIUM_RISK_KEYWORDS = [
        'free gift',
        'no credit card required',
        'limited spots',
        'exclusive offer',
        'special promotion',
        'act fast',
        'don\'t miss out',
        'instant approval',
        'lowest price',
        'satisfaction guaranteed',
        'work from home',
        'make money fast',
        'lose weight quickly'
    ]
    
    # Suspicious patterns
    SUSPICIOUS_PATTERNS = [
        r'\b\d+\s*%\s*off\b',  # Percentage discounts
        r'\$\d+,?\d*\s*(?:free|bonus)',  # Money offers
        r'click\s+here\s+(?:now|immediately)',  # Urgency
        r'(?:only|just)\s+\$?\d+',  # Price pressure
    ]
    
    def __init__(self, timeout: int = 10, max_content_size: int = 500000):
        self.timeout = timeout
        self.max_content_size = max_content_size
    
    async def analyze_content(self, domain: str) -> Dict:
        """
        Analyze website content for scam indicators
        
        Args:
            domain: Domain to analyze
            
        Returns:
            Dict with content analysis results
        """
        result = {
            'domain': domain,
            'content_available': False,
            'scam_score': 0.5,  # Neutral
            'risk_keyword_count': 0,
            'high_risk_keywords': [],
            'medium_risk_keywords': [],
            'suspicious_patterns': [],
            'text_length': 0,
            'has_forms': False,
            'external_links_count': 0,
            'analysis': []
        }
        
        try:
            # Fetch website content
            html_content = await self._fetch_content(domain)
            
            if html_content:
                result['content_available'] = True
                
                # Parse HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Extract text
                text = self._extract_text(soup)
                result['text_length'] = len(text)
                
                # Analyze for scam keywords
                keyword_analysis = self._analyze_keywords(text)
                result.update(keyword_analysis)
                
                # Check for suspicious patterns
                pattern_matches = self._check_patterns(text)
                result['suspicious_patterns'] = pattern_matches
                
                # Check for forms (phishing indicator)
                forms = soup.find_all('form')
                result['has_forms'] = len(forms) > 0
                
                # Count external links
                links = soup.find_all('a', href=True)
                external_links = [link for link in links if self._is_external_link(link['href'], domain)]
                result['external_links_count'] = len(external_links)
                
                # Calculate scam score
                result['scam_score'] = self._calculate_content_score(result)
                
                # Generate analysis
                result['analysis'] = self._generate_content_analysis(result)
                
                logger.info(f"Content analysis for {domain}: score={result['scam_score']:.2f}")
            else:
                result['analysis'].append('Website content could not be retrieved')
                
        except Exception as e:
            logger.error(f"Content analysis error for {domain}: {str(e)}")
            result['error'] = str(e)
        
        return result
    
    async def _fetch_content(self, domain: str) -> str:
        """Fetch website HTML content"""
        urls_to_try = [
            f"https://{domain}",
            f"http://{domain}",
        ]
        
        for url in urls_to_try:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        url,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                        allow_redirects=True,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    ) as response:
                        if response.status == 200:
                            content = await response.text()
                            # Limit content size
                            if len(content) > self.max_content_size:
                                content = content[:self.max_content_size]
                            return content
            except Exception as e:
                logger.debug(f"Failed to fetch {url}: {str(e)}")
                continue
        
        return ""
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract visible text from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "meta", "link"]):
            script.decompose()
        
        # Get text
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.lower()
    
    def _analyze_keywords(self, text: str) -> Dict:
        """Analyze text for scam keywords"""
        high_risk_found = []
        medium_risk_found = []
        
        # Check high risk keywords
        for keyword in self.HIGH_RISK_KEYWORDS:
            if keyword.lower() in text:
                high_risk_found.append(keyword)
        
        # Check medium risk keywords
        for keyword in self.MEDIUM_RISK_KEYWORDS:
            if keyword.lower() in text:
                medium_risk_found.append(keyword)
        
        return {
            'high_risk_keywords': high_risk_found,
            'medium_risk_keywords': medium_risk_found,
            'risk_keyword_count': len(high_risk_found) + len(medium_risk_found)
        }
    
    def _check_patterns(self, text: str) -> List[str]:
        """Check for suspicious patterns"""
        matches = []
        
        for pattern in self.SUSPICIOUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(pattern)
        
        return matches
    
    def _is_external_link(self, href: str, domain: str) -> bool:
        """Check if link is external"""
        try:
            parsed = urlparse(href)
            if parsed.netloc and domain not in parsed.netloc:
                return True
        except Exception:
            pass
        return False
    
    def _calculate_content_score(self, result: Dict) -> float:
        """Calculate content-based scam score (0-1)"""
        score = 0.0
        
        # High risk keywords (0.15 per keyword, max 0.6)
        high_risk_count = len(result['high_risk_keywords'])
        score += min(high_risk_count * 0.15, 0.6)
        
        # Medium risk keywords (0.05 per keyword, max 0.2)
        medium_risk_count = len(result['medium_risk_keywords'])
        score += min(medium_risk_count * 0.05, 0.2)
        
        # Suspicious patterns (0.1 per pattern, max 0.3)
        pattern_count = len(result['suspicious_patterns'])
        score += min(pattern_count * 0.1, 0.3)
        
        # Forms present (potential phishing)
        if result['has_forms'] and result['risk_keyword_count'] > 0:
            score += 0.2
        
        # Very short content (possible parking page)
        if result['text_length'] < 200 and result['text_length'] > 0:
            score += 0.1
        
        # Excessive external links
        if result['external_links_count'] > 50:
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_content_analysis(self, result: Dict) -> List[str]:
        """Generate human-readable analysis"""
        analysis = []
        
        if result['high_risk_keywords']:
            analysis.append(f"Found {len(result['high_risk_keywords'])} high-risk scam keywords")
        
        if result['medium_risk_keywords']:
            analysis.append(f"Found {len(result['medium_risk_keywords'])} medium-risk marketing keywords")
        
        if result['suspicious_patterns']:
            analysis.append(f"Detected {len(result['suspicious_patterns'])} suspicious text patterns")
        
        if result['has_forms']:
            analysis.append("Website contains forms (possible credential harvesting)")
        
        if result['text_length'] < 200 and result['text_length'] > 0:
            analysis.append("Very little content (possible parking page)")
        
        if result['external_links_count'] > 50:
            analysis.append(f"Excessive external links ({result['external_links_count']})")
        
        if not analysis:
            analysis.append("No obvious content-based risk indicators detected")
        
        return analysis
