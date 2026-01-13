"""
FastAPI Backend for AI-Powered Domain Safety Checker
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from typing import List, Dict, Optional
import re
import logging
from datetime import datetime

from services.whois_service import WhoisService
from services.ssl_service import SSLService
from services.dns_service import DNSService
from services.blacklist_service import BlacklistService
from services.content_analyzer import ContentAnalyzer
from services.hosting_service import HostingService
from ai.ml_model import MLModel
from ai.risk_engine import RiskEngine
from utils.validators import validate_domain

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Domain Safety Checker API",
    description="AI-powered domain safety analysis with explainable results",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
whois_service = WhoisService()
ssl_service = SSLService()
dns_service = DNSService()
blacklist_service = BlacklistService()
content_analyzer = ContentAnalyzer()
hosting_service = HostingService()
ml_model = MLModel()
risk_engine = RiskEngine()


class DomainCheckResponse(BaseModel):
    domain: str
    risk_score: float
    verdict: str
    confidence: float
    detailed_reasons: List[str]
    technical_signals: Dict
    analysis_timestamp: str


@app.get("/")
async def root():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "service": "Domain Safety Checker API",
        "version": "1.0.0"
    }


@app.get("/check-domain", response_model=DomainCheckResponse)
async def check_domain(
    domain: str = Query(..., description="Domain name to check (e.g., example.com)")
):
    """
    Analyze a domain for safety and scam indicators
    
    Args:
        domain: Domain name to check
        
    Returns:
        DomainCheckResponse with risk assessment and detailed analysis
    """
    try:
        # Validate domain format
        if not validate_domain(domain):
            raise HTTPException(status_code=400, detail="Invalid domain format")
        
        logger.info(f"Analyzing domain: {domain}")
        
        # Initialize signals dict
        signals = {}
        
        # Step 1: WHOIS Analysis
        logger.info("Step 1/6: WHOIS lookup...")
        whois_data = await whois_service.get_domain_info(domain)
        signals['whois'] = whois_data
        
        # Step 2: SSL/HTTPS Check
        logger.info("Step 2/6: SSL/HTTPS verification...")
        ssl_data = await ssl_service.check_ssl(domain)
        signals['ssl'] = ssl_data
        
        # Step 3: DNS Resolution
        logger.info("Step 3/6: DNS resolution...")
        dns_data = await dns_service.resolve_domain(domain)
        signals['dns'] = dns_data
        
        # Step 4: Blacklist Check
        logger.info("Step 4/6: Blacklist verification...")
        blacklist_data = await blacklist_service.check_domain(domain)
        signals['blacklist'] = blacklist_data
        
        # Step 5: Hosting & ASN
        logger.info("Step 5/6: Hosting analysis...")
        hosting_data = await hosting_service.get_hosting_info(domain, dns_data.get('ip'))
        signals['hosting'] = hosting_data
        
        # Step 6: Content Analysis
        logger.info("Step 6/6: Content analysis...")
        content_data = await content_analyzer.analyze_content(domain)
        signals['content'] = content_data
        
        # Extract features for ML model
        features = extract_features(signals)
        
        # Get ML prediction
        ml_prediction = ml_model.predict(features)
        
        # Get rule-based score
        rule_score = risk_engine.calculate_risk_score(signals)
        
        # Combine scores (weighted average)
        final_risk_score = (ml_prediction['risk_score'] * 0.6) + (rule_score * 0.4)
        
        # Determine verdict
        verdict, confidence = determine_verdict(final_risk_score, signals)
        
        # Generate detailed reasons
        detailed_reasons = risk_engine.generate_explanations(signals, final_risk_score)
        
        response = DomainCheckResponse(
            domain=domain,
            risk_score=round(final_risk_score, 2),
            verdict=verdict,
            confidence=round(confidence, 2),
            detailed_reasons=detailed_reasons,
            technical_signals=signals,
            analysis_timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Analysis complete for {domain}: {verdict} (risk: {final_risk_score})")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing domain {domain}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


def extract_features(signals: Dict) -> Dict:
    """Extract ML model features from signals"""
    whois = signals.get('whois', {})
    ssl = signals.get('ssl', {})
    blacklist = signals.get('blacklist', {})
    hosting = signals.get('hosting', {})
    content = signals.get('content', {})
    
    return {
        'domain_age_days': whois.get('domain_age_days', 0),
        'has_https': 1 if ssl.get('has_ssl', False) else 0,
        'ssl_valid': 1 if ssl.get('ssl_valid', False) else 0,
        'blacklist_count': blacklist.get('blacklist_hits', 0),
        'hosting_reputation_score': hosting.get('reputation_score', 50),
        'content_scam_score': content.get('scam_score', 0.5),
        'dns_resolved': 1 if signals.get('dns', {}).get('resolved', False) else 0,
        'domain_length': len(signals.get('whois', {}).get('domain', '')),
        'has_whois_privacy': 1 if whois.get('privacy_protected', False) else 0,
        'content_risk_keywords': content.get('risk_keyword_count', 0)
    }


def determine_verdict(risk_score: float, signals: Dict) -> tuple:
    """
    Determine verdict based on risk score and signals
    
    Returns:
        (verdict, confidence)
    """
    blacklist_hits = signals.get('blacklist', {}).get('blacklist_hits', 0)
    
    # Critical override: blacklist hits
    if blacklist_hits > 0:
        return "LIKELY SCAM", 0.95
    
    # Risk score based verdict
    if risk_score >= 70:
        return "LIKELY SCAM", 0.85
    elif risk_score >= 40:
        return "SUSPICIOUS", 0.75
    else:
        return "SAFE", 0.80


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
