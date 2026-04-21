#!/usr/bin/env python3
"""
Hybrid Intent Classifier for AIMEE
- Fast keyword matching for local execution
- Cloud LLM fallback for complex queries
"""

import re
import logging
from typing import Dict, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class IntentResult:
    intent_type: str
    action: str
    confidence: float
    skill_name: str
    source: str  # 'keyword', 'cloud', or 'unknown'


class HybridIntentClassifier:
    """
    Hybrid intent classifier combining fast keyword matching
    with cloud LLM fallback for complex queries.
    """
    
    # Intent patterns with confidence scores
    PATTERNS = {
        'MOVEMENT': {
            'actions': {
                'move_forward': [
                    r'\b(go\s+forward|move\s+forward|forward|ahead)\b',
                    r'\b(walk\s+forward|drive\s+forward)\b',
                ],
                'move_backward': [
                    r'\b(go\s+back|move\s+back|backward|back\s+up)\b',
                    r'\b(reverse|go\s+backward)\b',
                ],
                'turn_left': [
                    r'\b(turn\s+left|left\s+turn|go\s+left)\b',
                ],
                'turn_right': [
                    r'\b(turn\s+right|right\s+turn|go\s+right)\b',
                ],
                'stop': [
                    r'\b(stop|halt|freeze|stay)\b',
                ],
            },
            'confidence': 0.9,
        },
        'GREETING': {
            'actions': {
                'greet': [
                    r'\b(hello|hi|hey|greetings|howdy)\b',
                ],
                'goodbye': [
                    r'\b(goodbye|bye|see\s+ya|later)\b',
                ],
            },
            'confidence': 0.95,
        },
        'ARM_CONTROL': {
            'actions': {
                'wave': [
                    r'wave',
                    r'wave\s+(at|to|hello)',
                ],
                'point': [
                    r'\b(point|point\s+to|show\s+me)\b',
                ],
                'raise': [
                    r'\b(raise\s+hand|hand\s+up|put\s+hand\s+up)\b',
                ],
            },
            'confidence': 0.85,
        },
        'CAMERA': {
            'actions': {
                'look_at_me': [
                    r'\b(look\s+at\s+me|face\s+me|turn\s+to\s+me)\b',
                ],
                'track_face': [
                    r'\b(track\s+face|follow\s+face|face\s+tracking)\b',
                ],
            },
            'confidence': 0.88,
        },
        'AIMEECLOUD': {
            'actions': {
                'weather': [
                    r'\b(weather|forecast|temperature|rain|sunny)\b',
                ],
                'news': [
                    r'\b(news|headlines|what\s+happened|latest)\b',
                ],
                'story': [
                    r'\b(story|tell\s+me\s+a\s+story|narrative)\b',
                    r'\btell\s+me\s+a\s+story\s+about\b',
                    r'\btell\s+me\s+.*\s+story\b',
                ],
                'general_knowledge': [
                    r'\b(what\s+is|who\s+is|how\s+to|why\s+is|explain|tell\s+me)\b',
                ],
                'math': [
                    r'\b(calculate|compute|what\s+is\s+\d+\s*\+|math)\b',
                ],
            },
            'confidence': 0.75,  # Lower - needs cloud verification
        },
    }
    
    # Minimum confidence for local classification
    LOCAL_CONFIDENCE_THRESHOLD = 0.75
    
    def __init__(self, use_cloud_fallback: bool = True):
        self.use_cloud_fallback = use_cloud_fallback
        self.compiled_patterns = self._compile_patterns()
        logger.info("HybridIntentClassifier initialized")
    
    def _compile_patterns(self) -> Dict:
        """Compile regex patterns for faster matching."""
        compiled = {}
        for intent_type, config in self.PATTERNS.items():
            compiled[intent_type] = {
                'actions': {},
                'confidence': config['confidence']
            }
            for action, patterns in config['actions'].items():
                compiled[intent_type]['actions'][action] = [
                    re.compile(p, re.IGNORECASE) for p in patterns
                ]
        return compiled
    
    def classify(self, text: str) -> IntentResult:
        """
        Classify intent using keyword matching, fallback to cloud.
        
        Args:
            text: User input text
            
        Returns:
            IntentResult with intent type, action, confidence, source
        """
        text_lower = text.lower().strip()
        
        # Try keyword matching first
        keyword_result = self._keyword_classify(text_lower)
        
        if keyword_result.confidence >= self.LOCAL_CONFIDENCE_THRESHOLD:
            logger.debug(f"Keyword match: {keyword_result}")
            return keyword_result
        
        # Fallback to cloud if enabled and low confidence
        if self.use_cloud_fallback:
            logger.info(f"Low confidence ({keyword_result.confidence:.2f}), trying cloud...")
            cloud_result = self._cloud_classify(text)
            if cloud_result.confidence > keyword_result.confidence:
                return cloud_result
        
        # Return best local match even if low confidence
        return keyword_result
    
    def _keyword_classify(self, text: str) -> IntentResult:
        """Classify using keyword patterns."""
        best_match = None
        best_confidence = 0.0
        
        for intent_type, config in self.compiled_patterns.items():
            for action, patterns in config['actions'].items():
                for pattern in patterns:
                    if pattern.search(text):
                        # Calculate confidence based on match quality
                        match = pattern.search(text)
                        match_score = len(match.group()) / len(text)
                        confidence = config['confidence'] * (0.5 + 0.5 * match_score)
                        
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_match = (intent_type, action, confidence)
        
        if best_match:
            return IntentResult(
                intent_type=best_match[0],
                action=best_match[1],
                confidence=best_match[2],
                skill_name=best_match[0].lower(),
                source='keyword'
            )
        
        # No match found
        return IntentResult(
            intent_type='UNKNOWN',
            action='unknown',
            confidence=0.3,
            skill_name='',
            source='unknown'
        )
    
    def _cloud_classify(self, text: str) -> IntentResult:
        """
        Classify using cloud LLM (AimeeCloud).
        This is a placeholder - actual implementation would call cloud API.
        """
        # TODO: Implement actual cloud call
        # For now, return low confidence to indicate fallback needed
        return IntentResult(
            intent_type='AIMEECLOUD',
            action='general_query',
            confidence=0.6,
            skill_name='aimee_cloud',
            source='cloud'
        )


# Singleton instance
_classifier = None

def get_classifier() -> HybridIntentClassifier:
    """Get or create the singleton classifier."""
    global _classifier
    if _classifier is None:
        _classifier = HybridIntentClassifier()
    return _classifier


def classify_intent(text: str) -> Dict:
    """
    Convenience function to classify intent.
    
    Returns dict for easy JSON serialization.
    """
    classifier = get_classifier()
    result = classifier.classify(text)
    
    return {
        'intent_type': result.intent_type,
        'action': result.action,
        'confidence': round(result.confidence, 3),
        'skill_name': result.skill_name,
        'source': result.source,
    }


# Test patterns if run directly
if __name__ == '__main__':
    test_inputs = [
        "move forward",
        "hello there",
        "wave at me",
        "what's the weather in New York",
        "tell me a story about giants",
        "look at me",
        "calculate 15 times 3",
        "random unknown text",
    ]
    
    print("Testing Hybrid Intent Classifier:")
    print("=" * 60)
    
    for text in test_inputs:
        result = classify_intent(text)
        print(f"\nInput: '{text}'")
        print(f"  → {result['intent_type']}.{result['action']}")
        print(f"    Confidence: {result['confidence']}, Source: {result['source']}")
