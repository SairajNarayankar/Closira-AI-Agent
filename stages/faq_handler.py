"""
Stage 1: FAQ Answering
Handles customer questions using only SOP data with strict hallucination prevention.
"""

import json
from typing import Dict, Any, Optional
from utils.openai_client import OpenAIClient
from prompts.system_prompts import get_system_prompt, FAQ_PROMPT


class FAQHandler:
    """Handles FAQ answering with SOP-grounded responses."""
    
    def __init__(self, sop_data: Dict[str, Any], openai_client: OpenAIClient):
        """
        Initialize FAQ handler.
        
        Args:
            sop_data: SOP data dictionary
            openai_client: OpenAI client instance
        """
        self.sop_data = sop_data
        self.client = openai_client
        self.system_prompt = get_system_prompt(json.dumps(sop_data, indent=2))
    
    def handle_question(self, question: str, conversation_history: list) -> Dict[str, Any]:
        """
        Handle a customer FAQ question.
        
        Args:
            question: Customer's question
            conversation_history: Previous conversation messages
        
        Returns:
            Dict with response, confidence, and escalation info
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "system", "content": FAQ_PROMPT}
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        
        # Add current question
        messages.append({"role": "user", "content": question})
        
        # Get response from OpenAI
        response = self.client.chat_completion(
            messages=messages,
            temperature=0.3,  # Lower temperature for more consistent answers
            response_format={"type": "json_object"}
        )
        
        if "error" in response:
            return self._create_error_response(response["error"])
        
        try:
            result = response["content"]
            
            # Validate response structure
            required_fields = ["response", "confidence", "stage", "escalation_needed"]
            if not all(field in result for field in required_fields):
                return self._create_error_response("Invalid response structure")
            
            # Ensure confidence is within valid range
            result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))
            
            # Auto-escalate if confidence is too low
            if result["confidence"] < 0.7:
                result["escalation_needed"] = True
                if "escalation_reason" not in result or not result["escalation_reason"]:
                    result["escalation_reason"] = "Low confidence in answer"
            
            return result
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            return self._create_error_response(f"Failed to parse response: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> Dict[str, Any]:
        """Create an error response with escalation."""
        return {
            "response": "I apologize, but I'm having trouble processing your question. Let me connect you with a human agent who can assist you better.",
            "confidence": 0.0,
            "stage": "faq",
            "escalation_needed": True,
            "escalation_reason": f"System error: {error_message}",
            "data_collected": {}
        }
    
    def check_answer_in_sop(self, question: str) -> bool:
        """
        Check if a question can likely be answered from SOP.
        This is a simple heuristic check.
        
        Args:
            question: Customer's question
        
        Returns:
            True if question seems answerable from SOP
        """
        question_lower = question.lower()
        
        # Keywords that suggest answerable questions
        answerable_keywords = [
            "price", "cost", "hour", "open", "close", "service",
            "botox", "filler", "consultation", "book", "cancel"
        ]
        
        return any(keyword in question_lower for keyword in answerable_keywords)


