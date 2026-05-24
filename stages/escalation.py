"""
Stage 3: Escalation Detection
Detects when conversation should be handed off to a human agent.
"""

import json
import re
from typing import Dict, Any, List
from utils.openai_client import OpenAIClient
from prompts.system_prompts import get_system_prompt, ESCALATION_PROMPT


class EscalationDetector:
    """Detects escalation triggers and manages handoff to human agents."""
    
    # Sentiment keywords for escalation
    NEGATIVE_KEYWORDS = [
        "angry", "frustrated", "ridiculous", "terrible", "awful",
        "horrible", "worst", "useless", "disappointed", "upset",
        "complaint", "complain", "unacceptable", "disgusted"
    ]
    
    EXPLICIT_ESCALATION_PHRASES = [
        "speak to human", "talk to person", "real person",
        "human agent", "manager", "supervisor", "someone else"
    ]
    
    def __init__(self, sop_data: Dict[str, Any], openai_client: OpenAIClient):
        """
        Initialize escalation detector.
        
        Args:
            sop_data: SOP data dictionary
            openai_client: OpenAI client instance
        """
        self.sop_data = sop_data
        self.client = openai_client
        self.system_prompt = get_system_prompt(json.dumps(sop_data, indent=2))
        self.unanswered_questions = 0
    
    def check_escalation(
        self,
        message: str,
        conversation_history: list,
        last_confidence: float = 1.0
    ) -> Dict[str, Any]:
        """
        Check if escalation is needed based on multiple triggers.
        
        Args:
            message: Current customer message
            conversation_history: Previous conversation messages
            last_confidence: Confidence score from last response
        
        Returns:
            Dict with escalation decision and reason
        """
        escalation_reasons = []
        
        # Check 1: Low confidence threshold
        if last_confidence < 0.7:
            escalation_reasons.append(f"Low confidence score: {last_confidence:.2f}")
        
        # Check 2: Negative sentiment
        if self._detect_negative_sentiment(message):
            escalation_reasons.append("Negative sentiment detected")
        
        # Check 3: Explicit escalation request
        if self._detect_explicit_request(message):
            escalation_reasons.append("Customer explicitly requested human agent")
        
        # Check 4: Multiple unanswered questions
        if self._check_unanswered_questions(conversation_history):
            escalation_reasons.append("Multiple questions remain unanswered")
        
        # Check 5: Out of scope (use AI to detect)
        out_of_scope = self._check_out_of_scope(message, conversation_history)
        if out_of_scope:
            escalation_reasons.append("Question is outside SOP scope")
        
        # Determine if escalation is needed
        escalation_needed = len(escalation_reasons) > 0
        
        return {
            "escalation_needed": escalation_needed,
            "escalation_reasons": escalation_reasons,
            "primary_reason": escalation_reasons[0] if escalation_reasons else None,
            "confidence": 1.0 if escalation_needed else 0.0
        }
    
    def _detect_negative_sentiment(self, message: str) -> bool:
        """
        Detect negative sentiment in customer message.
        
        Args:
            message: Customer message
        
        Returns:
            True if negative sentiment detected
        """
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.NEGATIVE_KEYWORDS)
    
    def _detect_explicit_request(self, message: str) -> bool:
        """
        Detect explicit request for human agent.
        
        Args:
            message: Customer message
        
        Returns:
            True if explicit request detected
        """
        message_lower = message.lower()
        return any(phrase in message_lower for phrase in self.EXPLICIT_ESCALATION_PHRASES)
    
    def _check_unanswered_questions(self, conversation_history: list) -> bool:
        """
        Check if there are multiple unanswered questions.
        
        Args:
            conversation_history: Previous conversation messages
        
        Returns:
            True if more than 2 questions remain unanswered
        """
        # Count question marks in recent user messages
        recent_user_messages = [
            msg for msg in conversation_history[-6:]
            if msg["role"] == "user"
        ]
        
        question_count = sum(
            1 for msg in recent_user_messages
            if "?" in msg["content"]
        )
        
        return question_count > 2
    
    def _check_out_of_scope(self, message: str, conversation_history: list) -> bool:
        """
        Use AI to check if question is outside SOP scope.
        
        Args:
            message: Customer message
            conversation_history: Previous conversation messages
        
        Returns:
            True if question is out of scope
        """
        # Quick keyword check first
        sop_keywords = [
            "botox", "filler", "consultation", "price", "cost",
            "hour", "open", "close", "book", "cancel", "appointment"
        ]
        
        message_lower = message.lower()
        has_sop_keyword = any(keyword in message_lower for keyword in sop_keywords)
        
        # If no SOP keywords found, likely out of scope
        if not has_sop_keyword and "?" in message:
            return True
        
        return False
    
    def generate_escalation_message(
        self,
        reasons: List[str],
        conversation_history: list
    ) -> Dict[str, Any]:
        """
        Generate a professional escalation handoff message.
        
        Args:
            reasons: List of escalation reasons
            conversation_history: Previous conversation messages
        
        Returns:
            Dict with escalation message and metadata
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": ESCALATION_PROMPT},
            {"role": "system", "content": f"Escalation reasons: {', '.join(reasons)}"}
        ]
        
        messages.extend(conversation_history[-4:])  # Last 4 messages for context
        
        response = self.client.chat_completion(
            messages=messages,
            temperature=0.5,
            response_format={"type": "json_object"}
        )
        
        if "error" in response:
            return self._create_default_escalation_message(reasons)
        
        try:
            result = response["content"]
            result["escalation_reasons"] = reasons
            return result
        except (json.JSONDecodeError, KeyError):
            return self._create_default_escalation_message(reasons)
    
    def _create_default_escalation_message(self, reasons: List[str]) -> Dict[str, Any]:
        """Create a default escalation message."""
        return {
            "response": "I understand you need more detailed assistance. Let me connect you with one of our specialists who can help you better. They'll be with you shortly.",
            "confidence": 1.0,
            "stage": "escalation",
            "escalation_needed": True,
            "escalation_reasons": reasons,
            "data_collected": {}
        }


