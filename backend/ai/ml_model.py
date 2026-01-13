"""
Machine Learning Model for Scam Detection
"""
import numpy as np
from typing import Dict
import logging
import pickle
import os

logger = logging.getLogger(__name__)


class MLModel:
    """
    Machine Learning model for domain scam prediction
    Uses RandomForest-like decision logic (simulated for demo)
    In production, replace with actual trained model
    """
    
    def __init__(self):
        self.model_loaded = False
        self.feature_names = [
            'domain_age_days',
            'has_https',
            'ssl_valid',
            'blacklist_count',
            'hosting_reputation_score',
            'content_scam_score',
            'dns_resolved',
            'domain_length',
            'has_whois_privacy',
            'content_risk_keywords'
        ]
        
        # Feature weights (simulated model parameters)
        self.weights = {
            'domain_age_days': -0.05,  # Negative: older is better
            'has_https': -0.15,
            'ssl_valid': -0.10,
            'blacklist_count': 0.30,
            'hosting_reputation_score': -0.02,
            'content_scam_score': 0.40,
            'dns_resolved': -0.10,
            'domain_length': 0.01,
            'has_whois_privacy': 0.05,
            'content_risk_keywords': 0.05
        }
    
    def predict(self, features: Dict) -> Dict:
        """
        Predict scam probability
        
        Args:
            features: Dict of feature values
            
        Returns:
            Dict with prediction results
        """
        try:
            # Normalize features
            normalized_features = self._normalize_features(features)
            
            # Calculate weighted score
            score = self._calculate_score(normalized_features)
            
            # Apply sigmoid-like transformation
            probability = self._sigmoid(score)
            
            # Convert to 0-100 scale
            risk_score = probability * 100
            
            # Feature importance for explainability
            feature_importance = self._calculate_feature_importance(normalized_features)
            
            result = {
                'risk_score': risk_score,
                'probability': probability,
                'confidence': self._calculate_confidence(normalized_features),
                'feature_importance': feature_importance,
                'model_version': '1.0-simulated'
            }
            
            logger.info(f"ML prediction: risk_score={risk_score:.2f}, confidence={result['confidence']:.2f}")
            
            return result
            
        except Exception as e:
            logger.error(f"ML prediction error: {str(e)}")
            return {
                'risk_score': 50.0,
                'probability': 0.5,
                'confidence': 0.5,
                'feature_importance': {},
                'error': str(e)
            }
    
    def _normalize_features(self, features: Dict) -> Dict:
        """Normalize feature values to 0-1 range"""
        normalized = {}
        
        # Domain age (normalize to days, max 365*3 years considered "old")
        domain_age = features.get('domain_age_days', 0)
        normalized['domain_age_days'] = min(domain_age / (365 * 3), 1.0)
        
        # Binary features
        normalized['has_https'] = features.get('has_https', 0)
        normalized['ssl_valid'] = features.get('ssl_valid', 0)
        normalized['dns_resolved'] = features.get('dns_resolved', 0)
        normalized['has_whois_privacy'] = features.get('has_whois_privacy', 0)
        
        # Blacklist count (normalize, max 5 considered very bad)
        blacklist_count = features.get('blacklist_count', 0)
        normalized['blacklist_count'] = min(blacklist_count / 5.0, 1.0)
        
        # Hosting reputation (already 0-100, normalize to 0-1)
        hosting_rep = features.get('hosting_reputation_score', 50)
        normalized['hosting_reputation_score'] = hosting_rep / 100.0
        
        # Content scam score (already 0-1)
        normalized['content_scam_score'] = features.get('content_scam_score', 0.5)
        
        # Domain length (normalize, max 50 chars)
        domain_length = features.get('domain_length', 0)
        normalized['domain_length'] = min(domain_length / 50.0, 1.0)
        
        # Content risk keywords (normalize, max 10)
        keyword_count = features.get('content_risk_keywords', 0)
        normalized['content_risk_keywords'] = min(keyword_count / 10.0, 1.0)
        
        return normalized
    
    def _calculate_score(self, normalized_features: Dict) -> float:
        """Calculate weighted score from normalized features"""
        score = 0.0
        
        for feature_name, weight in self.weights.items():
            feature_value = normalized_features.get(feature_name, 0.5)
            score += feature_value * weight
        
        return score
    
    def _sigmoid(self, x: float) -> float:
        """Apply sigmoid function for probability"""
        try:
            # Shift and scale for better range
            scaled = x * 5  # Amplify the effect
            return 1 / (1 + np.exp(-scaled))
        except Exception:
            return 0.5
    
    def _calculate_confidence(self, normalized_features: Dict) -> float:
        """
        Calculate confidence in prediction
        Higher confidence when we have more information
        """
        # Count how many features we have good data for
        features_with_data = 0
        total_features = len(self.feature_names)
        
        # Check if critical features are available
        if normalized_features.get('dns_resolved', 0) == 1:
            features_with_data += 1
        
        if normalized_features.get('domain_age_days', 0) > 0:
            features_with_data += 1
        
        if normalized_features.get('has_https', 0) in [0, 1]:
            features_with_data += 1
        
        if normalized_features.get('content_scam_score', 0.5) != 0.5:
            features_with_data += 1
        
        # Base confidence on data availability
        base_confidence = features_with_data / 4.0
        
        # Increase confidence if we have strong signals
        blacklist_hits = normalized_features.get('blacklist_count', 0)
        if blacklist_hits > 0:
            base_confidence = max(base_confidence, 0.9)
        
        content_score = normalized_features.get('content_scam_score', 0.5)
        if content_score > 0.7 or content_score < 0.3:
            base_confidence = max(base_confidence, 0.8)
        
        return min(base_confidence, 0.95)
    
    def _calculate_feature_importance(self, normalized_features: Dict) -> Dict:
        """
        Calculate feature importance for explainability
        Shows which features contributed most to the prediction
        """
        importance = {}
        
        for feature_name, weight in self.weights.items():
            feature_value = normalized_features.get(feature_name, 0.5)
            contribution = abs(feature_value * weight)
            importance[feature_name] = round(contribution, 3)
        
        # Sort by importance
        sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_importance
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """
        Train the model (placeholder for actual training)
        In production, implement actual RandomForest/XGBoost training
        """
        logger.info("Training model...")
        # This is where you would train an actual model
        # For now, we use simulated logic
        self.model_loaded = True
        logger.info("Model training complete (simulated)")
    
    def save_model(self, path: str):
        """Save model to file"""
        try:
            with open(path, 'wb') as f:
                pickle.dump(self.weights, f)
            logger.info(f"Model saved to {path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self, path: str):
        """Load model from file"""
        try:
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    self.weights = pickle.load(f)
                self.model_loaded = True
                logger.info(f"Model loaded from {path}")
            else:
                logger.warning(f"Model file not found: {path}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
